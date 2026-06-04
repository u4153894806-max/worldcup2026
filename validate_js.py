import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'<script>(.*)</script>', html, re.DOTALL)
js = m.group(1)

# Check for duplicate name matches (keys that could hit multiple players)
SUSPICIOUS_KEYS = ["Gavi", "Pepe", "Gerson", "Vitinha", "Rodrygo", "Rodrigo",
                   "David", "Carlos", "Gomez", "Luis", "Santos", "Fernandez"]

print("=== Checking for ambiguous name matches ===")
for key in SUSPICIOUS_KEYS:
    matches = re.findall(r'name:"[^"]*' + re.escape(key) + r'[^"]*"', js)
    if len(matches) > 1:
        print(f"KEY '{key}' matches {len(matches)} players:")
        for match in matches:
            print(f"  {match}")

print("\n=== Checking all player entries for malformed structure ===")
# Each player should be: {name:"...", pos:"GK|DEF|MIL|ATT", club:"...", starter:true|false, goals:NUM, matches:NUM}
bad = []
for m2 in re.finditer(r'\{name:"[^"]*", pos:"[^"]*", club:"[^"]*", starter:(?:true|false), goals:\d+, matches:\d+\}', js):
    pass  # good

# Find malformed ones
all_players = re.findall(r'\{name:"[^"]+",.*?matches:\d+\}', js)
print(f"Total player-like entries found: {len(all_players)}")

# Find entries NOT matching the clean pattern
clean_pattern = re.compile(r'^\{name:"[^"]+", pos:"(?:GK|DEF|MIL|ATT)", club:"[^"]*", starter:(?:true|false), goals:\d+, matches:\d+\}$')
bad_entries = []
for entry in all_players:
    if not clean_pattern.match(entry.strip()):
        bad_entries.append(entry[:200])

print(f"Malformed entries: {len(bad_entries)}")
for e in bad_entries[:10]:
    print(f"  BAD: {e}")

print("\n=== Checking for syntax issues in showCountrySquad ===")
idx = js.find('function showCountrySquad')
end = js.find('\nfunction ', idx+1)
scs = js[idx:end]
print(f"showCountrySquad length: {len(scs)}")
# Count backticks
ticks = scs.count('`')
print(f"Backtick count: {ticks} (should be even)")
if ticks % 2 != 0:
    print("ODD NUMBER OF BACKTICKS - syntax error!")
    # Find the problematic line
    for i, line in enumerate(scs.split('\n')):
        if '`' in line:
            print(f"  L{i}: {line[:100]}")
