import networkx as nx
import matplotlib.pyplot as plt

# Function to clean text
def clean_text(text):
    # Implement your text cleaning process here
    cleaned_text = text.lower()  # Convert text to lowercase for consistency
    # Other cleaning steps (e.g., removing stopwords, punctuation, etc.)
    return cleaned_text

# Create a new graph
graph = nx.DiGraph()  # Use a directed graph since edges are directed

# Example document information
document_title = "YAHOO NEWS"
link_text = "MORE NEWS"
text_content = "REUTERS NEWS SERVICE REPORTS"

# Cleaned text content of the example document
cleaned_title = clean_text(document_title)
cleaned_link_text = clean_text(link_text)
cleaned_text_content = clean_text(text_content)

# Define sections of the document
sections = {
    "title": cleaned_title,
    "link": cleaned_link_text,
    "text": cleaned_text_content
}

# Create a set to store unique words
unique_words = set()

# Add nodes and edges to the graph
for section, content in sections.items():
    words = content.split()  # Split the content into words
    for word in words:
        if word not in unique_words:
            # Add node for each unique word
            node_label = f"{word}"  # Label format: word
            graph.add_node(node_label)
            unique_words.add(word)

    # Connect the unique word to the corresponding section node
    for word in words:
        graph.add_edge(word, f"{section}", label=section)

# Draw the graph
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(graph)  # Position nodes using the spring layout algorithm
nx.draw(graph, pos, with_labels=True, node_size=1000, node_color="lightblue", font_size=10, font_weight="bold")
edge_labels = nx.get_edge_attributes(graph, 'label')
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
plt.title("Graph Representation of Example Document")
plt.show()
