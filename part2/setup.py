import pandas as pd
import numpy as np
from sklearn.cluster import KMeans as kmeans
import numpy as np
import ast
import math
from indeces_creator import create
from elasticsearch import Elasticsearch
import json


# Big thanks to albertyw https://github.com/albertyw/avenews/blob/master/old/data/average-latitude-longitude-countries.csv data from 2013
# And to jasperderbie https://github.com/jasperdebie/VisInfo/blob/master/us-state-capitals.csv

#0 Create a list with the latitude and longitude of all the countries and states.
countries = pd.read_csv('.\Data\\average-latitude-longitude-countries.csv')
states = pd.read_csv('.\Data\states.csv')

countries_index = {}

for i in range(len(countries)):
    countries_index[countries["Country"].get(i).lower()] = [countries["Latitude"].get(i),countries["Longitude"].get(i)]

for i in range(len(states)):
    countries_index[states["name"].get(i).lower()] = [states["latitude"].get(i),states["longitude"].get(i)]

countries_index = dict(sorted(countries_index.items()))
countries_keys = list(countries_index.keys())

print("step 0 completed")

#1 Create a new dataframe for the users with one more column named pos that stores the 
# latitude and longitude of the country-state they are from.

users = pd.read_csv(".\Data\BX-Users.csv")

pos_values = []

for i in range(len(users)):
    for j in range(len(countries_keys)):
        if countries_keys[j] in users["location"].get(i):
            pos_values.append(countries_index[countries_keys[j]]) 
            break
    try:
        pos_values[i]
    except(IndexError):
        pos_values.append([0,0]) #if there is no info about a user's location
                                 #set this user's pos [0,0]
    
users.insert(3, "pos", pos_values) #new column and it's values insertion

users.to_csv(".\Data\BX-Users-Updated.csv", index=False)

print("step 1 completed")

#2 Apply clustering to the users using k-means algorithm.
# Age, longitude and latitude are the variables for the algorithm.

X = (users[["uid","age","pos"]]) #keep only uid age and pos

X = X.values.tolist() # datafram to list

for i in range(len(X)):
    if math.isnan(X[i][1]): #if age is nan
        X[i][1]=0           #set it to 0 
    X[i] = [X[i][0],X[i][1],X[i][2][0],X[i][2][1]] #seperate the pos list to 2 seperate values
                                                   # before: [uid,age,[lat,long]]
                                                   #after: [uid,age,lat,long]

X = np.array(X) #make X an np.array
X = X[:,1:4] #keep only age lat and long
km = kmeans(n_clusters=10) #set clustering to 10 clusters
km.fit(X) #Apply the clustering to X data

print("step 2 completed")

#3 Find each user's cluster with Kmeans.predict and store this info in user's dataframe

belongs_to_cluster=[]

for i in range(len(users)):
    #prediction = km.predict([[users["age"][i],users["pos"][i][0],users["pos"][i][1]]])
    a = X[i].reshape(1,-1)
    prediction = km.predict(a)
    belongs_to_cluster.append(int(prediction))
    
users.insert(4,"cluster_number",belongs_to_cluster)

users.to_csv(".\Data\BX-Users-Updated-2.csv", index=False)

print("step 3 completed")

#4 Create an index for the new users csv

index_name = "users_withclusters_index"
mapping ={
        "properties": {
            "uid": {"type": "text"}, 
            "location": {"type": "text"}, 
            "age": {"type": "text"}, 
            "pos": {"type": "text"},
            "cluster_number": {"type": "text"}
        }
        }
setting = None

try:
    create(".\Data\BX-Users-Updated-2.csv", index_name, mapping, setting)
except:
    None

print("step 4 completed")

#5 add to the reviews the cluster number of the user

es = Elasticsearch("http://localhost:9200",timeout=200)

ratings = pd.read_csv(".\Data\BX-Book-Ratings.csv")

#users = pd.read_csv(".\Data\BX-Users-Updated-2.csv")

users_dict = {}

for i in range(len(users)):
    users_dict[users["uid"].get(i)] = users["cluster_number"].get(i)

ratings_cluster = []

for i in range(len(ratings)):
    try:
        cluster_number = users_dict[ratings["uid"].get(i)]
    except:
        cluster_number = "none"
    ratings_cluster.append(cluster_number)

ratings.insert(3, "cluster_number", ratings_cluster)

ratings.to_csv(".\Data\BX-Books-Ratings-Updated.csv", index=False)

print("step 5 completed")

#6 find the average value of the reviews for each book that has been reviewed for each cluster (in the ratings csv there are reviews that belong to people who are not in
# the user's csv, in these cases we don't really care)

reviewerssum_and_ratingssum_perbook = {} # Format {"bookisbn_cluster": [reviwerstotal,reviwestotalvalue], ...}

for i in range(len(ratings)):
    if ratings["cluster_number"].get(i) != "none":
        key = str(ratings["isbn"].get(i))+"_"+str(ratings["cluster_number"].get(i))
        try:
            reviewerssum_and_ratingssum_perbook[key][0] += 1
            reviewerssum_and_ratingssum_perbook[key][1] += int(ratings["rating"].get(i))
        except:
            reviewerssum_and_ratingssum_perbook[key] = [1,int(ratings["rating"].get(i))]

averages = {}

for k, v in reviewerssum_and_ratingssum_perbook.items():
    averages[k] = v[1]/v[0]

print("step 6 completed")

#All the above computations happened to create the json file below, I am going to use this json file as an extra metric to compute the ratings of my search results
json_object = json.dumps(averages)

with open(".\Data\\averages.json", "w") as outfile:
    outfile.write(json_object)

