import re, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\worldcup2026\index.html'

with open(path, encoding='utf-8') as f:
    html = f.read()

# Step 1: mark the broken subdivision flag emojis as sentinels
ENG_FLAG = '\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F'
SCO_FLAG = '\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E006F\U000E007F'

html = html.replace(f'flag:"{ENG_FLAG}"', 'flag:"__ENG__"')
html = html.replace(f'flag:"{SCO_FLAG}"', 'flag:"__SCO__"')

# Step 2: inject flagHtml helper right before the teamData function
helper = '''function flagHtml(f) {
  if (f === "__ENG__") return "<img src='https://flagcdn.com/24x18/gb-eng.png' style='height:1.4em;vertical-align:middle;border-radius:2px' alt='ENG'>";
  if (f === "__SCO__") return "<img src='https://flagcdn.com/24x18/gb-sct.png' style='height:1.4em;vertical-align:middle;border-radius:2px' alt='SCO'>";
  return f;
}
'''

html = html.replace('function teamData(code) {', helper + 'function teamData(code) {', 1)

# Step 3: update all template literal flag usages to call flagHtml()
html = html.replace('${h.flag}', '${flagHtml(h.flag)}')
html = html.replace('${a.flag}', '${flagHtml(a.flag)}')
html = html.replace('${t.flag}', '${flagHtml(t.flag)}')
html = html.replace('${p.flag}', '${flagHtml(p.flag)}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

dest = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\recette_facturx_app\app\world_cup_2026.html'
shutil.copy(path, dest)
print('Done - flags fixed for ENG and SCO')
