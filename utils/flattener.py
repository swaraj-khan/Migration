import hashlib

MAX_KEY_LEN = 50

def shorten(key: str) -> str:
    if len(key) <= MAX_KEY_LEN:
        return key
    hash_suffix = hashlib.md5(key.encode()).hexdigest()[:6]
    return key[:MAX_KEY_LEN] + "_" + hash_suffix


def flatten_document(obj, parent_key="", result=None):
    if result is None:
        result = {}

    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{parent_key}_{k}" if parent_key else k
            new_key = shorten(new_key)
            flatten_document(v, new_key, result)

    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            new_key = f"{parent_key}_{i}"
            new_key = shorten(new_key)
            flatten_document(item, new_key, result)

    else:
        key = shorten(parent_key)
        result[key] = obj

    return result
