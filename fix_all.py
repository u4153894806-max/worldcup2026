import re, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\worldcup2026\index.html'

# FIFA code -> flagcdn ISO code
FLAG_CDN = {
    'ALG':'dz','ARG':'ar','AUS':'au','AUT':'at','BEL':'be','BIH':'ba',
    'BRA':'br','CPV':'cv','CAN':'ca','CIV':'ci','COD':'cd','COL':'co',
    'CRO':'hr','CUW':'cw','CZE':'cz','ECU':'ec','EGY':'eg','ENG':'gb-eng',
    'ESP':'es','FRA':'fr','GER':'de','GHA':'gh','HAI':'ht','IRN':'ir',
    'IRQ':'iq','JOR':'jo','JPN':'jp','KOR':'kr','KSA':'sa','MAR':'ma',
    'MEX':'mx','NED':'nl','NOR':'no','NZL':'nz','PAN':'pa','PAR':'py',
    'POR':'pt','QAT':'qa','RSA':'za','SCO':'gb-sct','SEN':'sn','SUI':'ch',
    'SWE':'se','TUN':'tn','TUR':'tr','URU':'uy','USA':'us','UZB':'uz',
}

with open(path, encoding='utf-8') as f:
    html = f.read()

# ── 1. Replace all flag emojis in TEAMS with __CODE__ sentinels ──────────────
# The flag field looks like: flag:"🇫🇷"  or flag:"__ENG__" (already done for ENG/SCO)
# We replace all emoji flags with __CODE__ using the known flag→code mapping
FLAG_TO_CODE = {
    '🇩🇿':'ALG','🇦🇷':'ARG','🇦🇺':'AUS','🇦🇹':'AUT','🇧🇪':'BEL','🇧🇦':'BIH',
    '🇧🇷':'BRA','🇨🇻':'CPV','🇨🇦':'CAN','🇨🇮':'CIV','🇨🇩':'COD','🇨🇴':'COL',
    '🇭🇷':'CRO','🇨🇼':'CUW','🇨🇿':'CZE','🇪🇨':'ECU','🇪🇬':'EGY',
    '🇪🇸':'ESP','🇫🇷':'FRA','🇩🇪':'GER','🇬🇭':'GHA','🇭🇹':'HAI','🇮🇷':'IRN',
    '🇮🇶':'IRQ','🇯🇴':'JOR','🇯🇵':'JPN','🇰🇷':'KOR','🇸🇦':'KSA','🇲🇦':'MAR',
    '🇲🇽':'MEX','🇳🇱':'NED','🇳🇴':'NOR','🇳🇿':'NZL','🇵🇦':'PAN','🇵🇾':'PAR',
    '🇵🇹':'POR','🇶🇦':'QAT','🇿🇦':'RSA','🇸🇳':'SEN','🇨🇭':'SUI',
    '🇸🇪':'SWE','🇹🇳':'TUN','🇹🇷':'TUR','🇺🇾':'URU','🇺🇸':'USA','🇺🇿':'UZB',
}
for emoji, code in FLAG_TO_CODE.items():
    html = html.replace(f'flag:"{emoji}"', f'flag:"__{code}__"')

# ── 2. Build the complete flagHtml function ───────────────────────────────────
cases = '\n'.join(
    f'  if(f==="__{code}__") return img("{cdn}");'
    for code, cdn in FLAG_CDN.items()
)
new_helper = f'''function flagHtml(f) {{
  function img(c) {{
    return "<img src='https://flagcdn.com/24x18/"+c+".png' style='height:1.4em;vertical-align:middle;border-radius:2px' alt='"+c+"'>";
  }}
{cases}
  return f;
}}
'''

# Remove old flagHtml if present
html = re.sub(r'function flagHtml\(f\) \{.*?\}\n', '', html, flags=re.DOTALL)
# Inject before teamData
html = html.replace('function teamData(code) {', new_helper + 'function teamData(code) {', 1)

# ── 3. Make sure all ${x.flag} calls go through flagHtml ─────────────────────
for var in ['h','a','t','p']:
    html = html.replace(f'${{flagHtml({var}.flag)}}', f'${{flagHtml({var}.flag)}}')  # idempotent
    html = html.replace(f'${{{var}.flag}}', f'${{flagHtml({var}.flag)}}')

# ── 4. Replace knockout phase content with "pas encore commencé" ──────────────
TBD_MSG = '''<div style="text-align:center;padding:60px 20px;color:var(--muted)">
  <div style="font-size:3rem;margin-bottom:16px">⏳</div>
  <div style="font-size:1.2rem;font-weight:700;color:var(--text);margin-bottom:8px">Pas encore commencé</div>
  <div style="font-size:0.9rem">Cette phase sera disponible à l'issue de la phase de groupes.<br>
  Le tournoi démarre le <strong style="color:var(--accent)">11 juin 2026</strong>.</div>
</div>'''

for phase_id in ['huitiemes-container', 'quarts-container', 'demis-container', 'finale-container']:
    # Replace buildPhase calls for these containers with direct innerHTML injection
    pass

# Replace the hardcoded knockout match data with TBD
html = re.sub(
    r'const H8_MATCHES = \[.*?\];',
    'const H8_MATCHES = [];',
    html, flags=re.DOTALL
)
html = re.sub(
    r'const QF_MATCHES = \[.*?\];',
    'const QF_MATCHES = [];',
    html, flags=re.DOTALL
)
html = re.sub(
    r'const SEMI_MATCHES = \[.*?\];',
    'const SEMI_MATCHES = [];',
    html, flags=re.DOTALL
)
html = re.sub(
    r'const FINAL_MATCHES = \[.*?\];',
    'const FINAL_MATCHES = [];',
    html, flags=re.DOTALL
)

# Replace buildPhase function to show TBD when no matches
tbd_msg_js = TBD_MSG.replace('\n', '').replace('"', '\\"')
old_build = 'function buildPhase(containerId, rounds) {\n  const container = document.getElementById(containerId);\n  let html = \'\';\n  rounds.forEach(round => {'
new_build = f'''function buildPhase(containerId, rounds) {{
  const container = document.getElementById(containerId);
  if (!rounds || rounds.length === 0 || rounds.every(r => !r.matches || r.matches.length === 0)) {{
    container.innerHTML = "{tbd_msg_js}";
    return;
  }}
  let html = \'\';
  rounds.forEach(round => {{'''
html = html.replace(old_build, new_build, 1)
# Close the extra brace introduced
html = html.replace(
    "  container.innerHTML = html;\n}",
    "  container.innerHTML = html;\n  }}\n}}",
    1
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

dest = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\recette_facturx_app\app\world_cup_2026.html'
shutil.copy(path, dest)
print('Done')
