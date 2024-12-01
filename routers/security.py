from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError
from sqlalchemy.orm import Session

from db import crud, schemas
from dependencies import get_db, oauth

router = APIRouter(tags=["security"])


@router.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/auth')
async def auth(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
        db_user = crud.get_user_by_email(db, user['email'])
        if not db_user:
            db_user = schemas.UserCreate(email=user['email'], name=user.get(
                'name', None), picture=user.get('picture', None))
            crud.create_user(db, db_user)
    return RedirectResponse(url='/')


@router.route('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')
