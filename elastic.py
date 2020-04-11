from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "178.128.217.254", "port": "9200"}])


# Tạo index "chat_user" để chứa các user
def create_user_index():
    if not es.indices.exists(index="chat_user"):  #1
        body = {  #2
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
            res = es.indices.create(index="chat_user", body=body)  #3
            return res
        except Exception as e:
            print("Already exists")


# Tạo index "chat_user"
create_user_index()


# Truy vấn thông tin user theo tên
async def get_user_by_username(username):
    body = {  #1
        "query": {
            "match": {
                "username": username
            }
        }
    }
    res = es.search(index='chat_user', body=body)  #2
    try:
        return res['hits']['hits'][0]['_source']  #3
    except:
        return []


# Tạo user mới
async def create_user(username, mail, password, id):
    body = {  #1
        "username": username,
        "email": mail,
        "password": password,
        "id": id
    }
    res = es.index(index='chat_user', doc_type='_doc', body=body)  #2
    return res


# Kiểm tra id đã dùng hay chưa
async def check_id(id):
    body = {  #1
        "query": {
            "match": {
                "id": id
            }
        }
    }
    res = es.search(index="chat_user", body=body)  #2
    try:
        return res['hits']['hits'][0]['_source']  #3
    except:
        return []
