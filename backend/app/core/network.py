import socket


def get_local_ip() -> str:
    """
    Определяет локальный IP-адрес машины в домашней/рабочей сети (Wi-Fi/LAN),
    исключая виртуальные интерфейсы WSL/Hyper-V/VPN.
    """
    fallback = '127.0.0.1'
    try:
        # Пробуем создать UDP-сокет без отправки пакета в сеть
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            candidate = s.getsockname()[0]
            if candidate and not candidate.startswith('127.'):
                return candidate
    except Exception:
        pass

    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if ip.startswith('192.168.'):
                return ip
            if not ip.startswith('127.') and fallback == '127.0.0.1':
                fallback = ip
    except Exception:
        pass

    return fallback
