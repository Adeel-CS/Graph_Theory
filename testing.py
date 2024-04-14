import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Load words from the file into a NumPy array
file_path = 'cleaned_content/food/food1.txt'
words = np.loadtxt(file_path, dtype=str)

# Create a new graph
graph = nx.Graph()

# Add nodes to the graph using elements of the NumPy array
unique_words = set()  # To store unique words (excluding periods)
for word in words:
    # Exclude periods and add unique words to the graph
    if '.' not in word and word not in unique_words:
        graph.add_node(word)
        unique_words.add(word)

# Count the number of nodes (unique words)
num_nodes = len(graph.nodes)



# Draw the graph
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(graph)  # Position nodes using the spring layout algorithm
nx.draw(graph, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=8, font_weight="bold")
plt.suptitle(f"Graph Representation of Example Document (Nodes: {num_nodes})", fontsize=12, y=1)
plt.show()
