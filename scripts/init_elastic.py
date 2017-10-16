from elasticsearch import Elasticsearch
from minyaneto.config.release import Config
from minyaneto.service.dal.search_svc import Dao, MINYANETO_INDEX, MINYANETO_DOCTYPE


def init_elastic():
    es = Elasticsearch(Config.ELASTIC_SEARCH_HOSTS)

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

    res = es.indices.create(index=MINYANETO_INDEX, ignore=400, body=mapping)
    print(res)


if __name__ == '__main__':
    init_elastic()
