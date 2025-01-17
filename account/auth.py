from knox.auth import TokenAuthentication
from django.utils.translation import gettext_lazy as _
from knox.settings import knox_settings


class CookieTokenAuthentication(TokenAuthentication):
    """
    Custom Token Authentication using cookies
    """
    """
    Donot change anything here, unless you know what you are doing
    """

    def authenticate(self, request):
        token = request.COOKIES.get('auth_token')

        if not token:
            return None

        # add token to request as authorization header
        request.META['HTTP_AUTHORIZATION'] = f"{knox_settings.AUTH_HEADER_PREFIX} {token}"

        # call parent authenticate, donot code on your own, ok DARPAN
        return super().authenticate(request)
