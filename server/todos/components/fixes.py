from typing import Union


def fix_data(data: Union[str, bytearray, int, bool]) -> Union[str, int, bool]:
    if isinstance(data, bytearray):
        return data.decode()
    return data
