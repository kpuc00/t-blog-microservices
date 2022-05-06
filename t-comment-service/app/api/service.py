import os
import httpx

USER_SERVICE_HOST_URL = 'http://localhost:8001/api/users/'
userUrl = os.environ.get('USER_SERVICE_HOST_URL') or USER_SERVICE_HOST_URL

ARTICLE_SERVICE_HOST_URL = 'http://localhost:8003/api/articles/'
articleUrl = os.environ.get(
    'ARTICLE_SERVICE_HOST_URL') or ARTICLE_SERVICE_HOST_URL


def is_user_present(userId: int):
    print(f'Requesting {userUrl}{userId}')
    r = httpx.get(f'{userUrl}{userId}')
    print(r)
    return True if r.status_code == 200 else False


def is_article_present(articleId: int):
    print(f'Requesting {articleUrl}{articleId}')
    r = httpx.get(f'{articleUrl}{articleId}')
    return True if r.status_code == 200 else False
