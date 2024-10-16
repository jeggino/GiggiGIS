# --- COSTANTS ---
WAARNEMERS = ["Luigi","Daan"]
HELP_FUNCTIE = "Zomer- of kraamverblijfplaats: De vrouwtjes wonen in de zomer in kraamverblijfplaatsen. Hier brengt ze hun jongen groot. voorkomende leven ze gecombineerd in groepen (kolonies). \nZomer- of mannenverblijfplaats: De mannetjes wonen in de zomer soms solitair, soms in groepen, maar altijd op een andere plaats dan de vrouwtjes van hun soort. \nTijdelijke of paarverblijfplaats: Vaak kennen vleermuizen ook tussenkwartieren, waar ze slechts kort verblijven tijdens de reis van hun winter- naar zomerkolonie. Zo trekken zowel de mannetjes als de vrouwtjes aan het einde van de zomer naar speciale paarkwartieren, waar ze slechts kort verblijven. Winterverblijfplaats: Vleermuizen overwinteren in gebouwen, bunkers, ijskelders, groeven en boomholtes."

GROUP = ["🦇 Vleermuizen","🪶 Vogels",  "🏠 Vleermuiskast",
         "📷 Camera", "🐀 Rat val", '𐂺 Vangkooi']

GROUP_DICT = {"🪶 Vogels":"Vogels",
              "🦇 Vleermuizen":"Vleermuizen", 
              "🏠 Vleermuiskast":"Vleermuiskast",
              "📷 Camera":"Camera",
             "🐀 Rat val":"Rat val",
              '𐂺 Vangkooi':'Vangkooi'}

VLEERMUISKAST_OPTIONS = ["Bewoond","Onbewoond"]

CAMERA_OPTIONS = ["Camera in het veld","Verwijderd, ratten gedetecteerd","Camera verwijderd, geen ratten gedetecteerd",
                  "Waarneming rat doorgegeven, geen actie op ondernomen"]

RAT_VAL_OPTIONS = ['Schietval in veld', 'Schietval in veld rat gedood','Schietval verwijderd, geen rat gedood','Schietval verwijderd, rat gedood']

RAT_VANGKOOI_OPTIONS = ['vangkooi in veld','vangkooi in veld, rat gevangen','vangkooi verwijderd, rat gevangen','vangkooi verwijderd, geen rat gevangen']



BAT_NAMES = ['Gewone dwergvleermuis','Ruige dwergvleermuis', 'Laatvlieger','Rosse vleermuis','Meervleermuis','Watervleermuis','...Andere(n)']

BAT_BEHAVIOURS = ['foeragerend', 'uitvliegend','invliegend', 'overvliegend', 
         'zwermend', 'sporen', 'balts', 'verkeersslachtoffer']

BAT_FUNCTIE = ['geen / onbekend','zomerverblijfplaats','kraamverblijfplaats','paarverblijfplaats', 'winterverblijfplaats']

BAT_VERBLIJF = ['geen / onbekend', 'dakgoot', 'spouwmuur', 'daklijst',
       'kantpan', 'regenpijp', 'holte', 'raamkozijn', 'luik', 'scheur',
       'schoorsteen', 'gevelbetimmering', 'nokpan', 'dakpan',
       'vleermuiskast', 'openingen in dak', 'dakkapel', 'schors','..ander']

BIRD_NAMES = ['Gierzwaluw','Huismus']

BIRD_NAMES_ANDER = ['...Andere(n)']

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
                   'Vleermuizen': {'Gewone dwergvleermuis': {'geen / onbekend': 'icons/pippip_geen.png',
                                                             'zomerverblijfplaats': 'icons/pippip_zommer.png',
                                                             'kraamverblijfplaats': 'icons/pippip_kraam.png',
                                                            'paarverblijfplaats': 'icons/pippip_paar.png',
                                                            'winterverblijfplaats': 'icons/pippip_winter.png'},
                                   'Ruige dwergvleermuis': {'geen / onbekend': 'icons/ruige_geen.png',
                                                             'zomerverblijfplaats': 'icons/ruige_zommer.png',
                                                             'kraamverblijfplaats': 'icons/ruige_kraam.png',
                                                            'paarverblijfplaats': 'icons/ruige_paar.png',
                                                            'winterverblijfplaats': 'icons/ruige_winter.png'},
                                   'Laatvlieger': {'geen / onbekend': 'icons/laat_geen.png',
                                                             'zomerverblijfplaats': 'icons/laat_zommer.png',
                                                             'kraamverblijfplaats': 'icons/laat_kraam.png',
                                                            'paarverblijfplaats': 'icons/laat_paar.png',
                                                            'winterverblijfplaats': 'icons/laat_winter.png'},
                                  'Rosse vleermuis': {'geen / onbekend': 'icons/rosse_geen.png',
                                                             'zomerverblijfplaats': 'icons/rosse_zommer.png',
                                                             'kraamverblijfplaats': 'icons/rosse_kraam.png',
                                                            'paarverblijfplaats': 'icons/rosse_paar.png',
                                                            'winterverblijfplaats': 'icons/rosse_winter.png'},
                                   'Meervleermuis': {'geen / onbekend': 'icons/meer_geen.png',
                                                             'zomerverblijfplaats': 'icons/meer_zommer.png',
                                                             'kraamverblijfplaats': 'icons/meer_kraam.png',
                                                            'paarverblijfplaats': 'icons/meer_paar.png',
                                                            'winterverblijfplaats': 'icons/meer_winter.png'},
                                   'Watervleermuis': {'geen / onbekend': 'icons/water_geen.png',
                                                             'zomerverblijfplaats': 'icons/water_zommer.png',
                                                             'kraamverblijfplaats': 'icons/water_kraam.png',
                                                            'paarverblijfplaats': 'icons/water_paar.png',
                                                            'winterverblijfplaats': 'icons/water_winter.png'},
                                    '...Andere(n)': {'geen / onbekend': 'icons/bat_geen.png',
                                                             'zomerverblijfplaats': 'icons/bat_zommer.png',
                                                             'kraamverblijfplaats': 'icons/bat_kraam.png',
                                                            'paarverblijfplaats': 'icons/bat_paar.png',
                                                            'winterverblijfplaats': 'icons/bat_winter.png'}},
                   'Vleermuiskast': {"Bewoond":"icons/bat_bow_full.jpg",
                                     "Onbewoond":"icons/bat_box_empty.jpg"},
                   'Camera': {'Camera in het veld': 'icons/camera-icon-orange.png',
                              'Verwijderd, ratten gedetecteerd': 'icons/camera-icon-red.png',
                              'Camera verwijderd, geen ratten gedetecteerd': 'icons/camera-icon-green.png',
                              'Waarneming rat doorgegeven, geen actie op ondernomen': 'icons/rat_maybe_2.png'},
                   'Rat val': {'Schietval in veld': 'icons/rat_trap_orange.png',
                               'Schietval in veld rat gedood': 'icons/rat_trap_green.png',
                               'Schietval verwijderd, geen rat gedood': 'icons/rat_trap_red.png',
                               'Schietval verwijderd, rat gedood': 'icons/rat_trap_purple.png'},
                   'Vangkooi': {'vangkooi in veld':'icons/rat_cage_veld_Nogevangen.png',
                                'vangkooi in veld, rat gevangen':'icons/rat_cage_veld_gevangen.png',
                                'vangkooi verwijderd, rat gevangen':'icons/rat_cage_noveld_gevangen.png',
                                'vangkooi verwijderd, geen rat gevangen':'icons/rat_cage_noveld_Nogevangen.png'},
                  "Vogels-Overig": {'...Andere(n)': {'geen / onbekend': 'icons/geen_nest.png',
                                                     'nestlocatie': 'icons/bird_nest.png',
                                                     'mogelijke nestlocatie': 'icons/mogelijk_nest.png'}}
                  }

DICTIONARY_USERS = {"Luigi": ["Niet gespecificeerd"],
                   "Daan": ["Niet gespecificeerd","Ratten Terschelling"]
                   }

DICTIONARY_PROJECTS = {"Overig":["Vogels","Vleermuizen","Vleermuiskast","Vogels-Overig"],
                      "Ratten Terschelling":["Camera","Rat val",'Vangkooi'],
                      "Admin":["Vogels","Vleermuizen","Vleermuiskast","Camera","Rat val",'Vangkooi',"Vogels-Overig"],
                       "Bats-balkans":["Vleermuizen"]}
