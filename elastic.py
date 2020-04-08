from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "178.128.217.254", "port": "9200"}])


def create_user_index():
    if not es.indices.exists(index="chat_user"):
        body = {
            "mappings": {
                "properties": {
                    "username": {"type": "keyword"},
                    "email": {"type": "text"},
                    "password": {"type": "text"},
                    "id": {"type": "keyword"}
                }
            }
        }
        try:
            res = es.indices.create(index="chat_user", body=body)
            return res
        except Exception as e:
            print("Already exists")


create_user_index()


async def get_user_by_username(username,):
    body = {
        "query": {
            "match": {
                "username": username
            }
        }
    }
    res = es.search(index='chat_user', body=body)
    try:
        return res['hits']['hits'][0]['_source']
    except:
        return []


async def create_user(username, mail, password, id):
    body = {
        "username": username,
        "email": mail,
        "password": password,
        "id": id
    }
    res = es.index(index='chat_user', doc_type='_doc', body=body)
    return res


async def check_id(id):
    body = {
        "query": {
            "match": {
                "id": id
            }
        }
    }
    res = es.search(index="chat_user", body=body)
    try:
        return res['hits']['hits'][0]['_source']
    except:
        return []
