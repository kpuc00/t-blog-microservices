import os
import httpx

USER_SERVICE_HOST_URL = 'http://localhost:8002/api/users/'
url = os.environ.get('USER_SERVICE_HOST_URL') or USER_SERVICE_HOST_URL


def is_user_present(userId: int):
    print(f'Requesting {url}{userId}')
    r = httpx.get(f'{url}{userId}')
    return True if r.status_code == 200 else False
