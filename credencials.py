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

ICON = {"Gierzwaluw":"https://cdn-icons-png.flaticon.com/128/732/732126.png",
        "Huismus":"https://cdn-icons-png.flaticon.com/128/8531/8531874.png",
        "Bat": "https://cdn-icons-png.flaticon.com/128/2250/2250418.png",
        "Nest_bezet": "icons/bat_bow_full.jpg",
        "Nest_unbezet": "icons/bat_box_empty.jpg",
        "Swift_nest": "icons/swift_nest.jpg"}

icon_dictionary['Vogels'] = {
    'Gierzwaluw':{'geen / onbekend':"swift.png", 
                  'nestlocatie':"swift_nest.png",
                  'mogelijke nestlocatie':"swift_mogelijk_nest.png"},
    'Huismus':{'geen / onbekend':"sparrow.png", 
              'nestlocatie':"sparrow_mogelijk_nest.png",
              'mogelijke nestlocatie':"sparrow_nest.png"},
}
