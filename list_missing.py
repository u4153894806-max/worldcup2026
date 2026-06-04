import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    html = f.read()

pattern = r'\{name:"([^"]+)", pos:"([^"]+)", club:"([^"]+)", starter:true, goals:0, matches:0, assists:0, rating:0\}'
matches = re.findall(pattern, html)
print(f'Total starters at 0: {len(matches)}')
for m in matches:
    print(f'{m[0]} | {m[1]} | {m[2]}')
