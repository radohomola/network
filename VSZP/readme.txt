Pre prihlasenie na zariadenia sa najskor treba prihlasit na mon. server alebo po novom collector (dostupny len cez socks)+rsa_key.
1. ~/.ssh/config
Host mon_ocmlyny
    Hostname mon.vszp.slovanet.sk
    Port 22
    User oss
    PreferredAuthentications publickey
    ProxyCommand /bin/nc.openbsd -X 5 -x 10.51.1.15:1080 %h %p
    IdentityFile ~/.ssh/id_rsa

2. group_vars/all.yml
ansible_host_key_checking: false
ansible_ssh_common_args: '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ProxyCommand="ssh -W %h:%p -q mon_ocmlyny"'
ansible_network_os: cisco.ios.ios

3. PREREQUISITES - create new virtual enviroment & install modules
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10
sudo apt install python3.10-dev
sudo apt install python3.10-venv
# install python
python3.10 -m venv --system-site-packages env/vszp
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
#pip 
python3 -m pip install -r requirements.txt
pip install --upgrade pip
python3 -m pip install --user https://github.com/ansible/ansible/archive/devel.tar.gz
# change current shell environment
source vszp/bin/activate

4. V subore credentials.yml treba cez ansible-vault zasifrovat krdencialy pre pristup na sw. ()
ansible-vault decrypt credentials.yml
ansible-vault encrypt credentials.yml

5. convert  cvs to yml
phyton3 testbed_gen.py -i inventory/test.yml -o inventory/test.yml
hosts_VSZP_zlp2_sw.yml

6. Spustenie playbooku:
ansible-playbook -vv -i inventory/hosts_VSZP_zlp2_sw.yml playbook_if_desc.yml
ansible-playbook -vv -i inventory/hosts_VSZP_zlp2_sw.yml playbook_if_sw_ios_mac.yml


Online textfsm parser: https://textfsm.nornir.tech/
NTC textfsm templates: https://github.com/networktocode/ntc-templates/blob/master/ntc_templates/templates/cisco_nxos_show_mac_address-table.textfsm
