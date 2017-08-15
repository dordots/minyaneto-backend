from elasticsearch import Elasticsearch

MINYANETO_INDEX = 'minyaneto'


class Dao(object):
    def __init__(self, es_hosts):
        self.es = Elasticsearch(es_hosts)

    def add_synagogue(self, synagouge_dict):
        res = self.es.index(index=MINYANETO_INDEX, doc_type='synagogues', body=synagouge_dict)
        return res['_id']

    def search_synagogues(self, geo_top_left, geo_bottom_right):
        b = {
            "query": {
                "geo_bounding_box": {
                    "geo": {
                        "top_left": geo_top_left,
                        "bottom_right": geo_bottom_right
                    }
                }
            }
        }

        res = self.es.search(index=MINYANETO_INDEX, doc_type='synagogues', body=b)
        return res['hits']['hits']
