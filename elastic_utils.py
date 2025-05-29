from elasticsearch import Elasticsearch

INDEX_NAME = "restaurants"

def get_es_client():
    return Elasticsearch(hosts=["http://elasticsearch:9200"])

def create_index(es):
    mapping = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "kuromoji_analyzer": {
                        "type": "custom",
                        "tokenizer": "kuromoji_tokenizer"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "restaurant_id": {"type": "keyword"},
                "restaurant_name": {
                    "type": "text",
                    "analyzer": "kuromoji_analyzer"
                },
                "description": {
                    "type": "text",
                    "analyzer": "kuromoji_analyzer"
                },
                "location": {"type": "geo_point"},
                "cuisine_type": {"type": "keyword"},
                "rating": {"type": "float"}
            }
        }
    }

    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, settings=mapping["settings"], mappings=mapping["mappings"])
        print(f"Index '{INDEX_NAME}' created.")
    else:
        print(f"Index '{INDEX_NAME}' đã tồn tại.")
