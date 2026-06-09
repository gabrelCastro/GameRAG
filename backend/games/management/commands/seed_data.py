import subprocess
import sys
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Popula o banco com jogos e interações de exemplo.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-interactions',
            action='store_true',
            help='Cria apenas os jogos, sem incluir usuários, favoritos, reviews e biblioteca.',
        )

    def handle(self, *args, **options):
        project_root = Path(__file__).resolve().parents[3]
        seed_games_path = project_root / 'seed_games.py'
        seed_interactions_path = project_root / 'seed_interactions.py'

        if not seed_games_path.exists():
            raise CommandError(f'Não encontrou o arquivo {seed_games_path}')

        self.stdout.write('Populando jogos de exemplo...')
        subprocess.check_call([sys.executable, str(seed_games_path)], cwd=str(project_root))

        if not options['no_interactions']:
            if not seed_interactions_path.exists():
                raise CommandError(f'Não encontrou o arquivo {seed_interactions_path}')
            self.stdout.write('Populando interações de exemplo...')
            subprocess.check_call([sys.executable, str(seed_interactions_path)], cwd=str(project_root))

        self.stdout.write(self.style.SUCCESS('Dados de exemplo populados com sucesso.'))
