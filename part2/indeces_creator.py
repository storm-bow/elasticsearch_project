import pandas as pd 
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

def create(csv_path,index_name,mapping,setting):
    dataframe = pd.read_csv(csv_path)
    listofbulk = []
    for counter in range(len(dataframe)):
        variables = {}
        for variable_name in dataframe.columns.values :
            data = dataframe[variable_name].get(counter)
            variables[variable_name] = str(data).replace("\n"," ")
        index = {
            "_index" : index_name,
            "_id": counter,
            "_source": variables
            }
        listofbulk.append(index)
    es = Elasticsearch("http://localhost:9200",timeout=200)
    es.indices.create(index = index_name, mappings = mapping, settings = setting)
    bulk(es,listofbulk)
