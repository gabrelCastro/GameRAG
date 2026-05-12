from django.contrib.auth.models import User


class UserService:
    def register(self, username: str, email: str, password: str) -> User:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=False,
        )
        return user
