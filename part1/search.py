from elasticsearch import Elasticsearch

def search(query_string,uid):

    es = Elasticsearch("http://localhost:9200",timeout=30)

    query = {
        "multi_match" : {
            "query":    query_string, 
            "fields": [ "summary^1.2", "book_title" ] 
    }
    }

    result = es.search(index="books_index",query=query,size=1000)
    
    for i in range(len(result["hits"]["hits"])):
        match = {
            "bool":{
                "must": [
                    {
                    "match": {
                        "uid":str(uid)
                    }
                    },
                    {
                    "match": {
                        "isbn":result["hits"]["hits"][i]["_source"]["isbn"]
                    }
                    }
                ]
            }
        }
        checkratings  = es.search(index="ratings_index",query=match)
        try:
            result["hits"]["hits"][i]["_score"] += int(checkratings["hits"]["hits"][0]["_source"]["rating"])
        except:
            pass
    result["hits"]["hits"].sort(key=lambda x: x["_score"])
    
    counter=0

    # Prints all the json object
    '''
    for i in result["hits"]["hits"][::-1][0:10]:
        a+=1
        print(a)
        print("{\n")
        for j in i:
            print(j,":",i[j])
        print("\n}\n")
    '''
    #Prints just the names of the books
    for i in result["hits"]["hits"][::-1][0:100]:
        counter=counter+1
        print(counter,"result","\"",str(i["_source"]["book_title"]),"\"","\n")
        
while(1):
    try:
        query_string = input("\nquery_string:\t")
        uid = input("\nuserid:\t")
        search(query_string,uid)
    except: 
        exit(1)
    
