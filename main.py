import socket
import requests


def get_service_name(s, port1, protocol1='http'):
    host = socket.gethostbyname(f'{s}')
    if port1 == 443:
        protocol1 = 'https'
    elif port1 == 80:
        protocol1 = 'http'
    try:
        response = requests.get(f'{protocol1}://{host}:{port1}', verify=False)
        if 'server' in headers.keys():
            service_name = response.headers.get('server')
            return f'{service_name}'
        elif 'Server' in headers.keys():
            service_name = response.headers.get('server')
            return f'{service_name}'
    except Exception:
        pass


def parse(text_response):
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
    return int(status_code), headers


def check_port(s, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(10)
        try:
            return sock.connect((f'{s}', port))
        except Exception:
            pass


s = input("Введите доменное имя: ")
print(check_port(f'{s}', 443))
print(check_port(f'{s}', 80))
if check_port(f'{s}', 443) is not None:
    port1 = 443
else:
    port1 = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((f'{s}', 80))
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
status_code, headers = parse(result.decode())
print()
print('Status Code: {}'.format(status_code))
print('Port: {}'.format(port1))
# метод 1
if 'server' in headers:
    print("Service_name: ", headers['server'])
elif 'Server' in headers:
    print("Service_name: ", headers['Server'])
# метод 2
print("Service_name: ", get_service_name(s, port1))
