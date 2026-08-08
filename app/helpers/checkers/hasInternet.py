import socket

def hasInternet(host: str='8.8.8.8', port: int=53, timeout: int=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False