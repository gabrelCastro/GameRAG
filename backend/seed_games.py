import os
import django
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GameRAG.settings')
django.setup()

from datetime import date
from games.models import Game

GAMES = [
    {
        "title": "The Witcher 3: Wild Hunt",
        "description": (
            "RPG de mundo aberto ambientado num universo sombrio inspirado no folclore eslavo. "
            "Você controla Geralt de Rívia, um caçador de monstros profissional em busca de sua filha adotiva "
            "enquanto uma entidade sobrenatural conhecida como O Cólquio avança destruindo tudo ao redor. "
            "Com mais de 100 horas de conteúdo, o jogo combina narrativa cinematográfica, escolhas morais com "
            "consequências reais, combate fluido e um dos mundos mais detalhados já criados nos videogames. "
            "As expansões Hearts of Stone e Blood and Wine são consideradas obras-primas por conta própria."
        ),
        "genre": "RPG",
        "platform": "PC",
        "price": 69.90,
        "developer": "CD Projekt Red",
        "publisher": "CD Projekt",
        "release_date": date(2015, 5, 19),
        "tags": ["mundo aberto", "fantasia", "escolhas morais", "single player", "premiado"],
        "rating": 9.8,
    },
    {
        "title": "Dark Souls III",
        "description": (
            "O terceiro e mais refinado capítulo da série soulsborne da FromSoftware. "
            "Ambientado no reino moribundo de Lothric, o jogo coloca o jogador como um Cinzeiro — "
            "um guerreiro ressuscitado para defeitar os Senhores das Cinzas e alimentar a Primeira Chama. "
            "Famoso pela dificuldade desafiadora mas justa, Dark Souls III recompensa paciência, aprendizado "
            "e domínio de mecânicas com uma sensação de conquista incomparável. "
            "O level design magistral, os bosses memoráveis e a lore profunda contada de forma fragmentada "
            "através dos itens fazem deste um dos melhores action-RPGs já feitos."
        ),
        "genre": "Action RPG",
        "platform": "PC",
        "price": 79.90,
        "developer": "FromSoftware",
        "publisher": "Bandai Namco",
        "release_date": date(2016, 4, 12),
        "tags": ["souls-like", "difícil", "fantasia sombria", "single player", "pvp"],
        "rating": 9.5,
    },
    {
        "title": "Red Dead Redemption 2",
        "description": (
            "Uma obra de arte narrativa da Rockstar ambientada no oeste americano de 1899. "
            "Você vive a história de Arthur Morgan, um fora-da-lei que começa a questionar sua vida criminosa "
            "enquanto a gangue Van der Linde luta pela sobrevivência contra um mundo em rápida modernização. "
            "Com o mundo aberto mais detalhado e vivo da história dos jogos, cada NPC tem rotina própria, "
            "o clima afeta o comportamento dos animais e até a barba do personagem cresce com o tempo. "
            "A narrativa é uma das mais emocionantes e maduras já contadas em um videogame."
        ),
        "genre": "Ação e Aventura",
        "platform": "PC",
        "price": 119.90,
        "developer": "Rockstar Games",
        "publisher": "Rockstar Games",
        "release_date": date(2018, 10, 26),
        "tags": ["mundo aberto", "western", "narrativa", "single player", "realismo"],
        "rating": 9.7,
    },
    {
        "title": "Hollow Knight",
        "description": (
            "Metroidvania indie desenvolvido por apenas três pessoas que rivaliza com qualquer AAA do gênero. "
            "Ambientado em Hallownest, um antigo reino de insetos subterrâneo devastado por uma praga, "
            "o jogo combina plataforma precisa, combate desafiador e uma atmosfera melancólica e poética. "
            "Com dezenas de horas de exploração, upgrades escondidos em cada canto e uma lore rica "
            "contada de forma ambiental, Hollow Knight é uma experiência que vai deixar você completamente absorto. "
            "Os DLCs gratuitos adicionaram conteúdo equivalente a jogos completos."
        ),
        "genre": "Metroidvania",
        "platform": "PC",
        "price": 29.90,
        "developer": "Team Cherry",
        "publisher": "Team Cherry",
        "release_date": date(2017, 2, 24),
        "tags": ["indie", "metroidvania", "plataforma", "difícil", "fantasia"],
        "rating": 9.4,
    },
    {
        "title": "Hades",
        "description": (
            "Roguelite que redefiniu o gênero ao colocar narrativa e personagens no centro de uma experiência "
            "de repetição. Você é Zagreus, filho do deus do submundo, tentando escapar do reino de Hades "
            "com a ajuda dos olimpianos. Cada tentativa fracassada avança a história de alguma forma — "
            "personagens comentam suas derrotas, relacionamentos evoluem e novos diálogos surgem mesmo após "
            "centenas de runs. O combate é fluido e satisfatório, com builds completamente diferentes em cada "
            "partida. Vencedor de inúmeros prêmios de jogo do ano, Hades é praticamente perfeito no que se propõe."
        ),
        "genre": "Roguelite",
        "platform": "PC",
        "price": 49.90,
        "developer": "Supergiant Games",
        "publisher": "Supergiant Games",
        "release_date": date(2020, 9, 17),
        "tags": ["roguelite", "mitologia grega", "indie", "ação", "narrativa"],
        "rating": 9.6,
    },
    {
        "title": "Sekiro: Shadows Die Twice",
        "description": (
            "Action-adventure da FromSoftware ambientado no Japão feudal do século XVI. "
            "Você joga como Wolf, um shinobi de braço de ferro que busca resgatar seu senhor e se vingar "
            "do clã inimigo que o atacou. Diferente dos Souls, Sekiro foca em combate de espada fluido e "
            "preciso baseado em duelos de pressão de postura, onde atacar e defender com timing perfeito "
            "é mais importante que grinding de level. A mobilidade do gancho ninja abre um level design "
            "vertical magnífico. Considerado por muitos o jogo mais satisfatório de se dominar."
        ),
        "genre": "Action Adventure",
        "platform": "PC",
        "price": 179.90,
        "developer": "FromSoftware",
        "publisher": "Activision",
        "release_date": date(2019, 3, 22),
        "tags": ["souls-like", "japão feudal", "difícil", "single player", "shinobi"],
        "rating": 9.4,
    },
    {
        "title": "Stardew Valley",
        "description": (
            "Jogo de fazenda e simulação criado por uma única pessoa ao longo de quatro anos. "
            "Você herda a fazenda do seu avô numa pequena cidade do interior e precisa reconstruí-la enquanto "
            "desenvolve relacionamentos com os moradores, explora minas repletas de monstros, pesca, cozinha "
            "e até casa. Stardew Valley é o antídoto perfeito para o estresse do mundo moderno: sem pressa, "
            "sem punição, apenas um ritmo de vida lento e reconfortante. "
            "O suporte ao multiplayer cooperativo permite cultivar a fazenda com amigos. "
            "Um dos jogos indie mais vendidos de todos os tempos com razão."
        ),
        "genre": "Simulação",
        "platform": "PC",
        "price": 29.90,
        "developer": "ConcernedApe",
        "publisher": "ConcernedApe",
        "release_date": date(2016, 2, 26),
        "tags": ["fazenda", "relaxante", "indie", "multiplayer", "rpg leve"],
        "rating": 9.3,
    },
    {
        "title": "Celeste",
        "description": (
            "Plataformador de precisão que narra a jornada de Madeline escalando a Montanha Celeste "
            "enquanto enfrenta seus próprios demônios internos — literalmente. "
            "Com controles pixel-perfect e design de fases genial que ensina mecânicas sem tutoriais, "
            "Celeste é desafiador mas nunca injusto: o checkpoint está sempre próximo. "
            "A narrativa sobre saúde mental, autoaceitação e síndrome do impostor é tocante e honesta. "
            "A trilha sonora de Lena Raine é uma das melhores já compostas para jogos. "
            "As fases B-Side e C-Side adicionam um desafio hardcore para quem quer mais."
        ),
        "genre": "Plataforma",
        "platform": "PC",
        "price": 39.90,
        "developer": "Maddy Thorson & Noel Berry",
        "publisher": "Matt Makes Games",
        "release_date": date(2018, 1, 25),
        "tags": ["plataforma", "indie", "difícil", "narrativa", "saúde mental"],
        "rating": 9.3,
    },
    {
        "title": "Baldur's Gate 3",
        "description": (
            "O RPG de turnos mais ambicioso já feito, desenvolvido pela Larian Studios com base no sistema "
            "Dungeons & Dragons 5ª edição. Com uma tadpole illithid no cérebro, você e seus companheiros "
            "percorrem os Reinos Esquecidos buscando uma cura enquanto forças sombrias conspiram ao redor. "
            "O jogo oferece uma liberdade de escolha absurda: praticamente toda situação tem múltiplas soluções, "
            "NPCs têm memória de tudo que você fez e o mundo reage às suas decisões de formas surpreendentes. "
            "Com co-op para 4 jogadores, mais de 200 horas de conteúdo e uma escrita excepcional, "
            "é o candidato mais forte ao maior RPG de todos os tempos."
        ),
        "genre": "RPG",
        "platform": "PC",
        "price": 199.90,
        "developer": "Larian Studios",
        "publisher": "Larian Studios",
        "release_date": date(2023, 8, 3),
        "tags": ["rpg", "d&d", "multiplayer", "turnos", "fantasia", "premiado"],
        "rating": 9.8,
    },
    {
        "title": "Doom Eternal",
        "description": (
            "FPS de ritmo frenético que eleva o combate do clássico Doom 2016 a outro nível. "
            "O Doom Slayer retorna para acabar com a invasão demoníaca na Terra numa dança de violência "
            "coreografada onde movimento constante e gerenciamento de recursos são mais importantes que mira. "
            "Cada tipo de inimigo tem uma fraqueza diferente, forçando o jogador a variar as armas em tempo real. "
            "O resultado é um combate que parece um metal pesado tocado em dificuldade máxima — intenso, "
            "exigente e incrivelmente satisfatório quando você encadeia uma sequência perfeita. "
            "A trilha sonora de Mick Gordon é agressiva e épica."
        ),
        "genre": "FPS",
        "platform": "PC",
        "price": 89.90,
        "developer": "id Software",
        "publisher": "Bethesda Softworks",
        "release_date": date(2020, 3, 20),
        "tags": ["fps", "ação", "demons", "frenético", "single player", "metal"],
        "rating": 9.1,
    },
    {
        "title": "Elden Ring",
        "description": (
            "Fruto da colaboração entre FromSoftware e George R.R. Martin, Elden Ring transporta a fórmula "
            "soulsborne para um mundo aberto gigantesco chamado Entre-Terras. "
            "Com a Elden Ring despedaçada e o Árvore-Mãe corrompida, você é um Maculado em busca dos "
            "fragmentos do anel para se tornar o novo Elden Lord. "
            "O mundo aberto permite abordar os desafios em qualquer ordem, tornando a dificuldade mais flexível "
            "sem perder a identidade da FromSoftware. Com bosses opcionais secretos, dungeons escondidas "
            "e um lore co-escrito com Martin, é possivelmente o jogo mais completo do estúdio."
        ),
        "genre": "Action RPG",
        "platform": "PC",
        "price": 249.90,
        "developer": "FromSoftware",
        "publisher": "Bandai Namco",
        "release_date": date(2022, 2, 25),
        "tags": ["souls-like", "mundo aberto", "fantasia sombria", "premiado", "george r.r. martin"],
        "rating": 9.7,
    },
    {
        "title": "Portal 2",
        "description": (
            "Puzzle game da Valve que usa portais espaciais para criar um dos designs de fases mais criativos "
            "da história dos jogos. Chell desperta novamente nas instalações da Aperture Science e precisa "
            "escapar com a ajuda do sarcástico GLaDOS e do ingênuo Wheatley. "
            "O humor é brilhante, o level design ensina mecânicas de forma elegante e orgânica, "
            "e o modo cooperativo para dois jogadores apresenta quebra-cabeças únicos que exigem comunicação "
            "e raciocínio conjunto. Considerado por muitos críticos como o jogo mais bem-desenhado de todos "
            "os tempos, Portal 2 é uma obra que envelheceu perfeitamente."
        ),
        "genre": "Puzzle",
        "platform": "PC",
        "price": 29.90,
        "developer": "Valve",
        "publisher": "Valve",
        "release_date": date(2011, 4, 19),
        "tags": ["puzzle", "co-op", "humor", "sci-fi", "clássico"],
        "rating": 9.5,
    },
    {
        "title": "Resident Evil 4 Remake",
        "description": (
            "Reimaginação magistral do clássico de 2005 que moderniza tudo sem perder a essência. "
            "Leon S. Kennedy é enviado à Espanha rural para resgatar a filha do presidente americano "
            "e se depara com uma seita religiosa de vilarejos infectados por um parasita de controle mental. "
            "O remake mantém a tensão e o ritmo do original mas adiciona profundidade à história, "
            "moderniza os controles para padrões atuais e retrabalha seções problemáticas do original. "
            "Ashley tem IA melhorada, o sistema de parry adiciona profundidade ao combate e a atmosfera "
            "de horror com ação equilibrada continua impecável."
        ),
        "genre": "Survival Horror",
        "platform": "PC",
        "price": 199.90,
        "developer": "Capcom",
        "publisher": "Capcom",
        "release_date": date(2023, 3, 24),
        "tags": ["survival horror", "ação", "remake", "single player", "clássico"],
        "rating": 9.4,
    },
    {
        "title": "Minecraft",
        "description": (
            "O jogo mais vendido da história, e por boas razões. Minecraft é um sandbox de construção e "
            "sobrevivência onde você coleta recursos, constrói estruturas e explora um mundo gerado "
            "proceduralmente praticamente infinito. Não há objetivos impostos — você define o que quer fazer. "
            "Pode construir réplicas de cidades reais, explorar cavernas em busca de diamantes, criar "
            "fazendas automáticas com redstone, ou simplesmente explorar biomas. "
            "O modo criativo remove toda limitação de recursos para construtores. "
            "Com décadas de suporte, mods e uma comunidade gigantesca, o jogo nunca para de crescer."
        ),
        "genre": "Sandbox",
        "platform": "PC",
        "price": 99.90,
        "developer": "Mojang Studios",
        "publisher": "Microsoft",
        "release_date": date(2011, 11, 18),
        "tags": ["sandbox", "sobrevivência", "construção", "multiplayer", "criativo"],
        "rating": 9.2,
    },
    {
        "title": "God of War (2018)",
        "description": (
            "Reinvenção ousada da série que trocou a Grécia Antiga pela mitologia nórdica e o espetáculo "
            "juvenil por uma narrativa adulta sobre paternidade e redenção. "
            "Kratos, agora um homem mais contido e soturno, ensina o filho Atreus a sobreviver num mundo "
            "de deuses e gigantes enquanto os dois carregam o peso de segredos não ditos. "
            "A câmara que nunca corta durante as mais de 25 horas de jogo é uma proeza técnica e narrativa. "
            "O combate com o Machado Leviatã tem um peso e impacto físico raramente sentido em outros jogos. "
            "Uma das experiências mais emocionantes que os videogames já produziram."
        ),
        "genre": "Ação e Aventura",
        "platform": "PC",
        "price": 149.90,
        "developer": "Santa Monica Studio",
        "publisher": "Sony Interactive Entertainment",
        "release_date": date(2018, 4, 20),
        "tags": ["ação", "mitologia nórdica", "narrativa", "single player", "premiado"],
        "rating": 9.7,
    },
    {
        "title": "Cyberpunk 2077",
        "description": (
            "RPG de ação da CD Projekt Red ambientado em Night City, uma megalópole californiana dominada "
            "por corporações e imersa em tecnologia cybernética. Você joga como V, um mercenário que acaba "
            "com o engrama de uma lenda do rock e terrorista morto chamado Johnny Silverhand na cabeça. "
            "Após anos de patches e atualizações, o jogo entrega um dos mundos futuristas mais detalhados "
            "e atmosféricos dos games, com uma narrativa ramificada excelente e a expansão Phantom Liberty "
            "sendo considerada uma das melhores DLCs já feitas. "
            "Agora é uma experiência completamente diferente do lançamento caótico de 2020."
        ),
        "genre": "RPG",
        "platform": "PC",
        "price": 149.90,
        "developer": "CD Projekt Red",
        "publisher": "CD Projekt",
        "release_date": date(2020, 12, 10),
        "tags": ["rpg", "cyberpunk", "mundo aberto", "sci-fi", "ação"],
        "rating": 9.0,
    },
    {
        "title": "Terraria",
        "description": (
            "Sandbox 2D de exploração, construção e sobrevivência com uma profundidade surpreendente. "
            "O que começa como um jogo simples de minerar e construir evolui para batalhas épicas contra "
            "bosses monstruosos à medida que você progride nas camadas do mundo. "
            "Com mais de 400 inimigos, 20 bosses, milhares de itens e múltiplas classes de personagem "
            "emergentes da escolha de armas, Terraria tem mais conteúdo que muitos AAAs por uma fração "
            "do preço. O desenvolvedor re-logic lançou atualizações gratuitas por mais de uma década, "
            "tornando-o um dos melhores custo-benefício dos jogos."
        ),
        "genre": "Sandbox",
        "platform": "PC",
        "price": 19.90,
        "developer": "Re-Logic",
        "publisher": "Re-Logic",
        "release_date": date(2011, 5, 16),
        "tags": ["sandbox", "2d", "sobrevivência", "construção", "multiplayer"],
        "rating": 9.2,
    },
    {
        "title": "Disco Elysium",
        "description": (
            "RPG de investigação policial completamente único que desafia tudo que você espera do gênero. "
            "Você acorda sem memória num quarto destruído de hotel e descobre que é um detetive alcoólatra "
            "investigando um assassinato numa cidade portuária pós-revolucionária chamada Revachol. "
            "Não há combate — tudo é resolvido através de diálogos e testes de habilidade, onde até "
            "os seus próprios pensamentos e instintos são personagens com quem você conversa. "
            "A escrita é brilhante, engraçada, trágica e politicamente afiada. "
            "Um dos jogos mais originais e literários já criados."
        ),
        "genre": "RPG",
        "platform": "PC",
        "price": 69.90,
        "developer": "ZA/UM",
        "publisher": "ZA/UM",
        "release_date": date(2019, 10, 15),
        "tags": ["rpg", "investigação", "indie", "narrativa", "político"],
        "rating": 9.5,
    },
    {
        "title": "Half-Life 2",
        "description": (
            "FPS que revolucionou os jogos em 2004 e ainda é referência em design até hoje. "
            "Gordon Freeman retorna para uma Terra ocupada pelo Combine, uma força alienígena totalitária, "
            "e lidera a resistência humana. Half-Life 2 introduziu física realista com o motor Source, "
            "o icônico Gravity Gun, e uma narrativa ambiental contada sem cutscenes onde o jogador "
            "nunca perde o controle. Cada capítulo apresenta mecânicas novas — buggy no litoral, "
            "helicóptero de caça, cidadela imponente — mantendo o ritmo sempre fresco. "
            "Um marco histórico que todo gamer deveria jogar."
        ),
        "genre": "FPS",
        "platform": "PC",
        "price": 19.90,
        "developer": "Valve",
        "publisher": "Valve",
        "release_date": date(2004, 11, 16),
        "tags": ["fps", "sci-fi", "clássico", "single player", "narrativa ambiental"],
        "rating": 9.6,
    },
    {
        "title": "The Legend of Zelda: Breath of the Wild",
        "description": (
            "O jogo que redefiniu o conceito de mundo aberto ao lançar em 2017. "
            "Link acorda sem memória e deve explorar livremente o vasto reino de Hyrule para reunir "
            "forças e enfrentar o Calamity Ganon. O motor de física permite soluções criativas para "
            "praticamente qualquer problema — você pode derrubar árvores para cruzar abismos, criar "
            "correntes de ar com fogo, ou usar metal como para-raios. "
            "Os 120 shrines oferecem puzzles variados e a liberdade de ir enfrentar o boss final "
            "logo no início é genuína. Uma das experiências mais alegres e liberadoras dos videogames."
        ),
        "genre": "Ação e Aventura",
        "platform": "Nintendo Switch",
        "price": 299.90,
        "developer": "Nintendo EPD",
        "publisher": "Nintendo",
        "release_date": date(2017, 3, 3),
        "tags": ["mundo aberto", "aventura", "puzzle", "nintendo", "premiado"],
        "rating": 9.7,
    },
]


def seed():
    created = 0
    skipped = 0
    for data in GAMES:
        obj, was_created = Game.objects.get_or_create(
            title=data["title"],
            platform=data["platform"],
            defaults=data,
        )
        if was_created:
            created += 1
            print(f"  [+] {obj.title}")
        else:
            skipped += 1
            print(f"  [=] {obj.title} (já existe)")

    print(f"\nConcluído: {created} criados, {skipped} ignorados.")


if __name__ == "__main__":
    seed()
