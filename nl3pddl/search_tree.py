
# This file implements the search tree structure used to store the conversation
# history and scores for each branch.

from langchain_core.messages import HumanMessage, AIMessage
from typing import Any

class MessageTree:
    """ 
    A tree of messages, the leaves are a queue of scored messages that may be
    selected from to continue the conversation.
    """

    def __init__(self, parent=None, message: HumanMessage | AIMessage | None = None):
        self.parent = parent
        self.children = []
        self.message = message
        self.score = 0
        self.json = None # Json returned by the model if any

    def leaves(self) -> list['MessageTree']:
        """ Returns all leaves of the tree. """
        if len(self.children) == 0:
            return [self]
        leaves = []
        for child in self.children:
            leaves.extend(child.leaves())
        return leaves

    def history(self) -> list[HumanMessage | AIMessage]:
        """ Returns the message history from the root to this node. """
        if self.parent is None:
            return []
        return self.parent.history() + [self.message]

    def get_max_score_leaf(self) -> 'MessageTree':
        """ Returns the leaf with the highest score. """
        leaves = self.leaves()
        if len(leaves) == 0:
            return None
        return max(leaves, key=lambda x: x.score)
    
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

class IndexedMessageTree:
    """ 
    Bundles a MessageTree with an index to a specific node for ease of
    integrating with langgraph.
    """

    def __init__(self):
        self.root = MessageTree()
        self.index = []

    def get(self) -> MessageTree:
        """ Returns the current node. """
        return self.root.atIndex(self.index)
    
    def index_leaves(self) -> list[MessageTree]:
        """ Returns all leaves of the tree. """
        return self.get().leaves()

    def history(self) -> list[HumanMessage | AIMessage]:
        """ Returns the message history from the root to the current node. """
        return self.get().history()

    def json_last(self) -> Any:
        """ Returns the json object of the current node. """
        return dict(self.get().json)

    def insert_on_current_branch_json_score(self, message : HumanMessage | AIMessage, json: dict, score: float) -> 'IndexedMessageTree':
        """ Inserts a message on the current branch. """
        node = self.root.atIndex(self.index)
        new_node = MessageTree(parent=node, message=message)
        node.children.append(new_node)
        self.index.append(len(node.children) - 1)
        new_node.json = json
        new_node.score = score
        return self

    def insert_on_current_branch(self, message : HumanMessage | AIMessage) -> 'IndexedMessageTree':
        """ 
        Inserts a message on the current branch. 
        Defaults to inheriting score 
        and json from the current node.
        """
        node = self.root.atIndex(self.index)
        return self.insert_on_current_branch_json_score(message, node.json, node.score)

    def insert_on_current_branch_score(self, message : HumanMessage | AIMessage, score: float) -> 'IndexedMessageTree':
        """ 
        Inserts a message on the current branch.
        Defaults to inheriting json from the current node.
        """
        node = self.root.atIndex(self.index)
        return self.insert_on_current_branch_json_score(message, node.json, score)

    def insert_on_current_branch_json(self, message : HumanMessage | AIMessage, json: dict) -> 'IndexedMessageTree':
        """ Inserts a message on the current branch. Defaults to inheriting score """
        node = self.root.atIndex(self.index)
        return self.insert_on_current_branch_json_score(message, json, node.score)

    def select_best_branch(self) -> 'IndexedMessageTree':
        """ Selects the best branch and moves the index to it. """
        best_leaf = self.root.get_max_score_leaf()
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
            new_node.score = node.score
            node.children.append(new_node)