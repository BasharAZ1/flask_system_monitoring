current_hostname = 'localhost'
current_username = ''
current_password = ''

mem_info_gb_formatted=0
total_space=0




def bytes_to_gb(bytes):
    return bytes / (1024.0 ** 3)

def kb_to_gb(kb):
     return round(float(kb) / 1024 / 1024,2)