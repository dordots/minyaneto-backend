# coding=utf-8

import json
import itertools
import logging
import os
import requests
import time
from datetime import datetime
from elasticsearch import Elasticsearch
from minyaneto.config.release import Config
from minyaneto.service.dal.search_svc import MINYANETO_INDEX, MINYANETO_DOCTYPE
from googletrans import Translator


RAW_PATH = "../data/raw_cities_data/"
DICT_FILE = "../data/dict.json"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def godaven_to_minyaneto(gd_item):
    """

    :param gd_item:
    {
    xxxx"City": "Jerusalem",
    xxxx"longitude": "35.21672",
    xxxx"Nusach": "Ari",
    xxxx"ShabbosMaariv": "",
    xxxx"ShacharisSun5": "9:15:00 AM",
    xxxx"ShacharisMTh1": "6:15:00 AM",
    xxxx"ShacharisMTh2": "7:10:00 AM",
    xxxx"ShacharisMTh3": "8:15:00 AM",
    xxxx"ShacharisSun1": "6:15:00 AM",
    xxxx"ShacharisMTh5": "9:15:00 AM",
    xxxx"ShacharisSun3": "8:15:00 AM",
    xxxx"ShacharisSun2": "7:10:00 AM",
    xxxx"Mincha1": "4:50:00 PM",
    xxxx"Email": "770Jerusalem@gmail.com",
    xxxx"Mincha2": "",
    xxxx"Updated": "11/6/2016 5:06:05 PM",
    xxxx"ShacharisRCh2": "7:10:00 AM",
    xxxx"Maariv Text": "25 minutes after sunset",
    xxxx"FridayMinchaText": "",
    xxxx"Maariv1": "5:40:00 PM",
    xxxx"Address2": "",
    xxxx"Phone1": "",
    xxxx"Miscellaneous": "",
    xxxx"ShacharisTWFTxt": "",
    xxxx"ShabbosMincha": "",
    xxxx"Address": "Lubawitsh 36 Ramat Shlomo",
    xxxx"ShabbosShacharis3": "",
    xxxx"ShacharisRCh3": "8:15:00 AM",
    xxxx"Maariv2": "",
    xxxx"Remote_computer_name": "98.109.112.172",
    xxxx"MinchaText": "15 minutes before sunset",
    xxxx"ShacharisMThTxt": "",
    xxxx"ShacharisRCh1": "6:15:00 AM",
    xxxx"Name": "770 Jerusalem",
    xxxx"Shiur": "",
    "ShacharisTWF2": "7:10:00 AM",
    xxxx"Country": "Israel",
    "ShacharisTWF1": "6:15:00 AM",
    "ShacharisTWF4": "8:45:00 AM",
    "ShacharisTWF5": "9:15:00 AM",
    xxx"latitude": "31.811922",
    xxxx"Added": "10/14/2012 11:15:20 PM",
    "ShabbosShacharis": "9:30:00 AM",
    "ShacharisRCh4": "8:45:00 AM",
    "ShabbosShacharis2": "",
    "ShacharisRCh5": "9:15:00 AM",
    xxxx"ID": "16587",
    "ShabbosMaarivText": "",
    "ShacharisSunTxt": "",
    xxxx"SubmitterName": " &#1502;&#1504;&#1495;&#1501; &#1492;&#1500;&#1508;&#1512;&#1497;&#1503;\xe2\u20ac\u017d ",
    "ShacharisTWF3": "8:15:00 AM",
    "ShacharisSun4": "8:45:00 AM",
    "ShacharisRChTxt": "",
    "Rabbi": "Yosef Izchak Havlin",
    "Browser_type": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4",
    "FridayMincha": "",
    "ShabbosMinchaText": "",
    "ShabbosSchacharisText": "(shabbat mavorchim - 10:00)",
    xxxx"ShacharisMTh4": "8:45:00 AM",
    xxxx"SubmitterEmail": "mmhalperin@gmail.com"
}
    :return:
    """

    def _parse_days(obj):
        if obj.lower().startswith('sun'):
            return ['sunday']
        if obj.lower().startswith('mth'):
            return ['monday', 'thursday']
        if obj.lower().startswith('twf'):
            return ['tuesday', 'wednesday', 'friday']
        if obj.lower().startswith('rch'):
            return ['rosh-chodesh']  # todo: rosh-chodesh handling

    def _try_parse_minyans(key, val):
        if not val or any([x in key.lower() for x in ['text', 'txt']]):  # if key is text/txt
            return None

        if key.lower().startswith('shacharis'):
            name = "shachrit"
            days = _parse_days(key[9:])  # datetime.strptime("9:15:00 AM", '%I:%M:%S %p')
        elif key.lower().startswith('mincha'):
            name = "mincha"
            days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday']
        elif key.lower().startswith('maariv'):
            name = "maariv"
            days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday']
        elif key.lower().startswith('friday'):
            name = "mincha_kabalat_shabat"
            days = ['friday']
        elif key.lower() == 'shabbosmaariv':
            name = "arvit_motzash"
            days = ['saturday']
        elif key.lower() == 'shabbosmincha':
            name = "mincha"
            days = ['saturday']
        elif key.lower().startswith('shabbosshacharis'):
            name = "shachrit"
            days = ['saturday']
        else:
            return None

        try:
            _time = datetime.strptime(val, '%I:%M:%S %p')
            time = _time.strftime("%H:%M:%S")
        except ValueError as e:
            print e
            time = '00:00:00'

        return [{"name": name, "time": time, "day": day} for day in days]

    minyaneto_item = {}
    minyaneto_item['address'] = gd_item['Address'] + ', ' + gd_item['City'] + ', ' + gd_item['Country']
    minyaneto_item['comments'] = gd_item['Miscellaneous']
    minyaneto_item['name'] = gd_item['Name']
    minyaneto_item['nosach'] = gd_item['Nusach']
    minyaneto_item['geo'] = {
        'lat': gd_item['latitude'],
        'lon': gd_item['longitude']
    }
    minyaneto_item['classes'] = True if gd_item['Shiur'] else False
    minyaneto_item['parking'] = None
    minyaneto_item['sefer-tora'] = None
    minyaneto_item['wheelchair-accessible'] = None

    minyaneto_item['minyans'] = []
    for k in gd_item:
        minyans = _try_parse_minyans(k, gd_item[k])
        if minyans:
            minyaneto_item['minyans'].extend(minyans)

    minyaneto_item['_submitter_ip'] = gd_item['Remote_computer_name']
    minyaneto_item['_submitter_name'] = gd_item['SubmitterName']
    minyaneto_item['_submitter_email'] = gd_item['SubmitterEmail']
    minyaneto_item['_added_on'] = time.time()
    minyaneto_item['_orig_godaven'] = gd_item

    return minyaneto_item


def scrape_godaven_to_files():
    # countries1 = ["Japan","South Korea","Vietnam","Singapore","Thailand","India","China","Georgia", "Congo"]
    # countries2 = ["Albania", "Austria", "Belarus", "Belgium", "Bosnia", "Bulgaria", "Croatia", "Czech Republic", "Denmark", "UK", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Moldova", "Montenegro", "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Russia", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine"]

    mexico_cities = ["Acapulco", "Bosques de las Lomas", "Cabo San Lucas", "Cancun", "ciudad de mexico", "Col. Polanco",
                     "Cozumel", "Cuernavaca", "estado de México", "Guadalajara", "Huixquilucan", "Huizquilucan",
                     "Interlomas", "Lomas de las Palmas", "Mexico", "México", "Mexico City", "México city",
                     "Mexico D.F.", "MIGUEL HIDALGO", "Naucalpan", "Naucalpan de Juárez", "Playa del Carmen",
                     "Polanco c.p.", "Polanco, Miguel Hidalgo, Mexico City", "Soliman Bay", "Tecamachalco",
                     "Tecamachalco, Mexico City", "Villa Florence"]
    canada_cities = ["Baysville", "Bracebridge", "Calgary", "Chomedey, LAVAL", "Côte Saint-Luc", "Cote St. Luc",
                     "Cote St. Luc (Suburb of Montreal)", "Cote St-Luc", "Dollard des Ormeaux", "Edmonton",
                     "Fredericton", "Halifax", "Hamilton", "Hampstead", "Innisfil", "Kawartha Lakes", "Kelowna",
                     "Kitchener", "Laval", "London", "Maple (near Richmond Hill)", "Mississauga", "Moncton",
                     "Mont Tremblant", "Montreal", "Montreal-Hampstead", "Nepean", "Nepean (near Ottawa)",
                     "Niagara Falls", "Ottawa", "Outremont", "Pierrefonds", "Quebec", "Richmond",
                     "Richmond Hill ( Toronto )", "Saint-laurent", "Saint-Laurent, Quebec", "Ste-Agathe-des-Monts",
                     "St-Laurent, Montreal", "Sudbury", "Surrey", "Surrey (White Rock)", "Thornhill", "Toronto",
                     "Toronto (North York)", "Vancouver", "Vaughan", "Victoria", "Ville Saint Laurent",
                     "Ville st laurent", "Ville St-Laurent (Suburb of Montreal)", "Wasaga Beach", "Waterloo",
                     "Westmount (Montreal)", "Weston", "Winnipeg"]
    south_africa_cities = ["Brentwoork Park, Benoni, Gauteng", "Cape Town", "Constantia - Cape Town",
                           "Durban, Kwa-Zulu Natal", "Edenvale", "Fairmount", "Gallo Manor, Sandton (Johannesburg)",
                           "Groenkloof, Pretoria", "Hyde Park. Sandton", "Johannesberg", "Johannesburg",
                           "Johannesburg (Sandton)", "Percelia Estate, Johannesburg", "River club",
                           "Sandton (Johannesburg)", "Sandton Central", "Savoy, Johannesburg", "Sea Point",
                           "Umhlanga Rocks"]
    australia_cities = ["Balaclava (Melbourne)", "Bondi", "Bondi (Sydney)", "Bondi Beach (Sydney)", "Bondi Junction",
                        "Bondi Junction (Sydney)", "Brisbane", "Caulfield (Melbourne)", "Caulfield North", "Coogee",
                        "Double Bay (Sydney)", "Dover Heights (Sydney)", "East Bentleigh", "East Brighton",
                        "East St Kilda", "East St Kilda (Melbourne)", "Forrest", "Glenside", "Gold Coast",
                        "Maroubra (Sydney)", "Melbourne", "Menora (Perth)", "Moorabbin", "Neutral Bay (Sydney)",
                        "Noranda (Perth)", "North Bondi (Sydney)", "North Caulfield", "Parramatta", "Perth",
                        "Port Melbourne", "Ripponlea", "Rose Bay (Sydney)", "South Caulfield", "St Ives (Sydney)",
                        "St. Kilda East", "Surfers Paradise", "Sydney"]
    israel_cities = ["Aderet", "Aiport City", "Airport City", "Akko", "Alon Shvut", "Arad", "Ariel", "Arnona",
                     "Asfar Israel", "Ashdod", "Ashkelon", "Asseret", "Azor", "Azor Zayin - Area 7, Ashdod",
                     "Bait Vagan", "Bar Ilan University, Ramat Gan", "Bat Ayin", "Bat Yam", "Bat-yam", "Bayit Vegan",
                     "Beer Sheva", "Beer Yakov", "Beersheva", "Beit El", "Beit Gamliel", "Beit Shemesh", "Beit Yatir",
                     "Beitar", "Beitar Illit", "Beith Shemesh, Ramath B", "Benei Yehoda", "Bet Shemesh", "Bet zayit",
                     "Betar Illit", "Bikat Hayarden", "Binyamina", "Bitar illit", "Bnei beraq", "Bnei Brak", "Bnei Ram",
                     "Caesarea", "Carmiel", "Chalutzah", "Efrat", "Eilat", "Ein Tzurim", "Elad", "Elazar", "Eli",
                     "Elkana", "Elkanah", "Even Yehuda", "Gan Ner", "Ganei Modiin,Yishuv Chashmonaim", "Ganei Tikva",
                     "Gilat", "Gimzo", "Ginot Shomron", "Gitit", "Givat Mordechai, Jerusalem", "Givat Shmuel",
                     "Givat Shmuel, Jerusalem", "Givat Shmul", "Givat Zeev", "Givatayim", "Gush Etzyon", "Hadera",
                     "Hadid", "Haifa", "Haifav", "Har Hebron", "Har Hotzvim, Jerusalem", "Har Nof (Jerusalem)",
                     "Har Nof Jerusalem", "Har Nof Yerushalyim", "Har Nof, Jerusalem", "Har Nof, POB 43033, Jerusalem",
                     "Hashmonaim", "Hatzor HaGlilit", "Hazon", "Hebron", "Herzliya", "Herzliya Pituach", "Hod HaSharon",
                     "Holon", "Itamar", "Jerusalem", "Karmiel", "Karnei Shomron", "Katsrin", "Kedumim", "Kefar Sava",
                     "Kefar yavez", "Kfar Adumim", "Kfar Chabad", "Kfar Chabad Bet", "Kfar Gidon", "Kfar Habad",
                     "Kfar hananya", "Kfar Haroe", "Kfar Saba", "Kfar Tapuach", "Kfar yona", "Kibbutz Alumim",
                     "Kibbutz Beerot Yitzchak", "Kibbutz Beit Rimon", "Kibbutz Maale Gilboa", "Kinneret",
                     "Kiriat Tivon", "Kiriyat Arbah", "Kiriyat Yam", "Kiryat Arba", "Kiryat Ata", "Kiryat Shemona",
                     "Kiryat Shmona", "Kiryat Yam", "Kiryat Yearim", "Kiryat Yearim / Telshe Stone", "Kochav Yair",
                     "Kvutzat Yavne", "Lod", "Maale adoumim", "Maale Adumim", "Maale Gilboa", "Maaleh Adumim", "Maalot",
                     "Ma'alot", "Maccabbim", "Male adommim", "Mazkeret Batya", "Meitar", "Mevaseret Zion",
                     "Migdal Haemek", "Mitzpe Netofa", "Mitzpeh Yericho", "Modi`in", "Modiin", "Modiin Ilit",
                     "Modiin-Maccabim-Reut", "Moreshet", "Moshav Ginaton", "Moshav Matityahu", "Moshav Merchavia",
                     "Moshav Olesh", "Moshav Pakin", "Nahariya", "Naharya", "Neriah", "Nes Tzionah", "Nesher",
                     "Ness Tziona", "Netanya", "Neve Daniel", "Nof Ayalon", "Ohr Yehudah", "Olga", "Omer", "Or Yehuda",
                     "Oranit", "Pardes Hanna", "Patish", "Pduel", "Pekiin Hadasa", "Petach Tikva", "Petach Tikvah",
                     "Petah Tikva", "Petah-Tikva", "Qatsrin", "Qiryat atta", "Qiryat Ekron", "Raanana", "Ra'anana",
                     "Ramat Aviv, Tel Aviv", "Ramat Beit Shemesh", "Ramat Beit Shemesh A", "Ramat beit shemesh aleph",
                     "Ramat Bet Shemesh", "Ramat gan", "Ramat Hagolan", "Ramat haKHaYaL, Tel Aviv", "Ramat Hasharon",
                     "Ramat Shlomo, Jerusalem", "Ramla", "Rammat-Gan", "Ramot 01 (Ramot Aleph), Jerusalem",
                     "Ramot, Jerusalem", "Rechasim", "Rechavia, Jerusalem", "Rechovot", "Rehavia, Jerusalem", "Rehovot",
                     "Revava", "Rishon LeTsiyon", "Rishon Lezion", "Rishon LTzion", "Rosh Haayin", "Rosh Ha'ayin",
                     "Rosh Pinna", "Rova 7, Ashdod", "Rova Zayin, City of Ashdod", "Saad", "Safed", "Sde Uziyahu",
                     "Sede Ilan", "Shaalvim", "Sha'alvim", "Shaaray Tikva", "shilo", "Shoresh", "Shuva",
                     "South East Gush Etzion", "Talmon", "Teana, Efrat", "Tekoa", "Tel Aviv", "Tel Aviv-Yafo",
                     "Tel Mond", "Telshe Stone/Kiryat Yearim", "Telz Stone", "Telzstone", "Tiberias", "Tirat Yehuda",
                     "Train Line", "Tsfat", "Tzefat", "Tzfat", "Tzrifin", "Yad Binyamin", "Yad Rambam",
                     "Yavneel, Breslov City", "Yehud", "Yeruham", "Yesud Hamalah, Upper Galilee", "ZEFAT",
                     "Zichron Yaakov", "Zichron Yakov", "Zikhron Yaakov", "Zikhron Ya'akov", "Zur Hadassah"]
    cities = itertools.chain(mexico_cities, canada_cities, south_africa_cities, australia_cities, israel_cities)

    for city in cities:
        filename = RAW_PATH + city + ".txt"
        if os.path.isfile(filename):
            continue
        url = "http://godaven.com/db/davenapi.aspx?results=20&city=" + city
        res = requests.get(url)
        if res.status_code == 200:
            if '/' in city:
                filename = RAW_PATH + city.replace('/', '--') + ".txt"

            with open(filename, "w") as f:
                f.write(res.text.encode('utf-8'))


def add_godaven_minyans_from_files_to_elastic():
    es = Elasticsearch(Config.ELASTIC_SEARCH_HOSTS)

    for filename in os.listdir(RAW_PATH):
        logger.info(filename)
        if filename.endswith(".txt"):
            with open(os.path.join(RAW_PATH, filename)) as f:
                data = f.read()
                try:
                    godaven_synagouges = json.loads("[{" + data[32:-3] + "]")
                except Exception as e:
                    raise e

                for godaven_synagouge in godaven_synagouges:
                    minyaneto_synagouge = godaven_to_minyaneto(godaven_synagouge)
                    res = es.index(index=MINYANETO_INDEX, doc_type=MINYANETO_DOCTYPE, body=minyaneto_synagouge)
                    print res



def create_translator():
    def _word(str):
        import re
        return " ".join(re.findall("[a-zA-Z]+", str)).lower()

    words = set()
    _dict = {}
    for filename in os.listdir(RAW_PATH):
        if filename.endswith(".txt"):
            with open(os.path.join(RAW_PATH, filename)) as f:
                data = f.read()
                godaven_synagouges = json.loads("[{" + data[32:-3] + "]")

                for godaven_synagouge in godaven_synagouges:
                    minyaneto_synagouge = godaven_to_minyaneto(godaven_synagouge)
                    words.update([_word(x) for x in minyaneto_synagouge['comments'].split(' ')])
                    words.update([_word(x) for x in minyaneto_synagouge['name'].split(' ')])


    for word in words:
        google_translate = Translator()
        res = google_translate.translate(word, src='en', dest='iw')
        _dict[word] = res.text

    with open(DICT_FILE, "w") as f:
        f.write(json.dumps(_dict, sort_keys=True, indent=4))

    pass



if __name__ == '__main__':
    # scrape_godaven_to_files()
    # add_godaven_minyans_from_files_to_elastic()
    create_translator()
