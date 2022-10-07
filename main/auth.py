import alt_path
from _import import *
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
import hashlib
import _global

security = HTTPBasic()

def get_login(credentials: HTTPBasicCredentials = Depends(security)):
    login, pwd = credentials.username, credentials.password
    md5 = hashlib.md5(pwd.encode('utf-8')).hexdigest()
    if time.time() - _global.login_last_bad_dt < 60:
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT,
            detail="Wait a minute and try again",
            headers={"WWW-Authenticate": "Basic"},
        )
    if login not in _global.users:
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT,
            detail="Access denied"
        )
    if md5 != _global.users[login].md5:
        _global.login_last_bad_dt = time.time()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return login
