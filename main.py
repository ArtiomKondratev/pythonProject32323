import socket
# from multiprocessing.pool import ThreadPool
# from tqdm import tqdm

# scanned = []


def parse(text_response):
    lines = text_response.split('\n')
    status_raw, lines = lines[0], lines[1:]
    status_raw = status_raw.split(' ')
    status_code, message = status_raw[1], status_raw[2:]
    empty_index = 1
    headers = {}
    for index, line in enumerate(lines):
        line = line.strip()
        line = line.strip('\r')
        if line == '':
            empty_index = index
            break
        print(line)
        k, _, v = line.partition(':')
        headers.setdefault(k.strip(), v.strip())
    content = ''.join(lines[empty_index + 1:])
    return int(status_code), headers, content


# def check_port(port):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#         sock.settimeout(1)
#         return None if sock.connect((f'{s}', port)) else port


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = input("Введите доменное имя: ")
sock.connect((f'{s}', 80))
content_items = [
    'GET / HTTP/1.1',
    f'Host: {s}',
    'Connection: keep-alive',
    'Accept: text/html',
    '\n'
]
content = '\n'.join(content_items)
print(content)
sock.send(content.encode())
result = sock.recv(10024)
status_code, headers, content = parse(result.decode())
print('Status Code: {}'.format(status_code))
print('Headers: {}'.format(headers))
print('Content:')
print(content)
# s = socket.gethostbyname(s)
# if __name__ == '__main__':
#     pool = ThreadPool(3000)
#     scanned = list(
#         tqdm(pool.imap(check_port, range(1, 65536)), total=65535, desc=f'Scanning {s}')
#     )


# def get_service_name(s, scanned):
#     port1 = 0
#     service_name = 'Неопределён'
#     if 443 in scanned:
#         protocol1 = 'https'
#         port1 = 443
#     elif 80 in scanned:
#         protocol1 = 'http'
#         port1 = 80
#     try:
#         sock.connect((f'{s}', port1))
#         content_items = [
#             'GET / HTTP/1.1',
#             f'Host: {s}',
#             'Connection: keep-alive',
#             'accept: text/html',
#             '\n'
#         ]
#         content = '\n'.join(content_items)
#         sock.send(content.encode())
#         result = sock.recv(10024)
#         status_code, headers, content = parse(result.decode())
#         if 'server' in headers.keys():
#             service_name = headers['server']
#             return f'{service_name}'
#     except Exception:
#         pass


# get_service_name(s,scanned)