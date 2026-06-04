import re, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\L1174214\OneDrive - TotalEnergies\Bureau\worldcup2026\index.html'

with open(path, encoding='utf-8') as f:
    html = f.read()

# Stats format: (name_key, goals, matches, assists, rating)
# name_key = distinctive part of the player name to match uniquely
STATS = [
    # ── EUROPEAN TOP LEAGUES ──────────────────────────────────────────
    ("Thibaut Courtois",    0, 30, 0, 7.05),
    ("Brandon Mechele",     0, 28, 0, 6.88),
    ("Maxim De Cuyper",     2, 30, 4, 7.12),
    ("Virgil Van Dijk",     8, 50, 3, 7.35),
    ("Jan Paul Van Hecke",  0, 32, 2, 6.82),
    ("Justin Kluivert",     2, 18, 0, 6.65),  # injured
    ("Wout Weghorst",       9, 32, 4, 7.18),
    ("Michael Olise",      21, 35, 28, 8.09),
    ("Aleksandar Pavlovic", 4, 38, 2, 7.15),
    ("Waldemar Anton",      1, 32, 2, 6.92),
    ("Antonio Ruediger",    1, 35, 1, 7.08),
    ("Jamie Leweling",      7, 34, 6, 7.05),
    ("Nick Woltemade",      8, 32, 5, 7.12),
    ("Josip Stanisic",      2, 30, 3, 6.95),
    ("Marin Pongracic",     1, 28, 1, 6.88),
    ("Duje Caleta-Car",     1, 22, 1, 6.75),
    ("Nikola Moro",         2, 24, 1, 6.97),
    ("Ante Budimir",       17, 37, 0, 7.25),
    ("Nico Elvedi",         0, 33, 2, 6.96),
    ("Denis Zakaria",       1, 28, 2, 6.88),
    ("Johan Manzambi",      2, 25, 3, 6.78),
    ("Dan Ndoye",           1, 28, 1, 6.75),
    ("Jacob Widell Zetterstrom", 0, 38, 0, 6.85),
    ("Gustaf Lagerbielke",  1, 26, 0, 6.72),
    ("Isak Hien",           1, 32, 1, 6.95),
    ("Gabriel Gudmundsson", 1, 30, 3, 6.82),
    ("Herman Johansson",    1, 28, 2, 6.68),
    ("Daniel Svensson",     0, 25, 1, 6.75),
    ("Benjamin Nygren",     6, 30, 4, 6.88),
    ("Lucas Bergvall",      1, 30, 3, 6.92),
    ("Anthony Elanga",      0, 28, 2, 6.88),
    ("Alexander Schlager",  0, 28, 0, 6.85),
    ("David Affengruber",   1, 25, 1, 6.62),
    ("Kevin Danso",         0, 28, 0, 6.88),
    ("Gregor Kobel",        0, 34, 0, 7.05),
    ("Miro Muheim",         1, 30, 4, 6.78),
    ("Juan Musso",          0, 18, 0, 6.75),
    ("Valentin Barco",      1, 22, 2, 6.65),
    ("Caglar Soyuncu",      1, 28, 0, 6.85),
    ("Salih Ozcan",         1, 30, 3, 6.82),
    ("Orkun Kokcu",         4, 28, 6, 7.12),
    ("Kerem Akturkoglu",    8, 30, 7, 7.22),
    ("Deniz Gul",           5, 24, 3, 6.95),
    # ── PORTUGAL ─────────────────────────────────────────────────────
    ("Diogo Dalot",         1, 38, 3, 7.13),
    ("Matheus Nunes",       2, 30, 4, 6.98),
    ("Tomas Araujo",        2, 32, 1, 7.02),
    # ── SCOTLAND ─────────────────────────────────────────────────────
    ("Angus Gunn",          0, 32, 0, 6.85),
    ("Aaron Hickey",        1, 28, 3, 6.92),
    ("McTOMINAY Scott",    10, 30, 3, 7.30),
    ("Grant Hanley",        0, 24, 0, 6.72),
    ("McGINN John",         3, 28, 3, 6.95),
    ("Che Adams",           5, 28, 2, 6.88),
    # ── NORWAY ───────────────────────────────────────────────────────
    ("Morten Thorsby",      2, 28, 3, 6.75),
    ("Kristoffer Ajer",     0, 30, 1, 6.82),
    ("Leo Ostigard",        0, 24, 1, 6.72),
    ("David Moller Wolfe",  0, 22, 1, 6.68),
    ("Patrick Berg",        3, 30, 5, 6.92),
    ("Jorgen Strand Larsen", 4, 36, 1, 6.98),
    # ── BRAZIL ───────────────────────────────────────────────────────
    ("Neymar Jr",          11, 24, 4, 7.12),
    ("Wesley",              0, 28, 1, 6.85),
    ("Alex Sandro",         0, 22, 1, 6.65),
    ("Bruno Guimaraes",     9, 35, 5, 7.28),
    ("Matheus Cunha",      10, 33, 2, 7.29),
    ("Mauricio",            3, 28, 4, 6.95),
    # ── ARGENTINA ────────────────────────────────────────────────────
    # Already have most; add remaining:
    # ── COLOMBIA ─────────────────────────────────────────────────────
    ("David Ospina",        0, 20, 0, 6.78),  # GK
    ("Jhon Lucumi",         0, 25, 0, 6.85),
    ("Santiago Arias",      0, 18, 1, 6.62),
    ("Kevin Castano",       2, 22, 3, 6.75),
    ("Jorge Carrascal",     2, 28, 5, 6.92),
    ("Jhon Cordoba",       17, 28, 5, 7.35),
    ("Jhon Arias",          3, 30, 2, 6.88),
    # ── ECUADOR ──────────────────────────────────────────────────────
    ("Felix Torres",        0, 28, 0, 6.78),
    ("Jordy Alcivar",       2, 25, 4, 6.72),
    ("Willian Pacho",       1, 28, 0, 7.05),
    ("Pervis Estupinan",    1, 24, 3, 6.88),
    ("Anthony Valencia",    2, 25, 3, 6.72),
    ("Kendry Paez",         4, 28, 6, 7.08),
    ("Kevin Rodriguez",     8, 30, 5, 7.12),
    # ── URUGUAY ──────────────────────────────────────────────────────
    ("Jose Maria Gimenez",  1, 28, 0, 7.02),
    ("Sebastian Caceres",   1, 28, 1, 6.82),
    ("Manuel Ugarte",       0, 22, 0, 6.69),
    ("Nicolas De La Cruz",  4, 28, 8, 7.05),
    ("Giorgian De Arrascaeta", 7, 26, 9, 7.35),
    # ── PARAGUAY ─────────────────────────────────────────────────────
    ("Gatito Fernandez",    0, 30, 0, 6.82),
    ("Gustavo Velazquez",   0, 25, 1, 6.65),
    ("Omar Alderete",       0, 22, 0, 6.72),
    ("Juan Jose Caceres",   0, 20, 0, 6.62),
    ("Junior Alonso",       1, 28, 0, 6.78),
    ("Ramon Sosa",          5, 28, 4, 6.92),
    ("Diego Gomez",         2, 25, 3, 6.82),
    ("Antonio Sanabria",    5, 22, 1, 6.75),
    # ── MEXICO ───────────────────────────────────────────────────────
    ("Raul Rangel",         0, 30, 0, 6.82),
    ("Jorge Sanchez",       1, 25, 3, 6.72),
    ("Johan Vasquez",       0, 24, 0, 6.78),
    ("Erik Lira",           2, 28, 4, 6.75),
    ("Alvaro Fidalgo",      3, 28, 5, 6.88),
    # ── PANAMA ───────────────────────────────────────────────────────
    ("Luis Mejia",          0, 28, 0, 6.72),
    ("Cesar Blackman",      0, 22, 0, 6.58),
    ("Jose Cordoba",        0, 20, 0, 6.55),
    ("Fidel Escobar",       0, 22, 0, 6.62),
    ("Edgardo Farina",      0, 18, 0, 6.45),
    ("Cristian Martinez",   1, 22, 2, 6.58),
    ("Jose Luis Rodriguez", 1, 25, 2, 6.62),
    ("Adalberto Carrasquilla", 2, 25, 4, 6.75),
    ("Tomas Rodriguez",     4, 28, 3, 6.82),
    ("Ismael Diaz",         3, 25, 4, 6.78),
    ("Edgar Yoel Barcenas", 3, 22, 3, 6.72),
    # ── CANADA ───────────────────────────────────────────────────────
    ("Dayne St. Clair",     0, 28, 0, 6.75),
    ("Alfie Jones",         0, 22, 0, 6.55),
    ("Luc De Fougerolles",  0, 18, 0, 6.42),
    ("Joel Waterman",       0, 22, 0, 6.52),
    ("Mathieu Choiniere",   3, 28, 4, 6.72),
    ("Ismael Kone",         1, 20, 2, 6.65),
    ("Liam Millar",         2, 22, 3, 6.68),
    # ── USA ──────────────────────────────────────────────────────────
    ("Sergino Dest",        2, 38, 8, 7.02),
    ("Chris Richards",      1, 32, 0, 6.87),
    ("Auston Trusty",       2, 41, 1, 6.95),
    ("Giovanni Reyna",      4, 28, 6, 6.98),
    ("McKENNIE Weston",     9, 38, 8, 7.22),
    ("Brenden Aaronson",    4, 35, 5, 6.98),
    # ── AUSTRALIA ────────────────────────────────────────────────────
    ("Mathew Ryan",         0, 28, 0, 6.72),
    ("Milos Degenek",       0, 22, 0, 6.55),
    ("Alessandro Circati",  0, 22, 0, 6.58),
    ("Jacob Italiano",      0, 18, 0, 6.42),
    ("Jordan Bos",          1, 28, 2, 6.72),
    ("Jason Geria",         1, 20, 3, 6.55),
    ("Mathew Leckie",       3, 22, 2, 6.72),
    ("Connor Metcalfe",     2, 28, 3, 6.78),
    # ── NEW ZEALAND ──────────────────────────────────────────────────
    ("Max Crocombe",        0, 32, 0, 6.65),
    ("Tim Payne",           0, 20, 0, 6.42),
    ("Francis De Vries",    0, 15, 0, 6.38),
    ("Tyler Bindon",        0, 20, 0, 6.45),
    ("Michael Boxall",      0, 28, 0, 6.55),
    ("Joe Bell",            1, 25, 2, 6.58),
    ("Matthew Garbett",     2, 22, 3, 6.55),
    ("Marko Stamenic",      3, 28, 4, 6.72),
    ("Sarpreet Singh",      2, 18, 3, 6.55),
    # ── JAPAN ────────────────────────────────────────────────────────
    ("Zion Suzuki",         0, 30, 0, 6.88),
    ("Yukinari Sugawara",   2, 30, 5, 6.95),
    ("Shogo Taniguchi",     0, 25, 0, 6.72),
    ("Kou Itakura",         0, 32, 2, 6.88),
    ("Yuto Nagatomo",       0, 22, 1, 6.55),
    ("Ao Tanaka",           3, 35, 4, 6.98),
    ("Takefusa Kubo",       2, 24, 4, 6.95),
    ("Keisuke Goto",        4, 25, 3, 6.82),
    ("Daizen Maeda",        7, 38, 5, 7.05),
    # ── KOREA (already in inject_stats3) ─────────────────────────────
    # ── SAUDI ARABIA ─────────────────────────────────────────────────
    ("Nawaf Alaqidi",       0, 28, 0, 6.78),
    ("Ali Majrashi",        0, 25, 1, 6.62),
    ("Ali Lajami",          0, 28, 0, 6.72),
    ("Abdulelah Alamri",    1, 25, 2, 6.65),
    ("Hassan Altambakti",   0, 28, 1, 6.72),
    ("Nasser Aldawsari",    5, 28, 7, 6.98),
    ("Musab Aljuwayr",      3, 25, 4, 6.82),
    ("Aiman Yahya",         4, 25, 2, 6.88),
    ("Feras Albrikan",      6, 25, 4, 6.95),
    ("Salem Aldawsari",     7, 28, 5, 7.02),
    ("Saleh Alshehri",      5, 25, 3, 6.88),
    # ── IRAN ─────────────────────────────────────────────────────────
    ("Saleh Hardani",       0, 22, 0, 6.58),
    ("Ehsan Hajisafi",      0, 20, 2, 6.55),
    ("Shoja Khalilzadeh",   0, 22, 0, 6.52),
    ("Milad Mohammadi",     0, 22, 1, 6.55),
    ("Saeid Ezatolahi",     1, 25, 2, 6.72),
    ("Mohammad Mohebbi",    1, 20, 1, 6.45),
    ("Mehdi Ghayedi",       4, 22, 3, 6.72),
    ("Ali Alipour",         7, 24, 2, 6.88),
    # ── IRAQ ─────────────────────────────────────────────────────────
    ("Fahad Talib",         0, 22, 0, 6.62),
    ("Rebin Ghareeb",       0, 20, 0, 6.45),
    ("Zaid Tahseen",        0, 18, 0, 6.42),
    ("Akam Hashim",         0, 18, 0, 6.38),
    ("Munaf Younus",        0, 20, 0, 6.45),
    ("Youssef Amyn",        2, 22, 3, 6.62),
    ("Ibrahim Bayesh",      1, 20, 2, 6.52),
    ("Ali Alhamadi",        1, 8,  0, 6.42),
    ("Ahmed Qasim",         2, 15, 1, 6.55),
    # ── JORDAN ───────────────────────────────────────────────────────
    ("Yazeed Abulaila",     0, 25, 0, 6.65),
    ("Mohammad Abuhasheesh", 0, 22, 0, 6.42),
    ("Abdallah Nasib",      0, 20, 0, 6.38),
    ("Husam Abudahab",      0, 22, 0, 6.45),
    ("Yazan Alarab",        1, 18, 1, 6.42),
    ("Amer Jamous",         1, 22, 2, 6.52),
    ("Mohammad Abuzraiq",   5, 25, 3, 6.72),
    ("Noor Alrawabdeh",     2, 20, 3, 6.55),
    ("Ali Olwan",           3, 22, 2, 6.62),
    ("Mousa Altamari",      4, 22, 3, 6.88),
    ("Odeh Fakhoury",       3, 22, 2, 6.65),
    # ── QATAR ────────────────────────────────────────────────────────
    ("Mahmoud Abunada",     0, 22, 0, 6.65),
    ("Lucas Mendes",        0, 22, 1, 6.62),
    ("Issa Laye",           0, 18, 0, 6.45),
    ("Jassem Gaber",        0, 20, 0, 6.52),
    ("Abdulaziz Hatem",     2, 22, 3, 6.72),
    ("Ahmed Alaaeldin",     4, 22, 2, 6.75),
    ("Edmilson Junior",     8, 25, 5, 7.05),
    ("Mohammed Muntari",    5, 22, 2, 6.88),
    ("Hassan Alhaydos",     6, 22, 8, 7.02),
    # ── UZBEKISTAN ───────────────────────────────────────────────────
    ("Abdukodir Khusanov",  0, 17, 0, 7.12),
    ("Khojiakbar Alijonov", 0, 22, 0, 6.55),
    ("Farrukh Sayfiev",     0, 20, 0, 6.48),
    ("Rustam Ashurmatov",   0, 22, 0, 6.52),
    ("Akmal Mozgovoy",      1, 22, 2, 6.58),
    ("Jamshid Iskanderov",  1, 20, 2, 6.52),
    ("Odiljon Xamrobekov",  1, 18, 1, 6.45),
    ("Jaloliddin Masharipov", 3, 22, 4, 6.72),
    ("Oston Urunov",        4, 22, 5, 6.88),
    # ── SOUTH AFRICA ─────────────────────────────────────────────────
    ("Thabang Matuludi",    0, 20, 0, 6.38),
    ("Khulumani Ndamane",   0, 22, 0, 6.42),
    ("Thalente Mbatha",     2, 25, 3, 6.62),
    ("Aubrey Modiba",       0, 22, 1, 6.52),
    ("Oswin Appollis",      5, 25, 4, 6.82),
    ("Tshepang Moremi",     3, 20, 2, 6.65),
    ("Relebohile Mofokeng", 8, 28, 5, 7.02),
    # ── GHANA ────────────────────────────────────────────────────────
    ("Lawrence Ati Zigi",   0, 28, 0, 6.88),
    ("Alidu Seidu",         0, 22, 1, 6.72),
    ("Caleb Yirenkyi",      1, 20, 2, 6.52),
    ("Jonas Adjetey",       0, 22, 0, 6.55),
    ("Abdul Mumin",         0, 25, 0, 6.65),
    ("Fatawu Issahaku",     9, 44, 7, 7.05),
    ("Kwasi Sibo",          3, 30, 3, 6.72),
    ("Brandon Thomas-Asante", 4, 25, 1, 6.78),
    # ── SENEGAL ──────────────────────────────────────────────────────
    ("Yehvann Diouf",       0, 28, 0, 6.82),
    ("Mamadou Sarr",        0, 18, 0, 6.55),
    ("Abdoulaye Seck",      0, 22, 0, 6.45),
    ("Idrissa Gana Gueye",  1, 28, 1, 6.75),
    ("Pathe Ciss",          1, 25, 2, 6.68),
    ("Assane Diao",         5, 25, 4, 6.92),
    ("Bamba Dieng",         7, 15, 1, 6.88),
    # ── ALGERIA ──────────────────────────────────────────────────────
    ("Melvin Mastil",       0, 12, 0, 6.38),
    ("Achraf Abada",        0, 15, 0, 6.42),
    ("Mohamed Amine Tougai", 0, 18, 0, 6.45),
    ("Zineddine Belaid",    0, 18, 0, 6.42),
    ("Ramiz Zerrouki",      2, 28, 3, 6.82),
    ("Fares Chaibi",        3, 25, 4, 6.88),
    ("Anis Hadj Moussa",    5, 30, 6, 6.98),
    # ── EGYPT ────────────────────────────────────────────────────────
    ("Mohamed Elshenawy",   0, 28, 0, 6.78),
    ("Yasser Ibrahim",      1, 28, 0, 6.72),
    ("Mohamed Hany",        0, 25, 1, 6.68),
    ("Hossam Abdelmaguid",  0, 22, 0, 6.52),
    ("Ramy Rabia",          0, 20, 0, 6.45),
    ("Mohamed Abdelmoneim", 0, 20, 1, 6.62),
    ("Trezeguet",           5, 22, 3, 6.88),
    ("Emam Ashour",         3, 25, 4, 6.82),
    ("Hamza Abdelkarim",    2, 15, 1, 6.55),
    ("Mostafa Zico",        4, 25, 3, 6.72),
    # ── TUNISIA ──────────────────────────────────────────────────────
    ("Mouhib Chamakh",      0, 20, 0, 6.45),
    ("Ali Abdi",            0, 22, 1, 6.62),
    ("Omar Rekik",          0, 18, 0, 6.48),
    ("Adam Arous",          1, 20, 0, 6.52),
    ("Elias Achouri",       3, 25, 2, 6.78),
    ("Elias Saad",          4, 28, 3, 6.82),
    ("Hazem Mastouri",      2, 18, 1, 6.55),
    ("Ismael Gharbi",       4, 25, 4, 6.88),
    ("Ayyoub Bouaddi",      0, 25, 1, 6.72),
    ("Chemsdine Talbi",     3, 28, 3, 6.82),
    # ── MOROCCO ──────────────────────────────────────────────────────
    ("Soufiane Rahimi",     7, 25, 5, 7.08),
    ("Brahim Diaz",         3, 34, 8, 6.98),  # all comps incl. UCL
    ("Ismael Saibari",      6, 28, 7, 7.05),
    # ── DR CONGO ─────────────────────────────────────────────────────
    ("Lionel Mpasi",        0, 25, 0, 6.65),
    ("Aaron Wan-Bissaka",   0, 25, 2, 6.78),
    ("Steve Kapuadi",       0, 18, 0, 6.42),
    ("Axel Tuanzebe",       0, 18, 0, 6.45),
    ("Dylan Batubinsika",   0, 18, 0, 6.38),
    ("Ngalayel Mukau",      1, 22, 2, 6.65),
    ("Nathanael Mbuku",     2, 22, 3, 6.62),
    ("Samuel Moutoussamy",  1, 20, 1, 6.48),
    ("Brian Cipenga",       2, 20, 1, 6.55),
    ("Theo Bongonda",       3, 22, 2, 6.62),
    ("Gael Kakuta",         2, 20, 1, 6.52),
    # ── IVORY COAST ──────────────────────────────────────────────────
    ("Yahia Fofana",        0, 22, 0, 6.62),
    ("Ousmane Diomande",    0, 22, 1, 7.25),
    ("Ghislain Konan",      0, 22, 2, 6.62),
    ("Jean Michael Seri",   1, 18, 1, 6.45),
    ("Wilfried Singo",      1, 28, 4, 6.88),
    ("Odilon Kossounou",    0, 30, 1, 7.05),
    ("Ange-Yoan Bonny",     8, 32, 6, 7.12),
    ("Yan Diomande",       12, 28, 8, 7.61),
    # ── CAPE VERDE ───────────────────────────────────────────────────
    ("Stopira",             0, 20, 0, 6.42),
    ("Diney Borges",        0, 18, 0, 6.35),
    ("Pico Lopes",          0, 22, 1, 6.52),
    ("Logan Costa",         1, 28, 1, 6.82),
    ("Kevin Pina",          2, 22, 3, 6.62),
    ("Jovane Cabral",       3, 20, 2, 6.72),
    ("Joao Paulo",          2, 18, 3, 6.55),
    ("Gilson Benchimol",    4, 22, 2, 6.62),
    ("Jamiro Monteiro",     2, 22, 3, 6.65),
    # ── CURAÇAO ──────────────────────────────────────────────────────
    ("Shurandy Sambo",      0, 25, 1, 6.52),
    ("Roshon Van Eijma",    0, 22, 1, 6.45),
    ("Sherel Floranus",     0, 22, 1, 6.48),
    ("Godfried Roemeratoe", 1, 22, 2, 6.52),
    ("Juninho Bacuna",      3, 22, 4, 6.62),
    ("Livano Comenencia",   1, 22, 3, 6.58),
    ("Juergen Locadia",     4, 20, 2, 6.65),
    ("Jeremy Antonisse",    2, 15, 1, 6.48),
    # ── HAITI ────────────────────────────────────────────────────────
    ("Mohamed Toure",       4, 22, 2, 6.72),
    # ── BOSNIA ───────────────────────────────────────────────────────
    ("Nikola Vasilj",       0, 30, 0, 6.88),
    ("Nihad Mujakic",       0, 20, 0, 6.45),
    ("Dennis Hadzikadunic", 0, 18, 0, 6.48),
    ("Tarik Muharemovic",   0, 18, 0, 6.42),
    ("Benjamin Tahirovic",  1, 25, 3, 6.72),
    ("Armin Gigovic",       2, 25, 3, 6.65),
    ("Samed Bazdar",        4, 25, 3, 6.82),
    # ── BELGIUM ──────────────────────────────────────────────────────
    ("Nikola Vasilj",       0, 30, 0, 6.88),  # BIH GK
]

updated = 0
not_found = []

for (key, goals, matches, assists, rating) in STATS:
    # Match the player entry in HTML
    pattern = (
        r'(\{name:"[^"]*' + re.escape(key) + r'[^"]*", pos:"[^"]*", club:"[^"]*", starter:[^,]*, )'
        r'goals:\d+(, matches:)\d+(, assists:)\d+(, rating:)[\d.]+'
    )
    replacement = r'\g<1>goals:' + str(goals) + r'\g<2>' + str(matches) + r'\g<3>' + str(assists) + r'\g<4>' + str(rating)
    new_html, n = re.subn(pattern, replacement, html)
    if n > 0:
        html = new_html
        updated += n
    else:
        not_found.append(key)

print(f'Updated {updated} player entries')
if not_found:
    print(f'Not found ({len(not_found)}):')
    for k in not_found:
        print(f'  - {k}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Done')
