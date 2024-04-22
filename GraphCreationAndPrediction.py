import os
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns



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
def predict_class(new_graph, training_data, k=3, decay_factor=0.5):
    category_distances = {}  # Dictionary to store distances for each category
    for category, graphs in training_data:
        category_distances[category] = []  # Initialize list for distances in the category
        for graph in graphs:
            distance = calculate_maximum_common_subgraph_distance(new_graph, graph)
            category_distances[category].append(distance)

    # Calculate weighted votes based on distances
    class_weights = {}
    for category, distances in category_distances.items():
        total_weight = 0
        for i, dist in enumerate(sorted(distances)[:k], 1):  # Consider only k nearest neighbors
            weight = (1 / (dist + 0.0001)) * (decay_factor ** i)  # Adding a small value to avoid division by zero
            total_weight += weight
        class_weights[category] = total_weight
    
    # Normalize weights
    total_weight = sum(class_weights.values())
    if total_weight == 0:
        return None  # Return None if all distances are infinity
    for category in class_weights:
        class_weights[category] /= total_weight
    
    # Choose the class with maximum weighted vote
    majority_class = max(class_weights, key=class_weights.get)
    return majority_class


# Example usage:
folder_path = 'cleaned_content'
training_data, testing_data = create_graphs_from_files(folder_path)



# Function to generate confusion matrix
def generate_confusion_matrix(true_labels, predicted_labels, classes):
    cm = confusion_matrix(true_labels, predicted_labels, labels=classes)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    plt.show()


true_predicted_categories = {}

# Predict the class for all graphs in each category in the testing data
true_labels = []
predicted_labels = []
for category, graphs in testing_data:
    print(f"\nCategory: {category}")
    for graph in graphs:
        true_category = category  # True category is the category of the current testing data
        predicted_category = predict_class(graph, training_data)
        true_predicted_categories[(true_category, predicted_category)] = true_predicted_categories.get((true_category, predicted_category), 0) + 1
        true_labels.append(true_category)
        predicted_labels.append(predicted_category)
        print(f"True Category: {true_category}, Predicted Category: {predicted_category}")


# Define the classes
classes = list(set(true_labels))
# Generate confusion matrix
generate_confusion_matrix(true_labels, predicted_labels, classes)