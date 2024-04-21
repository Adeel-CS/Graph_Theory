import os
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from sklearn.metrics import confusion_matrix
import seaborn as sns

# Function to create a graph from a sentence
def create_graph(sentence):
    words = sentence.split()
    graph = nx.Graph()
    graph.add_nodes_from(words)
    for i in range(len(words)-1):
        graph.add_edge(words[i], words[i+1])
    return graph

# Function to calculate MCS between two graphs
def calculate_mcs(graph1, graph2):
    mcs = 0
    nodes1 = list(graph1.nodes())
    nodes2 = list(graph2.nodes())
    for node1 in nodes1:
        for node2 in nodes2:
            if graph1.has_edge(node1, node2) and graph2.has_edge(node1, node2):
                mcs += 1
    return mcs

# Function to calculate MCS distance between two graphs
def calculate_mcs_distance(graph1, graph2):
    mcs = calculate_mcs(graph1, graph2)
    max_size = max(len(graph1), len(graph2))
    return 1 - (mcs / max_size)

# Function to create graphs from files in the cleaned_content folder
def create_graphs_from_files(folder_path, max_files=15):
    graphs = []
    categories = os.listdir(folder_path)
    for category in categories:
        category_folder = os.path.join(folder_path, category)
        if os.path.isdir(category_folder):
            category_graphs = []
            for i in range(1, max_files + 1):  # Take only the first `max_files` files
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
                    category_graphs.append(G)
            graphs.append((category, category_graphs))
    return graphs

# Function to display a graph using Matplotlib
def display_graph(graph, category_name, graph_index):
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=300, font_size=10, node_color='skyblue', edge_color='gray', linewidths=1)
    plt.suptitle(f"Graph Example - {category_name}")
    plt.show()

# Generate sample data
sports_sentences = [
    "He scored a goal in the final match.",
    "The team won the championship.",
    "She is practicing tennis every day.",
    "They are training for the upcoming race.",
    "Basketball is his favorite sport."
]

marketing_sentences = [
    "The new product launch was a success.",
    "We have a special discount for our customers.",
    "Our marketing strategy needs improvement.",
    "They are targeting a new market segment.",
    "The advertisement campaign increased sales."
]

# Create graphs for each sentence
sports_graphs = [create_graph(sentence) for sentence in sports_sentences]
marketing_graphs = [create_graph(sentence) for sentence in marketing_sentences]

# Combine all graphs and labels
all_graphs = sports_graphs + marketing_graphs
labels = ['sports'] * len(sports_graphs) + ['marketing'] * len(marketing_graphs)

# Function to predict the class of a new sentence
def predict_class(new_sentence, k=3, decay_factor=0.5):
    new_graph = create_graph(new_sentence)
    distances = [(calculate_mcs_distance(new_graph, graph), label) for graph, label in zip(all_graphs, labels)]
    distances.sort()  # Sort distances
    total_weight = 0
    class_weights = {}
    for i, (dist, label) in enumerate(distances[:k], 1):  # Consider only k nearest neighbors
        weight = (1 / (dist + 0.0001)) * (decay_factor ** i)  # Adding a small value to avoid division by zero
        class_weights[label] = class_weights.get(label, 0) + weight
        total_weight += weight
    if total_weight == 0:
        return None  # Return None if all distances are infinity
    # Normalize weights
    for label in class_weights:
        class_weights[label] /= total_weight
    # Choose the class with maximum weighted vote
    majority_class = max(class_weights, key=class_weights.get)
    return majority_class

# Function to generate confusion matrix
def generate_confusion_matrix(true_labels, predicted_labels, classes):
    cm = confusion_matrix(true_labels, predicted_labels, labels=classes)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    plt.show()

# Create graphs from files in the cleaned_content folder
folder_path = 'cleaned_content'
all_category_graphs = create_graphs_from_files(folder_path)

# Display the last graph from each category
for category, category_graphs in all_category_graphs:
    last_index = len(category_graphs) - 1
    print(f"Last index for {category} category:", last_index)
    display_graph(category_graphs[last_index], category, last_index)
