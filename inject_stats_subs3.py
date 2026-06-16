import re, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\worldcup2026\index.html'

with open(path, encoding='utf-8') as f:
    html = f.read()

STATS = [
    # AUTRICHE
    ("Christoph Baumgartner", 5, 28, 6,  7.00),
    ("Florian Grillitsch",     1, 22, 2,  6.80),
    ("Stefan Posch",           1, 28, 2,  6.80),
    ("Romano Schmid",          4, 28, 5,  6.90),
    ("Philipp Lienhart",       1, 24, 1,  6.75),

    # NORVEGE
    ("Antonio Nusa",           6, 28, 4,  6.90),
    ("Erling Haaland",        34, 38, 8,  7.85),  # peut etre titulaire

    # PORTUGAL
    ("Renato Veiga",           1, 22, 2,  6.85),
    ("Goncalo Guedes",         5, 24, 3,  6.85),
    ("Pedro Neto",             5, 28, 7,  7.00),
    ("Rafael Leao",           12, 30, 8,  7.20),

    # SENEGAL
    ("Bara Sapoko Ndiaye",     1, 12, 1,  6.70),
    ("El Hadji Malick Diouf",  2, 28, 3,  6.90),
    ("Pape Gueye",             2, 26, 2,  6.80),

    # SUISSE
    ("Djibril Sow",            2, 28, 3,  6.85),
    ("Michel Aebischer",       2, 26, 3,  6.80),
    ("Dan Ndoye",              8, 30, 6,  7.00),
    ("Fabian Rieder",          3, 28, 4,  6.85),

    # COTE D'IVOIRE
    ("Evann Guessand",         6, 26, 3,  6.90),
    ("Sebastien Haller",       5, 22, 2,  6.85),
    ("Odilon Kossounou",       1, 28, 1,  6.85),

    # MAROC
    ("Chadi Riad",             1, 22, 1,  6.80),
    ("Adam Aznou",             0, 14, 2,  6.75),
    ("Bilal El Khannouss",     5, 28, 6,  7.00),

    # ANGLETERRE
    ("Dean Henderson",         0, 36, 0,  6.95),

    # USA
    ("Tani Oluwaseyi",         4, 20, 3,  6.85),
    ("Paxten Aaronson",        3, 22, 3,  6.80),
    ("Patrick Schulte",        0, 24, 0,  6.80),

    # GHANA
    ("Alex Freeman",           0, 16, 1,  6.65),
    ("Antoine Semenyo",        8, 34, 5,  7.00),
    ("Jordan Ayew",            5, 28, 3,  6.80),

    # ECOSSE
    ("Ryan Jack",              1, 24, 2,  6.75),
    ("Stuart Armstrong",       3, 28, 4,  6.85),
    ("John Souttar",           1, 20, 0,  6.75),
    ("Scott McKenna",          1, 24, 1,  6.75),

    # SUEDE
    ("Jordan Larsson",         5, 26, 4,  6.85),
    ("Sebastian Larsson",      1, 22, 3,  6.75),
    ("Pontus Jansson",         2, 28, 1,  6.85),
    ("Marcus Danielson",       1, 22, 0,  6.75),

    # TUNISIE
    ("Saif-Eddine Khaoui",     3, 24, 3,  6.80),
    ("Montassar Talbi",        1, 26, 1,  6.80),
    ("Mohamed Drame",          0, 18, 1,  6.70),

    # JAPON
    ("Ayase Ueda",            18, 34, 4,  7.20),
    ("Daichi Kamada",          4, 28, 6,  6.95),
    ("Wataru Endo",            1, 30, 3,  6.90),
    ("Hiroki Ito",             1, 26, 2,  6.90),

    # COREE
    ("Seok-hyeon Oh",          0, 20, 0,  6.70),
    ("In-Beom Hwang",          2, 26, 3,  6.80),
    ("Seung-ho Paik",          4, 28, 5,  6.90),

    # AUSTRALIE
    ("Harry Souttar",          1, 18, 0,  6.75),
    ("Riley McGree",           4, 26, 5,  6.90),
    ("Ajdin Hrustic",          2, 22, 3,  6.80),

    # MEXIQUE
    ("Alexis Vega",            4, 24, 3,  6.80),
    ("Jorge Sanchez",          1, 22, 2,  6.75),
    ("Jose Juan Macias",       5, 20, 2,  6.80),
    ("Erik Lira",              1, 22, 2,  6.75),

    # PANAMA
    ("Edgar Barcenas",         2, 22, 3,  6.75),
    ("Jose Rodriguez",         1, 20, 2,  6.70),

    # PARAGUAY
    ("Richard Sanchez",        2, 26, 3,  6.80),
    ("Julio Enciso",           5, 24, 4,  6.90),
    ("Junior Alonso",          1, 22, 0,  6.75),
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
