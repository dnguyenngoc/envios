

def decode_or_str(bytes):
    try:
        return bytes.decode('utf-8')
    except:
        return str(bytes)