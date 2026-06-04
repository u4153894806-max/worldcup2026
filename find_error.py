import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Extract script
m = re.search(r'<script>(.*)</script>', html, re.DOTALL)
js = m.group(1)

# Check for unmatched braces in TEAMS
teams_m = re.search(r'const TEAMS = \{(.*?)\};\s*\n', js, re.DOTALL)
if not teams_m:
    print("TEAMS not found as expected")
else:
    print("TEAMS found, length:", len(teams_m.group(1)))

# Check each player line for syntax issues
player_lines = [l for l in js.split('\n') if 'goals:' in l and 'matches:' in l]
print(f"\nTotal player lines: {len(player_lines)}")

# Look for any lines that might have been corrupted
for i, line in enumerate(player_lines):
    # Check it has the expected structure
    if not re.match(r'\s*\{name:"[^"]+", pos:"[^"]+", club:"[^"]+", starter:(true|false), goals:\d+, matches:\d+\}', line.strip()):
        print(f"SUSPICIOUS line {i}: {line[:200]}")

print("\nChecking buildGroups function...")
bg_m = re.search(r'function buildGroups\(\)(.*?)^function ', js, re.MULTILINE | re.DOTALL)
if bg_m:
    print("buildGroups found, first 300 chars:", bg_m.group(1)[:300])
else:
    print("buildGroups NOT found!")
    # Search for it differently
    idx = js.find('function buildGroups')
    if idx >= 0:
        print("Found at index", idx, ":", js[idx:idx+100])
