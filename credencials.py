# --- COSTANTS ---
WAARNEMERS = ["Luigi","Daan"]
HELP_FUNCTIE = "Zomer- of kraamverblijfplaats: De vrouwtjes wonen in de zomer in kraamverblijfplaatsen. Hier brengt ze hun jongen groot. voorkomende leven ze gecombineerd in groepen (kolonies). \nZomer- of mannenverblijfplaats: De mannetjes wonen in de zomer soms solitair, soms in groepen, maar altijd op een andere plaats dan de vrouwtjes van hun soort. \nTijdelijke of paarverblijfplaats: Vaak kennen vleermuizen ook tussenkwartieren, waar ze slechts kort verblijven tijdens de reis van hun winter- naar zomerkolonie. Zo trekken zowel de mannetjes als de vrouwtjes aan het einde van de zomer naar speciale paarkwartieren, waar ze slechts kort verblijven. Winterverblijfplaats: Vleermuizen overwinteren in gebouwen, bunkers, ijskelders, groeven en boomholtes."

GROUP = ["🦇 Vleermuizen","🪶 Vogels",  "🏠 Vleermuiskast",
         "📷 Camera", "🐀 Rat val"]

GROUP_DICT = {"🪶 Vogels":"Vogels",
              "🦇 Vleermuizen":"Vleermuizen", 
              "🏠 Vleermuiskast":"Vleermuiskast",
              "📷 Camera":"Camera",
             "🐀 Rat val":"Rat val"}

VLEERMUISKAST_OPTIONS = ["Ja","Nee"]

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


icon_dictionary = {'Vogels': {'Gierzwaluw': {'geen / onbekend': 'swift.png',
   'nestlocatie': 'icons/swift_nest.png',
   'mogelijke nestlocatie': 'swift_mogelijk_nest.png'},
  'Huismus': {'geen / onbekend': 'sparrow.png',
   'nestlocatie': 'icons/sparrow_nest.png',
   'mogelijke nestlocatie': 'sparrow_mogelijk_nest.png'}},
 'Vleermuizen': {'Gewone dwergvleermuis': {'geen / onbekend': 'pippip_foraging.png',
   'zomerverblijfplaats': 'pippip_zommer.png',
   'kraamverblijfplaats': 'pippip_kraam.png'},
  'Ruige dwergvleermuis': {'geen / onbekend': 'ruige_foraging.png',
   'zomerverblijfplaats': 'ruige_zommer.png',
   'kraamverblijfplaats': 'ruige_kraam.png'},
  'Laatvlieger': {'geen / onbekend': 'laatflieger_foraging.png',
   'zomerverblijfplaats': 'laatvlieger_zommer.png',
   'kraamverblijfplaats': 'laatvlieger_kraam.png'}},
 'Vleermuiskast': {},
 'Camera': {'Camera in het veld': 'camera-icon-orange.png',
  'Verwijderd, ratten gedetecteerd': 'camera-icon-red.png',
  'Camera verwijderd, geen ratten gedetecteerd': 'camera-icon-green.png'},
 'Rat val': {'Val nog in het veld': 'rat_trap_orange.png',
  'Val verwijderd. Geen\xa0ratten\xa0gedood': 'rat_trap_green.png',
  'Val verwijderd. Ratten gedood': 'rat_trap_red.png'}}
