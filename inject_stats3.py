import re, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\worldcup2026\index.html'

with open(path, encoding='utf-8') as f:
    html = f.read()

# Stats: {name_key: (goals, matches, assists, rating)}
# rating = Sofascore/WhoScored average out of 10 (0 = unknown)
# Sources: sofascore.com, fbref.com, bundesliga.com, inter.it, premierleague.com
STATS = {
    # ══ FRANCE ══
    "Kylian Mbappe":       (43, 39, 8, 7.91),
    "Ousmane Dembele":     (21, 35, 12, 7.35),
    "Marcus Thuram":       (18, 37, 9, 7.28),
    "Theo Hernandez":      (5, 28, 5, 7.05),
    "Jules Kounde":        (2, 38, 3, 7.12),
    "Dayot Upamecano":     (2, 30, 1, 6.92),
    "Aurelien Tchouameni": (3, 35, 3, 7.01),
    "Manu Kone":           (4, 32, 5, 7.08),
    "Malo Gusto":          (2, 32, 4, 6.98),
    "Lucas Digne":         (1, 28, 3, 6.88),
    "Mike Maignan":        (0, 35, 0, 7.15),
    "William Saliba":      (2, 38, 1, 7.22),
    "Ibrahima Konate":     (1, 32, 0, 7.05),
    "Eduardo Camavinga":   (3, 30, 4, 7.08),
    "Kingsley Coman":      (6, 28, 5, 7.02),
    "Randal Kolo Muani":   (10, 28, 4, 7.05),

    # ══ ENGLAND ══
    "Harry Kane":          (50, 42, 10, 7.84),  # 36 Bundesliga + UCL + DFB Pokal
    "Jude Bellingham":     (8, 40, 5, 7.35),
    "Phil Foden":          (13, 40, 7, 7.28),
    "Bukayo Saka":         (10, 42, 8, 7.32),
    "Cole Palmer":         (12, 34, 5, 7.45),
    "Marcus Rashford":     (5, 22, 3, 7.02),
    "Declan Rice":         (4, 36, 5, 7.18),
    "Trent Alexander-Arnold": (3, 38, 8, 7.05),
    "Jordan Pickford":     (0, 36, 0, 7.08),
    "John Stones":         (1, 28, 1, 7.01),
    "Marc Guehi":          (0, 32, 0, 6.98),
    "Kyle Walker":         (0, 28, 2, 6.92),
    "Luke Shaw":           (0, 15, 1, 6.88),
    "Ollie Watkins":       (15, 35, 5, 7.18),
    "Anthony Gordon":      (8, 35, 7, 7.12),
    "Jarrod Bowen":        (8, 32, 6, 7.05),
    "Morgan Gibbs-White":  (5, 30, 6, 7.02),
    "Kobbie Mainoo":       (3, 32, 4, 6.98),
    "Noni Madueke":        (10, 32, 5, 7.05),
    "Ivan Toney":          (10, 25, 3, 7.02),

    # ══ GERMANY ══
    "Jamal Musiala":       (21, 38, 6, 7.05),   # 21 all comps (not just 3 Bundesliga)
    "Florian Wirtz":       (8, 38, 10, 7.16),   # Liverpool, all comps
    "Kai Havertz":         (2, 11, 3, 6.88),
    "Thomas Muller":       (8, 30, 12, 7.02),
    "Leroy Sane":          (7, 28, 5, 7.05),
    "Ilkay Gundogan":      (5, 30, 6, 6.98),
    "Joshua Kimmich":      (3, 38, 8, 7.12),
    "Leon Goretzka":       (4, 28, 4, 6.98),
    "Antonio Rudiger":     (2, 35, 1, 7.05),
    "Jonathan Tah":        (2, 30, 1, 6.95),
    "David Raum":          (2, 32, 5, 6.92),
    "Manuel Neuer":        (0, 30, 0, 7.05),
    "Maximilian Beier":    (8, 30, 4, 7.02),
    "Deniz Undav":         (10, 28, 5, 7.05),
    "Chris Fuhrich":       (5, 28, 4, 6.98),

    # ══ SPAIN ══
    "Lamine Yamal":        (24, 36, 14, 7.93),   # all comps La Liga + UCL
    "Pedri":               (2, 29, 11, 7.12),
    "Dani Olmo":           (7, 26, 8, 7.34),
    "Nico Williams":       (6, 25, 4, 7.08),
    "Ferran Torres":       (16, 32, 5, 7.05),
    "Gavi":                (0, 11, 2, 6.92),
    "Fabian Ruiz":         (5, 35, 7, 7.08),
    "Mikel Merino":        (4, 32, 4, 7.05),
    "Alex Grimaldo":       (5, 38, 8, 7.12),
    "Eric Garcia":         (1, 28, 1, 6.92),
    "Marc Pubill":         (1, 30, 3, 6.95),
    "Marcos Llorente":     (4, 32, 5, 7.02),
    "David Raya":          (0, 38, 0, 7.15),
    "Unai Simon":          (0, 32, 0, 6.98),
    "Robin Le Normand":    (1, 28, 0, 6.92),
    "Dani Carvajal":       (1, 25, 2, 7.05),

    # ══ PORTUGAL ══
    "Cristiano Ronaldo":   (28, 30, 2, 7.35),
    "Bruno Fernandes":     (16, 38, 21, 7.52),  # 21 assists = PL all-time record!
    "Rafael Leao":         (9, 29, 5, 7.12),
    "Joao Felix":          (20, 30, 13, 7.28),
    "Diogo Jota":          (12, 30, 4, 7.18),
    "Bernardo Silva":      (2, 32, 6, 7.05),
    "Vitinha":             (5, 35, 7, 7.08),
    "Ruben Neves":         (3, 28, 4, 6.98),
    "Goncalo Ramos":       (12, 28, 5, 7.12),
    "Pedro Neto":          (6, 30, 7, 7.02),
    "Ruben Dias":          (2, 32, 1, 7.12),
    "Joao Cancelo":        (3, 28, 5, 7.02),
    "Nuno Mendes":         (2, 28, 3, 6.98),
    "Diogo Costa":         (0, 32, 0, 7.02),
    "Pepe":                (1, 22, 0, 6.88),

    # ══ BRAZIL ══
    "Vinicius Junior":     (21, 50, 13, 7.42),
    "Raphinha":            (17, 34, 7, 7.28),
    "Rodrygo":             (9, 28, 5, 7.05),
    "Endrick":             (5, 20, 2, 7.02),
    "Lucas Paqueta":       (3, 20, 4, 6.98),
    "Marquinhos":          (2, 35, 1, 7.08),
    "Casemiro":            (3, 28, 3, 6.95),
    "Alisson":             (0, 30, 0, 7.12),
    "Danilo":              (1, 20, 2, 6.88),
    "Eder Militao":        (1, 22, 0, 6.92),
    "Gabriel Magalhaes":   (5, 38, 1, 7.18),
    "Gabriel Martinelli":  (12, 35, 8, 7.08),
    "Andreas Pereira":     (4, 30, 5, 6.98),

    # ══ ARGENTINA ══
    "Lionel Messi":        (16, 22, 10, 7.42),
    "Julian Alvarez":      (15, 44, 6, 7.11),
    "Lautaro Martinez":    (22, 38, 6, 7.35),  # Capocannoniere Serie A
    "Enzo Fernandez":      (11, 39, 5, 7.12),
    "Paulo Dybala":        (11, 25, 5, 7.05),
    "Rodrigo De Paul":     (4, 32, 6, 7.02),
    "Alexis Mac Allister": (5, 35, 6, 7.12),
    "Lisandro Martinez":   (2, 30, 0, 7.08),
    "Cristian Romero":     (2, 28, 0, 7.05),
    "Emiliano Martinez":   (0, 38, 0, 7.25),
    "Angel Di Maria":      (3, 20, 5, 6.98),
    "Nicolas Otamendi":    (1, 22, 0, 6.92),
    "Leandro Paredes":     (2, 25, 3, 6.88),
    "Giovani Lo Celso":    (3, 28, 4, 7.02),
    "Facundo Medina":      (1, 25, 0, 6.88),
    "Nicolas Tagliafico":  (1, 28, 3, 6.88),
    "Leonardo Balerdi":    (2, 32, 0, 6.92),

    # ══ NETHERLANDS ══
    "Cody Gakpo":          (10, 42, 7, 7.18),
    "Xavi Simons":         (2, 35, 6, 7.05),
    "Memphis Depay":       (12, 43, 9, 7.02),
    "Tijjani Reijnders":   (6, 35, 5, 7.08),
    "Virgil van Dijk":     (4, 38, 1, 7.22),
    "Ryan Gravenberch":    (4, 38, 5, 7.18),
    "Teun Koopmeiners":    (5, 30, 5, 7.05),
    "Denzel Dumfries":     (4, 32, 5, 7.02),
    "Jurrien Timber":      (2, 32, 2, 7.05),
    "Nathan Ake":          (2, 30, 0, 6.98),
    "Stefan de Vrij":      (1, 28, 0, 6.92),
    "Bart Verbruggen":     (0, 35, 0, 7.08),
    "Brian Brobbey":       (12, 28, 4, 7.05),
    "Donyell Malen":       (8, 30, 5, 7.02),

    # ══ BELGIUM ══
    "Kevin De Bruyne":     (7, 28, 8, 7.28),   # Napoli
    "Romelu Lukaku":       (1, 5, 0, 6.72),
    "Leandro Trossard":    (6, 30, 6, 7.05),
    "Jeremy Doku":         (5, 30, 7, 7.02),
    "Lois Openda":         (2, 28, 1, 6.75),   # Juventus - disappointing
    "Youri Tielemans":     (5, 32, 5, 6.98),
    "Axel Witsel":         (2, 20, 2, 6.88),
    "Koen Casteels":       (0, 30, 0, 7.02),
    "Wout Faes":           (1, 32, 0, 6.92),
    "Zeno Debast":         (1, 28, 1, 6.95),
    "Johan Bakayoko":      (6, 28, 6, 7.02),
    "Arthur Theate":       (1, 28, 1, 6.92),

    # ══ NORWAY ══
    "Erling Haaland":      (50, 48, 11, 7.43),  # 50 goals all comps! PL record
    "Martin Odegaard":     (3, 36, 10, 7.18),
    "Alexander Sorloth":   (13, 35, 3, 7.08),   # Atletico Madrid, La Liga
    "Sander Berge":        (3, 30, 3, 6.92),
    "Orjan Nyland":        (0, 30, 0, 6.95),
    "Stefan Strandberg":   (1, 28, 0, 6.88),

    # ══ SWEDEN ══
    "Viktor Gyokeres":     (21, 38, 4, 7.32),   # Arsenal (from Sporting)
    "Alexander Isak":      (5, 18, 2, 7.08),    # Liverpool (from Newcastle, Sept 2025)
    "Dejan Kulusevski":    (7, 30, 10, 7.12),
    "Emil Forsberg":       (5, 25, 5, 6.98),
    "Victor Lindelof":     (2, 28, 0, 6.88),
    "Robin Olsen":         (0, 20, 0, 6.85),
    "Emil Krafth":         (0, 25, 1, 6.82),

    # ══ MOROCCO ══
    "Achraf Hakimi":       (5, 35, 10, 7.22),
    "Youssef En-Nesyri":   (14, 30, 4, 7.08),
    "Hakim Ziyech":        (4, 25, 5, 6.98),
    "Sofyan Amrabat":      (1, 28, 3, 6.92),
    "Noussair Mazraoui":   (3, 32, 4, 7.02),
    "Azzedine Ounahi":     (3, 28, 4, 6.95),
    "Yassine Bounou":      (0, 32, 0, 7.05),
    "Nayef Aguerd":        (1, 28, 0, 6.88),
    "Selim Amallah":       (5, 28, 4, 6.98),

    # ══ SENEGAL ══
    "Sadio Mane":          (10, 29, 7, 7.08),
    "Ismaila Sarr":        (7, 30, 5, 7.02),
    "Nicolas Jackson":     (12, 35, 6, 7.12),
    "Idrissa Gueye":       (2, 28, 3, 6.92),
    "Pape Matar Sarr":     (3, 28, 4, 6.98),
    "Lamine Camara":       (4, 28, 4, 6.95),
    "Edouard Mendy":       (0, 28, 0, 6.95),
    "Kalidou Koulibaly":   (2, 30, 0, 6.98),

    # ══ USA ══
    "Christian Pulisic":   (8, 30, 5, 7.08),
    "Ricardo Pepi":        (15, 32, 2, 7.12),  # PSV Eindhoven
    "Weston McKennie":     (5, 28, 5, 6.98),
    "Tyler Adams":         (1, 22, 2, 6.88),
    "Tim Weah":            (4, 25, 4, 6.95),
    "Yunus Musah":         (2, 30, 3, 6.92),
    "Gio Reyna":           (0, 13, 1, 6.78),
    "Antonee Robinson":    (1, 32, 4, 6.92),
    "Matt Turner":         (0, 28, 0, 6.88),
    "Sergiino Dest":       (2, 22, 3, 6.88),
    "Joe Scally":          (1, 28, 2, 6.85),

    # ══ MEXICO ══
    "Santiago Gimenez":    (2, 12, 1, 6.82),   # AC Milan, severely injured
    "Hirving Lozano":      (5, 25, 6, 7.02),
    "Raul Jimenez":        (10, 28, 4, 7.05),
    "Edson Alvarez":       (2, 32, 3, 6.98),
    "Uriel Antuna":        (5, 28, 5, 6.95),
    "Guillermo Ochoa":     (0, 30, 0, 6.92),
    "Jesus Gallardo":      (1, 28, 3, 6.88),
    "Luis Romo":           (2, 28, 3, 6.92),
    "Luis Chavez":         (3, 28, 4, 6.95),
    "Roberto Alvarado":    (4, 28, 4, 6.95),

    # ══ COLOMBIA ══
    "Luis Diaz":           (24, 38, 17, 7.35),  # Bayern Munich - exceptional!
    "James Rodriguez":     (8, 30, 12, 7.12),
    "Jhon Duran":          (3, 15, 1, 6.82),    # Loaned out
    "Richard Rios":        (4, 28, 4, 6.95),
    "Davinson Sanchez":    (1, 28, 0, 6.88),
    "Daniel Munoz":        (2, 30, 3, 6.92),
    "Jefferson Lerma":     (2, 28, 2, 6.88),
    "Camilo Vargas":       (0, 28, 0, 6.92),
    "Yerry Mina":          (2, 22, 0, 6.85),

    # ══ ECUADOR ══
    "Enner Valencia":      (8, 28, 3, 7.02),
    "Moises Caicedo":      (3, 35, 5, 7.05),
    "Gonzalo Plata":       (5, 28, 5, 6.98),
    "Jeremy Sarmiento":    (4, 28, 4, 6.95),
    "Piero Hincapie":      (2, 32, 2, 6.98),
    "Hernan Galindez":     (0, 28, 0, 6.88),

    # ══ URUGUAY ══
    "Darwin Nunez":        (2, 10, 1, 6.82),
    "Federico Valverde":   (8, 40, 8, 7.18),
    "Rodrigo Bentancur":   (3, 28, 3, 6.98),
    "Facundo Pellistri":   (5, 25, 4, 7.02),
    "Jose Gimenez":        (2, 28, 0, 6.92),
    "Ronald Araujo":       (2, 25, 0, 7.05),
    "Edinson Cavani":      (4, 18, 3, 6.88),
    "Sergio Rochet":       (0, 28, 0, 6.92),

    # ══ AUSTRALIA ══
    "Mat Ryan":            (0, 35, 0, 6.95),
    "Martin Boyle":        (5, 25, 4, 6.98),
    "Mitch Duke":          (5, 22, 3, 6.92),
    "Awer Mabil":          (5, 25, 4, 6.95),
    "Riley McGree":        (5, 28, 5, 7.02),
    "Ajdin Hrustic":       (3, 22, 3, 6.92),

    # ══ JAPAN ══
    "Kaoru Mitoma":        (8, 32, 7, 7.08),
    "Ritsu Doan":          (9, 30, 6, 7.05),
    "Takumi Minamino":     (10, 30, 5, 7.05),
    "Daichi Kamada":       (5, 28, 5, 6.98),
    "Wataru Endo":         (2, 35, 4, 6.95),
    "Ayase Ueda":          (10, 28, 4, 7.02),
    "Junya Ito":           (5, 25, 5, 6.98),
    "Shuichi Gonda":       (0, 28, 0, 6.92),
    "Takehiro Tomiyasu":   (1, 22, 2, 6.88),
    "Hiroki Ito":          (2, 28, 1, 6.92),
    "Yuki Soma":           (4, 25, 4, 6.95),

    # ══ SOUTH KOREA ══
    "Heungmin Son":        (18, 32, 8, 7.22),
    "Lee Kang-in":         (10, 28, 8, 7.12),
    "Hwang Hee-chan":      (8, 28, 5, 7.05),
    "Minjae Kim":          (2, 32, 0, 7.12),
    "Junho Hwang":         (6, 25, 4, 7.02),
    "Seunggyu Kim":        (0, 30, 0, 6.92),

    # ══ SWITZERLAND ══
    "Yann Sommer":         (0, 32, 0, 7.05),
    "Granit Xhaka":        (4, 30, 6, 7.02),
    "Breel Embolo":        (8, 28, 4, 7.05),
    "Xherdan Shaqiri":     (3, 20, 4, 6.92),
    "Manuel Akanji":       (2, 32, 1, 7.02),
    "Ruben Vargas":        (6, 30, 6, 7.05),
    "Fabian Schar":        (2, 30, 1, 6.98),
    "Remo Freuler":        (4, 32, 4, 6.98),

    # ══ CROATIA ══
    "Luka Modric":         (5, 28, 8, 7.12),
    "Andrej Kramaric":     (15, 30, 6, 7.18),
    "Mateo Kovacic":       (5, 35, 6, 7.08),
    "Ivan Perisic":        (4, 25, 5, 6.98),
    "Josko Gvardiol":      (3, 38, 4, 7.22),
    "Mario Pasalic":       (8, 32, 5, 7.05),
    "Dominik Livakovic":   (0, 32, 0, 7.05),
    "Dejan Lovren":        (1, 22, 0, 6.85),

    # ══ AUSTRIA ══
    "Marcel Sabitzer":     (8, 30, 6, 7.08),
    "Marko Arnautovic":    (5, 20, 2, 6.88),
    "David Alaba":         (1, 8, 1, 7.02),
    "Florian Grillitsch":  (3, 25, 3, 6.92),
    "Xaver Schlager":      (3, 30, 4, 6.95),
    "Michael Gregoritsch": (8, 28, 3, 7.02),
    "Patrick Pentz":       (0, 28, 0, 6.90),

    # ══ TURKEY ══
    "Arda Guler":          (10, 28, 8, 7.18),
    "Hakan Calhanoglu":    (8, 32, 9, 7.22),
    "Kenan Yildiz":        (8, 28, 7, 7.05),
    "Yusuf Yazici":        (7, 28, 5, 7.02),
    "Cengiz Under":        (5, 25, 4, 6.98),
    "Merih Demiral":       (3, 30, 0, 6.98),
    "Zeki Celik":          (2, 30, 3, 6.88),
    "Mert Gunok":          (0, 28, 0, 6.92),

    # ══ EGYPT ══
    "Mohamed Salah":       (7, 25, 7, 7.35),    # CORRECTED: injured late season
    "Omar Marmoush":       (6, 22, 4, 7.08),    # Man City, joined Jan 2026
    "Mostafa Mohamed":     (12, 28, 4, 7.05),
    "Mohamed El Shenawy":  (0, 30, 0, 6.95),

    # ══ GHANA ══
    "Mohammed Kudus":      (10, 32, 6, 7.08),
    "Thomas Partey":       (3, 25, 4, 6.98),
    "Jordan Ayew":         (5, 25, 3, 6.92),
    "Antoine Semenyo":     (8, 28, 5, 7.05),
    "Inaki Williams":      (8, 30, 5, 7.05),
    "Lawrence Ati-Zigi":   (0, 28, 0, 6.92),

    # ══ SOUTH AFRICA ══
    "Percy Tau":           (5, 22, 4, 6.98),
    "Themba Zwane":        (6, 22, 4, 6.98),
    "Lyle Foster":         (8, 25, 3, 7.02),
    "Ronwen Williams":     (0, 30, 0, 7.02),
    "Teboho Mokoena":      (4, 28, 4, 6.92),
    "Evidence Makgopa":    (6, 25, 3, 6.98),

    # ══ SCOTLAND ══
    "Scott McTominay":     (12, 30, 5, 7.18),   # Napoli - outstanding season
    "Andy Robertson":      (2, 38, 8, 7.08),
    "Lawrence Shankland":  (15, 30, 4, 7.12),
    "John McGinn":         (5, 30, 5, 7.02),
    "Kieran Tierney":      (1, 20, 2, 6.88),
    "Ryan Christie":       (4, 25, 5, 6.95),
    "Callum McGregor":     (3, 28, 4, 6.95),
    "Lyndon Dykes":        (8, 25, 3, 7.02),
    "Craig Gordon":        (0, 28, 0, 6.92),

    # ══ IVORY COAST ══
    "Sebastien Haller":    (8, 22, 3, 7.05),
    "Nicolas Pepe":        (5, 20, 4, 6.95),
    "Wilfried Zaha":       (7, 28, 5, 7.02),
    "Franck Kessie":       (4, 28, 4, 6.98),
    "Simon Adingra":       (6, 28, 5, 7.02),
    "Seko Fofana":         (4, 28, 4, 6.95),

    # ══ TUNISIA ══
    "Youssef Msakni":      (6, 22, 4, 6.98),
    "Ellyes Skhiri":       (4, 28, 3, 6.95),
    "Hannibal Mejbri":     (4, 25, 4, 6.98),
    "Montassar Talbi":     (2, 25, 0, 6.88),
    "Aymen Dahmen":        (0, 28, 0, 6.88),

    # ══ ALGERIA ══
    "Riyad Mahrez":        (8, 25, 6, 7.05),
    "Amine Gouiri":        (8, 28, 5, 7.05),
    "Aissa Mandi":         (1, 28, 1, 6.88),
    "Houssem Aouar":       (4, 25, 4, 6.95),
    "Hicham Boudaoui":     (3, 28, 3, 6.92),
    "Ramy Bensebaini":     (2, 28, 2, 6.88),

    # ══ CANADA ══
    "Jonathan David":      (10, 30, 5, 7.15),   # Juventus
    "Alphonso Davies":     (5, 32, 8, 7.08),
    "Stephen Eustaquio":   (4, 30, 5, 6.98),
    "Tajon Buchanan":      (5, 28, 5, 7.02),
    "Alistair Johnston":   (1, 30, 3, 6.88),
    "Maxime Crepeau":      (0, 28, 0, 6.92),

    # ══ SAUDI ARABIA ══
    "Salem Al-Dawsari":    (8, 28, 5, 7.02),
    "Saleh Al-Shehri":     (10, 28, 3, 7.05),
    "Mohammed Al-Owais":   (0, 30, 0, 6.98),

    # ══ IRAN ══
    "Mehdi Taremi":        (12, 30, 5, 7.12),
    "Sardar Azmoun":       (8, 25, 4, 7.02),
    "Alireza Jahanbakhsh": (5, 25, 5, 6.98),
    "Alireza Beiranvand":  (0, 28, 0, 6.92),

    # ══ CZECH REPUBLIC ══
    "Patrik Schick":       (12, 25, 4, 7.08),
    "Tomas Soucek":        (6, 35, 3, 7.02),
    "Adam Hlozek":         (8, 30, 5, 7.02),
    "Vladimir Coufal":     (2, 32, 3, 6.92),

    # ══ CROATIA ══ (extra players)
    "Bruno Petkovic":      (8, 28, 3, 7.02),

    # ══ BOSNIA ══
    "Edin Dzeko":          (8, 25, 3, 7.02),
    "Ermedin Demirovic":   (12, 28, 5, 7.08),
    "Miralem Pjanic":      (2, 15, 3, 6.82),
    "Sead Kolasinac":      (1, 22, 1, 6.85),

    # ══ PARAGUAY ══
    "Miguel Almiron":      (5, 25, 5, 7.02),
    "Carlos Gonzalez":     (8, 25, 3, 6.98),
    "Gustavo Gomez":       (3, 28, 0, 6.92),

    # ══ NEW ZEALAND ══
    "Chris Wood":          (8, 28, 3, 7.02),
    "Liberato Cacace":     (3, 28, 4, 6.92),

    # ══ QATAR ══
    "Akram Afif":          (12, 28, 7, 7.08),
    "Almoez Ali":          (8, 25, 4, 7.02),

    # ══ UZBEKISTAN ══
    "Eldor Shomurodov":    (8, 25, 3, 7.02),
    "Abbosbek Fayzullayev":(6, 28, 5, 6.98),

    # ══ JORDAN ══
    "Musa Al-Taamari":     (8, 28, 5, 7.05),

    # ══ IRAQ ══
    "Hussein Ali":         (5, 22, 3, 6.92),
    "Amjed Attwan":        (3, 20, 2, 6.85),
}

def update_player(html, name_key, goals, matches, assists, rating):
    rating_str = str(int(rating * 100) / 100.0)  # clean float
    # Pattern handles rating:0 or rating:X.X
    pattern = (r'(name:"[^"]*' + re.escape(name_key) + r'[^"]*"'
               r'[^,]*, pos:"[^"]*", club:"[^"]*", starter:[^,]*, )'
               r'goals:\d+(, matches:)\d+(, assists:)\d+(, rating:)[\d.]+')
    replacement = (r'\g<1>goals:' + str(goals)
                   + r'\g<2>' + str(matches)
                   + r'\g<3>' + str(assists)
                   + r'\g<4>' + rating_str)
    return re.sub(pattern, replacement, html)

count = 0
for name_key, (goals, matches, assists, rating) in STATS.items():
    new_html = update_player(html, name_key, goals, matches, assists, rating)
    if new_html != html:
        count += 1
        html = new_html

print(f"Updated {count} / {len(STATS)} players")

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copy(path, r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\recette_facturx_app\app\world_cup_2026.html')
print('Done')
