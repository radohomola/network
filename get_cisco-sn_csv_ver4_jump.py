import os
import paramiko
import socks
import csv
import telnetlib

# Define the jump host and SSH port here.
jump_host = 'mon.vszp.slovanet.sk'
jump_port = 22  # Change to the appropriate port if needed

# Define the SOCKS5 proxy hostname and port here.
socks_proxy_host = '10.51.1.15'
socks_proxy_port = 1080  # Change to the appropriate port

# Define the SSH key file path here (optional).
private_key_file = '/home/homolar/scripts/oss_rsa-key-identity_putty.ppk'

# Define the input and output CSV file paths.
input_csv_file = 'Inventory_hosts_VSZP_zlp2.csv'
output_csv_file = 'output_zlp.csv'

# Define the SSH username for the jump host.
ssh_username = 'oss'

# Define the SSH password (if needed).
ssh_password = ''

# Define the Telnet username and password.
telnet_username = 'major'
telnet_password = 'rmv7ACT'

# Check if the input CSV file exists and is readable.
if not os.path.exists(input_csv_file) or not os.access(input_csv_file, os.R_OK):
    print('Error: Input CSV file does not exist or is not readable.')
    exit(1)

# Check if the output CSV file does not exist already. If it does exist, prompt the user to confirm overwriting it.
if os.path.exists(output_csv_file):
    print(f'Output CSV file {output_csv_file} already exists. Overwrite it? (y/n)')
    response = input()
    if response != 'y':
        exit(0)

# Create a SOCKS5 proxy connection.
proxy = socks.socksocket()
proxy.set_proxy(socks.SOCKS5, socks_proxy_host, socks_proxy_port)

# Establish an SSH connection to the jump host through the proxy.
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Use a private key for authentication.
    ssh_key = paramiko.RSAKey(filename=private_key_file)

    ssh_client.connect(jump_host, port=jump_port, username=ssh_username, pkey=ssh_key, sock=proxy)

    # Open the input CSV file and read the contents into a list called `devices`.
    with open(input_csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        devices = list(reader)

    # Create a new list called `hosts` and populate it with the IP addresses and hostnames of the devices.
    hosts = []
    for device in devices:
        hostname = device[0]
        ip_address = device[1]
        hosts.append({'hostname': hostname, 'ip_address': ip_address})

    # Iterate over the `hosts` list and connect to each device to retrieve the serial number using Telnet.
    with open(output_csv_file, 'a', encoding='utf-8') as output_csv:
        writer = csv.writer(output_csv, delimiter=',')
        for host in hosts:
            try:
                # Establish an SSH connection to the target device through the jump host.
                ssh_client_transport = ssh_client.get_transport()
                dest_addr = (host['ip_address'], 23)  # Telnet port on the target device
                local_addr = ('', 0)
                channel = ssh_client_transport.open_channel('direct-tcpip', dest_addr, local_addr)
                telnet_connection = telnetlib.Telnet()
                telnet_connection.open(host['ip_address'], port=0)  # Port 0 indicates that Telnet will use the existing channel
                telnet_connection.read_until(b'Username: ')
                telnet_connection.write(telnet_username.encode('utf-8') + b'\n')
                telnet_connection.read_until(b'Password: ')
                telnet_connection.write(telnet_password.encode('utf-8') + b'\n')

                # Send commands to retrieve the serial number using Telnet.
                telnet_connection.write(b'show version | include Serial Number\n')
                serial_output = telnet_connection.read_until(b'#').decode('utf-8')

                # Extract the serial number from the Telnet output (you may need to adjust this depending on the device's prompt and format).
                serial_number = serial_output.split('Serial Number: ')[1].strip()

                # Write the results to the output CSV file.
                writer.writerow([host['hostname'], serial_number])

                # Close the Telnet connection.
                telnet_connection.close()

            except Exception as e:
                print(f'Error connecting to device {host["hostname"]}: {str(e)}')

    # Close the SSH connection to the jump host.
    ssh_client.close()

    print('Done!')

except Exception as e:
    print(f'Error connecting to the jump host: {str(e)}')

