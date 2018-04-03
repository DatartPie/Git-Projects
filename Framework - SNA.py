# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 10:29:32 2016

@author: ppareek1
"""
print ()

import networkx
from operator import itemgetter
import matplotlib.pyplot

# Read the data from the amazon-books.txt;
# populate amazonProducts nested dicitonary;
# key = ASIN; value = MetaData associated with ASIN
fhr = open('./amazon-books.txt', 'r', encoding='utf-8', errors='ignore')
amazonBooks = {}
fhr.readline()
for line in fhr:
    cell = line.split('\t')
    MetaData = {}
    MetaData['Id'] = cell[0].strip() 
    ASIN = cell[1].strip()
    MetaData['Title'] = cell[2].strip()
    MetaData['Categories'] = cell[3].strip()
    MetaData['Group'] = cell[4].strip()
    MetaData['SalesRank'] = int(cell[5].strip())
    MetaData['TotalReviews'] = int(cell[6].strip())
    MetaData['AvgRating'] = float(cell[7].strip())
    MetaData['DegreeCentrality'] = int(cell[8].strip())
    MetaData['ClusteringCoeff'] = float(cell[9].strip())
    amazonBooks[ASIN] = MetaData
fhr.close()

# Read the data from amazon-books-copurchase.adjlist;
# assign it to copurchaseGraph weighted Graph;
# node = ASIN, edge= copurchase, edge weight = category similarity
fhr=open("amazon-books-copurchase.edgelist", 'rb')
copurchaseGraph=networkx.read_weighted_edgelist(fhr)
fhr.close()

# Now let's assume a person is considering buying the following book;
# what else can we recommend to them based on copurchase behavior 
# we've seen from other users?
print ("Looking for Recommendations for Customer Purchasing this Book:")
print ("--------------------------------------------------------------")
purchasedAsin = '0805047905'

# Let's first get some metadata associated with this book
print ("ASIN = ", purchasedAsin) 
print ("Title = ", amazonBooks[purchasedAsin]['Title'])
print ("Categories = ", amazonBooks[purchasedAsin]['Categories'])
print ("SalesRank = ", amazonBooks[purchasedAsin]['SalesRank'])
print ("TotalReviews = ", amazonBooks[purchasedAsin]['TotalReviews'])
print ("AvgRating = ", amazonBooks[purchasedAsin]['AvgRating'])
print ("DegreeCentrality = ", amazonBooks[purchasedAsin]['DegreeCentrality'])
print ("ClusteringCoeff = ", amazonBooks[purchasedAsin]['ClusteringCoeff'])
    
# Now let's look at the ego network associated with purchasedAsin in the
# copurchaseGraph - which is esentially comprised of all the books 
# that have been copurchased with this book in the past
# (1) YOUR CODE HERE: 
#     Get the depth-1 ego network of purchasedAsin from copurchaseGraph,
#     and assign the resulting graph to purchasedAsinEgoGraph.
n = purchasedAsin
purchasedAsinEgoGraph = networkx.ego_graph(copurchaseGraph, n, radius=1)
# = networkx.Graph()


# Next, recall that the edge weights in the copurchaseGraph is a measure of
# the similarity between the books connected by the edge. So we can use the 
# island method to only retain those books that are highly simialr to the 
# purchasedAsin
# (2) YOUR CODE HERE: 
#     Use the island method on purchasedAsinEgoGraph to only retain edges with 
#     threshold >= 0.5, and assign resulting graph to purchasedAsinEgoTrimGraph
threshold = 0.5
purchasedAsinEgoTrimGraph = networkx.Graph()
for f, t, e in purchasedAsinEgoGraph.edges(data=True):
    if e['weight'] >= threshold:
        purchasedAsinEgoTrimGraph.add_edge(f,t,e)
        



# Next, recall that given the purchasedAsinEgoTrimGraph you constructed above, 
# you can get at the list of nodes connected to the purchasedAsin by a single 
# hop (called the neighbors of the purchasedAsin) 
# (3) YOUR CODE HERE: 
#     Find the list of neighbors of the purchasedAsin in the 
#     purchasedAsinEgoTrimGraph, and assign it to purchasedAsinNeighbors
#purchasedAsinNeighbors = purchasedAsinEgoTrimGraph[purchasedAsin]
purchasedAsinNeighbors = purchasedAsinEgoTrimGraph.neighbors(purchasedAsin)
print(purchasedAsinNeighbors)

# Next, let's pick the Top Five book recommendations from among the 
# purchasedAsinNeighbors based on one or more of the following data of the 
# neighboring nodes: SalesRank, AvgRating, TotalReviews, DegreeCentrality, 
# and ClusteringCoeff
# (4) YOUR CODE HERE: 
#     Note that, given an asin, you can get at the metadata associated with  
#     it using amazonBooks (similar to lines 49-56 above).
#     Now, come up with a composite measure to make Top Five book 
#     recommendations based on one or more of the following metrics associated 
#     with nodes in purchasedAsinNeighbors: SalesRank, AvgRating, 
#     TotalReviews, DegreeCentrality, and ClusteringCoeff 

#combining avg rating and no. of reviews to form a common factor

#finding the max no of review in the list to find the factor which falls between (0,1)
list_for_max_reviews = []

for i in purchasedAsinNeighbors:
    list_for_max_reviews.append(amazonBooks[i]['TotalReviews'])

max_no_reviews = max(list_for_max_reviews)

#sorted list of tuples of Asin with factor
listasin_factor = []
for asin in purchasedAsinNeighbors:
    score_review = amazonBooks[asin]['TotalReviews'] / max_no_reviews
    factor = amazonBooks[asin]['AvgRating'] * score_review
    tup_factor = (asin, round(factor, 3))
    listasin_factor.append(tup_factor)
 
sorted_listasin_factor = sorted(listasin_factor, key=itemgetter(1), reverse=True)
print(sorted_listasin_factor)

#top n (n=15 or n=5) Asin with respect to factor

if len(purchasedAsinNeighbors) >= 15:
    top_sorted_listasin_factor = sorted_listasin_factor[:15]
else:
    top_sorted_listasin_factor = sorted_listasin_factor[:5]


#integrating what is co-purchased the most with our final recommendation
#through degree centrality (DC) measure : the higher the DC, the higher chances
#of getting the book co-purchased with our 'node' book

list_topasinfactor_DC = []
for item in top_sorted_listasin_factor:
    tup_DC = (item[0], amazonBooks[item[0]]['DegreeCentrality'])
    list_topasinfactor_DC.append(tup_DC)
#sorting with highest DC measure
sorted_list_topasinfactor_DC = sorted(list_topasinfactor_DC, key=itemgetter(1), reverse=True)  

recommendation_list = sorted_list_topasinfactor_DC [:5]
  
print(recommendation_list)    

# Print Top 5 recommendations (ASIN, and associated Title, Sales Rank, 
# TotalReviews, AvgRating, DegreeCentrality, ClusteringCoeff)
# (5) YOUR CODE HERE:  
i=1

for item in recommendation_list:
    print("\nRecommendation ", i, ":")
    print ("ASIN = ", item[0]) 
    print ("Title = ", amazonBooks[item[0]]['Title'])
    print ("Categories = ", amazonBooks[item[0]]['Categories'])
    print ("SalesRank = ", amazonBooks[item[0]]['SalesRank'])
    print ("TotalReviews = ", amazonBooks[item[0]]['TotalReviews'])
    print ("AvgRating = ", amazonBooks[item[0]]['AvgRating'])
    print ("DegreeCentrality = ", amazonBooks[item[0]]['DegreeCentrality'])
    print ("ClusteringCoeff = ", amazonBooks[item[0]]['ClusteringCoeff'])
    i= i+1
    









