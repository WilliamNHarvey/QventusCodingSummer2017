import json
import itertools
import time

#counts the number of tweets with unicode
containedUnicode = 0

#keeps track of current edge pairs
edges = []
#keeps track of the time current edge pairs were recorded, and their index in the edges array
timeIn = []
#keeps track of current existing nodes
nodes = []

#calculates the average degree, given current edges and nodes
def currentAverage(edges, nodes):
    edgeCount = []
    for node in nodes:
        edgeCount.append([node, 0])
    for edge in edges:
        for count in edgeCount:
            #if the node is part of this edge pair, add one to its count
            if(count[0] == edge[0] or count[0] == edge[1]):
                count[1] += 1
    total = 0
    for finalCount in edgeCount:
        total += finalCount[1]

    #return the average degree as a string with two decimal places
    return "{0:.2f}".format(1.0 * total/len(nodes))

with open('tweet_input/tweets.txt','rb') as infile, open('tweet_output/ft1.txt','w') as ft1, open('tweet_output/ft2.txt','w') as ft2:
    for line in infile:
        #ft1
        #removes unicode from the entire tweet
        removedUnicode = line.decode('unicode_escape').encode('ascii','ignore')
        if(line != removedUnicode):
            containedUnicode += 1
        #removes escape characters
        tweet = json.loads(removedUnicode)
        ft1.write(tweet['text'] + ' (timestamp: ' + tweet['created_at'] + ")\n")

        #ft2
        #maps tweet created time to a unix timestamp
        tweetTime = time.mktime(time.strptime(tweet['created_at'],"%a %b %d %H:%M:%S +0000 %Y"))
        edgesToDelete = []
        for a, b in itertools.combinations(tweet['entities']['hashtags'], 2):
            node1 = a['text']
            node2 = b['text']
            if(node1 != node2):
                #if the node pair doesn't have an edge, add it
                #if the edge already exists, update it by adding it and removing the older pair
                if([node1, node2] not in edges and [node2, node1] not in edges):
                    index = len(edges)
                    edges.append([node1, node2])
                    timeIn.append([tweetTime, index])
                elif([node1, node2] in edges):
                    index = len(edges)
                    edgesToDelete.append(edges.index([node1, node2]))
                    edges.append([node1, node2])
                    timeIn.append([tweetTime, index])
                elif ([node2, node1] in edges):
                    index = len(edges)
                    edgesToDelete.append(edges.index([node2, node1]))
                    edges.append([node1, node2])
                    timeIn.append([tweetTime, index])

                #add nodes in the pair to the list of nodes
                if(node1 not in nodes):
                    nodes.append(node1)
                if (node2 not in nodes):
                    nodes.append(node2)

        for key,edge in enumerate(timeIn):
            if(tweetTime - edge[0] > 60):
                edgesToDelete.append(edge[1])
                #this shifts edges that aren't being removed down in the timeIn array,
                #keeping their recorded indexes accurate with the edges array
                for key2,edge2 in enumerate(timeIn):
                    if(edge2[1] > edge[1]):
                        timeIn[key2][1] -= 1
                #removes the old edge from the timeIn array
                del timeIn[key]

        #removes old edges from the edges array
        for i in sorted(edgesToDelete, key=int, reverse=True):
            del edges[i]

        nodesToRemove = nodes[:]
        for node in nodes:
            for group in edges:
                #if the node is still in an edge, don't remove it
                if(node in nodesToRemove and node in group):
                    nodesToRemove.remove(node)

        #removes nodes that no longer exist in any edge
        for remove in nodesToRemove:
            nodes.remove(remove)

        #calculates the average degree and writes it
        ft2.write(currentAverage(edges, nodes) + "\n")

    ft1.write("\n" + str(containedUnicode) + ' tweets contained Unicode.')

