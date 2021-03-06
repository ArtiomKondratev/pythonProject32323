import socket
import requests
import re
import ipaddress
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import threading

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ScannerSN:
    # Код Стаса
    host = None
    mask = None
    ports_to_scan = []
    max_threading = 100

    def __init__(self):
        self.get_input_data()

    def get_input_data(self):
        self.get_ip()
        if len(self.host) > 0:
            if len(self.mask) > 0:
                self.get_ports()
                if len(self.ports_to_scan) > 0:
                    return
            else:
                print('No mask')
                return
        else:
            print('No host')
            return

    def get_ip(self):
        choice = input('Если у вас есть IP - введите {IP}. Если у вас есть доменное имя - введите {DI}: ')
        if choice == 'IP':
            ip = input('Введите сетевой адресс и сетевой префикс в  формате 127.0.0.1/24\n').replace(' ', '')
            if len(ip) > 0:
                check_ip = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/(\d{1,3})", ip)
                if len(check_ip) > 0:
                    self.host = check_ip[0][0]
                    self.mask = check_ip[0][1]
                    return self.host, self.mask
            print('No ip')
        elif choice == 'DI':
            domain = input('Введите домен: ')
            ip = socket.gethostbyname(domain)
            print(ip)
            mask = input('Введите маску: ')
            ip = ip + "/" + mask
            if len(ip) > 0 and len(mask) > 0:
                check_ip = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/(\d{1,3})", ip)
                if len(check_ip) > 0:
                    self.host = check_ip[0][0]
                    self.mask = check_ip[0][1]
                    return self.host, self.mask
            print('No domain or mask')

    def get_ports(self):
        ports = input('Введите через пробел порты, которые нужно просканировать: ')
        if len(ports) > 0:
            self.ports_to_scan = list(set([int(port) for port in re.findall('[0-9]+', ports)]))
            if len(self.ports_to_scan) > 0:
                return self.ports_to_scan
        print('No correct ports or no ports at all')

    def start_cumming(self):
        if len(self.host) > 0 and len(self.ports_to_scan) > 0 and len(self.mask) > 0:
            print('Проверка запущена...')
            network = ipaddress.ip_network(f'{self.host}/{self.mask}', strict=False)
            network_address = network.network_address
            broadcast_address = network.broadcast_address

            if network_address is not None:
                self.scan_ports(ip=f'{network_address}', ports=self.ports_to_scan)

            if broadcast_address is not None and broadcast_address != network_address:
                self.scan_ports(ip=f'{network_address}', ports=self.ports_to_scan)

            for host in list(network.hosts()):
                if str(f'{host}') != str(network_address) and str(f'{host}') != str(broadcast_address):
                    while threading.active_count() > self.max_threading:
                        time.sleep(1)
                    self.scan_ports(ip=f'{host}', ports=self.ports_to_scan)

    def scan_ports(self, ip, ports):
        for port in ports:
            self.check_connection(ip=ip, port=port)

    def check_connection(self, ip, port):
        sock = socket.socket()
        try:
            sock.settimeout(5.0)
            sock.connect((ip, port))
        except Exception as err:
            print(err)
        else:
            if port == 443 or port == 80:
                msg = self.get_service_name(host=ip, port=port)
                print(f'{ip} {port} OPEN {msg}')
            else:
                print(f'{ip} {port} OPEN')
        finally:
            sock.close()

    @staticmethod
    def get_service_name(host, port, protocol1='http'):
        if port == 443:
            protocol1 = 'https'
        elif port == 80:
            protocol1 = 'http'
        try:
            response = requests.get(f'{protocol1}://{host}:{port}', verify=False)
            header = response.headers
            if 'server' in header.keys():
                service_name = response.headers.get('server')
                return f'{service_name}'
            elif 'Server' in header.keys():
                service_name = response.headers.get('server')
                return f'{service_name}'
        except Exception as err:
            print(err)


class NedoScannerSN:
    def __init__(self):
        print(self.output())

    def get_input_data(self):
        s = input("Введите доменное имя: ")
        return s

    def request(self, s, port1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect_ex((f'{s}', port1))
        content_items = [
            'GET / HTTP/1.1',
            f'Host: {s}',
            'Connection: keep-alive',
            'Accept: text/html',
            '\n'
        ]
        content = '\n'.join(content_items)
        sock.send(content.encode())
        result = sock.recv(10024)
        status_code, headers = self.parse(result.decode())
        return status_code, headers

    def parse(self, text_response):
        lines = text_response.split('\n')
        status_raw, lines = lines[0], lines[1:]
        status_raw = status_raw.split(' ')
        status_code, message = status_raw[1], status_raw[2:]
        headers = {}
        for index, line in enumerate(lines):
            line = line.strip()
            line = line.strip('\r')
            if line == '':
                break
            print(line)
            k, _, v = line.partition(':')
            headers.setdefault(k.strip(), v.strip())
        status_code = int(status_code)
        return status_code, headers

    def check_port(self, s, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(10)
            try:
                return sock.connect_ex((f'{s}', port))
            except Exception as err:
                print(err)

    def output(self):
        s = self.get_input_data()
        if len(s) > 0:
            if self.check_port(f'{s}', 443) == 0:
                port1 = 443
            else:
                port1 = 80
            status_code, headers = self.request(s, port1)
            print('Status Code: {}'.format(status_code))
            print('Port: {}'.format(port1))
            if 'server' in headers:
                return "Service_name: ", headers['server']
            elif 'Server' in headers:
                return "Service_name: ", headers['Server']
        print('No input')
