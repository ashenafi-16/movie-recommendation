from django.conf import settings
from rest_framework.response import Response

def set_token_cookies(response: Response, access_token: str | None= None, refresh_token: str | None=None) -> None:
    if access_token:
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS'],value=access_token,
            max_age=settings.SIMPLE_JWT['AUTH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )
        
    if refresh_token:
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],value=refresh_token,
            max_age=settings.SIMPLE_JWT['AUTH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            
        )

def delete_token_cookies(response: Response) -> None:
    response.delete_cookie(
        settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS'],
        domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )

    response.delete_cookie(
        settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
        path=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH_PATH"],
        domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )