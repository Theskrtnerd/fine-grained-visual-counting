import json
import networkx as nx
from networkx.algorithms.community import kernighan_lin_bisection
import plotly.graph_objects as go

def load_data(categories_path, pairs_path):
    with open(categories_path, 'r') as f:
        categories = json.load(f)
    with open(pairs_path, 'r') as f:
        pairs = json.load(f)
    return categories, pairs

def create_graph(categories, pairs):
    G = nx.Graph()
    for category in categories:
        G.add_node(category["abbreviation"])
    for pair in pairs:
        G.add_edge(pair[0], pair[1])
    return G

def initialize_clusters(G, n_clusters):
    # Start with a single partition using the KL algorithm
    partition = kernighan_lin_bisection(G)
    
    # If more than 2 clusters are needed, iteratively apply KL bisection
    while len(partition) < n_clusters:
        new_partition = []
        for subgraph in partition:
            subgraph_nodes = list(subgraph)
            if len(subgraph_nodes) > 1:
                subgraph_partition = kernighan_lin_bisection(G.subgraph(subgraph_nodes))
                new_partition.extend(subgraph_partition)
            else:
                new_partition.append(subgraph)
        partition = new_partition
    
    # Convert partition to clusters
    clusters = [set(part) for part in partition[:n_clusters]]
    
    # Count the number of crossing edges
    crossing_edges = 0
    for i, cluster in enumerate(clusters):
        for j in range(i + 1, len(clusters)):
            for node in cluster:
                for neighbor in G.neighbors(node):
                    if neighbor in clusters[j]:
                        crossing_edges += 1
    
    print(f"Number of crossing edges between clusters: {crossing_edges}")
    
    return clusters

def cluster_graph(G, n_clusters):
    clusters = initialize_clusters(G, n_clusters)
    edges_removed = 0

    while True:
        cluster_sizes = [len(cluster) for cluster in clusters]
        max_size = max(cluster_sizes)
        min_size = min(cluster_sizes)
        if max_size - min_size <= 1:
            break

        # Find the largest and smallest clusters
        largest_cluster_index = cluster_sizes.index(max_size)
        smallest_cluster_index = cluster_sizes.index(min_size)

        # Move a node from the largest cluster to the smallest cluster
        largest_cluster = list(clusters[largest_cluster_index])
        smallest_cluster = list(clusters[smallest_cluster_index])

        # Find the node with the fewest connections to other clusters
        node_to_move = min(largest_cluster, key=lambda node: sum(1 for neighbor in G.neighbors(node) if neighbor not in largest_cluster))

        largest_cluster.remove(node_to_move)
        smallest_cluster.append(node_to_move)

        # Update the clusters
        clusters[largest_cluster_index] = set(largest_cluster)
        clusters[smallest_cluster_index] = set(smallest_cluster)

        # Count the edges removed
        for node in clusters[largest_cluster_index]:
            if G.has_edge(node, node_to_move):
                edges_removed += 1
                G.remove_edge(node, node_to_move)
        for node in clusters[smallest_cluster_index]:
            if G.has_edge(node, node_to_move):
                edges_removed += 1
                G.remove_edge(node, node_to_move)

    print(f"Number of edges removed: {edges_removed}")
    return clusters

def visualize_clusters(G, clusters):
    pos = nx.spring_layout(G)  # Layout for the nodes

    for i, cluster in enumerate(clusters):
        subgraph = G.subgraph(cluster)

        # Create edge traces
        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines'
        )

        for edge in subgraph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += (x0, x1, None)
            edge_trace['y'] += (y0, y1, None)

        # Create node traces
        node_trace = go.Scatter(
            x=[pos[node][0] for node in subgraph.nodes()],
            y=[pos[node][1] for node in subgraph.nodes()],
            text=[G.nodes[node].get('label', '') for node in subgraph.nodes()],
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                )
            )
        )

        # Create the figure
        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title=f'Cluster {i+1}',
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text=f"Cluster {i+1}",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False))
                        )

        # Show the figure
        fig.show()

def main():
    categories_path = 'categories.json'
    pairs_path = 'pairs.json'
    n_clusters = 5  # Adjust the number of clusters as needed

    categories, pairs = load_data(categories_path, pairs_path)
    G = create_graph(categories, pairs)
    clusters = cluster_graph(G, n_clusters)

    for i, cluster in enumerate(clusters):
        print(f"Cluster {i+1}: {list(cluster)}")

if __name__ == "__main__":
    main()