import os
import httpx

USER_SERVICE_HOST_URL = 'http://localhost:8001/api/users/'
userUrl = os.environ.get('USER_SERVICE_HOST_URL') or USER_SERVICE_HOST_URL

BLOG_SERVICE_HOST_URL = 'http://localhost:8002/api/blogs/'
blogUrl = os.environ.get('BLOG_SERVICE_HOST_URL') or BLOG_SERVICE_HOST_URL


def is_user_present(userId: int):
    print(f'Requesting {userUrl}{userId}')
    r = httpx.get(f'{userUrl}{userId}')
    print(r)
    return True if r.status_code == 200 else False


def is_blog_present(blogId: int):
    print(f'Requesting {blogUrl}{blogId}')
    r = httpx.get(f'{blogUrl}{blogId}')
    return True if r.status_code == 200 else False
