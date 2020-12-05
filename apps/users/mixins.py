import os
import time

from hashlib import md5


def get_upload_file(instance, filename):
    """Generates an image upload path like: model_name/ab/cd/<hash>.<ext>"""
    data = str(filename) + str(instance) + str(time.time())
    hashed_name = md5(data.encode('utf-8')).hexdigest()
    path_parts = [
        str(instance.__class__.__name__).lower(),
        hashed_name[:2],
        hashed_name[2:4],
        f"{hashed_name}.{filename.split('.')[-1]}",
    ]
    return os.path.join(*path_parts)
