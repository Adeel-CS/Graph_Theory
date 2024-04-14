import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Load content from the file into a NumPy array
file_path = 'food1.txt'
with open(file_path, 'r') as file:
    file_content = file.read()

# Split the content into different sections based on the '###' delimiter
sections = file_content.split('###')

# Check if all sections are present
if len(sections) >= 3:
    # Create a new graph
    graph = nx.Graph()

    # Extract sections
    title = sections[0].strip()  # First part before the first '###'
    link = sections[1].strip()    # Second part between the first and second '###'
    text = sections[2].strip()    # Third part after the second '###'

    # Split each section into words and add unique words to the graph
    unique_words = set()  # To store unique words (excluding full stops)
    for section_content in [title, link, text]:
        words = section_content.split()  # Split the content into words
        for word in words:
            # Add unique words to the graph (excluding full stops)
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
else:
    print("Error: Not enough sections found in the file.")






# import numpy as np

# # Load content from the file into a NumPy array
# file_path = 'food1.txt'
# with open(file_path, 'r') as file:
#     file_content = file.read()

# # Split the content into different sections based on the '###' delimiter
# sections = np.split(file_content.split('###'), [1, 2])

# # Extract the sections
# title = sections[0][0].strip()  # First part before the first '###'
# link = sections[1][0].strip()    # Second part between the first and second '###'
# text = sections[2][0].strip()    # Third part after the second '###'

# # Display the sections
# print("Title:", title)
# print("Link:", link)
# print("Text:", text)
