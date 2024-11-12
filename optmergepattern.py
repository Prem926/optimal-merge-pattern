import streamlit as st
import heapq
import time
import matplotlib.pyplot as plt
import networkx as nx

def draw_visualization(file_sizes, merge_cost, step):
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.set_title(f"Step {step}: Merged file size = {merge_cost}", fontsize=14)
    
    x_offset = 0
    colors = ['#FF6F61', '#6FA6FF', '#FFD27F', '#95E06C', '#F392B4']
    
    # Draw the rectangles
    for i, size in enumerate(file_sizes):
        rect_width = size  # scaled for better fit
        ax.barh(1, rect_width, left=x_offset, color=colors[i % len(colors)], edgecolor='black')
        ax.text(x_offset + rect_width / 2, 1, str(size), va='center', ha='center', color='white', fontsize=12)
        x_offset += rect_width
    
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_xlim(0, sum(file_sizes) + 10)
    
    st.pyplot(fig)
    time.sleep(2)  # Pause to simulate animation

def draw_merge_tree(tree_graph, step):
    # Draw the merging tree
    pos = nx.spring_layout(tree_graph)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title(f"Merge Tree at Step {step}", fontsize=14)

    # Draw nodes and edges
    nx.draw(tree_graph, pos, with_labels=True, node_color="#95E06C", edge_color="#FF6F61", node_size=1000, font_size=12, ax=ax)

    st.pyplot(fig)
    time.sleep(2)

def optimal_merge_pattern(file_sizes):
    steps = ""
    total_cost = 0
    heapq.heapify(file_sizes)
    step = 1

    placeholder = st.empty()
    tree_placeholder = st.empty()

    # Initialize the tree graph
    tree_graph = nx.Graph()

    while len(file_sizes) > 1:
        first_smallest = heapq.heappop(file_sizes)
        second_smallest = heapq.heappop(file_sizes)
        merge_cost = first_smallest + second_smallest
        total_cost += merge_cost
        heapq.heappush(file_sizes, merge_cost)

        steps += f"Merge {first_smallest} and {second_smallest}: New file = {merge_cost}, Total cost = {total_cost}\n"
        
        # Add nodes and edges to the merge tree
        tree_graph.add_node(merge_cost)
        tree_graph.add_edge(first_smallest, merge_cost)
        tree_graph.add_edge(second_smallest, merge_cost)

        # Update visualizations
        with placeholder.container():
            draw_visualization(file_sizes, merge_cost, step)

        with tree_placeholder.container():
            draw_merge_tree(tree_graph, step)

        step += 1

    steps += f"\nFinal total merge cost: {total_cost}"
    return steps

# Streamlit UI
st.title("Optimal Merge Pattern (Heap-based)")

file_sizes_str = st.text_input("Enter file sizes separated by spaces", "10 20 30 40 50")
compute_button = st.button("Compute")

if compute_button:
    try:
        file_sizes = list(map(int, file_sizes_str.split()))
        if len(file_sizes) < 2:
            st.error("Please enter at least two file sizes.")
        else:
            result = optimal_merge_pattern(file_sizes)
            st.write(result)
    except ValueError:
        st.error("Please enter valid integers separated by spaces.")
