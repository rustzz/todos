def fix_data(data):
    if isinstance(data, bytearray):
        return data.decode()
    return data
