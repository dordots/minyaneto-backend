from elasticsearch import Elasticsearch
from minyaneto.config.release import Config
from minyaneto.service.dal.search_svc import MINYANETO_INDEX, MINYANETO_DOCTYPE, MINYANETO_INDEX_TEST


def init_elastic(index):
    es = Elasticsearch(Config.ES_HOSTS)

    mapping = {
        "mappings": {
            MINYANETO_DOCTYPE: {
                "properties": {
                    "geo": {
                        "type": "geo_point"
                    }
                }
            }
        }
    }

    res = es.indices.create(index=index, ignore=400, body=mapping)
    print(res)


if __name__ == '__main__':
    # init_elastic(MINYANETO_INDEX)
    init_elastic(MINYANETO_INDEX_TEST)
