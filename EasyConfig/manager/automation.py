import os, time
from netmiko import ConnectHandler
from .models import Project, Device, Interface
import threading
from pythonping import ping
worker = threading.Semaphore(2)


def configuration_router(device_id, port,name,interface, ip_address, mask):
    with worker:
        ssh_enable = False
        try:
            connection = ConnectHandler(
                device_type = "cisco_ios_telnet",
                host = "192.168.56.101",
                port = port
            )
            connection.enable()
            print(f"S-a connectat telnet la {name}!")
            username = os.getenv('ROUTER_SSH_USER')
            password = os.getenv('ROUTER_SSH_PASSW')
            commands = [f'interface {interface}', f'ip address {ip_address} {mask}','no shutdown',f'hostname {name}', "ip domain-name test", 'crypto key generate rsa modulus 1024' , f'username {username} privilege 15 password {password}' , 'line vty 0 4' , 'transport input ssh', 'login local']
            output = connection.send_config_set(commands)
            print(output)
            ssh_enable = True
            
            print("SSH gata!")
            connection.disconnect()
            if ssh_enable:
                time.sleep(2)
                ssh_conection(ip_address,username, password)
            interface_obj = Interface.objects.get(device_id = device_id, name = interface)
            interface_obj.is_configured =True
            interface_obj.save()
            print("S-a configurat interfata!")
            return [ip_address, ssh_enable, username, password]
        except Exception as e:
            print(e)

def ssh_conection(ip_address,username, password):
    try:
        connection = ConnectHandler(
            device_type = "cisco_ios",
            host = ip_address,
            username = username,
            password = password,
            verbose = True
        )

        connection.enable()
        print("Conexiune SSH realizata cu succes!")
        '''save_command = 'write memory'
        connection.send_command(save_command)
        connection.send_command('\n')
        print("S-a salvat configuratia actuala!")'''
        connection.disconnect()
    except Exception as e:
        print(e)

def vpcs_configuration(device_id, port,name,interface,ip_address, mask, default_gateway):
    with worker:
        try:
            connection = ConnectHandler(
                device_type = "cisco_ios_telnet",
                host = "192.168.56.101",
                port = port,
                global_delay_factor = 2
            )
            print(f"S-a connectat telnet la {name}!")
            connection.send_command(f'ip {ip_address} {mask} {default_gateway} ')
            print("S-a configurat adresa ip!")
            print("Se salvează configurația PC-ului...")
            output_save = connection.send_command("save")
            print(f"Configurația pentru {name} a fost aplicată și salvată cu succes!")
            connection.disconnect()
            interface_obj = Interface.objects.get(device_id = device_id, name = interface)
            interface_obj.is_configured =True
            interface_obj.save()
        except Exception as e:
            print(e)

def funct_ping(ip_adress):
    list_resp = ping(ip_adress,count = 3, verbose=True)
    if list_resp.success():
        print("Pachetele au fost trimise cu succes!\n")
        return {
            'status': 'success',
            'message': f"Pachetele au fost trimise cu succes către {ip_adress}! Dispozitivul răspunde."
        }
    else:
        print(f"Request Timed Out! Echipamentul cu IP-ul {ip_adress} nu răspunde.")
        return {
            'status': 'fail',
            'message': f"Request Timed Out! Echipamentul cu IP-ul {ip_adress} Nu răspunde. Verificati rutele!"
        }

        


