import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Cria ou atualiza um usuário admin para o projeto.'

    def add_arguments(self, parser):
        parser.add_argument('--username', default=os.environ.get('ADMIN_USERNAME'))
        parser.add_argument('--email', default=os.environ.get('ADMIN_EMAIL', ''))
        parser.add_argument('--password', default=os.environ.get('ADMIN_PASSWORD'))
        parser.add_argument('--first-name', dest='first_name', default=os.environ.get('ADMIN_FIRST_NAME', ''))
        parser.add_argument('--last-name', dest='last_name', default=os.environ.get('ADMIN_LAST_NAME', ''))

    def handle(self, *args, **options):
        username = (options.get('username') or '').strip()
        email = (options.get('email') or '').strip()
        password = options.get('password')
        first_name = (options.get('first_name') or '').strip()
        last_name = (options.get('last_name') or '').strip()

        if not username:
            raise CommandError('Informe --username ou ADMIN_USERNAME.')

        if not password:
            raise CommandError('Informe --password ou ADMIN_PASSWORD.')

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={'email': email},
        )

        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        if created or not user.has_usable_password():
            user.set_password(password)

        user.save()

        action = 'criado' if created else 'atualizado'
        self.stdout.write(self.style.SUCCESS(f'Usuário admin "{username}" {action} com sucesso.'))