from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from indeces_creator import create

mappings = {
    "books": {
        "properties": {
            "isbn": {"type": "text"}, 
            "book_title": {"type": "text"}, 
            "book_author": {"type": "text"}, 
            "year_of_publication": {"type": "text"}, 
            "publisher": {"type": "text"}, 
            "summary": {"type": "text", "term_vector": "with_positions_offsets_payloads", "store" : True, "analyzer" : "fulltext_analyzer"}, 
            "category": {"type": "text"}
            }
    },
    "users": {
        "properties": {
            "uid": {"type": "text"}, 
            "location": {"type": "text"}, 
            "age": {"type": "text"}, 
        }
    },
    "ratings": {
        "properties": {
            "uid": {"type": "text"},
            "isbn": {"type": "text"},
            "rating": {"type": "text"},
    }
    }
}

settings = {
    "books": {
        "analysis" : {
        "analyzer": { 
            "fulltext_analyzer": { 
                "type": "custom", 
                "tokenizer": 
                "whitespace", 
                "filter": [ "lowercase", "type_as_payload"] 
                }
            }
        }
    },
    "users": None,
    "ratings": None
}

es = Elasticsearch("http://localhost:9200",timeout=200)
try:
    es.indices.delete(index = "books_index")
    es.indices.delete(index = "users_index")
    es.indices.delete(index = "ratings_index")
except:
    print("\nCreating indices for books, users and ratings.\n")

create(".\Data\BX-Books.csv","books_index",mappings["books"],settings["books"])
create(".\Data\BX-Users.csv","users_index",mappings["users"],settings["users"])
create(".\Data\BX-Book-Ratings.csv","ratings_index",mappings["ratings"],settings["ratings"])
