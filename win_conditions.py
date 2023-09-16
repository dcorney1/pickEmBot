import pandas as pd
import numpy as np

array_of_tuples = [
    (['User1'], 35, np.array([[3, -35], [2, 0]])),
    (['User2'], 7, np.array([[2, 0], [3, 0]])),
    (['User3'], 3, np.array([[2, 0], [0, 2]]))
]


def is_win_con(array_of_tuples):
    max_index = None
    max_second_value = -float("inf")
    for index, item in enumerate(array_of_tuples):
        _, second_value, _ = item
        if second_value > max_second_value:
            max_second_value = second_value
            max_index = index
            print(max_index)
    max_key = array_of_tuples[max_index][0]
    max_score = array_of_tuples[max_index][1]
    max_dict = array_of_tuples[max_index][2]
    for row in array_of_tuples:
        if row[0] == max_key:
            continue
        potential_difference = np.sum(np.max(row[2] - max_dict, axis=1))
        score = row[1]
        if score + potential_difference >= max_score:
            return False, None
    return True, max_key


class TreeNode:
    def __init__(self, score, scores_list, name):
        self.name = name
        self.score = score
        self.potentials = scores_list
        self.left = None
        self.right = None
        self.tie = None


class BinaryTree:
    def perfectBinaryTree(self, score, scores_list, group):
        queue = []
        i = 0
        root = TreeNode(score, scores_list, group)
        queue.append(root)
        while len(queue) > 0:
            size = len(queue)
            if i >= len(scores_list):
                break
            else:
                for j in range(size):
                    node = queue.pop(0)
                    node.left = TreeNode(node.score+scores_list[i][0][1], scores_list[i:], scores_list[i][0][0])
                    node.right = TreeNode(node.score+scores_list[i][1][1], scores_list[i:], scores_list[i][1][0])
                    node.tie = TreeNode(node.score+scores_list[i][2][1], scores_list[i:], scores_list[i][2][0])
                    queue.append(node.left)
                    queue.append(node.right)
                    queue.append(node.tie)
            i += 1
        return root

    # Inorder traversal of the tree (Left Root Right)
    def inOrderTraversal(self, node):
        if node is None:
            return
        self.inOrderTraversal(node.left)
        self.test.append((node.score, node.potentials))
        self.inOrderTraversal(node.right)
        return self.test

    # Driver code
    def main(self, score, scores_list, name):
        binaryTreeRoot = self.perfectBinaryTree(score, scores_list, name)
        return binaryTreeRoot


df = pd.read_csv(r'./output.csv')
df = df[['cbs_id','game', 'choice', 't1', 't2', 'weight']]
df['score1'] = df.apply(lambda row: (row['t1'], row['weight']) if row['t1'] == row['choice'] else (row['t1'], 0), axis=1)
df['score2'] = df.apply(lambda row: (row['t2'], row['weight']) if row['t2'] == row['choice'] else (row['t2'], 0), axis=1)
df['score3'] = df.apply(lambda row: (f'Tie: {row["game"]}', 0), axis=1)

groups_dict = {}
for group, group_df in df.groupby('cbs_id'):
    group_df.sort_values(by='game', inplace=True)
    bTree=BinaryTree()
    groups_dict[group] = BinaryTree.main(0, group_df[['score1', 'score2', 'score3']].values.tolist(), group)
