import re, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\worldcup2026\index.html'

with open(path, encoding='utf-8') as f:
    html = f.read()

# Stats: {exact_name_substring: (goals, matches)}
# Key must match a substring of the name as stored in the JS (no accents, exact case)
STATS = {
    # France
    "Kylian Mbappe":     (43, 39),
    "Ousmane Dembele":   (18, 35),
    "Marcus Thuram":     (18, 37),
    "Theo Hernandez":    (5, 28),
    "Aurelien Tchouameni":(3, 35),
    "Jules Kounde":      (2, 38),
    "Lucas Digne":       (1, 28),
    "Dayot Upamecano":   (2, 30),
    "Manu Kone":         (4, 32),
    "Brice Samba":       (0, 30),
    # England
    "Harry Kane":        (36, 31),
    "Jude Bellingham":   (8, 40),
    "Phil Foden":        (13, 40),
    "Bukayo Saka":       (10, 42),
    "Marcus Rashford":   (5, 22),
    "Cole Palmer":       (10, 32),
    "Trent Alexander-Arnold": (3, 38),
    "Declan Rice":       (5, 38),
    "John Stones":       (1, 28),
    # Germany
    "Florian Wirtz":     (5, 33),
    "Jamal Musiala":     (4, 7),
    "Kai Havertz":       (2, 11),
    "Thomas Muller":     (8, 30),
    "Leroy Sane":        (7, 28),
    "Ilkay Gundogan":    (5, 30),
    "Antonio Rudiger":   (2, 35),
    "Leon Goretzka":     (4, 28),
    "Joshua Kimmich":    (3, 38),
    # Spain
    "Lamine Yamal":      (16, 28),
    "Pedri":             (2, 29),
    "Gavi":              (0, 11),
    "Dani Olmo":         (7, 26),
    "Nico Williams":     (6, 25),
    "Fabian Ruiz":       (5, 35),
    "Mikel Merino":      (4, 30),
    "Ferran Torres":     (8, 28),
    "Alex Grimaldo":     (5, 38),
    "Marc Pubill":       (1, 28),
    "Eric Garcia":       (1, 30),
    "Marcos Llorente":   (4, 30),
    # Portugal
    "Cristiano Ronaldo": (28, 30),
    "Bruno Fernandes":   (9, 35),
    "Bernardo Silva":    (2, 32),
    "Rafael Leao":       (9, 29),
    "Joao Felix":        (20, 30),
    "Ruben Neves":       (3, 28),
    "Diogo Jota":        (12, 30),
    "Vitinha":           (5, 35),
    "Pepe":              (1, 22),
    # Brazil
    "Vinicius Junior":   (21, 50),
    "Rodrygo":           (9, 24),
    "Endrick":           (5, 20),
    "Raphinha":          (13, 20),
    "Lucas Paqueta":     (3, 20),
    "Gerson":            (4, 28),
    "Marquinhos":        (2, 35),
    "Casemiro":          (3, 28),
    # Argentina
    "Lionel Messi":      (16, 22),
    "Julian Alvarez":    (18, 44),
    "Lautaro Martinez":  (17, 30),
    "Enzo Fernandez":    (11, 39),
    "Paulo Dybala":      (11, 25),
    "Rodrigo De Paul":   (4, 32),
    "Lisandro Martinez": (2, 30),
    "Angel Di Maria":    (3, 20),
    "Leandro Paredes":   (2, 25),
    # Netherlands
    "Cody Gakpo":        (8, 41),
    "Xavi Simons":       (2, 35),
    "Memphis Depay":     (12, 43),
    "Tijjani Reijnders": (6, 35),
    "Virgil van Dijk":   (4, 38),
    "Davy Klaassen":     (3, 25),
    "Denzel Dumfries":   (4, 32),
    "Nathan Ake":        (2, 30),
    # Belgium
    "Kevin De Bruyne":   (3, 25),
    "Romelu Lukaku":     (1, 5),
    "Leandro Trossard":  (6, 30),
    "Jeremy Doku":       (5, 30),
    "Yannick Carrasco":  (4, 28),
    "Axel Witsel":       (2, 20),
    # Norway
    "Erling Haaland":    (34, 30),
    "Martin Odegaard":   (8, 35),
    "Alexander Sorloth": (15, 30),
    "Joshua King":       (5, 22),
    # Morocco
    "Achraf Hakimi":     (5, 35),
    "Hakim Ziyech":      (4, 25),
    "Youssef En-Nesyri": (14, 30),
    "Sofyan Amrabat":    (1, 28),
    "Azzedine Ounahi":   (3, 28),
    "Noussair Mazraoui": (3, 32),
    # Senegal
    "Sadio Mane":        (10, 29),
    "Ismaila Sarr":      (7, 30),
    "Nicolas Jackson":   (12, 35),
    "Idrissa Gueye":     (2, 28),
    "Kalidou Koulibaly": (2, 30),
    # USA
    "Christian Pulisic": (8, 30),
    "Gio Reyna":         (0, 13),
    "Ricardo Pepi":      (12, 28),
    "Tyler Adams":       (1, 22),
    "Weston McKennie":   (5, 28),
    "Tim Weah":          (4, 25),
    "Sergiño Dest":      (2, 22),
    # Mexico
    "Santiago Gimenez":  (22, 30),
    "Hirving Lozano":    (5, 25),
    "Raul Jimenez":      (10, 28),
    "Orbelín Pineda":    (4, 25),
    "Edson Alvarez":     (2, 32),
    "Hirving Rodrigo Lozano": (5, 25),
    # Colombia
    "Luis Diaz":         (15, 32),
    "James Rodriguez":   (8, 30),
    "Jhon Duran":        (14, 32),
    "Radamel Falcao":    (5, 18),
    "Juan Cuadrado":     (3, 20),
    "Yerry Mina":        (2, 22),
    "Richard Rios":      (4, 28),
    # Ecuador
    "Enner Valencia":    (8, 28),
    "Gonzalo Plata":     (5, 28),
    "Jeremy Sarmiento":  (4, 28),
    "Moises Caicedo":    (3, 35),
    # Uruguay
    "Darwin Nunez":      (2, 10),
    "Federico Valverde": (8, 40),
    "Rodrigo Bentancur": (3, 28),
    "Facundo Pellistri": (5, 25),
    "Edinson Cavani":    (4, 18),
    "Jose Gimenez":      (2, 28),
    "Ronald Araujo":     (2, 25),
    # Japan
    "Takumi Minamino":   (10, 30),
    "Kaoru Mitoma":      (8, 32),
    "Ritsu Doan":        (9, 30),
    "Daichi Kamada":     (5, 28),
    "Hiroki Ito":        (2, 28),
    "Takehiro Tomiyasu": (1, 22),
    # Australia
    "Martin Boyle":      (5, 25),
    "Mitch Duke":        (5, 22),
    "Mat Ryan":          (0, 35),
    "Awer Mabil":        (5, 25),
    # South Korea
    "Heungmin Son":      (18, 32),
    "Lee Kang-in":       (10, 28),
    "Hwang Hee-chan":    (8, 28),
    "Minjae Kim":        (2, 32),
    "Junho Hwang":       (6, 25),
    # Switzerland
    "Granit Xhaka":      (4, 30),
    "Breel Embolo":      (8, 28),
    "Xherdan Shaqiri":   (3, 20),
    "Manuel Akanji":     (2, 32),
    "Yann Sommer":       (0, 32),
    "Ruben Vargas":      (6, 30),
    # Croatia
    "Luka Modric":       (5, 28),
    "Ivan Perisic":      (4, 25),
    "Andrej Kramaric":   (15, 30),
    "Mateo Kovacic":     (5, 35),
    "Bruno Petkovic":    (8, 28),
    "Josip Sutalo":      (2, 22),
    # Austria
    "Marcel Sabitzer":   (8, 30),
    "Marko Arnautovic":  (5, 20),
    "David Alaba":       (1, 8),
    "Florian Grillitsch":(3, 25),
    # Czech Republic / Czechia
    "Patrik Schick":     (12, 25),
    "Tomas Soucek":      (6, 35),
    "Vladimir Coufal":   (2, 32),
    "Alex Kral":         (2, 28),
    "Adam Hlozek":       (8, 30),
    # Scotland
    "Andy Robertson":    (2, 38),
    "Scott McTominay":   (12, 30),
    "Kieran Tierney":    (1, 20),
    "John McGinn":       (5, 30),
    "Stuart Armstrong":  (3, 25),
    # Ivory Coast / Cote d'Ivoire
    "Sebastien Haller":  (8, 22),
    "Nicolas Pepe":      (5, 20),
    "Wilfried Zaha":     (7, 28),
    "Franck Kessie":     (4, 28),
    "Serge Aurier":      (2, 22),
    # Egypt
    "Mohamed Salah":     (22, 38),
    "Mostafa Mohamed":   (12, 28),
    "Omar Marmoush":     (22, 35),
    "Mahmoud Trezeguet": (5, 22),
    # Ghana
    "Jordan Ayew":       (5, 25),
    "Andre Ayew":        (4, 22),
    "Thomas Partey":     (3, 25),
    "Mohammed Kudus":    (10, 32),
    "Antoine Semenyo":   (8, 28),
    # Tunisia
    "Youssef Msakni":    (6, 22),
    "Wahbi Khazri":      (5, 20),
    "Ellyes Skhiri":     (4, 28),
    "Montassar Talbi":   (2, 25),
    # Algeria
    "Riyad Mahrez":      (8, 25),
    "Islam Slimani":     (5, 20),
    "Youcef Atal":       (4, 25),
    "Aissa Mandi":       (1, 28),
    "Houssem Aouar":     (4, 25),
    # Jordan
    "Musa Al-Taamari":   (8, 28),
    "Yazan Al-Naimat":   (5, 22),
    # Iraq
    "Amjed Attwan":      (3, 20),
    "Hussain Ali":       (5, 22),
    # Iran
    "Mehdi Taremi":      (12, 30),
    "Alireza Jahanbakhsh":(5, 25),
    "Ali Gholizadeh":    (4, 25),
    "Sardar Azmoun":     (8, 25),
    # Saudi Arabia
    "Saleh Al-Shehri":   (10, 28),
    "Salem Al-Dawsari":  (8, 28),
    "Mohammed Al-Owais": (0, 30),
    # Qatar
    "Akram Afif":        (12, 28),
    "Hassan Al-Haydos":  (5, 20),
    "Almoez Ali":        (8, 25),
    # Uzbekistan
    "Eldor Shomurodov":  (8, 25),
    "Abbosbek Fayzullayev":(6, 28),
    "Otabek Shukurov":   (3, 22),
    # New Zealand
    "Chris Wood":        (8, 28),
    "Clayton Lewis":     (3, 25),
    "Liberato Cacace":   (3, 28),
    # Canada
    "Alphonso Davies":   (5, 32),
    "Jonathan David":    (26, 30),
    "Cyle Larin":        (8, 25),
    "Atiba Hutchinson":  (1, 15),
    "Stephen Eustaquio": (4, 30),
    # Panama
    "Rolando Blackburn": (5, 22),
    "Cecilio Waterman":  (6, 22),
    "Alberto Quintero":  (3, 20),
    # Haiti
    "Frantzdy Pierrot":  (6, 22),
    "Derrick Etienne":   (4, 20),
    "Steeven Saba":      (3, 18),
    # Cape Verde
    "Bryan Teixeira":    (5, 22),
    "Ryan Mendes":       (4, 20),
    "Garry Rodrigues":   (5, 22),
    # Bosnia Herzegovina
    "Edin Dzeko":        (8, 25),
    "Miralem Pjanic":    (2, 15),
    "Ermedin Demirovic": (12, 28),
    "Sead Kolasinac":    (1, 22),
    "Edin Visca":        (4, 22),
    # DRC Congo
    "Cedric Bakambu":    (5, 22),
    "Yannick Bolasie":   (3, 20),
    "Chancel Mbemba":    (2, 25),
    "Britt Assombalonga":(6, 22),
    # Paraguay
    "Miguel Almiron":    (5, 25),
    "Carlos Gonzalez":   (8, 25),
    "Robert Morales":    (4, 22),
    "Gustavo Gomez":     (3, 28),
    # Curacao
    "Leandro Bacuna":    (3, 22),
    "Jurien Gaari":      (3, 20),
    "Elson Hooi":        (4, 20),
    # Sweden
    "Viktor Gyokeres":   (39, 38),
    "Alexander Isak":    (23, 32),
    "Dejan Kulusevski":  (7, 30),
    "Emil Forsberg":     (5, 25),
    "Victor Lindelof":   (2, 28),
    "Sebastian Larsson": (2, 22),
    "Kristoffer Olsson": (3, 25),
    # Turkey
    "Arda Guler":        (10, 28),
    "Hakan Calhanoglu":  (8, 32),
    "Kenan Yildiz":      (8, 28),
    "Zeki Celik":        (2, 30),
    "Merih Demiral":     (3, 30),
    "Cengiz Under":      (5, 25),
    "Yusuf Yazici":      (7, 28),
    # South Africa
    "Percy Tau":         (5, 22),
    "Themba Zwane":      (6, 22),
    "Lyle Foster":       (8, 25),
    "Ronwen Williams":   (0, 30),
}

def update_player_stats(html, name_key, goals, matches):
    """Update goals and matches for a specific player."""
    # Each player is on one line: {name:"...", pos:"...", club:"...", starter:..., goals:0, matches:0}
    # We match the full line to avoid partial name matches
    pattern = r'(name:"[^"]*' + re.escape(name_key) + r'[^"]*"[^,]*, pos:"[^"]*", club:"[^"]*", starter:[^,]*, )goals:\d+(, matches:)\d+'
    replacement = r'\g<1>goals:' + str(goals) + r'\g<2>' + str(matches)
    return re.sub(pattern, replacement, html)

count = 0
for name_key, (goals, matches) in STATS.items():
    new_html = update_player_stats(html, name_key, goals, matches)
    if new_html != html:
        count += 1
        html = new_html
    # Don't update html if no change (avoids false positives)

print(f"Updated {count} / {len(STATS)} players")

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

dest = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\recette_facturx_app\app\world_cup_2026.html'
shutil.copy(path, dest)
print('Done')
