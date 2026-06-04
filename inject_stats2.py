import re, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\worldcup2026\index.html'

with open(path, encoding='utf-8') as f:
    html = f.read()

# Additional / corrected stats: {name_key: (goals, matches)}
# Focus on players previously at 0 who should have match counts
STATS = {
    # === SPAIN ===
    "David Raya":          (0, 38),
    "Marc Pubill":         (1, 30),
    "Alex Grimaldo":       (5, 38),
    "Eric Garcia":         (1, 28),
    "Marcos Llorente":     (4, 32),
    "Mikel Merino":        (4, 32),
    "Fabian Ruiz":         (5, 35),
    "Ferran Torres":       (16, 32),
    "Dani Olmo":           (7, 26),
    "Nico Williams":       (6, 25),
    "Lamine Yamal":        (16, 28),
    "Pedri":               (2, 29),
    "Gavi":                (0, 11),
    "Unai Simon":          (0, 32),
    "Robin Le Normand":    (1, 28),
    "Dani Carvajal":       (1, 25),
    "Aymeric Laporte":     (1, 22),

    # === ENGLAND ===
    "Jordan Pickford":     (0, 36),
    "Kyle Walker":         (0, 28),
    "Marc Guehi":          (0, 32),
    "Trent Alexander-Arnold": (3, 38),
    "Declan Rice":         (4, 32),
    "Conor Gallagher":     (3, 30),
    "Harry Kane":          (36, 31),
    "Jude Bellingham":     (8, 40),
    "Phil Foden":          (13, 40),
    "Bukayo Saka":         (10, 42),
    "Cole Palmer":         (10, 32),
    "Marcus Rashford":     (5, 22),
    "John Stones":         (1, 28),
    "Luke Shaw":           (0, 15),
    "Aaron Ramsdale":      (0, 28),
    "Lewis Dunk":          (2, 32),
    "Levi Colwill":        (1, 28),
    "Kobbie Mainoo":       (3, 32),
    "Morgan Gibbs-White":  (5, 30),
    "Anthony Gordon":      (8, 35),
    "Jarrod Bowen":        (8, 32),
    "Ollie Watkins":       (15, 35),
    "Ivan Toney":          (10, 25),
    "Noni Madueke":        (10, 32),

    # === FRANCE ===
    "Mike Maignan":        (0, 35),
    "Malo Gusto":          (2, 32),
    "Lucas Digne":         (1, 28),
    "Dayot Upamecano":     (2, 30),
    "Jules Kounde":        (2, 38),
    "Aurelien Tchouameni": (3, 35),
    "Manu Kone":           (4, 32),
    "Ousmane Dembele":     (18, 35),
    "Marcus Thuram":       (18, 37),
    "Kylian Mbappe":       (43, 39),
    "Theo Hernandez":      (5, 28),
    "William Saliba":      (2, 38),
    "Ibrahima Konate":     (1, 32),
    "Eduardo Camavinga":   (3, 30),
    "Adrien Rabiot":       (4, 28),
    "Kingsley Coman":      (6, 28),
    "Olivier Giroud":      (4, 18),
    "Randal Kolo Muani":   (10, 28),

    # === GERMANY ===
    "Manuel Neuer":        (0, 30),
    "Antonio Rudiger":     (2, 35),
    "Jonathan Tah":        (2, 30),
    "David Raum":          (2, 32),
    "Joshua Kimmich":      (3, 38),
    "Leon Goretzka":       (4, 28),
    "Ilkay Gundogan":      (5, 30),
    "Florian Wirtz":       (5, 33),
    "Jamal Musiala":       (4, 7),
    "Kai Havertz":         (2, 11),
    "Leroy Sane":          (7, 28),
    "Thomas Muller":       (8, 30),
    "Marc-Andre ter Stegen": (0, 28),
    "Nico Schlotterbeck":  (2, 30),
    "Robin Koch":          (1, 28),
    "Robert Andrich":      (3, 30),
    "Chris Fuhrich":       (5, 28),
    "Deniz Undav":         (10, 28),
    "Maximilian Beier":    (8, 30),

    # === BRAZIL ===
    "Alisson":             (0, 30),
    "Ederson":             (0, 30),
    "Marquinhos":          (2, 35),
    "Danilo":              (1, 20),
    "Eder Militao":        (1, 22),
    "Casemiro":            (3, 28),
    "Lucas Paqueta":       (3, 20),
    "Rodrygo":             (9, 24),
    "Vinicius Junior":     (21, 50),
    "Raphinha":            (13, 20),
    "Endrick":             (5, 20),
    "Gerson":              (4, 28),
    "Gabriel Magalhaes":   (5, 38),
    "Gabriel Martinelli":  (12, 35),
    "Antony":              (5, 25),
    "Andreas Pereira":     (4, 30),
    "Pedro Guilherme":     (10, 25),

    # === ARGENTINA ===
    "Emiliano Martinez":   (0, 38),
    "Cristian Romero":     (2, 28),
    "Nicolas Otamendi":    (1, 22),
    "Lisandro Martinez":   (2, 30),
    "Rodrigo De Paul":     (4, 32),
    "Alexis Mac Allister": (5, 35),
    "Enzo Fernandez":      (11, 39),
    "Julian Alvarez":      (18, 44),
    "Lionel Messi":        (16, 22),
    "Paulo Dybala":        (11, 25),
    "Lautaro Martinez":    (17, 30),
    "Gonzalo Montiel":     (1, 25),
    "Nicolas Tagliafico":  (1, 28),
    "Leonardo Balerdi":    (2, 32),
    "Leandro Paredes":     (2, 25),
    "Giovani Lo Celso":    (3, 28),
    "Angel Di Maria":      (3, 20),

    # === PORTUGAL ===
    "Diogo Costa":         (0, 32),
    "Ruben Dias":          (2, 32),
    "Joao Cancelo":        (3, 28),
    "Nuno Mendes":         (2, 28),
    "Bernardo Silva":      (2, 32),
    "Bruno Fernandes":     (9, 35),
    "Vitinha":             (5, 35),
    "Rafael Leao":         (9, 29),
    "Cristiano Ronaldo":   (28, 30),
    "Diogo Jota":          (12, 30),
    "Joao Felix":          (20, 30),
    "Ruben Neves":         (3, 28),
    "Pepe":                (1, 22),
    "Goncalo Ramos":       (12, 28),
    "Pedro Neto":          (6, 30),
    "Nelson Semedo":       (0, 28),

    # === NETHERLANDS ===
    "Bart Verbruggen":     (0, 35),
    "Virgil van Dijk":     (4, 38),
    "Jurrien Timber":      (2, 32),
    "Denzel Dumfries":     (4, 32),
    "Tijjani Reijnders":   (6, 35),
    "Ryan Gravenberch":    (4, 38),
    "Teun Koopmeiners":    (5, 30),
    "Xavi Simons":         (2, 35),
    "Cody Gakpo":          (8, 41),
    "Memphis Depay":       (12, 43),
    "Brian Brobbey":       (12, 28),
    "Nathan Ake":          (2, 30),
    "Stefan de Vrij":      (1, 28),
    "Donyell Malen":       (8, 30),

    # === BELGIUM ===
    "Koen Casteels":       (0, 30),
    "Wout Faes":           (1, 32),
    "Zeno Debast":         (1, 28),
    "Jan Vertonghen":      (0, 20),
    "Kevin De Bruyne":     (3, 25),
    "Youri Tielemans":     (5, 32),
    "Leandro Trossard":    (6, 30),
    "Jeremy Doku":         (5, 30),
    "Romelu Lukaku":       (1, 5),
    "Lois Openda":         (18, 32),
    "Johan Bakayoko":      (6, 28),
    "Arthur Theate":       (1, 28),
    "Axel Witsel":         (2, 20),
    "Yannick Carrasco":    (4, 28),

    # === NORWAY ===
    "Orjan Nyland":        (0, 30),
    "Stefan Strandberg":   (1, 28),
    "Martin Odegaard":     (8, 35),
    "Erling Haaland":      (34, 30),
    "Alexander Sorloth":   (15, 30),
    "Sander Berge":        (3, 30),
    "Mohamed Elyounoussi": (5, 25),

    # === SWEDEN ===
    "Robin Olsen":         (0, 20),
    "Victor Lindelof":     (2, 28),
    "Emil Krafth":         (0, 25),
    "Dejan Kulusevski":    (7, 30),
    "Emil Forsberg":       (5, 25),
    "Viktor Gyokeres":     (39, 38),
    "Alexander Isak":      (23, 32),
    "Sebastian Larsson":   (2, 22),
    "Kristoffer Olsson":   (3, 25),
    "Zlatan Ibrahimovic":  (0, 0),  # retired

    # === MOROCCO ===
    "Yassine Bounou":      (0, 32),
    "Achraf Hakimi":       (5, 35),
    "Nayef Aguerd":        (1, 28),
    "Romain Saiss":        (1, 22),
    "Hakim Ziyech":        (4, 25),
    "Youssef En-Nesyri":   (14, 30),
    "Sofyan Amrabat":      (1, 28),
    "Azzedine Ounahi":     (3, 28),
    "Noussair Mazraoui":   (3, 32),
    "Selim Amallah":       (5, 28),

    # === SENEGAL ===
    "Edouard Mendy":       (0, 28),
    "Kalidou Koulibaly":   (2, 30),
    "Sadio Mane":          (10, 29),
    "Ismaila Sarr":        (7, 30),
    "Nicolas Jackson":     (12, 35),
    "Idrissa Gueye":       (2, 28),
    "Pape Matar Sarr":     (3, 28),
    "Lamine Camara":       (4, 28),

    # === USA ===
    "Matt Turner":         (0, 28),
    "Tyler Adams":         (1, 22),
    "Weston McKennie":     (5, 28),
    "Christian Pulisic":   (8, 30),
    "Gio Reyna":           (0, 13),
    "Ricardo Pepi":        (12, 28),
    "Tim Weah":            (4, 25),
    "Yunus Musah":         (2, 30),
    "Antonee Robinson":    (1, 32),
    "Sergiino Dest":       (2, 22),
    "Joe Scally":          (1, 28),
    "DeAndre Yedlin":      (0, 15),
    "Cameron Carter-Vickers": (1, 28),
    "Matt Miazga":         (1, 22),
    "Reggie Cannon":       (0, 20),

    # === MEXICO ===
    "Guillermo Ochoa":     (0, 30),
    "Santiago Gimenez":    (22, 30),
    "Hirving Lozano":      (5, 25),
    "Raul Jimenez":        (10, 28),
    "Edson Alvarez":       (2, 32),
    "Uriel Antuna":        (5, 28),
    "Jesus Gallardo":      (1, 28),
    "Cesar Montes":        (1, 25),
    "Luis Romo":           (2, 28),
    "Luis Chavez":         (3, 28),
    "Roberto Alvarado":    (4, 28),
    "Alexis Vega":         (3, 22),
    "Henry Martin":        (8, 25),

    # === COLOMBIA ===
    "Camilo Vargas":       (0, 28),
    "Luis Diaz":           (15, 32),
    "James Rodriguez":     (8, 30),
    "Jhon Duran":          (14, 32),
    "Richard Rios":        (4, 28),
    "Yerry Mina":          (2, 22),
    "Juan Cuadrado":       (3, 20),
    "Davinson Sanchez":    (1, 28),
    "Daniel Munoz":        (2, 30),
    "Jefferson Lerma":     (2, 28),
    "Lerma":               (2, 28),

    # === AUSTRALIA ===
    "Mat Ryan":            (0, 35),
    "Martin Boyle":        (5, 25),
    "Mitch Duke":          (5, 22),
    "Awer Mabil":          (5, 25),
    "Harry Souttar":       (1, 22),
    "Lewis Miller":        (1, 25),
    "Ajdin Hrustic":       (3, 22),
    "Keanu Baccus":        (2, 22),
    "Riley McGree":        (5, 28),
    "Marco Tilio":         (3, 22),

    # === JAPAN ===
    "Shuichi Gonda":       (0, 28),
    "Takehiro Tomiyasu":   (1, 22),
    "Hiroki Ito":          (2, 28),
    "Ritsu Doan":          (9, 30),
    "Kaoru Mitoma":        (8, 32),
    "Takumi Minamino":     (10, 30),
    "Daichi Kamada":       (5, 28),
    "Wataru Endo":         (2, 35),
    "Yuki Soma":           (4, 25),
    "Ayase Ueda":          (10, 28),
    "Junya Ito":           (5, 25),

    # === SOUTH KOREA ===
    "Heungmin Son":        (18, 32),
    "Minjae Kim":          (2, 32),
    "Hwang Hee-chan":      (8, 28),
    "Lee Kang-in":         (10, 28),
    "Junho Hwang":         (6, 25),
    "Seunggyu Kim":        (0, 30),

    # === SWITZERLAND ===
    "Yann Sommer":         (0, 32),
    "Manuel Akanji":       (2, 32),
    "Granit Xhaka":        (4, 30),
    "Breel Embolo":        (8, 28),
    "Xherdan Shaqiri":     (3, 20),
    "Ruben Vargas":        (6, 30),
    "Fabian Schar":        (2, 30),
    "Ricardo Rodriguez":   (1, 25),
    "Remo Freuler":        (4, 32),
    "Silvan Widmer":       (2, 28),

    # === CROATIA ===
    "Dominik Livakovic":   (0, 32),
    "Luka Modric":         (5, 28),
    "Ivan Perisic":        (4, 25),
    "Andrej Kramaric":     (15, 30),
    "Mateo Kovacic":       (5, 35),
    "Bruno Petkovic":      (8, 28),
    "Josip Sutalo":        (2, 22),
    "Dejan Lovren":        (1, 22),
    "Josko Gvardiol":      (3, 38),
    "Mario Pasalic":       (8, 32),
    "Ivan Rakitic":        (3, 22),

    # === AUSTRIA ===
    "Patrick Pentz":       (0, 28),
    "Marko Arnautovic":    (5, 20),
    "David Alaba":         (1, 8),
    "Marcel Sabitzer":     (8, 30),
    "Florian Grillitsch":  (3, 25),
    "Xaver Schlager":      (3, 30),
    "Nicolas Seiwald":     (3, 28),
    "Stefan Posch":        (1, 28),
    "Michael Gregoritsch": (8, 28),

    # === TURKEY ===
    "Mert Gunok":          (0, 28),
    "Arda Guler":          (10, 28),
    "Hakan Calhanoglu":    (8, 32),
    "Kenan Yildiz":        (8, 28),
    "Zeki Celik":          (2, 30),
    "Merih Demiral":       (3, 30),
    "Cengiz Under":        (5, 25),
    "Yusuf Yazici":        (7, 28),
    "Samet Akaydin":       (1, 28),
    "Okay Yokuslu":        (2, 28),
    "Ozan Kabak":          (1, 25),

    # === IRAN ===
    "Alireza Beiranvand":  (0, 28),
    "Mehdi Taremi":        (12, 30),
    "Alireza Jahanbakhsh": (5, 25),
    "Sardar Azmoun":       (8, 25),
    "Ali Gholizadeh":      (4, 25),
    "Ehsan Hajsafi":       (1, 25),

    # === EGYPT ===
    "Mohamed El Shenawy":  (0, 30),
    "Mohamed Salah":       (22, 38),
    "Omar Marmoush":       (22, 35),
    "Mostafa Mohamed":     (12, 28),
    "Ahmed Hegazi":        (1, 22),
    "Amr El Sulaya":       (3, 25),

    # === CANADA ===
    "Maxime Crepeau":      (0, 28),
    "Alphonso Davies":     (5, 32),
    "Jonathan David":      (26, 30),
    "Cyle Larin":          (8, 25),
    "Stephen Eustaquio":   (4, 30),
    "Alistair Johnston":   (1, 30),
    "Kamal Miller":        (1, 28),
    "Richie Laryea":       (2, 25),
    "Tajon Buchanan":      (5, 28),
    "Lucas Cavallini":     (5, 22),

    # === URUGUAY ===
    "Sergio Rochet":       (0, 28),
    "Darwin Nunez":        (2, 10),
    "Federico Valverde":   (8, 40),
    "Rodrigo Bentancur":   (3, 28),
    "Facundo Pellistri":   (5, 25),
    "Jose Gimenez":        (2, 28),
    "Ronald Araujo":       (2, 25),
    "Edinson Cavani":      (4, 18),
    "Matias Vina":         (1, 22),
    "Nahitan Nandez":      (2, 25),

    # === ECUADOR ===
    "Hernan Galindez":     (0, 28),
    "Enner Valencia":      (8, 28),
    "Moises Caicedo":      (3, 35),
    "Gonzalo Plata":       (5, 28),
    "Jeremy Sarmiento":    (4, 28),
    "Piero Hincapie":      (2, 32),
    "Angelo Preciado":     (1, 28),
    "Carlos Gruezo":       (2, 25),
    "John Yeboah":         (4, 22),

    # === SAUDI ARABIA ===
    "Mohammed Al-Owais":   (0, 30),
    "Salem Al-Dawsari":    (8, 28),
    "Saleh Al-Shehri":     (10, 28),
    "Firas Al-Buraikan":   (8, 25),
    "Ali Al-Hassan":       (3, 25),
    "Mohammed Kanno":      (2, 28),
    "Ali Al-Bulaihi":      (1, 28),
    "Yasser Al-Shahrani":  (1, 22),

    # === QATAR ===
    "Meshaal Barsham":     (0, 25),
    "Akram Afif":          (12, 28),
    "Almoez Ali":          (8, 25),
    "Hassan Al-Haydos":    (5, 20),
    "Abdelkarim Hassan":   (2, 25),
    "Pedro Miguel":        (1, 25),
    "Karim Boudiaf":       (2, 25),

    # === GHANA ===
    "Lawrence Ati-Zigi":   (0, 28),
    "Mohammed Kudus":      (10, 32),
    "Thomas Partey":       (3, 25),
    "Jordan Ayew":         (5, 25),
    "Antoine Semenyo":     (8, 28),
    "Andre Ayew":          (4, 22),
    "Daniel Amartey":      (1, 22),
    "Inaki Williams":      (8, 30),
    "Tariq Lamptey":       (2, 25),

    # === SOUTH AFRICA ===
    "Ronwen Williams":     (0, 30),
    "Percy Tau":           (5, 22),
    "Themba Zwane":        (6, 22),
    "Lyle Foster":         (8, 25),
    "Bafana Bafana":       (0, 0),
    "Teboho Mokoena":      (4, 28),
    "Yusuf Maart":         (3, 25),
    "Terrence Mashego":    (1, 25),
    "Evidence Makgopa":    (6, 25),

    # === SCOTLAND ===
    "Craig Gordon":        (0, 28),
    "Andy Robertson":      (2, 38),
    "Scott McTominay":     (12, 30),
    "Kieran Tierney":      (1, 20),
    "John McGinn":         (5, 30),
    "Stuart Armstrong":    (3, 25),
    "Ryan Christie":       (4, 25),
    "Callum McGregor":     (3, 28),
    "Lawrence Shankland":  (15, 30),
    "Lyndon Dykes":        (8, 25),
    "Ryan Jack":           (2, 25),
    "Kenny McLean":        (2, 22),

    # === IVORY COAST ===
    "Badra Ali Sangare":   (0, 28),
    "Sebastien Haller":    (8, 22),
    "Nicolas Pepe":        (5, 20),
    "Wilfried Zaha":       (7, 28),
    "Franck Kessie":       (4, 28),
    "Serge Aurier":        (2, 22),
    "Eric Bailly":         (1, 20),
    "Jean-Philippe Gbamin":(2, 22),
    "Simon Adingra":       (6, 28),
    "Seko Fofana":         (4, 28),

    # === TUNISIA ===
    "Aymen Dahmen":        (0, 28),
    "Youssef Msakni":      (6, 22),
    "Wahbi Khazri":        (5, 20),
    "Ellyes Skhiri":       (4, 28),
    "Montassar Talbi":     (2, 25),
    "Mohamed Drager":      (1, 22),
    "Hannibal Mejbri":     (4, 25),
    "Aissa Laidouni":      (3, 25),
    "Dylan Bronn":         (1, 22),

    # === ALGERIA ===
    "Rais M'Bolhi":        (0, 28),
    "Riyad Mahrez":        (8, 25),
    "Aissa Mandi":         (1, 28),
    "Houssem Aouar":       (4, 25),
    "Youcef Atal":         (4, 25),
    "Islam Slimani":       (5, 20),
    "Hicham Boudaoui":     (3, 28),
    "Amine Gouiri":        (8, 28),
    "Ramy Bensebaini":     (2, 28),

    # === CZECH REPUBLIC ===
    "Tomas Vaclik":        (0, 25),
    "Patrik Schick":       (12, 25),
    "Tomas Soucek":        (6, 35),
    "Vladimir Coufal":     (2, 32),
    "Adam Hlozek":         (8, 30),
    "Antonin Barak":       (4, 28),
    "Lukas Cerv":          (3, 25),
    "Lukas Provod":        (3, 25),

    # === BOSNIA ===
    "Jasmin Handanovic":   (0, 22),
    "Edin Dzeko":          (8, 25),
    "Miralem Pjanic":      (2, 15),
    "Ermedin Demirovic":   (12, 28),
    "Sead Kolasinac":      (1, 22),
    "Edin Visca":          (4, 22),
    "Asmir Begovic":       (0, 20),
    "Amar Dedic":          (2, 25),
    "Sasa Lukic":          (3, 25),

    # === JORDAN ===
    "Mahmoud Shuaibi":     (0, 22),
    "Musa Al-Taamari":     (8, 28),
    "Yazan Al-Naimat":     (5, 22),
    "Ahmad Hayel":         (3, 22),
    "Baha Faisal":         (2, 20),

    # === IRAQ ===
    "Jalal Hassan":        (0, 22),
    "Amjed Attwan":        (3, 20),
    "Hussein Ali":         (5, 22),
    "Mohanad Ali":         (4, 22),
    "Ali Adnan":           (1, 22),
    "Ahmed Yaseen":        (2, 20),

    # === NEW ZEALAND ===
    "Stefan Marinovic":    (0, 22),
    "Chris Wood":          (8, 28),
    "Clayton Lewis":       (3, 25),
    "Liberato Cacace":     (3, 28),
    "Bill Tuilagi":        (4, 22),
    "Elijah Just":         (3, 20),
    "Marco Rojas":         (3, 18),

    # === CURACAO ===
    "Eloy Room":           (0, 22),
    "Leandro Bacuna":      (3, 22),
    "Jurien Gaari":        (3, 20),
    "Elson Hooi":          (4, 20),
    "Cuco Martina":        (1, 15),

    # === CAPE VERDE ===
    "Vozinha":             (0, 22),
    "Bryan Teixeira":      (5, 22),
    "Ryan Mendes":         (4, 20),
    "Garry Rodrigues":     (5, 22),
    "Steven Fortes":       (1, 20),
    "Patrick Andrade":     (2, 22),

    # === HAITI ===
    "Johny Placide":       (0, 20),
    "Frantzdy Pierrot":    (6, 22),
    "Derrick Etienne":     (4, 20),
    "Jean-Ricner Bellegarde":(4, 28),
    "Wilson Isidor":       (5, 22),

    # === PANAMA ===
    "Orlando Mosquera":    (0, 22),
    "Rolando Blackburn":   (5, 22),
    "Cecilio Waterman":    (6, 22),
    "Alberto Quintero":    (3, 20),
    "Edgar Barcenas":      (3, 22),
    "Anibal Godoy":        (1, 22),
    "Roman Torres":        (2, 20),
    "Jose Fajardo":        (3, 22),

    # === PARAGUAY ===
    "Antony Silva":        (0, 25),
    "Miguel Almiron":      (5, 25),
    "Carlos Gonzalez":     (8, 25),
    "Gustavo Gomez":       (3, 28),
    "Roberto Morales":     (4, 22),
    "Santiago Arzamendia": (2, 25),
    "Fabian Balbuena":     (1, 22),
    "Matias Rojas":        (4, 25),
    "Alejandro Romero":    (4, 22),

    # === DRC CONGO ===
    "Joel Kiassumbua":     (0, 22),
    "Cedric Bakambu":      (5, 22),
    "Yannick Bolasie":     (3, 20),
    "Chancel Mbemba":      (2, 25),
    "Britt Assombalonga":  (6, 22),
    "Chadrac Akolo":       (4, 22),
    "Arthur Masuaku":      (1, 22),
    "Gabriel Zakuani":     (1, 18),

    # === UZBEKISTAN ===
    "Utkir Yusupov":       (0, 25),
    "Eldor Shomurodov":    (8, 25),
    "Abbosbek Fayzullayev":(6, 28),
    "Otabek Shukurov":     (3, 22),
    "Jasur Yakhshiboev":   (4, 22),
    "Khojimat Erkinov":    (3, 22),
    "Sherzod Nasrullayev": (2, 22),
    "Dostonbek Khamdamov": (3, 20),
}

def update_player_stats(html, name_key, goals, matches):
    pattern = r'(name:"[^"]*' + re.escape(name_key) + r'[^"]*"[^,]*, pos:"[^"]*", club:"[^"]*", starter:[^,]*, )goals:\d+(, matches:)\d+'
    replacement = r'\g<1>goals:' + str(goals) + r'\g<2>' + str(matches)
    return re.sub(pattern, replacement, html)

count = 0
for name_key, (goals, matches) in STATS.items():
    new_html = update_player_stats(html, name_key, goals, matches)
    if new_html != html:
        count += 1
        html = new_html

print(f"Updated {count} / {len(STATS)} players")

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

import shutil
dest = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\recette_facturx_app\app\world_cup_2026.html'
shutil.copy(path, dest)
print('Done')
