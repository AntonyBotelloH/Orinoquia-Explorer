from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailBackend(ModelBackend):
    """
    Permite iniciar sesión con correo electrónico (o alternativamente con documento/username).
    El usuario en base de datos sigue siendo el documento.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        identifier = username or kwargs.get('email')
        if identifier is None or password is None:
            return None

        try:
            # Busca por correo electrónico (prioridad) o por username (documento)
            user = UserModel.objects.filter(
                Q(email__iexact=identifier) | Q(username__iexact=identifier)
            ).first()
            if user and user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception:
            return None
        return None
