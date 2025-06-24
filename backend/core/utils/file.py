import random
import string


async def generate_unique_name(filename: str, length=8) -> str:
    name, ext = filename.rsplit('.', 1)
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return f"{name}_{random_str}.{ext}"
