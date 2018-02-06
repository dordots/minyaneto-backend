from elasticsearch import Elasticsearch

MINYANETO_INDEX = 'minyaneto'
MINYANETO_DOCTYPE = 'synagogues'


class Dao(object):
    def __init__(self, es_hosts):
        self.es = Elasticsearch(es_hosts)

    def add_synagogue(self, synagouge_dict):
        res = self.es.index(index=MINYANETO_INDEX, doc_type=MINYANETO_DOCTYPE, body=synagouge_dict)
        return res['_id']

    def update_synagogue(self, id,  synagouge_dict):
        res = self.es.update(index=MINYANETO_INDEX,doc_type=MINYANETO_DOCTYPE, id=id, body={"doc": synagouge_dict})

    def search_synagogues_in_rectangle(self, geo_top_left, geo_bottom_right, max_hits=10):
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

        res = self.es.search(index=MINYANETO_INDEX, doc_type=MINYANETO_DOCTYPE, body=b, size=max_hits)
        return res['hits']['hits']

    def search_synagogues_in_circle(self, center, radius, max_hits=10):
        b = {
            "query": {
                "bool" : {
                    "must" : {
                        "match_all" : {}
                    },
                    "filter" : {
                        "geo_distance" : {
                            "distance" : radius,
                            "geo" : center
                        }
                    }
                }
            }
        }

        res = self.es.search(index=MINYANETO_INDEX, doc_type=MINYANETO_DOCTYPE, body=b, size=max_hits)
        return res['hits']['hits']

    def get_synagogue(self, id):
        res = self.es.get(index=MINYANETO_INDEX, id=id)
        return res
