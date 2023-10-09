Pre prihlasenie na zariadenia sa najskor treba prihlasit na mon. server (ten je vyrieseny port forwardom na CRP-ASA FW ale port forward je dostupny len cez socks).
1. ~/.ssh/config
Host mon_ocmlyny
    Hostname 217.145.192.228
    Port 24
    User oss
    PreferredAuthentications publickey
    ProxyCommand /bin/nc.openbsd -X 5 -x 10.51.1.15:1080 %h %p
    IdentityFile ~/.ssh/id_rsa

2. group_vars/all.yml
ansible_host_key_checking: false
ansible_ssh_common_args: '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ProxyCommand="ssh -W %h:%p -q mon_ocmlyny"'
ansible_network_os: cisco.ios.ios

3. V subore credentials.yml treba cez ansible-vault zasifrovat krdencialy pre pristup na sw.
ansible-vault decrypt credentials.yml
ansible-vault encrypt credentials.yml


Spustenie playbooku:
ansible-playbook -vv -i inventory/test.yml playbook_if_desc.yml

Online textfsm parser: https://textfsm.nornir.tech/
NTC textfsm templates: https://github.com/networktocode/ntc-templates/blob/master/ntc_templates/templates/cisco_nxos_show_mac_address-table.textfsm


ansible==8.3.0
ansible-core==2.15.3
ansible-pylibssh==1.1.0
bcrypt==4.0.1
cffi==1.15.1
cryptography==41.0.3
future==0.18.3
Jinja2==3.1.2
MarkupSafe==2.1.3
packaging==23.1
paramiko==3.3.1
pycparser==2.21
PyNaCl==1.5.0
PyYAML==6.0.1
resolvelib==1.0.1
six==1.16.0
textfsm==1.1.3
