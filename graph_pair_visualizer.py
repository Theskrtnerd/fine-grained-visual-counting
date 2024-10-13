import json
import networkx as nx
import os
import plotly.graph_objects as go
import matplotlib.pyplot as plt

with open('categories.json', 'r') as f:
    categories = json.load(f)

with open('pairs.json', 'r') as f:
    pairs = json.load(f)

G = nx.Graph()

# Add nodes to the graph with label as an attribute
for category in categories:
    G.add_node(category["abbreviation"], label=category["name"])

# Add edges to the graph
for pair in pairs:
    G.add_edge(pair[0], pair[1])

# Convert NetworkX graph to Plotly graph
pos = nx.spring_layout(G)  # Layout for the nodes

# Create edge traces
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=1, color='#888'),
    hoverinfo='none',
    mode='lines'
)

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += (x0, x1, None)
    edge_trace['y'] += (y0, y1, None)

# Create node traces
node_trace = go.Scatter(
    x=[pos[node][0] for node in G.nodes()],
    y=[pos[node][1] for node in G.nodes()],
    text=[G.nodes[node].get('label', '') for node in G.nodes()],  # Safely access the label
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
                    title='Network Graph',
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[dict(
                        text="Interactive Graph",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002)],
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False))
                )

# Show the figure
fig.show()
