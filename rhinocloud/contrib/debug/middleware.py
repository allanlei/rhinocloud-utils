import logging
import traceback
from django.conf import settings

logger = logging.getLogger('django')

class ReverseProxySSLMiddleware(object):
    SSL_HEADERS = {
        'HTTP_X_FORWARDED_SSL': 'on'
    }
    def process_request(self, request, *args, **kwargs):
        if not request.is_secure():
            def is_secure():
                for header, value in self.SSL_HEADERS.items():
                    if header in request.META and request.META[header] == value:
                        return True
                return False
            request.is_secure = is_secure


class ExceptionLoggingMiddleware(object):
    def process_exception(self, request, exception):
        if settings.DEBUG:
            if request.is_ajax():
                traceback.print_exc()
        return None
