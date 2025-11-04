
"""
This file implements the search tree structure used to store the conversation
history and scores for each branch.
"""

from typing import Any

from langchain_core.messages import HumanMessage, AIMessage

from nl3pddl.config import ALWAYS_EVALUATE
from nl3pddl.params import Params

class MessageTree:
    """ 
    Data structure representing a search tree of messages, 
    the leaves from a queue (open list) of scored messages that may be
    selected from to continue the conversation.
    """
    _next_id = 0

    def __init__(self,
        params: Params,
        parent=None, 
        message: HumanMessage | AIMessage | None = None,
        langraph_node: str = "no-node",
    ):
        self.id = MessageTree._next_id
        MessageTree._next_id += 1
        self.params = params

        self.parent = parent
        self.children = []
        self.message = message
        self.json = None                        # last valid json output from the LLM
        self.langraph_node = langraph_node      # name of the corresponding langraph node if any
        self.g = 0                              # Cost to reach this node, lower is better
        self.h = float('inf')                   # Heuristic score, lower is better
        self.score = float('inf')               # Combined score, lower is better
        self.true_score = 0                     # True score wrt eval problems

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
        """ Returns the true message history from the root to this node. """
        if self.parent is None:
            return []
        return self.parent.message_history() + [self.message]
    
    def squashed_message_history(self) -> list[HumanMessage | AIMessage]:
        """ Returns the message history from the root to this node, merging consecutive human messages into a single message. """
        if self.parent is None:
            return []
        history = self.parent.squashed_message_history()
        if isinstance(self.message, HumanMessage) and history and isinstance(history[-1], HumanMessage):
            # Merge consecutive human messages
            history[-1] = HumanMessage(
                content=history[-1].content + "\n" + self.message.content
            )
        else:
            history.append(self.message)
        return history


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
        """
        Returns a string representation of the tree for debugging purposes.
        """
        s = " " * depth + f"-{depth} id:{self.id} {self.langraph_node} "
        if self.message is None:
            s += f"Root\n"
        elif isinstance(self.message, str):
            # Sometimes a string is used instead of a message object
            # we fallback to this for safety
            s += f" str? (G: {self.g}, H: {self.h}, Score: {self.score})\n"
        else:
            if ALWAYS_EVALUATE:
                s += f"{self.message.type.upper()} (G: {self.g}, H: {self.h}, Score: {self.score}, True Score: {self.true_score})\n"
            else:
                s += f"{self.message.type.upper()} (G: {self.g}, H: {self.h}, Score: {self.score})\n"
        for child in self.children:
            s += child.to_str(depth + 1)
        return s
    
    def update_score(
        self, 
        h_score: float,
        g_score : float | None = None
    ) -> 'IndexedMessageTree':
        """ Updates the score of the current node, given a new heuristic score. """
        self.h = h_score
        if g_score is None:
            self.g = self.parent.g + 1 if self.parent is not None else 0
        else:
            self.g = g_score
        # Evaluate the combined score using the search heuristic
        self.score = eval(self.params.search_heuristic, {'G': self.g, 'H': self.h})
        return self

class IndexedMessageTree:
    """ 
    Bundles a MessageTree with an index to a specific node for ease of
    integrating with langgraph.
    """

    def __init__(self, params: Params):
        self.root = MessageTree(params)
        self.index = []

    def get(self) -> MessageTree:
        """ Returns the current node. """
        return self.root.atIndex(self.index)
    
    def index_leaves(self) -> list[MessageTree]:
        """ Returns all leaves of the tree. """
        return self.get().leaves()

    def message_history(self) -> list[HumanMessage | AIMessage]:
        """ Returns the message history from the root to the current node. """
        return self.get().message_history()

    def squashed_message_history(self) -> list[HumanMessage | AIMessage]:
        """ Returns the squashed message history (compressed human messages) from the root to the current node. """
        return self.get().squashed_message_history()

    def json_last(self) -> Any:
        """ Returns the json object of the current node. """
        return dict(self.get().json)

    def insert_on_current_branch_json_score(
        self,
        message : HumanMessage | AIMessage,
        json: dict,
        h_score: float, 
        langraph_node : str = ""
    ) -> 'IndexedMessageTree':
        """ Inserts a message on the current branch. """
        node = self.root.atIndex(self.index)
        new_node = MessageTree(node.params, node, message, langraph_node)
        node.children.append(new_node)
        self.index.append(len(node.children) - 1)
        new_node.json = json
        new_node.update_score(h_score, node.g + 1)
        # Evaluate the combined score using the search heuristic
        return self

    def insert_on_current_branch(
        self, 
        message : HumanMessage | AIMessage,
        langraph_node : str = ""
    ) -> 'IndexedMessageTree':
        """ 
        Inserts a message on the current branch. 
        Defaults to inheriting score 
        and json from the current node.
        """
        n = self.get()
        return self.insert_on_current_branch_json_score(message, n.json, n.h, langraph_node)

    def insert_on_current_branch_score(
        self, 
        message : HumanMessage | AIMessage,
        h_score: float,
        langraph_node : str = ""
    ) -> 'IndexedMessageTree':
        """ 
        Inserts a message on the current branch.
        Defaults to inheriting json from the current node.
        """
        n = self.get()
        return self.insert_on_current_branch_json_score(message, n.json, h_score, langraph_node)

    def insert_on_current_branch_json(
        self, 
        message : HumanMessage | AIMessage,
        json: dict,
        langraph_node : str = ""
    ) -> 'IndexedMessageTree':
        """ 
        Inserts a message on the current branch. Defaults to inheriting score 
        """
        n = self.get()
        return self.insert_on_current_branch_json_score(message, json, n.h, langraph_node)

    def select_best_branch(self) -> 'IndexedMessageTree':
        """ Selects the best branch and moves the index to it. """
        best_leaf = self.root.get_min_score_leaf()
        if best_leaf is None:
            return self
        self.index = best_leaf.index()
        return self

    def insert_batch_on_current_branch(
        self,
        messages: list[HumanMessage | AIMessage],
        langraph_node: str = ""
    ) -> None:
        """
        Inserts multiple messages on the current branch.
        Defaults to inheriting score and json from the current node.
        WARNING: This does NOT move the index to any of the new nodes, and
        simply adds them as children of the current node.
        use select_best_branch() after this to select one of them.
        """
        node = self.get()
        for message in messages:
            new_node = MessageTree(node.params, node, message, langraph_node)
            new_node.update_score(node.h, node.g + 1)
            node.children.append(new_node)

    def to_str(self) -> None:
        """ Prints the tree for debugging purposes. """
        return self.root.to_str(0)
    
    def update_score(
        self, 
        h_score: float,
        g_score : float | None = None
    ) -> 'IndexedMessageTree':
        """ Updates the score of the current node, given a new heuristic score. """
        self.get().update_score(h_score, g_score)
        return self

    def domain_construction_history(self) -> list['MessageTree']:
        """ Return the history of nodes from the build_domain node to the current node """
        node = self.get()
        history = node.node_history()
        # find the build_domain node
        build_domain_index = None
        for i, n in enumerate(history):
            if n.langraph_node == "build_domain":
                build_domain_index = i
                break
        if build_domain_index is None:
            return []
        return history[build_domain_index:]

    def H_history_str(self) -> str:
        """ Return a string of the hscores from the build domain node to the current node, seperated by , """
        history = self.domain_construction_history()
        return ", ".join([f"{n.h:.2f}" for n in history])
    
    def true_history_str(self) -> str:
        """ Return a string of the true scores from the build domain node to the current node, seperated by , """
        history = self.domain_construction_history()
        return ", ".join([f"{n.true_score}" for n in history])

#Testing...
# tree = IndexedMessageTree(Params())
# tree.insert_on_current_branch(HumanMessage("Hello"))
# tree.insert_on_current_branch(AIMessage("Hi there!"))
# tree.insert_on_current_branch(HumanMessage("How are you?"))
# tree.insert_batch_on_current_branch([AIMessage("I'm good."), AIMessage("How can I help you?")])
# tree.select_best_branch()
# print(tree.to_str())
# print("Nice")