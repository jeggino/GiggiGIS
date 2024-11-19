# --- LOGO/MENU' ---
IMAGE_2 ="icon/menu.jpg"


# --- DIMENSIONS ---
OUTPUT_width = '95%'
OUTPUT_height = 550
    

# --- DIMENSIONS ---
ICON_SIZE = (20,20)
ICON_SIZE_huismus = (28,28)
ICON_SIZE_rat_maybe = (255,150)

# --- OPTIONS ---
soortgroup =["📷 Camera", "💉 Rat val", '🪤 Vangkooi','🔫 Rat geschoten']
DICT_SORTGROUP = {"📷 Camera":"Camera", "💉 Rat val":"Rat val",'🪤 Vangkooi':'Vangkooi','🔫 Rat geschoten':'Rat geschoten'}
choice_opdracht = [DICT_SORTGROUP[item] for item in soortgroup]

CAMERA_OPTIONS = ["Camera in het veld","Verwijderd, ratten gedetecteerd","Camera verwijderd, geen ratten gedetecteerd",
                  "Waarneming rat doorgegeven, geen actie op ondernomen"]

RAT_VAL_OPTIONS = ['Schietval in veld', 'Schietval in veld rat gedood','Schietval verwijderd, geen rat gedood','Schietval verwijderd, rat gedood']

RAT_VANGKOOI_OPTIONS = ['vangkooi in veld','vangkooi in veld, rat gevangen','vangkooi verwijderd, rat gevangen','vangkooi verwijderd, geen rat gevangen']

icon_dictionary = {
                   'Camera': {'Camera in het veld': 'icon/camera-icon-orange.png',
                              'Verwijderd, ratten gedetecteerd': 'icon/camera-icon-red.png',
                              'Camera verwijderd, geen ratten gedetecteerd': 'icon/camera-icon-green.png',
                              'Waarneming rat doorgegeven, geen actie op ondernomen': 'icon/rat_maybe_2.png'},
                   'Rat val': {'Schietval in veld': 'icon/rat_trap_orange.png',
                               'Schietval in veld rat gedood': 'icon/rat_trap_green.png',
                               'Schietval verwijderd, geen rat gedood': 'icon/rat_trap_red.png',
                               'Schietval verwijderd, rat gedood': 'icon/rat_trap_purple.png'},
                   'Vangkooi': {'vangkooi in veld':'icon/rat_cage_veld_Nogevangen.png',
                                'vangkooi in veld, rat gevangen':'icon/rat_cage_veld_gevangen.png',
                                'vangkooi verwijderd, rat gevangen':'icon/rat_cage_noveld_gevangen.png',
                                'vangkooi verwijderd, geen rat gevangen':'icon/rat_cage_noveld_Nogevangen.png'},
    'Rat geschoten':{'Rat geschoten':'icon/rat_shot.png'}
}
