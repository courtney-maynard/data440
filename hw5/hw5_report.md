<h1 align = "center">HW 5 - Graph Partitioning</h1>

<h3 align = "center">Courtney Maynard</h3>
<h3 align = "center">DATA 440, Fall 2024</h3>
<h3 align = "center">November 12th, 2024</h3>

## Q1: Color Nodes Based on Final Split

### Code:
```python
# IMPORT STATEMENTS
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import networkx as nx
import scipy
import matplotlib.patches as mpatches
import matplotlib.lines as mlines


# EXPLORING KARATE CLUB GRAPH
karate_base = nx.karate_club_graph()

print('The nodes (members), zero-based: ', list(karate_base.nodes), '\n')
print('The edges of the nodes (members): ', list(karate_base.edges), '\n')
print('The degrees of the connections between nodes (members): ', list(karate_base.degree))


# CREATING THE KARATE CLUB SPLIT BY DIFFERENT COLORED NODES

# creating data frame of the nodes, so that I can then decide a color for the nodes 
# and then iteratively add them to a new graph object to illustrate the split.
split_df = pd.DataFrame(columns = ['Node', 'Edges', 'Degree', 'Color'])

# need to renumber/'rename' each node to not be zero based in order to match the split
# shown in the lectures
for each_member in karate_base:

    # color according to split shown in lecture slides
    mr_hi_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 17, 18, 20, 22]
    if (each_member+1) in mr_hi_list:
        color = 'lavender'
    else:
        color = 'lightblue'

    # need to also add one to each node value in the edge pairs
    edges = karate_base.edges(each_member)
    corrected_edges = [(each_edge[0] + 1, each_edge[1] + 1) for each_edge in edges]
    
    split_df.loc[len(split_df)] = [each_member+1, corrected_edges, karate_base.degree(each_member), color]
    #print('Successfully added to dataframe')


# now, I will construct a new graph with all the right color splits and numbering
karate_split = nx.Graph()

for _, member in split_df.iterrows():
    node = member['Node']
    karate_split.add_node(node, color=member['Color'])
    edges = member['Edges']
    
    for edge in edges:
        karate_split.add_edge(edge[0], edge[1])

#print("Number of nodes in karate_split:", len(karate_split.nodes))
#print("Number of rows in split_df:", len(split_df))


# DRAW THE GRAPH
node_colors = split_df['Color']
nx.draw_spring(karate_split, with_labels=True, node_color=node_colors, font_size = 10)

# making a legend by creating circlular symbols
lavender_circle= mlines.Line2D([], [], marker='o', color='w', label='Mr. Hi', markersize=10, markerfacecolor='lavender', markeredgewidth=2)
lightblue_circle = mlines.Line2D([], [], marker='o', color='w', label='John A.', markersize=10, markerfacecolor='lightblue', markeredgewidth=2)
plt.legend(handles=[lavender_circle, lightblue_circle], loc='upper left', fontsize=12, frameon=False, prop={'family': 'DejaVu Serif'})

plt.title('Karate Club Eventual Split, Where Each Node is A Member of the Original Club', fontsize=12, fontname='DejaVu Serif', color='black')

plt.axis('off') 
plt.savefig('Karate_Split_Colored_Graph.png')
plt.show()

```
<img src="Karate_Split_Colored_Graph.png">

### Commentary:
