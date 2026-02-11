from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


# Allows login with any case variation (e.g., 'Admin' or 'admin').
# Uses __iexact to match username regardless of capitalization.
class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)


        users = UserModel.objects.filter(
            Q(**{'{}__iexact'.format(UserModel.USERNAME_FIELD): username}) |
            Q(email__iexact=username)
        )

        # Get the first user if found
        user = users.first()

        if user:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        else:
            # Run check password for security reasons (timing attacks)
            # Even if the user doesn't exist
            UserModel().set_password(password)

        return None