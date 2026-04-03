from rest_framework.throttling import SimpleRateThrottle

class ViewerRateThrottle(SimpleRateThrottle):
    scope = 'viewer'

    def get_cache_key(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return None
        if user.role == "VIEWER":
            return self.cache_format % {
                "scope": self.scope,
                "ident": user.pk
            }
        return None