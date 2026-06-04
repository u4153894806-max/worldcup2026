import re, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\worldcup2026\index.html'

with open(path, encoding='utf-8') as f:
    html = f.read()

STATS = [
    ("Joel Ordonez",    0, 30, 1, 6.95),
    ("Ezri Konsa",      0, 34, 0, 6.75),
    ("Nico Oreilly",    0, 15, 0, 6.62),
    ("Elliot Anderson", 3, 36, 4, 7.05),
    ("Yeremy Pino",     5, 28, 3, 6.88),
    ("Marten De Roon",  1, 32, 2, 7.07),
    ("Tyler Fletcher",  0, 12, 0, 6.42),
]

updated = 0
for (key, goals, matches, assists, rating) in STATS:
    pattern = (
        r'(\{name:"[^"]*' + re.escape(key) + r'[^"]*", pos:"[^"]*", club:"[^"]*", starter:[^,]*, )'
        r'goals:\d+(, matches:)\d+(, assists:)\d+(, rating:)[\d.]+'
    )
    replacement = r'\g<1>goals:' + str(goals) + r'\g<2>' + str(matches) + r'\g<3>' + str(assists) + r'\g<4>' + str(rating)
    new_html, n = re.subn(pattern, replacement, html)
    if n > 0:
        html = new_html
        updated += n
        print(f'  OK: {key}')
    else:
        print(f'  NOT FOUND: {key}')

print(f'Updated {updated}')
with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Done')
