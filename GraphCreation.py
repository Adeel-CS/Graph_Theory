# import os
# import networkx as nx
# import matplotlib.pyplot as plt

# # Function to create graphs from files in the cleaned_content folder
# def create_graphs_from_files(folder_path, max_files=15):
#     graphs = []
#     categories = os.listdir(folder_path)
#     for category in categories:
#         category_folder = os.path.join(folder_path, category)
#         if os.path.isdir(category_folder):
#             category_graphs = []
#             for i in range(1, max_files + 1):  # Take only the first `max_files` files
#                 file_path = os.path.join(category_folder, f"url{i}.txt")
#                 if os.path.isfile(file_path):
#                     G = nx.Graph()
#                     with open(file_path, 'r') as file:
#                         words = file.read().split()
#                         for i in range(len(words) - 1):
#                             word1 = words[i]
#                             word2 = words[i + 1]
#                             if G.has_edge(word1, word2):
#                                 G[word1][word2]['weight'] += 1
#                             else:
#                                 G.add_edge(word1, word2, weight=1)
#                     category_graphs.append(G)
#             graphs.append((category, category_graphs))
#     return graphs

# # Function to display a graph using Matplotlib
# def display_graph(graph, category_name, graph_index):
#     plt.figure(figsize=(10, 6))
#     pos = nx.spring_layout(graph)
#     nx.draw(graph, pos, with_labels=True, node_size=300, font_size=10, node_color='skyblue', edge_color='gray', linewidths=1)
#     plt.suptitle(f"Graph Example - {category_name}")
#     num_nodes = len(graph.nodes())
#     plt.text(0.5, 0.95, f"Number of Nodes: {num_nodes}", horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
#     plt.show(block=False)


# # Create graphs from files in the cleaned_content folder
# folder_path = 'cleaned_content'
# all_category_graphs = create_graphs_from_files(folder_path)

# # Display the last graph from each category
# for category, category_graphs in all_category_graphs:
#     last_index = len(category_graphs) - 1
#     print(f"Last index for {category} category:", last_index)
#     display_graph(category_graphs[last_index], category, last_index)



