current_hostname = 'localhost'
current_username = ''
current_password = ''

def bytes_to_gb(bytes):
    return bytes / (1024.0 ** 3)


def kb_to_gb(kb):
     return round(float(kb) / 1024 / 1024,2)


def mb_to_gb(mb):
     return round(float(mb) / 1024)
