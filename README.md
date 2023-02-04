# elasticsearch_project
This project is split in two parts.
The first part is stored inside the part1 folder and the second inside the part2 folder.

Its part has a setup and a search file. To run the search file you must first run the setup file.
Before anything you must have installed the elastic search in your PC and have it running. 
For both parts you must first run the setup files that will create the indeces needed and create the required files.
To run the second part you must first run the setup file from the first part and then the setup from the second part !
Both files have a file called indeces_creator, this file contains a function called create that is used by the setup files
to create the required elastic search indeces.
What is this project ?

I have created 2 simulations of a book's search engine if I can call it that way. There are 3 files that I started with, one csv 
with some books data, one with some users and one with some reviews of the users to the books. The final results can be seen 
running the search files of each part. 

The search function of the first part does the following:

1) Given a user id and a string it finds the 1000 top books based in the BM25 elastic search scoring method.
2) If there is a book that the user with the specified id has rated, then it sums the elasticsearch score with the user's rating
for that book.
3) It sorts the results again with respect to the new scores and prints them.

The search function of the second part does the same thing but there is a major difference. In the setup file I have applied 
a clustering method called kmeans to the users based on their age and location. I have also calculated the average rating that the 
users of a cluster have given to a book if at least one of these users has rated it. This information is stored in a json file called
averages and is used by the search function. The search function does what the first search function does but it sorts the results using 
the average rating of the specified users cluster for the books that he hasn't reviewed.

For the clustering I also used two csv files fould in the links below
Big thanks to albertyw https://github.com/albertyw/avenews/blob/master/old/data/average-latitude-longitude-countries.csv data from 2013
and to jasperderbie https://github.com/jasperdebie/VisInfo/blob/master/us-state-capitals.csv
