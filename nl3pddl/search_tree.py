
# This file implements the search tree structure used to store the conversation
# history and scores for each branch.


import sys
from typing import Any

from langchain_core.messages import HumanMessage, AIMessage

from nl3pddl.params import Params

class MessageTree:
    """ 
    A tree of messages, the leaves are a queue of scored messages that may be
    selected from to continue the conversation.
    """

    def __init__(self, parent=None, message: HumanMessage | AIMessage | None = None):
        self.parent = parent
        self.children = []
        self.message = message
        self.g = 0
        self.h = float('inf') # Heuristic score, lower is better
        self.score = float('inf') # Combined score, lower is better
        self.json = None # Json returned by the model if any

    def leaves(self) -> list['MessageTree']:
        """ Returns all leaves of the tree. """
        if len(self.children) == 0:
            return [self]
        leaves = []
        for child in self.children:
            leaves.extend(child.leaves())
        return leaves

    def node_history(self) -> list['MessageTree']:
        """ Returns the message history from the root to this node. """
        if self.parent is None:
            return []
        return self.parent.node_history() + [self]

    def message_history(self) -> list[HumanMessage | AIMessage]:
        """ Returns the message history from the root to this node. """
        if self.parent is None:
            return []
        return self.parent.message_history() + [self.message]

    def get_min_score_leaf(self) -> 'MessageTree':
        """ Returns the leaf with the lowest score. """
        leaves = self.leaves()
        if len(leaves) == 0:
            return None
        return min(leaves, key=lambda x: x.score)
    
    def index(self) -> list[int]:
        """ Returns the index of this node in the tree. """
        if self.parent is None:
            return []
        return self.parent.index() + [self.parent.children.index(self)]
    
    def atIndex(self, index: list[int]) -> 'MessageTree':
        """ Returns the node at the given index. """
        if len(index) == 0:
            return self
        return self.children[index[0]].atIndex(index[1:])
    
    def to_str(self, depth: int) -> str:
        """ TODO: move to main class """
        s = None
        if self.message is None:
            s = f"-{depth} Root\n"
        elif isinstance(self.message, str):
            s = " " * depth + f"-{depth} str? (G: {self.g}, H: {self.h}, Score: {self.score})\n"
        else:
            s = " " * depth + f"-{depth} {self.message.type.upper()} (G: {self.g}, H: {self.h}, Score: {self.score})\n"
        for child in self.children:
            s += child.to_str(depth + 1)
        return s

class IndexedMessageTree:
    """ 
    Bundles a MessageTree with an index to a specific node for ease of
    integrating with langgraph.
    """

    def __init__(self, p : Params):
        self.root = MessageTree()
        self.index = []
        self.params = p

    def get(self) -> MessageTree:
        """ Returns the current node. """
        return self.root.atIndex(self.index)
    
    def index_leaves(self) -> list[MessageTree]:
        """ Returns all leaves of the tree. """
        return self.get().leaves()

    def message_history(self) -> list[HumanMessage | AIMessage]:
        """ Returns the message history from the root to the current node. """
        return self.get().message_history()

    def json_last(self) -> Any:
        """ Returns the json object of the current node. """
        return dict(self.get().json)


    def update_score(self, h_score: float) -> 'IndexedMessageTree':
        """ Updates the score of the current node. """
        node = self.root.atIndex(self.index)
        node.h = h_score
        # Evaluate the combined score using the search heuristic
        node.score = eval(self.params.search_heuristic, {'G': node.g, 'H': node.h})
        return self

    def insert_on_current_branch_json_score(self, message : HumanMessage | AIMessage, json: dict, h_score: float) -> 'IndexedMessageTree':
        """ Inserts a message on the current branch. """
        node = self.root.atIndex(self.index)
        new_node = MessageTree(parent=node, message=message)
        node.children.append(new_node)
        self.index.append(len(node.children) - 1)
        new_node.g = node.g + 1
        new_node.h = h_score
        new_node.json = json
        # Evaluate the combined score using the search heuristic
        new_node.score = eval(self.params.search_heuristic, {'G': new_node.g, 'H': new_node.h})
        return self

    def insert_on_current_branch(self, message : HumanMessage | AIMessage) -> 'IndexedMessageTree':
        """ 
        Inserts a message on the current branch. 
        Defaults to inheriting score 
        and json from the current node.
        """
        node = self.root.atIndex(self.index)
        return self.insert_on_current_branch_json_score(message, node.json, node.h)

    def insert_on_current_branch_score(self, message : HumanMessage | AIMessage, h_score: float) -> 'IndexedMessageTree':
        """ 
        Inserts a message on the current branch.
        Defaults to inheriting json from the current node.
        """
        node = self.root.atIndex(self.index)
        return self.insert_on_current_branch_json_score(message, node.json, h_score)

    def insert_on_current_branch_json(self, message : HumanMessage | AIMessage, json: dict) -> 'IndexedMessageTree':
        """ Inserts a message on the current branch. Defaults to inheriting score """
        node = self.root.atIndex(self.index)
        return self.insert_on_current_branch_json_score(message, json, node.h)

    def select_best_branch(self) -> 'IndexedMessageTree':
        """ Selects the best branch and moves the index to it. """
        best_leaf = self.root.get_min_score_leaf()
        if best_leaf is None:
            return self
        self.index = best_leaf.index()
        return self

    def insert_batch_on_current_branch(self, messages: list[HumanMessage | AIMessage]):
        """ Inserts multiple messages on the current branch. Defaults to inheriting score """
        """ This should be immediately followed by a select_best_branch() call """
        node = self.get()
        for message in messages:
            new_node = MessageTree(parent=node, message=message)
            new_node.h = node.h
            new_node.g = node.g + 1
            new_node.score = eval(self.params.search_heuristic, {'G': new_node.g, 'H': new_node.h})
            new_node.json = node.json
            node.children.append(new_node)

    def to_str(self) -> None:
        """ Prints the tree for debugging purposes. """
        return self.root.to_str(0)

#Testing...
# tree = IndexedMessageTree(Params())
# tree.insert_on_current_branch(HumanMessage("Hello"))
# tree.insert_on_current_branch(AIMessage("Hi there!"))
# tree.insert_on_current_branch(HumanMessage("How are you?"))
# tree.insert_batch_on_current_branch([AIMessage("I'm good."), AIMessage("How can I help you?")])
# tree.select_best_branch()
# print(tree.to_str())
# print("Nice")