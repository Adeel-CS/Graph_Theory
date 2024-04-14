import networkx as nx
import matplotlib.pyplot as plt

# Create a new graph
graph = nx.DiGraph()  # Use a directed graph since edges are directed

# Load content from the file into a NumPy array
file_path = 'food1.txt'
with open(file_path, 'r') as file:
    file_content = file.read()

# Split the content into different sections based on the '###' delimiter
sections = {}
section_names = ["title", "link", "text"]
content_parts = file_content.split('###')
for i, name in enumerate(section_names):
    if i < len(content_parts):
        sections[name] = content_parts[i].strip()

# Extract the sections from the content
document_title = sections.get("title", "")
link_text = sections.get("link", "")
text_content = sections.get("text", "")

# print("Example document information:")
# print("Document Title:", document_title)
# print("Link Text:", link_text)
# print("Text Content:", text_content)

# Cleaned text content of the example document


# Define sections of the document
sections = {
    "title": document_title,
    "link": link_text,
    "text": text_content
}

# Create a set to store unique words
unique_words = set()

# Add nodes and edges to the graph
for section, content in sections.items():
    words = content.split()  # Split the content into words
    for word in words:
        # Exclude adding the period as a node
        if word != '.' and word not in unique_words:
            # Add node for each unique word
            node_label = f"{word}"  # Label format: word
            graph.add_node(node_label)
            unique_words.add(word)

    # Connect the unique word to the corresponding section node
    for i in range(len(words)-1):
        source_word = words[i]
        target_word = words[i+1]
        # Check if there's a full stop between the words
        if '.' not in source_word and '.' not in target_word:
            graph.add_edge(source_word, target_word, label=section)

# Count the number of nodes created
num_nodes = len(graph.nodes)

# Draw the graph
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(graph, k=0.3)  # Position nodes using the spring layout algorithm with a larger k value
nx.draw(graph, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=8, font_weight="bold")
edge_labels = nx.get_edge_attributes(graph, 'label')
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
plt.suptitle(f"Graph Representation of Example Document (Nodes: {num_nodes})", fontsize=12, y=0.95)
plt.show()
