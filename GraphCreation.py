import os
import networkx as nx
import matplotlib.pyplot as plt

# Function to create graphs from files in the cleaned_content folder
def create_graphs_from_files(folder_path, max_train_files=12, max_test_files=3):
    training_data = []
    testing_data = []
    categories = os.listdir(folder_path)
    for category in categories:
        category_folder = os.path.join(folder_path, category)
        if os.path.isdir(category_folder):
            category_train_graphs = []
            category_test_graphs = []
            for i in range(1, max_train_files + 1):  # Take the first `max_train_files` files for training
                file_path = os.path.join(category_folder, f"url{i}.txt")
                if os.path.isfile(file_path):
                    G = nx.Graph()
                    with open(file_path, 'r') as file:
                        words = file.read().split()
                        for i in range(len(words) - 1):
                            word1 = words[i]
                            word2 = words[i + 1]
                            if G.has_edge(word1, word2):
                                G[word1][word2]['weight'] += 1
                            else:
                                G.add_edge(word1, word2, weight=1)
                    category_train_graphs.append(G)
            for i in range(max_train_files + 1, max_train_files + max_test_files + 1):  # Take the next `max_test_files` files for testing
                file_path = os.path.join(category_folder, f"url{i}.txt")
                if os.path.isfile(file_path):
                    G = nx.Graph()
                    with open(file_path, 'r') as file:
                        words = file.read().split()
                        for i in range(len(words) - 1):
                            word1 = words[i]
                            word2 = words[i + 1]
                            if G.has_edge(word1, word2):
                                G[word1][word2]['weight'] += 1
                            else:
                                G.add_edge(word1, word2, weight=1)
                    category_test_graphs.append(G)
            training_data.append((category, category_train_graphs))
            testing_data.append((category, category_test_graphs))
    return training_data, testing_data

# Function to calculate the maximum common subgraph (MCS) between two graphs
def calculate_maximum_common_subgraph(graph1, graph2):
    common_subgraph_count = 0  # Initialize count for common subgraph
    nodes_graph1 = list(graph1.nodes())  # Get nodes of graph1
    nodes_graph2 = list(graph2.nodes())  # Get nodes of graph2
    # Iterate over all pairs of nodes in both graphs
    for node1 in nodes_graph1:
        for node2 in nodes_graph2:
            # Check if both graphs have an edge between the current pair of nodes
            if graph1.has_edge(node1, node2) and graph2.has_edge(node1, node2):
                common_subgraph_count += 1  # Increment count for common subgraph
    return common_subgraph_count

# Function to calculate the MCS distance between two graphs
def calculate_maximum_common_subgraph_distance(graph1, graph2):
    common_subgraph_count = calculate_maximum_common_subgraph(graph1, graph2)  # Calculate count for common subgraph
    max_graph_size = max(len(graph1), len(graph2))  # Get maximum graph size
    # Calculate and return the MCS distance
    return 1 - (common_subgraph_count / max_graph_size)


# Function to predict the class of a new graph based on maximum common subgraph (MCS) distances
def predict_graph_class(new_graph, training_data, k=3, decay_factor=0.5):
    category_mcs_distances = {}  # Dictionary to store MCS distances for each category
    for category, graphs in training_data:
        category_mcs_distances[category] = []  # Initialize list for MCS distances in the category
        for graph in graphs:
            mcs_distance = calculate_maximum_common_subgraph_distance(new_graph, graph)
            category_mcs_distances[category].append(mcs_distance)
    return category_mcs_distances



# Example usage:
folder_path = 'cleaned_content'
training_data, testing_data = create_graphs_from_files(folder_path)

def display_graphs(graphs, category_name, category_type):
    plt.figure(figsize=(10, 6))
    plt.suptitle(f"Graphs - {category_type} - {category_name}", fontsize=16)
    num_graphs = len(graphs)
    rows = num_graphs // 2 + (num_graphs % 2 > 0)
    for i, graph in enumerate(graphs, start=1):
        plt.subplot(rows, 2, i)
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_size=300, font_size=10, node_color='skyblue', edge_color='gray', linewidths=1)
        plt.title(f"Graph {i}")
        num_nodes = len(graph.nodes())
        plt.text(0.5, 0.95, f"Number of Nodes: {num_nodes}", horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
    plt.tight_layout()
    plt.show()

# Assuming you have already populated the `training_data` variable

# Print the contents of training_data
print("Training Data:")
for category, graph in training_data:
    print("Category:", category)
    # print("Graph:", graph)
    

# Predict the class for all graphs in each category in the testing data
predicted_classes = {}
for category, graphs in testing_data:
    predicted_classes[category] = []
    for graph in graphs:
        category_mcs_distances = predict_graph_class(graph, training_data)
        predicted_class = max(category_mcs_distances, key=category_mcs_distances.get)
        predicted_classes[category].append(predicted_class)

# Print the predicted classes for each category
for category, predictions in predicted_classes.items():
    print(f"Predicted classes for category '{category}': {predictions}")











# # Create a dictionary to store the count of graphs for each category
# category_graph_counts = {}

# # Count the number of graphs for each category
# for category, graphs in training_data:
#     if category in category_graph_counts:
#         category_graph_counts[category] += len(graphs)
#     else:
#         category_graph_counts[category] = len(graphs)

# # Print the counts for each category
# for category, count in category_graph_counts.items():
#     print(f"Category '{category}' has {count} graph(s).")


# # Create a dictionary to store the count of graphs for each category in testing_data
# testing_category_graph_counts = {}

# # Count the number of graphs for each category in testing_data
# for category, graphs in testing_data:
#     if category in testing_category_graph_counts:
#         testing_category_graph_counts[category] += len(graphs)
#     else:
#         testing_category_graph_counts[category] = len(graphs)

# # Print the counts for each category in testing_data
# for category, count in testing_category_graph_counts.items():
#     print(f"Category '{category}' has {count} graph(s) in testing data.")





