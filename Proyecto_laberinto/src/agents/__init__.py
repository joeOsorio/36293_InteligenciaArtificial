# agents/__init__.py
from agents.agent import Agent
from agents.dfs_agent import DFSAgent
from agents.bfs_agent import BFSAgent
from agents.right_hand_agent import RightHandAgent

AGENTS = {
    "dfs": DFSAgent,
    "bfs": BFSAgent,
    "right_hand": RightHandAgent,
}
