import re, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\worldcup2026\index.html'

with open(path, encoding='utf-8') as f:
    html = f.read()

# Stats des remplaçants notables - saison 2024-25
# (goals, matches, assists, sofascore_rating)
STATS = [
    # === FRANCE ===
    ("Marcus Thuram",       11, 36, 8,  7.20),
    ("Kingsley Coman",       4, 26, 5,  7.00),
    ("Randal Kolo Muani",    7, 22, 3,  6.95),
    ("Matteo Guendouzi",     3, 34, 5,  6.95),
    ("Jonathan Clauss",      1, 26, 4,  6.80),
    ("Youssouf Fofana",      2, 32, 2,  6.90),
    ("Khephren Thuram",      3, 30, 3,  7.00),
    ("Castello Lukeba",      1, 26, 1,  6.90),
    ("Theo Hernandez",       3, 28, 8,  7.10),

    # === ANGLETERRE ===
    ("Eberechi Eze",        11, 34, 6,  7.20),
    ("Amad Diallo",         14, 35, 5,  7.30),
    ("Reece James",          2, 18, 3,  7.00),
    ("Ivan Toney",          12, 30, 4,  7.00),
    ("Leny Yoro",            0, 10, 0,  6.95),
    ("Cole Palmer",         25, 34, 14, 7.68),  # starter probablement
    ("Morgan Rogers",        8, 35, 9,  7.15),
    ("Noni Madueke",         9, 32, 5,  7.10),
    ("Jarrod Bowen",         9, 34, 6,  7.05),
    ("Ollie Watkins",       19, 36, 8,  7.35),

    # === ESPAGNE ===
    ("Pedro Porro",          3, 36, 8,  7.10),
    ("Ferran Torres",        8, 30, 5,  7.05),
    ("Dani Olmo",            6, 22, 4,  7.20),
    ("Dean Huijsen",         2, 28, 1,  7.10),
    ("Mikel Oyarzabal",     15, 30, 4,  7.29),
    ("Martin Zubimendi",     0, 38, 5,  7.15),
    ("Pau Cubarsi",          1, 38, 1,  7.20),
    ("Mikel Merino",         4, 25, 4,  7.05),

    # === ALLEMAGNE ===
    ("Konrad Laimer",        3, 30, 9,  7.10),
    ("Florian Wirtz",       18, 40, 20, 7.65),  # probablement titulaire
    ("Kai Havertz",         14, 38, 8,  7.25),
    ("Leroy Sane",           8, 26, 7,  7.00),
    ("Thomas Muller",        4, 28, 8,  6.95),
    ("Maximilian Beier",    10, 34, 5,  7.05),

    # === PAYS-BAS ===
    ("Frenkie De Jong",      1, 19, 4,  7.00),
    ("Crysencio Summerville", 5, 31, 2, 7.00),
    ("Brian Brobbey",       15, 34, 6,  7.15),
    ("Quinten Timber",       4, 30, 6,  7.05),
    ("Jeremie Frimpong",     5, 34, 10, 7.20),

    # === BELGIQUE ===
    ("Charles De Ketelaere", 12, 35, 8, 7.25),
    ("Amadou Onana",         2, 25, 0,  6.95),
    ("Leandro Trossard",     8, 34, 6,  7.10),

    # === SUISSE ===
    ("Yann Sommer",          0, 38, 0,  7.35),
    ("Gregor Kobel",         0, 30, 0,  7.10),
    ("Manuel Akanji",        1, 28, 2,  7.00),
    ("Granit Xhaka",         4, 36, 6,  7.10),
    ("Breel Embolo",         8, 28, 4,  6.90),

    # === AUTRICHE ===
    ("Marcel Sabitzer",      6, 30, 6,  7.05),
    ("Patrick Wimmer",       5, 34, 7,  7.00),

    # === PORTUGAL ===
    ("Goncalo Inacio",       2, 32, 3,  7.20),
    ("Francisco Trincao",    9, 30, 5,  7.05),
    ("Vitinha",              4, 40, 8,  7.20),
    ("Joao Felix",          10, 28, 6,  7.10),

    # === CROATIE ===
    ("Petar Sucic",          4, 28, 7,  7.05),
    ("Luka Sucic",           6, 30, 8,  7.10),
    ("Borna Sosa",           1, 26, 4,  6.85),

    # === ITALIE ===
    ("Federico Chiesa",      1, 14, 1,  6.72),
    ("Giacomo Raspadori",    8, 35, 4,  6.93),
    ("Lorenzo Pellegrini",   6, 32, 5,  6.85),
    ("Federico Dimarco",     4, 40, 9,  7.15),
    ("Sandro Tonali",        3, 31, 3,  6.95),
    ("Riccardo Calafiori",   1, 24, 2,  6.90),
    ("Mateo Retegui",       24, 40, 5,  7.38),
    ("Alessandro Bastoni",   2, 36, 4,  7.05),

    # === ETATS-UNIS ===
    ("Folarin Balogun",     19, 30, 4,  7.20),
    ("Timothy Weah",         2, 25, 2,  6.90),
    ("Cucho Hernandez",     11, 30, 3,  6.95),
    ("Tyler Adams",          0, 18, 2,  6.85),
    ("Yunus Musah",          2, 28, 4,  6.90),
    ("Gio Reyna",            5, 22, 5,  6.95),

    # === ALGERIE ===
    ("Mohamed Amoura",       8, 34, 3,  7.05),
    ("Rayan Ait-Nouri",      0, 32, 2,  7.10),
    ("Youcef Atal",          3, 22, 3,  6.90),

    # === MAROC ===
    ("Abde Ezzalzouli",      8, 32, 7,  7.05),
    ("Ilias Chair",          7, 30, 5,  6.95),
    ("Munir El Haddadi",     5, 28, 4,  6.85),

    # === SENEGAL ===
    ("Ismaila Sarr",         9, 28, 5,  7.00),
    ("Nicolas Jackson",     14, 34, 8,  7.15),
    ("Lamine Camara",        4, 32, 5,  6.95),

    # === EGYPTE ===
    ("Mostafa Mohamed",     12, 32, 4,  7.00),
    ("Omar Marmoush",       15, 34, 12, 7.35),
    ("Emam Ashour",          3, 28, 4,  6.90),

    # === NIGERIA (Ghana/COD area) ===
    ("Antoine Semenyo",      8, 34, 5,  7.00),
    ("Jordan Ayew",          5, 28, 3,  6.80),
    ("Inaki Williams",      10, 34, 4,  7.00),

    # === BRESIL ===
    ("Endrick",              7, 24, 2,  7.00),
    ("Gabriel Martinelli",  10, 28, 8,  7.05),
    ("Rodrygo",             15, 36, 10, 7.20),
    ("Andreas Pereira",      5, 32, 6,  6.95),

    # === ARGENTINE ===
    ("Paulo Dybala",        13, 26, 6,  7.25),
    ("Nicolas Gonzalez",     5, 22, 4,  6.95),
    ("Exequiel Palacios",    2, 30, 4,  6.90),
    ("Valentin Carboni",     4, 22, 3,  6.90),

    # === MEXIQUE ===
    ("Santiago Gimenez",    24, 32, 6,  7.30),
    ("Hirving Lozano",       8, 26, 5,  6.95),
    ("Uriel Antuna",         6, 28, 4,  6.85),

    # === COLOMBIE ===
    ("Luis Diaz",           11, 34, 6,  7.15),
    ("Rafael Santos Borre",  7, 28, 3,  6.95),
    ("Jorge Carrascal",      5, 28, 6,  6.95),

    # === URUGUAY ===
    ("Maxi Gomez",           8, 26, 3,  6.90),
    ("Martin Caceres",       0, 18, 1,  6.70),

    # === EQUATEUR ===
    ("Jeremy Sarmiento",     4, 28, 4,  6.85),
    ("Angel Mena",           5, 22, 2,  6.80),

    # === CANADA ===
    ("Jonathan David",      26, 34, 4,  7.40),
    ("Tajon Buchanan",       5, 30, 7,  7.00),

    # === COREE ===
    ("Hwang Hee-chan",       8, 28, 4,  6.95),
    ("Cho Gue-sung",         9, 26, 3,  6.90),

    # === JAPON ===
    ("Kaoru Mitoma",        10, 32, 7,  7.10),
    ("Takefusa Kubo",        9, 34, 8,  7.10),
    ("Ritsu Doan",           8, 30, 6,  7.00),

    # === AUSTRALIE ===
    ("Craig Goodwin",        3, 24, 4,  6.80),
    ("Cameron Burgess",      1, 22, 0,  6.75),

    # === TURQUIE ===
    ("Kerem Akturkoglu",    10, 32, 8,  7.10),
    ("Yunus Akgun",          5, 28, 4,  6.90),
    ("Baris Alper Yilmaz",   8, 30, 5,  6.95),

    # === NORVEGE ===
    ("Alexander Sorloth",   18, 34, 6,  7.20),
    ("Martin Odegaard",     10, 24, 8,  7.30),

    # === SUEDE ===
    ("Dejan Kulusevski",    12, 36, 12, 7.30),
    ("Aleksandar Isak",     23, 34, 6,  7.40),
    ("Emil Forsberg",        3, 24, 4,  6.85),

    # === REP. TCHEQUE ===
    ("Patrik Schick",       12, 28, 4,  7.05),
    ("Tomas Soucek",         6, 36, 3,  7.00),
    ("Vladimir Coufal",      1, 28, 3,  6.80),
]

updated = 0
not_found = []
for (key, goals, matches, assists, rating) in STATS:
    pattern = (
        r'(\{name:"[^"]*' + re.escape(key) + r'[^"]*", pos:"[^"]*", club:"[^"]*", starter:false, )'
        r'goals:\d+(, matches:)\d+(, assists:)\d+(, rating:)[\d.]+'
    )
    replacement = r'\g<1>goals:' + str(goals) + r'\g<2>' + str(matches) + r'\g<3>' + str(assists) + r'\g<4>' + str(rating)
    new_html, n = re.subn(pattern, replacement, html)
    if n > 0:
        html = new_html
        updated += n
        print(f'  OK: {key}')
    else:
        not_found.append(key)

print(f'\nUpdated: {updated}')
if not_found:
    print(f'Not found ({len(not_found)}):')
    for k in not_found:
        print(f'  - {k}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Done')
