import re, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\worldcup2026\index.html'

with open(path, encoding='utf-8') as f:
    html = f.read()

# Add assists:0, rating:0 to every player entry that doesn't already have them
# Pattern: matches:N} -> matches:N, assists:0, rating:0}
before = html.count('assists:')
html = re.sub(
    r'(goals:\d+, matches:\d+)\}',
    r'\1, assists:0, rating:0}',
    html
)
after = html.count('assists:')
print(f'Added assists/rating fields to {after - before} players')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Done')
