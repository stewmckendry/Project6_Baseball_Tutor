def print_graph_triples(graph, include_metadata=True, max_examples=None):
    print("\n📊 Knowledge Graph Triples:")
    count = 0

    for u, v, d in graph.edges(data=True):
        pred = d.get("predicate", "relatedTo")
        line = f"({u}) --[{pred}]--> ({v})"

        if include_metadata:
            meta = {k: v for k, v in d.items() if k != "predicate"}
            if meta:
                meta_str = ", ".join(f"{k}: {v}" for k, v in meta.items())
                line += f"  [meta: {meta_str}]"

        print(line)
        count += 1
        if max_examples and count >= max_examples:
            break

    print(f"\n🧠 Total: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges\n")

    print("🧾 Node Metadata (explanations, sources):")
    for node, attrs in graph.nodes(data=True):
        relevant = {k: v for k, v in attrs.items() if k in ["explanation", "source", "recommended_action_sequence"]}
        if relevant:
            print(f"• {node}: {relevant}")
