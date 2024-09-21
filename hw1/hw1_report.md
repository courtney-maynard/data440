
<h1 align = "center">HW 1 - Web Science Intro</h1>

<h3 align = "center">Courtney Maynard</h3>
<h3 align = "center">DATA 440, Fall 2024</h3>
<h3 align = "center">September 24th</h3>

## Question 1
*Consider the 'bow-tie' structure of the web and the following links A - G. Draw the resulting directed graph showing how the nodes are connected to each other. For the graph list the nodes (in alphabetical order) that are each of the categories.*

### Answer
<img src="q1hw1-directed graph.png">

#### Node Categories:
- Strongly Connected Components (Blue): A, B, C, G
- IN (Pink): M, O, P
- OUT (Orange): D, H
- Tendrils (Yellow): I, K, L
   - I can reach OUT
   - K is reachable from I, which can reach OUT
   - L can reach OUT
- Tubes (Red): N
   - N is a tube because it connects an IN node (M) with an OUT node (D), bypassing the SCC
- Disconnected (Green): E, F
  
### Discussion
To construct this graph, I first sketched all the nodes on paper as I read them. Then, once I realized how they were clustered, I created a visualization on the computer and set it up so the components were easily identifiable by color-coding them. I started by finding the strongly connected components to determine which nodes were in each category. I traced through each node to see which others it reached and determined that *A*, *B*, *C*, and *G* could all reach each other directly. Next, I looked for the nodes that were strictly **OUT** or **IN** from the **SCC**, which led me to *O*, *M*, and *P* as **IN** nodes, and *D* and *H* as **OUT**. I noticed that *M* was connecting to *N*, which then connected to *D*, and since *N* is **IN** and *D* is **OUT**, that made *N* a tube. I identified *E* and *F* as disconnected because they don't connect to other nodes. I identified the remaining nodes, *I*, *K*, and *L* as tendrils because they were either directed to **OUT** (*I* and *L*) or connected to another tendril (*K*), but could not reach the **SCC**. I identified no tendrils reachable from **IN**, since *N* ended up being a tube. 

## Question 2
*Load the URI in the browser and take a screenshot. Then, in a single curl command, issue a HEAD HTTP request for the second URI. Show the HTTP response headers, follow any redirects, and change the User-Agent HTTP request field to DATA 440_691. Show the commands and results*

### Answer


### Discussion
Explanation in progress

# Q3 
Coding in progress
Explanation not started
