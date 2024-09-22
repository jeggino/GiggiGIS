# --- COSTANTS ---

WIDTH_SCREEN = int(streamlit_js_eval(js_expressions='screen.width', key = 'SCR'))
HEIGHT_SCREEN = streamlit_js_eval(js_expressions='screen.height', key = 'SCR1')
OUTPUT_height = HEIGHT_SCREEN * 0.75
OUTPUT_width = WIDTH_SCREEN

HELP_FUNCTIE = "Zomer- of kraamverblijfplaats: De vrouwtjes wonen in de zomer in kraamverblijfplaatsen. Hier brengt ze hun jongen groot. voorkomende leven ze gecombineerd in groepen (kolonies). \nZomer- of mannenverblijfplaats: De mannetjes wonen in de zomer soms solitair, soms in groepen, maar altijd op een andere plaats dan de vrouwtjes van hun soort. \nTijdelijke of paarverblijfplaats: Vaak kennen vleermuizen ook tussenkwartieren, waar ze slechts kort verblijven tijdens de reis van hun winter- naar zomerkolonie. Zo trekken zowel de mannetjes als de vrouwtjes aan het einde van de zomer naar speciale paarkwartieren, waar ze slechts kort verblijven. Winterverblijfplaats: Vleermuizen overwinteren in gebouwen, bunkers, ijskelders, groeven en boomholtes."

GROUP = ["🦇 Vleermuizen","🪶 Vogels",  "🏠 Vleermuiskast",
         "📷 Camera", "🐀 Rat val"]

GROUP_DICT = {"🪶 Vogels":"Vogels",
              "🦇 Vleermuizen":"Vleermuizen", 
              "🏠 Vleermuiskast":"Vleermuiskast",
              "📷 Camera":"Camera",
             "🐀 Rat val":"Rat val"}

VLEERMUISKAST_OPTIONS = ["Bewoond","Onbewoond"]

CAMERA_OPTIONS = ["Camera in het veld","Verwijderd, ratten gedetecteerd","Camera verwijderd, geen ratten gedetecteerd"]

RAT_VAL_OPTIONS = ["Val nog in het veld","Val verwijderd. Ratten gedood","Val verwijderd. Geen ratten gedood"]

BAT_NAMES = ['Gewone dwergvleermuis','Ruige dwergvleermuis', 'Laatvlieger']

BAT_BEHAVIOURS = ['foeragerend', 'uitvliegend','invliegend', 'overvliegend', 
         'zwermend', 'sporen', 'balts', 'verkeersslachtoffer']

BAT_FUNCTIE = ['geen / onbekend','zomerverblijfplaats','kraamverblijfplaats']

BAT_VERBLIJF = ['geen / onbekend', 'dakgoot', 'spouwmuur', 'daklijst',
       'kantpan', 'regenpijp', 'holte', 'raamkozijn', 'luik', 'scheur',
       'schoorsteen', 'gevelbetimmering', 'nokpan', 'dakpan',
       'vleermuiskast', 'openingen in dak', 'dakkapel', 'schors']

BIRD_NAMES = ['Gierzwaluw','Huismus']

BIRD_BEHAVIOURS = ['overvliegend',  'nest-indicerend gedrag', 'foeragerend', 'invliegend', 'uitvliegend',
       'roepend vanuit gebouw', 'baltsend / zingend op gebouw',
       'baltsend / zingend in vegetatie, struik of boom', 'sporen',
        'copula']



BIRD_FUNCTIE = ['geen / onbekend', 'nestlocatie', 'mogelijke nestlocatie']

BIRD_VERBLIJF = ['geen / onbekend', 'dakgoot', 'kantpan', 'zonnepaneel', 'nokpan', 'nestkast',
       'gevelbetimmering', 'openingen in dak', 'regenpijp',
        'dakpan', 'spouwmuur', 'onder dakrand',
       'raamkozijn', 'luik', 'schoorsteen', 'daklijst', 'dakkapel',
       'in struweel / struiken', 'holte', 'op / bij nest in boom',
       'scheur', 'vleermuiskast']

VLEERMUISKAST_VERBLIJF = ["Op boom", "Op gebouw"]


icon_dictionary = {'Vogels': {'Gierzwaluw': {'geen / onbekend': 'icons/swift.png',
   'nestlocatie': 'icons/swift_nest.png',
   'mogelijke nestlocatie': 'icons/swift_mogelijk_nest.png'},
  'Huismus': {'geen / onbekend': 'icons/sparrow.png',
   'nestlocatie': 'icons/sparrow_nest.png',
   'mogelijke nestlocatie': 'icons/sparrow_mogelijk_nest.png'}},
 'Vleermuizen': {'Gewone dwergvleermuis': {'geen / onbekend': 'icons/pippip_foraging.png',
   'zomerverblijfplaats': 'icons/pippip_zommer.png',
   'kraamverblijfplaats': 'icons/pippip_kraam.png'},
  'Ruige dwergvleermuis': {'geen / onbekend': 'icons/ruige_foraging.png',
   'zomerverblijfplaats': 'icons/ruige_zommer.png',
   'kraamverblijfplaats': 'icons/ruige_kraam.png'},
  'Laatvlieger': {'geen / onbekend': 'icons/laatflieger_foraging.png',
   'zomerverblijfplaats': 'icons/laatvlieger_zommer.png',
   'kraamverblijfplaats': 'icons/laatvlieger_kraam.png'}},
 'Vleermuiskast': {"Bewoond":"icons/bat_bow_full.jpg",
                   "Onbewoond":"icons/bat_box_empty.jpg"},
 'Camera': {'Camera in het veld': 'icons/camera-icon-orange.png',
  'Verwijderd, ratten gedetecteerd': 'icons/camera-icon-red.png',
  'Camera verwijderd, geen ratten gedetecteerd': 'icons/camera-icon-green.png'},
 'Rat val': {'Val nog in het veld': 'icons/rat_trap_orange.png',
  'Val verwijderd. Ratten gedood': 'icons/rat_trap_green.png',
  'Val verwijderd. Geen ratten gedood': 'icons/rat_trap_red.png'}}

DICTIONARY_USERS = {"Luigi": ["Niet gespecificeerd"],
                   "Daan": ["Niet gespecificeerd","A-001"]
                   }

DICTIONARY_PROJECTS = {"Overing":["Vogels","Vleermuizen","Vleermuiskast"],
                      "A-001":["Camera","Rat val"],
                      "Admin":["Vogels","Vleermuizen","Vleermuiskast","Camera","Rat val"]}

