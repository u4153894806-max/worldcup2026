import re, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\worldcup2026\index.html'

with open(path, encoding='utf-8') as f:
    html = f.read()

# Stats ciblées pour les remplaçants présents dans les squads
# pattern pour starter:false uniquement
# (key, goals, matches, assists, rating)
STATS = [
    # === FRANCE subs ===
    ("Rayan Cherki",         17, 35, 11, 7.30),
    ("Bradley Barcola",      13, 34, 6,  7.10),
    ("Ngolo Kante",           2, 26, 4,  7.00),
    ("Ibrahima Konate",       1, 32, 0,  7.05),
    ("Mike Maignan",          0, 35, 0,  7.15),
    ("William Saliba",        2, 38, 1,  7.22),
    ("Warren Zaire-Emery",    4, 28, 7,  7.05),
    ("Desire Doue",           8, 28, 6,  7.10),
    ("Lucas Hernandez",       0, 20, 0,  6.80),
    ("Jean-Philippe Mateta",  16, 34, 6, 7.15),
    ("Maghnes Akliouche",     8, 32, 7,  7.05),
    ("Maxence Lacroix",       1, 26, 0,  6.85),
    ("Adrien Rabiot",         4, 28, 0,  6.90),

    # === ANGLETERRE subs ===
    ("Leny Yoro",             0, 10, 0,  6.95),
    ("Tino Livramento",       2, 30, 5,  7.00),
    ("Jordan Henderson",      1, 28, 3,  6.80),
    ("Dan Burn",              2, 32, 1,  6.80),
    ("Djed Spence",           1, 22, 3,  6.80),
    ("Jarell Quansah",        1, 28, 0,  6.85),
    ("James Trafford",        0, 30, 0,  7.00),
    ("Haji Wright",           8, 28, 3,  6.90),

    # === ESPAGNE subs ===
    ("Joan Garcia",           0, 8,  0,  7.05),
    ("Rodri",                 0, 5,  0,  7.20),
    ("Marc Cucurella",        1, 30, 5,  6.90),

    # === ALLEMAGNE subs ===
    ("Pascal Gross",          5, 34, 8,  7.10),
    ("Felix Nmecha",          3, 28, 2,  6.85),
    ("Malick Thiaw",          1, 25, 1,  6.90),
    ("Lennart Karl",          0, 15, 1,  6.70),
    ("Ibrahim Maza",          3, 18, 4,  6.90),

    # === PAYS-BAS subs ===
    ("Mark Flekken",          0, 32, 0,  7.15),
    ("Jorrel Hato",           2, 30, 2,  7.00),
    ("Micky Van De Ven",      0, 22, 2,  7.05),
    ("Noa Lang",              8, 28, 6,  7.00),
    ("Mats Wieffer",          2, 32, 3,  6.90),
    ("Tsuyoshi Watanabe",     1, 28, 2,  6.80),

    # === BELGIQUE subs ===
    ("Dodi Lukebakio",       12, 30, 5,  7.05),
    ("Koni De Winter",        2, 25, 1,  6.90),
    ("Alexis Saelemaekers",   4, 30, 6,  7.00),
    ("Senne Lammens",         0, 12, 0,  6.70),
    ("Hans Vanaken",          5, 30, 8,  7.05),
    ("Joaquin Seys",          2, 28, 3,  6.80),

    # === SUISSE subs ===
    ("Ardon Jashari",         3, 28, 4,  6.95),

    # === PORTUGAL subs ===
    ("Francisco Conceicao",   9, 35, 7,  7.15),
    ("Vitinha",               4, 40, 8,  7.20),
    ("Joao Felix",           10, 28, 6,  7.10),

    # === CROATIE subs ===
    ("Ivor Pandur",           0, 20, 0,  6.80),
    ("Borna Sosa",            1, 26, 4,  6.85),

    # === ITALIE subs ===
    ("Bremer",                0, 5,  0,  7.00),
    ("Evan Ndicka",           2, 32, 2,  6.95),

    # === BRESIL subs ===
    ("Igor Thiago",           8, 20, 2,  6.95),

    # === AFRIQUE ===
    ("Yoane Wissa",          15, 32, 5,  7.25),
    ("Krepin Diatta",         5, 26, 4,  6.90),
    ("Moussa Niakhate",       2, 22, 0,  6.75),
    ("Neil El Aynaoui",       3, 28, 4,  6.90),
    ("Ernest Nuamah",         6, 26, 4,  6.90),

    # === ETATS-UNIS subs ===
    ("Malik Tillman",         5, 25, 4,  6.95),
    ("Carney Chukwuemeka",    3, 20, 2,  6.80),

    # === NORVEGE subs ===
    ("Fredrik Aursnes",       2, 30, 3,  6.85),
    ("Andreas Schjelderup",   5, 28, 6,  6.95),
    ("Julian Ryerson",        2, 26, 3,  6.85),

    # === TURQUIE subs ===
    ("Altay Bayindir",        0, 8,  0,  6.75),
    ("Ferdi Kadioglu",        3, 32, 5,  7.05),
    ("Kaan Ayhan",            2, 28, 1,  6.75),
    ("Kerem Akturkoglu",     10, 32, 8,  7.10),
    ("Baris Alper Yilmaz",    8, 30, 5,  6.95),
    ("Eren Elmali",           1, 22, 2,  6.75),
    ("Abdulkerim Bardakci",   2, 28, 0,  6.80),
    ("Ismail Jakobs",         1, 24, 3,  6.80),
    ("Ugurcan Cakir",         0, 26, 0,  6.85),

    # === URUGUAY subs ===
    ("Mathias Olivera",       1, 30, 4,  6.95),
    ("Geronimo Rulli",        0, 22, 0,  6.90),

    # === SUEDE subs ===
    ("Viktor Johansson",      0, 28, 0,  6.90),
    ("Yasin Ayari",           3, 28, 4,  6.85),
    ("Gustaf Nilsson",        7, 30, 4,  6.90),
    ("Anis Slimane",          4, 28, 5,  6.90),
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
    print(f'Not found ({len(not_found)}): {", ".join(not_found)}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Done')
