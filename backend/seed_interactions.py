import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GameRAG.settings')
django.setup()

from django.contrib.auth.models import User
from games.models import Game, GameFavorite, GameLibraryEntry, GameReview

# ---------------------------------------------------------------------------
# Usuários
# ---------------------------------------------------------------------------

USERS = [
    {'username': 'mario_gamer',   'email': 'mario@example.com',   'password': 'senha123'},
    {'username': 'ana_plays',     'email': 'ana@example.com',     'password': 'senha123'},
    {'username': 'pedro_rpg',     'email': 'pedro@example.com',   'password': 'senha123'},
    {'username': 'julia_indie',   'email': 'julia@example.com',   'password': 'senha123'},
]

# ---------------------------------------------------------------------------
# Reviews: (username, game_title, rating, comment)
# ---------------------------------------------------------------------------

REVIEWS = [
    ('mario_gamer', 'Elden Ring',                   10, 'O jogo me consumiu por 200 horas. Cada boss é uma lição de humildade e superação. Obra-prima absoluta.'),
    ('mario_gamer', 'Dark Souls III',                9, 'A FromSoftware no seu auge antes do Elden Ring. Dancer of the Boreal Valley é o boss mais bonito que já enfrentei.'),
    ('mario_gamer', 'Doom Eternal',                 10, 'O combate mais satisfatório que já joguei. Não consigo ouvir a trilha do Mick Gordon sem sentir adrenalina.'),
    ('mario_gamer', 'Sekiro: Shadows Die Twice',     8, 'Genial, mas o sistema de postura demorou pra clicar. Quando clicou, não consegui parar.'),
    ('mario_gamer', 'Half-Life 2',                   9, 'Joguei pela primeira vez em 2024 e ainda é incrível. O Gravity Gun é pura genialidade.'),
    ('mario_gamer', 'Portal 2',                     10, 'O GLaDOS é o melhor personagem de jogo já criado. Joguei o co-op com meu irmão e foi perfeito.'),

    ('ana_plays',   'The Witcher 3: Wild Hunt',      10, 'A Ilha de Toussaint em Blood and Wine é um dos lugares mais bonitos que já visitei em qualquer jogo. Narrativa impecável.'),
    ('ana_plays',   'Baldur\'s Gate 3',              10, 'Passei 80 horas na primeira run e ainda perdi coisas. Jaheira e Astarion são personagens inesquecíveis.'),
    ('ana_plays',   'Disco Elysium',                 10, 'O jogo mais literário que já toquei. A escrita é de outro nível. Fiquei com Harry Du Bois na cabeça por semanas.'),
    ('ana_plays',   'Cyberpunk 2077',                 8, 'Depois dos patches ficou muito bom. Night City é absurdamente detalhada. A DLC Phantom Liberty é excelente.'),
    ('ana_plays',   'Stardew Valley',                 9, 'Comprei para relaxar e fiquei viciada. O meu casamento com Harvey foi mais emocionante que esperava.'),
    ('ana_plays',   'God of War (2018)',              10, 'A cena final com Kratos e Atreus me fez chorar. Nunca imaginei me importar tanto com esses personagens.'),

    ('pedro_rpg',   'Baldur\'s Gate 3',              10, 'D&D 5e na tela do PC. Minha campanha como Clérigo de Shadowheart foi épica. Rejogabilidade infinita.'),
    ('pedro_rpg',   'The Witcher 3: Wild Hunt',       9, 'A missão Ladies of the Wood é perturbadora do jeito certo. CD Projekt Red em forma máxima.'),
    ('pedro_rpg',   'Hollow Knight',                  9, 'O lore contado através dos itens e ambiente é brilhante. Hornet é icônica.'),
    ('pedro_rpg',   'Elden Ring',                    10, 'A lore co-escrita com George R.R. Martin é densa demais. Malenia é injusta mas memorável.'),
    ('pedro_rpg',   'Hades',                          9, 'Pela primeira vez um roguelite onde me importo com os personagens. Zagreus e Megaera são ótimos.'),
    ('pedro_rpg',   'Celeste',                        8, 'A narrativa sobre saúde mental é honesta e corajosa. As fases C-Side são desumanas.'),

    ('julia_indie', 'Hollow Knight',                 10, 'Team Cherry fez algo que estúdios com 100x mais orçamento não conseguem. Abswin total.'),
    ('julia_indie', 'Celeste',                       10, 'Chorei na montanha. A Madeline é a protagonista indie mais bem escrita que conheço.'),
    ('julia_indie', 'Hades',                         10, 'A Supergiant Games não erra nunca. A história de Zagreus e Nyx me tocou demais.'),
    ('julia_indie', 'Stardew Valley',                 9, 'Passei um verão inteiro jogando isso. Perfeito para desligar do mundo.'),
    ('julia_indie', 'Terraria',                       8, 'Parece simples, mas é profundíssimo. A batalha contra o Moon Lord foi épica.'),
    ('julia_indie', 'Disco Elysium',                  9, 'Harry Du Bois é o protagonista mais humano e quebrado já escrito num jogo.'),
    ('julia_indie', 'Portal 2',                       9, 'Wheatley é hilário. O final me surpreendeu de verdade.'),
]

# ---------------------------------------------------------------------------
# Favoritos: (username, game_title)
# ---------------------------------------------------------------------------

FAVORITES = [
    ('mario_gamer', 'Elden Ring'),
    ('mario_gamer', 'Doom Eternal'),
    ('mario_gamer', 'Portal 2'),
    ('mario_gamer', 'Dark Souls III'),

    ('ana_plays',   'The Witcher 3: Wild Hunt'),
    ('ana_plays',   'Baldur\'s Gate 3'),
    ('ana_plays',   'God of War (2018)'),
    ('ana_plays',   'Disco Elysium'),
    ('ana_plays',   'Stardew Valley'),

    ('pedro_rpg',   'Baldur\'s Gate 3'),
    ('pedro_rpg',   'The Witcher 3: Wild Hunt'),
    ('pedro_rpg',   'Elden Ring'),
    ('pedro_rpg',   'Hollow Knight'),

    ('julia_indie', 'Hollow Knight'),
    ('julia_indie', 'Celeste'),
    ('julia_indie', 'Hades'),
    ('julia_indie', 'Disco Elysium'),
]

# ---------------------------------------------------------------------------
# Biblioteca: (username, game_title, status, hours_played)
# ---------------------------------------------------------------------------

STATUS = GameLibraryEntry

LIBRARY = [
    ('mario_gamer', 'Elden Ring',                   STATUS.STATUS_COMPLETED,    210.0),
    ('mario_gamer', 'Dark Souls III',               STATUS.STATUS_COMPLETED,    95.0),
    ('mario_gamer', 'Doom Eternal',                 STATUS.STATUS_COMPLETED,    40.0),
    ('mario_gamer', 'Sekiro: Shadows Die Twice',    STATUS.STATUS_COMPLETED,    55.0),
    ('mario_gamer', 'Half-Life 2',                  STATUS.STATUS_COMPLETED,    12.0),
    ('mario_gamer', 'Portal 2',                     STATUS.STATUS_COMPLETED,    9.5),
    ('mario_gamer', 'Cyberpunk 2077',               STATUS.STATUS_PLAYING,      38.0),
    ('mario_gamer', 'Baldur\'s Gate 3',             STATUS.STATUS_WANT_TO_PLAY, 0.0),

    ('ana_plays',   'The Witcher 3: Wild Hunt',     STATUS.STATUS_COMPLETED,    130.0),
    ('ana_plays',   'Baldur\'s Gate 3',             STATUS.STATUS_COMPLETED,    85.0),
    ('ana_plays',   'God of War (2018)',             STATUS.STATUS_COMPLETED,    27.0),
    ('ana_plays',   'Disco Elysium',                STATUS.STATUS_COMPLETED,    32.0),
    ('ana_plays',   'Cyberpunk 2077',               STATUS.STATUS_COMPLETED,    62.0),
    ('ana_plays',   'Stardew Valley',               STATUS.STATUS_PLAYING,      120.0),
    ('ana_plays',   'Elden Ring',                   STATUS.STATUS_DROPPED,      18.0),
    ('ana_plays',   'Celeste',                      STATUS.STATUS_WANT_TO_PLAY, 0.0),

    ('pedro_rpg',   'Baldur\'s Gate 3',             STATUS.STATUS_COMPLETED,    90.0),
    ('pedro_rpg',   'The Witcher 3: Wild Hunt',     STATUS.STATUS_COMPLETED,    115.0),
    ('pedro_rpg',   'Elden Ring',                   STATUS.STATUS_COMPLETED,    160.0),
    ('pedro_rpg',   'Hollow Knight',                STATUS.STATUS_COMPLETED,    48.0),
    ('pedro_rpg',   'Hades',                        STATUS.STATUS_PLAYING,      35.0),
    ('pedro_rpg',   'Celeste',                      STATUS.STATUS_PLAYING,      14.0),
    ('pedro_rpg',   'Disco Elysium',                STATUS.STATUS_WANT_TO_PLAY, 0.0),
    ('pedro_rpg',   'Dark Souls III',               STATUS.STATUS_DROPPED,      22.0),

    ('julia_indie', 'Hollow Knight',                STATUS.STATUS_COMPLETED,    55.0),
    ('julia_indie', 'Celeste',                      STATUS.STATUS_COMPLETED,    30.0),
    ('julia_indie', 'Hades',                        STATUS.STATUS_COMPLETED,    65.0),
    ('julia_indie', 'Stardew Valley',               STATUS.STATUS_PLAYING,      200.0),
    ('julia_indie', 'Terraria',                     STATUS.STATUS_COMPLETED,    80.0),
    ('julia_indie', 'Disco Elysium',                STATUS.STATUS_COMPLETED,    28.0),
    ('julia_indie', 'Portal 2',                     STATUS.STATUS_COMPLETED,    10.0),
    ('julia_indie', 'Minecraft',                    STATUS.STATUS_PLAYING,      350.0),
    ('julia_indie', 'The Witcher 3: Wild Hunt',     STATUS.STATUS_WANT_TO_PLAY, 0.0),
    ('julia_indie', 'Baldur\'s Gate 3',             STATUS.STATUS_WANT_TO_PLAY, 0.0),
]


def seed_users():
    print('\n=== Usuários ===')
    users = {}
    for data in USERS:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={'email': data['email']},
        )
        if created:
            user.set_password(data['password'])
            user.save()
            print(f'  [+] {user.username}')
        else:
            print(f'  [=] {user.username} (já existe)')
        users[user.username] = user
    return users


def seed_reviews(users):
    print('\n=== Reviews ===')
    created = skipped = 0
    games_cache = {g.title: g for g in Game.objects.all()}

    for username, title, rating, comment in REVIEWS:
        user = users.get(username)
        game = games_cache.get(title)
        if not user or not game:
            print(f'  [!] Pulando "{title}" — usuário ou jogo não encontrado')
            continue

        _, was_created = GameReview.objects.get_or_create(
            game=game,
            user=user,
            defaults={'rating': rating, 'comment': comment},
        )
        if was_created:
            created += 1
        else:
            skipped += 1

    print(f'  {created} criadas, {skipped} ignoradas.')


def seed_favorites(users):
    print('\n=== Favoritos ===')
    created = skipped = 0
    games_cache = {g.title: g for g in Game.objects.all()}

    for username, title in FAVORITES:
        user = users.get(username)
        game = games_cache.get(title)
        if not user or not game:
            print(f'  [!] Pulando "{title}" — usuário ou jogo não encontrado')
            continue

        _, was_created = GameFavorite.objects.get_or_create(game=game, user=user)
        if was_created:
            created += 1
        else:
            skipped += 1

    print(f'  {created} criados, {skipped} ignorados.')


def seed_library(users):
    print('\n=== Biblioteca ===')
    created = skipped = 0
    games_cache = {g.title: g for g in Game.objects.all()}

    for username, title, lib_status, hours in LIBRARY:
        user = users.get(username)
        game = games_cache.get(title)
        if not user or not game:
            print(f'  [!] Pulando "{title}" — usuário ou jogo não encontrado')
            continue

        _, was_created = GameLibraryEntry.objects.get_or_create(
            game=game,
            user=user,
            defaults={'status': lib_status, 'hours_played': hours},
        )
        if was_created:
            created += 1
        else:
            skipped += 1

    print(f'  {created} criadas, {skipped} ignoradas.')


if __name__ == '__main__':
    users = seed_users()
    seed_reviews(users)
    seed_favorites(users)
    seed_library(users)
    print('\nConcluído.')
