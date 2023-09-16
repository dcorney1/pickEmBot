class TreeNode:
    def __init__(self, val):
        self.val = val
        self.children = []

def compare_nodes_between_trees(trees):
    if not trees:
        return

    n = len(trees)
    for i in range(n):
        if len(trees[i]) != len(trees[0]):
            raise ValueError("All trees must have the same number of nodes.")

    for node_index in range(len(trees[0])):
        node_values = [tree[node_index].val for tree in trees]

        if all(val == node_values[0] for val in node_values):
            print(f"Node {node_index}: Equal values in all trees")
        else:
            largest_value = max(node_values)
            largest_trees = [i for i, val in enumerate(node_values) if val == largest_value]

            for tree_index in largest_trees:
                print(f"Node {node_index}: Tree {tree_index} has the largest value ({largest_value})")

# Usage example:
# Create your equal-sized trees and store them in a list of lists
trees = [[TreeNode(10), TreeNode(20), TreeNode(30)],
         [TreeNode(15), TreeNode(25), TreeNode(35)],
         [TreeNode(10), TreeNode(20), TreeNode(30)]]

compare_nodes_between_trees(trees)