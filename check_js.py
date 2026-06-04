import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'<script>(.*)</script>', html, re.DOTALL)
js = m.group(1)

lines = js.split('\n')

# Track template literal depth
depth = 0
for i, line in enumerate(lines):
    bt = line.count('`')
    if bt > 0:
        print(f'L{i+1} depth={depth} ticks={bt}: {line[:120]}')
    depth += bt % 2  # each backtick toggles (rough)
