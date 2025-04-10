from pyvis.network import Network
import networkx as nx
import tempfile
import streamlit.components.v1 as components

from src.utils.logging.logging import setup_logger
logger = setup_logger()


def visualize_graph(graph, highlight_nodes=None):

    logger.info("Visualizing the graph...")

    net = Network(height="600px", width="100%", directed=True)
    net.barnes_hut()  # for physics layout (spreading out the nodes in a nice way)

    highlight_nodes = set(highlight_nodes or [])

    # add and color nodes
    for node in graph.nodes():
        color = "#ffcc00" if node in highlight_nodes else "#97c2fc"
        net.add_node(node, label=node, color=color)
    logger.info("Nodes added to the graph.")

    # add edges and labels
    for u, v, d in graph.edges(data=True):
        label = d.get("predicate", "")
        net.add_edge(u, v, label=label)
    logger.info("Edges added to the graph.")

    # Save to temp file and display in Streamlit
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.show(tmp_file.name, notebook=False)
        components.html(open(tmp_file.name, 'r').read(), height=600, scrolling=True)
    logger.info("Graph visualization complete.")
