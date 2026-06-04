import re, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# ── 1. Replace the stats page HTML ──────────────────────────────────────────
new_stats_div = '''<div id="stats" class="page">
  <h2 style="font-size:1.2rem;font-weight:800;margin-bottom:16px;">Effectifs officiels par sélection</h2>
  <div style="display:flex;gap:12px;align-items:center;margin-bottom:24px;flex-wrap:wrap;">
    <select id="country-select" onchange="showCountrySquad(this.value)" style="background:var(--surface);border:2px solid var(--border);color:var(--text);padding:10px 16px;border-radius:8px;font-size:0.95rem;font-weight:600;cursor:pointer;outline:none;min-width:240px;transition:border-color 0.2s;" onfocus="this.style.borderColor='var(--accent2)'" onblur="this.style.borderColor='var(--border)'">
      <option value="">— Choisir une sélection —</option>
    </select>
    <input id="player-search" type="text" placeholder="🔍 Rechercher un joueur ou un club..."
      oninput="filterSquad(this.value)"
      style="background:var(--surface);border:2px solid var(--border);color:var(--text);padding:10px 14px;border-radius:8px;font-size:0.9rem;outline:none;min-width:260px;transition:border-color 0.2s;" onfocus="this.style.borderColor='var(--accent2)'" onblur="this.style.borderColor='var(--border)'">
  </div>
  <div id="squad-display" style="min-height:200px;"></div>
</div>'''

html = re.sub(
    r'<div id="stats" class="page">.*?</div>\s*\n\n<script>',
    new_stats_div + '\n\n<script>',
    html, flags=re.DOTALL
)

# ── 2. New buildStats + showCountrySquad + filterSquad ──────────────────────
new_js = r'''function buildStats() {
  const sel = document.getElementById('country-select');
  const groups = [
    {label:'Groupe A', codes:['MEX','RSA','KOR','CZE']},
    {label:'Groupe B', codes:['CAN','SUI','QAT','BIH']},
    {label:'Groupe C', codes:['BRA','MAR','SCO','HAI']},
    {label:'Groupe D', codes:['USA','PAR','AUS','TUR']},
    {label:'Groupe E', codes:['GER','CUW','CIV','ECU']},
    {label:'Groupe F', codes:['NED','JPN','TUN','SWE']},
    {label:'Groupe G', codes:['BEL','EGY','IRN','NZL']},
    {label:'Groupe H', codes:['ESP','CPV','KSA','URU']},
    {label:'Groupe I', codes:['FRA','SEN','NOR','IRQ']},
    {label:'Groupe J', codes:['ARG','ALG','AUT','JOR']},
    {label:'Groupe K', codes:['POR','COL','UZB','COD']},
    {label:'Groupe L', codes:['ENG','CRO','GHA','PAN']},
  ];
  groups.forEach(g => {
    const og = document.createElement('optgroup');
    og.label = g.label;
    g.codes.forEach(code => {
      const t = teamData(code);
      const opt = document.createElement('option');
      opt.value = code;
      opt.textContent = t.name;
      og.appendChild(opt);
    });
    sel.appendChild(og);
  });
}

function showCountrySquad(code) {
  const container = document.getElementById('squad-display');
  document.getElementById('player-search').value = '';
  if (!code) {
    container.innerHTML = '<div style="text-align:center;padding:60px;color:var(--muted);font-size:0.95rem;">Sélectionne une équipe ci-dessus pour voir son effectif</div>';
    return;
  }
  const t = teamData(code);
  const byPos = {'GK':[],'DEF':[],'MIL':[],'ATT':[]};
  t.players.forEach(p => { if(byPos[p.pos]) byPos[p.pos].push(p); });
  const posLabels = {'GK':'🧤 Gardiens','DEF':'🛡️ Défenseurs','MIL':'⚙️ Milieux','ATT':'⚡ Attaquants'};
  const hostBadge = t.host ? '<span style="background:var(--accent);color:#000;padding:1px 8px;border-radius:10px;font-size:0.72rem;font-weight:700;margin-left:8px;">PAYS HÔTE</span>' : '';

  let rows = '';
  ['GK','DEF','MIL','ATT'].forEach(pos => {
    if (!byPos[pos].length) return;
    let playerRows = '';
    byPos[pos].forEach(p => {
      const num = t.players.indexOf(p) + 1;
      playerRows += `<div class="player-searchable" data-name="${p.name.toLowerCase()}" data-club="${p.club.toLowerCase()}"
        style="display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:6px;font-size:0.82rem;cursor:default;border-bottom:1px solid var(--border);"
        onmouseover="this.style.background='var(--surface2)'" onmouseout="this.style.background=''">
        <span style="width:22px;text-align:center;color:var(--muted);font-size:0.72rem;font-weight:700;">${num}</span>
        <span class="player-pos pos-${p.pos}" style="font-size:0.62rem;width:28px;text-align:center;padding:2px 0;">${p.pos}</span>
        <span style="flex:1;font-weight:${p.starter?'600':'400'};">${p.name}</span>
        <span style="font-size:0.75rem;color:var(--muted);max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${p.club}">${p.club}</span>
        <span class="starter-dot ${p.starter?'starter':'sub'}" title="${p.starter?'Titulaire':'Remplaçant'}" style="flex-shrink:0;"></span>
      </div>`;
    });
    rows += `<div style="background:var(--surface);border:1px solid var(--border);border-radius:10px;overflow:hidden;">
      <div style="padding:10px 14px;font-weight:700;font-size:0.82rem;background:var(--surface2);border-bottom:1px solid var(--border);color:var(--accent2);">${posLabels[pos]} <span style="color:var(--muted);font-weight:400;">(${byPos[pos].length})</span></div>
      ${playerRows}
    </div>`;
  });

  container.innerHTML = `
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:20px;padding:16px 20px;background:var(--surface);border:1px solid var(--border);border-radius:12px;">
      <span style="font-size:2.2rem;">${flagHtml(t.flag)}</span>
      <div>
        <div style="font-size:1.3rem;font-weight:800;">${t.name}${hostBadge}</div>
        <div style="font-size:0.82rem;color:var(--muted);margin-top:2px;">${t.players.length} joueurs · <span style="color:var(--green);">●</span> Titulaires numéros 1-11</div>
      </div>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;">${rows}</div>`;
}

function filterSquad(query) {
  const q = query.toLowerCase().trim();
  const code = document.getElementById('country-select').value;
  if (!code && q) return;
  document.querySelectorAll('.player-searchable').forEach(el => {
    const match = !q || el.dataset.name.includes(q) || el.dataset.club.includes(q);
    el.style.display = match ? '' : 'none';
  });
}'''

# Replace old buildStats + filterPlayers
html = re.sub(
    r'function buildStats\(\).*?function filterPlayers\(query\) \{.*?\}',
    new_js,
    html, flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

dest = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\recette_facturx_app\app\world_cup_2026.html'
shutil.copy('index.html', dest)
print('Done')
