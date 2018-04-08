# coding=utf-8

import json
import logging
import os
import time
from datetime import datetime
from elasticsearch import Elasticsearch
from minyaneto.config.release import Config
from minyaneto.service.dal.search_svc import MINYANETO_INDEX, MINYANETO_DOCTYPE

RAW_PATH = "../data/kipa/"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def kipa_to_minyaneto(kipa_item):
    def _try_parse_minyans(key, val):

        if key == u'שחרית בחול':
            name = "shachrit"
            days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday']
        elif key == u'שחרית בראש חודש':
            name = "shachrit"
            days = ['rosh-chodesh']
        elif key == u'שחרית ביום שישי':
            name = "shachrit"
            days = ['friday']
        elif key == u'שחרית בשני וחמישי':
            name = "shachrit"
            days = ['monday', 'thursday']
        elif key == u'מנחה בחול':
            name = "mincha"
            days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday']
        elif key == u'ערבית בחול':
            name = "maariv"
            days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday']
        elif key == u'ערבית בצאת שבת':
            name = "maariv"
            days = ['saturday']
        elif key == u'מנחה ביום שישי':
            name = "mincha_kabalat_shabat"
            days = ['friday']
        elif key == u'תפילה בערב שבת':
            name = "arvit_motzash"
            days = ['saturday']
        elif key == u'מנחה בשבת':
            name = "mincha"
            days = ['saturday']
        elif key == u'שחרית בשבת':
            name = "shachrit"
            days = ['saturday']
        else:
            return None

        try:
            _time = datetime.strptime(val[:5], '%H:%M')
            time = _time.strftime("%H:%M:%S")
        except ValueError as e:
            print e
            time = '00:00:00'

        return [{"name": name, "time": time, "day": day} for day in days]

    if 'coordinates' not in kipa_item:
        print 'missing coordinates:'
        print kipa_item
        return None

    minyaneto_item = {}
    minyaneto_item['address'] = kipa_item['address'] + u', ישראל'
    minyaneto_item['name'] = kipa_item['title']
    minyaneto_item['nosach'] = kipa_item['prayer_kind'].replace(u'נוסח תפילה ', '')
    minyaneto_item['geo'] = {
        'lat': kipa_item['coordinates']['lat'],
        'lon': kipa_item['coordinates']['lng']
    }
    minyaneto_item['classes'] = None
    minyaneto_item['parking'] = None
    minyaneto_item['sefer-tora'] = None
    minyaneto_item['wheelchair-accessible'] = u' גישה לנכים' in kipa_item['other_services']

    minyaneto_item['minyans'] = []
    for k in kipa_item['prayer_times']:
        minyans = _try_parse_minyans(k, kipa_item['prayer_times'][k])
        if minyans:
            minyaneto_item['minyans'].extend(minyans)

    return minyaneto_item


def extract_synagogues():
    synagouges = []

    for filename in os.listdir(RAW_PATH):
        logger.info(filename)
        if filename.endswith(".json"):
            with open(os.path.join(RAW_PATH, filename)) as f:
                kipa_synagouge = json.loads(f.read().decode('windows-1255'))

                synagouge = kipa_to_minyaneto(kipa_synagouge)
                if not synagouge:
                    continue
                synagouge['_added_on'] = synagouge['_last_modified_on'] = time.time()
                synagouge['_origin'] = "kipa"
                synagouge['_orig'] = kipa_synagouge

                synagouges.append(synagouge)

    return synagouges


def add_to_elastic(synagouges):
    es = Elasticsearch(Config.ES_HOSTS)
    for synagouge in synagouges:
        try:
            res = es.index(index=MINYANETO_INDEX, doc_type=MINYANETO_DOCTYPE, body=synagouge)
            print res
        except Exception as e:
            print e


if __name__ == '__main__':
    synagouges = extract_synagogues()
    # add_to_elastic(synagouges)
    print 'done'
