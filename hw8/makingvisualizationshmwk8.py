## USING THE FUNCTIONS ADAPTED FROM CHAPTER 3, FROM THE CO-LAB NOTEBOOK
from PIL import Image, ImageDraw
from math import sqrt
import random
import csv


## GENERAL FUNCTIONS
def readfile(filename):
    # This is a function that I wrote from scratch   -MCW
    data = []
    rownames = []
    colnames = []
    num_rows = 0
    with open(filename) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            if num_rows > 0:
                rownames.append(row[0])    # save the row names
                data.append([float(x) for x in row[1:]])  # save the values as floats
            else:
                for col in row[1:]:
                    colnames.append(col)    # save the column names
            num_rows = num_rows + 1
    return (rownames, colnames, data)


def pearson(v1, v2):#distance function
    # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    # Sums of the squares
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    # Sum of the products
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    # Calculate r (Pearson score)
    num = pSum - sum1 * sum2 / len(v1)
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2)/ len(v1)))
    if den == 0:
        return 0

    return 1.0 - num / den

def rotatematrix(data):
    newdata = []
    for i in range(len(data[0])):
        newrow = [data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata


## HIERARCHICAL CLUSTERING FUNCTIONS
class bicluster:

    def __init__(self, vec, left=None, right=None, distance=0.0, id=None,):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1

    # Clusters are initially just the rows
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

    # loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
        # distances is the cache of distance calculations
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = \
                        distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)


    # calculate the average of the two clusters
        mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i])
                    / 2.0 for i in range(len(clust[0].vec))]

    # create the new cluster
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]],
                            right=clust[lowestpair[1]], distance=closest,
                            id=currentclustid)

    # cluster ids that weren't in the original set are negative
        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]

'''
printclust(clust, labels = None, n = 0, file=None)
    - changed from the original function in order to save the ascii dendogram as a file instead
    of just outputting to the screen
    - now takes file name in the recursive function
'''
def printclust(clust, labels=None, n=0, file=None):
    # indent to make a hierarchy layout
    line = ' ' * n
    if clust.id < 0:
    # negative id means that this is branch
        line += '-\n'
    else:
    # positive id means that this is an endpoint
        if labels == None:
            line += f'{clust.id}\n'
        else:
            line += f'{labels[clust.id]}\n'
    
    # write out to a file
    if file:
        file.write(line)
    else:
        print(line, end='')

    # now print the right and left branches
    if clust.left != None:
        printclust(clust.left, labels=labels, n=n + 1, file=file)
    if clust.right != None:
        printclust(clust.right, labels=labels, n=n + 1, file=file)


## DENDOGRAM FUNCTIONS
def getheight(clust):
    # Is this an endpoint? Then the height is just 1
    if clust.left == None and clust.right == None:
        return 1

    # Otherwise the height is the same of the heights of
    # each branch
    return getheight(clust.left) + getheight(clust.right)


def getdepth(clust):
    # The distance of an endpoint is 0.0
    if clust.left == None and clust.right == None:
        return 0

    # The distance of a branch is the greater of its two sides
    # plus its own distance
    return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance


def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
    # height and width
    h = getheight(clust) * 20
    w = 1200
    depth = getdepth(clust)

    # width is fixed, so scale distances accordingly
    scaling = float(w - 150) / depth

    # Create a new image with a white background
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))

    # Draw the first node
    drawnode(
        draw,
        clust,
        10,
        h / 2,
        scaling,
        labels,
        )
    img.save(jpeg, 'JPEG')


def drawnode(
    draw,
    clust,
    x,
    y,
    scaling,
    labels,
    ):
    if clust.id < 0:
        h1 = getheight(clust.left) * 20
        h2 = getheight(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
    # Line length
        ll = clust.distance * scaling
    # Vertical line from this cluster to children
        draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))

    # Horizontal line to left item
        draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill=(255, 0, 0))

    # Horizontal line to right item
        draw.line((x, bottom - h2 / 2, x + ll, bottom - h2 / 2), fill=(255, 0,0))
        
    # Call the function to draw the left and right nodes
        drawnode(
            draw,
            clust.left,
            x + ll,
            top + h1 / 2,
            scaling,
            labels,
            )
        drawnode(
            draw,
            clust.right,
            x + ll,
            bottom - h2 / 2,
            scaling,
            labels,
            )
    else:
    # If this is an endpoint, draw the item label
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))

## K MEANS CLUSTERING
def kcluster(rows, distance=pearson, k=4):
    # Determine the minimum and maximum values for each point
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows]))for i in range(len(rows[0]))]

    # Create k randomly placed centroids
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0]
                for i in range(len(rows[0]))] for j in range(k)]

    lastmatches = None
    for t in range(100):
        print ('Iteration %d' % t)
        bestmatches = [[] for i in range(k)]

    # Find which centroid is the closest for each row
        for j in range(len(rows)):
            row = rows[j]
            bestmatch = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[bestmatch], row):
                    bestmatch = i
            bestmatches[bestmatch].append(j)

    # If the results are the same as last time, this is complete
        if bestmatches == lastmatches:
            break
        lastmatches = bestmatches

    # Move the centroids to the average of their members
        for i in range(k):
            avgs = [0.0] * len(rows[0])
            if len(bestmatches[i]) > 0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(bestmatches[i])
                clusters[i] = avgs

    return bestmatches


## Q3: Create Dendrogram and ASCII
accountsnames, words, data = readfile("tweet_term_matrix.txt")
accounts_cluster = hcluster(data)
with open("ascii_twitter_accounts.txt", "w") as f:
    printclust(accounts_cluster, labels=accountsnames, file=f)

drawdendrogram(accounts_cluster, accountsnames, jpeg = 'dendogram_twitter_accounts.jpeg')


## Q4: Cluster using K-Means
k_values = [5, 10, 20]

# perform the k-means
for each_k in k_values:
    kclust = kcluster(data, k = each_k)

    k_filename = f'k_means_clusters_k{each_k}.txt'

    with open(k_filename, "w") as file:
        file.write(f"k-Means clustering results for k={each_k}\n")
        file.write('-' * 100 + '\n')
        
        # each clusters account and the cluster number written into the file
        for cluster_count, cluster in enumerate(kclust):
            file.write(f"cluster {cluster_count + 1}:\n")
            accounts_in_cluster = [accountsnames[r] for r in cluster]
            file.write(", ".join(accounts_in_cluster) + "\n")
            file.write('\n')  # want to leave space between clusters for readability
            
    print('results for k=', each_k, 'written to ', k_filename)
