import re

def get_Cookie(headers):
    pattern = r'(?:[\S\s]*)?Cookie: (?:[\S\s]*)?path=(.*)(?:;|\n)'
    try:
        print()
        return re.match(pattern, headers.decode('utf-8')).group(1)
    except:
        return None

def get_path(headers):
    pattern = r'^(?:GET|POST|PUT|PATCH|DELETE) (/.*?) HTTP/1'
    url_path = re.match(pattern , headers.decode('utf-8')).group(1)
    cookie_path = get_Cookie(headers)
    print(url_path, cookie_path)

    return url_path, cookie_path


def recv_data(conn, addr, byte_size):
    print(f"⬅️⬅️⬅️ {addr[0]}:{addr[1]}")
    data = b''
    while True:
        data1 = conn.recv(byte_size)
        data += data1
        if b'\r\n\r\n' in data:
            break
    headers, body = data.split(b'\r\n\r\n', 1)
    headers+= b'\r\n\r\n'
    print(headers)
    # Parse based on Content-Length
    if b'Content-Length' in headers:
        content_length = int((re.search(b'Content-Length: (\d+)', headers).group(1)).decode('utf-8'))
        while(len(body) < content_length):
            data1 = conn.recv(byte_size)
            body += data1
    elif b'Transfer-Encoding: chunked' in headers:
        while True:
            data1 = conn.recv(byte_size)
            body += data1
            print(body)
            if b'0\r\n\r\n' in body:
                break


    return headers, body


def add_path_cookie(headers, path):
    # add set-cookie header
    headers = headers.replace(b"\r\n\r\n", b"\r\n") + b'Set-Cookie: path=' + path + b'\r\n\r\n'
    return headers
    

if __name__ == '__main__':
    print("Class defining proxy utilities")
