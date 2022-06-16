import os
import httpx
from fastapi import HTTPException, status

USER_SERVICE_HOST_URL = 'http://localhost:8002/api/users/'
url = os.environ.get('USER_SERVICE_HOST_URL') or USER_SERVICE_HOST_URL


def is_user_present(userId: int, token: str):
    print(f'Requesting {url}{userId}')
    r = httpx.get(f'{url}{userId}', headers={'Authorization': token})
    if r.status_code == 200:
        return True
    elif r.status_code == 401:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        return False
