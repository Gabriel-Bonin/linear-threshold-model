# -*- coding: utf-8 -*-

#!pip install ndlib
#!pip install thresholdmodel

import ndlib
import thresholdmodel
import networkx as nx
import pandas as pd
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import ndlib.models.compartments.NodeThreshold as ns
from thresholdmodel import ThreshModel
import seaborn as sns
import matplotlib.pyplot as plt

# opening c.elegans connections using data in file 'data'
neurons = pd.read_excel('data.xlsx')

# building a graph with networkx and creating links between nodes
G = nx.Graph()
Node1 = neurons['Nó_1']
Node2 = neurons['Nó_2']

connections = list(zip(Node1, Node2))
G.add_edges_from(connections)
#nx.draw(G)
#plt.show()

# making the analysis with only the biggest component, i.e, ignoring the two disconnected nodes 
Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
g = G.subgraph(Gcc[0])

# creating a function to simulate LTM
def ltm(node):
  # model selection
  model = ep.ThresholdModel(g)
  # model Configuration
  config = mc.Configuration()
  # taking a node as seed
  infected = node
  # selecting only 1 node to be the seed
  ################################################
  config.add_model_initial_configuration('Infected', infected)
  ################################################
  # setting node parameters
  threshold = 0.008
  for i in g.nodes():
    config.add_node_configuration("threshold", i, threshold)

  model.set_initial_status(config)

  # simulation execution
  iterations = model.iteration_bunch(bunch_size=8)

  # since the object 'iterations' has a lot of keys in the dict, we only need to take 'status'
  it0 = iterations[0]['status'].items() #  Shows what node is the seed initial seed
  it1 = iterations[1]['status'].items()
  it2 = iterations[2]['status'].items()
  it3 = iterations[3]['status'].items()
  it4 = iterations[4]['status'].items()
  it5 = iterations[5]['status'].items()
  it6 = iterations[6]['status'].items()
  it7 = iterations[7]['status'].items()

  it = [it0,it1,it2,it3,it4,it5,it6,it7]
  return it

# the simulation is already complete and now we want to visualize it in a dataframe 
# the dataframe will indicate how many iterations are necessary to a node get activated
list_of_nodes = list(g.nodes())
final_list = []
final_list = list_of_nodes

data = pd.DataFrame(index = list_of_nodes, columns= list_of_nodes)

for k in list_of_nodes: 
  neuron = [k]
  it = ltm(neuron)

  for i in range(len(it)):
    it[i] = pd.Series(it[i]).apply(lambda x: x[0])

  for j in range(len(it)):
    data.loc[it[j], neuron] = j

# here we can already print the result as a dataframe
# print(data)

# now plotting a heatmap with the results
data1 = data
for i in data1.columns:
  data1[i] = data1[i].apply(lambda x: int(x))

fig, ax = plt.subplots()

sns.set()
sns.heatmap(data1.values,cmap = sns.cm.rocket_r,yticklabels=False, xticklabels=False,
            cbar_kws={'label': 'Adoption Time'})

plt.xlabel('Targets')
plt.ylabel('Seeds')
ax.xaxis.tick_top() # x axis on top
ax.xaxis.set_label_position('top')
ax.collections[0].colorbar.set_label("Adoption Time")
