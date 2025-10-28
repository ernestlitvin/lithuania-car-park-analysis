# --- DICTIONARIES FOR CLEANING DATA ---

CORRECTIONS = {
    'VW': 'VOLKSWAGEN',
    'VOLKSWAGEN. VW': 'VOLKSWAGEN',
    'VOLKSWAGEN-VW': 'VOLKSWAGEN',
    'VOLKSWAGEN-VW VOLKSWAGEN. VW': 'VOLKSWAGEN',
    'MERCEDES-BENZ': 'MERCEDES',
    'MERCEDES BENZ': 'MERCEDES',
    'BAYER.MOT.WERKE-BMW': 'BMW',
    'BMW AG': 'BMW',
    'BMW I': 'BMW',
    'DAIMLERCHRYSLER (D)': 'CHRYSLER',
    'FORD (D)': 'FORD',
    'ROVER': 'LAND ROVER',
    'TOYOTA MEM (B)': 'TOYOTA',
    'SKODA (CZ)': 'SKODA',
    'SEAT (E)': 'SEAT',
    'RENAULT/CARPOL': 'RENAULT',
    'RENAULT (F)': 'RENAULT',
    'VOLVO (S)': 'VOLVO',
    'PEUGEOT (F)': 'PEUGEOT',
    'AUDI AUDI': 'AUDI',
    'FUJI HEAVY IND.(J)': 'SUBARU',
    'NISSAN EUROPE (F)': 'NISSAN',
    'MITSUBISHI (J)': 'MITSUBISHI',
    'FORD (D) FORD': 'FORD',
    'KIA MOTOR (ROK)': 'KIA',
    'VOLVO (S) VOLVO': 'VOLVO',
    'TESLA MOTORS': 'TESLA',
    'ADAM OPEL GMBH': 'OPEL',
    'SKODA (CZ) SKODA': 'SKODA',
    'HYUNDAI MOTOR (ROK)': 'HYUNDAI',
    'JAGUAR LAND ROVER LIMITED': 'LAND ROVER',
    'OPEL OPEL': 'OPEL',
    'BAYER.MOT.WERKE-BMW BMW': 'BMW',
    'CITROEN (F)': 'CITROEN',
    'B.M.W.': 'BMW',
    'MAZDA (J)': 'MAZDA',
    'FIAT (I)': 'FIAT',
    'DAIMLERCHRYSLER (USA)': 'CHRYSLER',
    'HONDA MOTOR (J)': 'HONDA',
    'DAIMLERCHRYSLER AG': 'CHRYSLER',
    'FORD W GMBH': 'FORD',
    'MERCEDES-AMG': 'MERCEDES',
    'HONDA (GB)': 'HONDA',
    'LANDROVER': 'LAND ROVER',
    'DAIMLER AG': 'MERCEDES',
    'TOYOTA EUROPE (B)': 'TOYOTA',
    'FUJI HEAVY IND. (J)': 'SUBARU',
    'ALFA': 'ALFA ROMEO',
    'DS': 'CITROEN',
    'SSANGYONG': 'SSANG YONG'
}

CORRECTIONS_MODELS = {
    'AUDI A6': 'A6',
    'AUDI A4': 'A4',
    'AUDI A3': 'A3',
    'TOYOTA RAV4': 'RAV4',
    'TOYOTA AVENSIS': 'AVENSIS',
    'TOYOTA COROLLA': 'COROLLA',
    'TOYOTA AURIS': 'AURIS',
    'TOYOTA C-HR': 'C-HR',
    'TOYOTA YARIS': 'YARIS',
    'TOYOTA COROLLA VERSO': 'COROLLA VERSO',
    'TOYOTA PRIUS': 'PRIUS',
    'NISSAN QASHQAI': 'QASHQAI',
    'NISSAN X-TRAIL': 'X-TRAIL',
    'HONDA CR-V': 'CR-V'
}

COLORS_UPDATE = {
    'PILKA': 'Grey',
    'JUODA': 'Black',
    'MĖLYNA': 'Blue',
    'BALTA': 'White',
    'RAUDONA': 'Red',
    'ŽALIA': 'Green',
    'RUDA': 'Brown'
}

# --- LOADING DATA ---

FILE_PATH = 'Atviri_TP_parko_duomenys.csv'

COLS_TO_USE = [
    'MARKE',
    'KOMERCINIS_PAV',
    'DEGALAI',
    'GAMYBOS_METAI',
    'PIRM_REG_DATA',
    'KATEGORIJA_KLASE',
    'SPALVA',
    'GALIA',
    'SAVIVALDYBE'
]

DATA_TYPES = {
    'MARKE': 'category',
    'KOMERCINIS_PAV': 'category',
    'KATEGORIJA_KLASE': 'category',
    'DEGALAI': 'category',
    'SPALVA': 'category',
    'SAVIVALDYBE': 'category'
}

LT_COLS = {
    'MARKE': 'mark',
    'KOMERCINIS_PAV': 'model',
    'DEGALAI': 'fuel_type',
    'GAMYBOS_METAI': 'production_year',
    'PIRM_REG_DATA': 'first_reg_date',
    'KATEGORIJA_KLASE': "car_cat",
    'SPALVA': 'color',
    'GALIA': 'power',
    'SAVIVALDYBE': 'municipality'
}

# --- LISTS FOR FILTERING ---

GARBAGE_MARK = ['NUASMENINTA']
GARBAGE_MODEL = ['NUASMENINTA', '-']
GARBAGE_MUNICIPALITY = ['ČEKIJA.', 'LATVIJA.', 'BALTARUSIJA.', 'JUNGTINĖ KARALYSTĖ.', 'KANADA.']

# --- LISTS FOR HYPOTHESISES ---

GERMAN_MARKS = ['VOLKSWAGEN', 'AUDI', 'BMW', 'OPEL', 'MERCEDES', 'SMART', 'PORSCHE']
IS_VILNIUS_LIST = ['VILNIAUS M. SAV.', 'VILNIAUS R. SAV.']