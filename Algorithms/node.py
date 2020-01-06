# node.py

from dataclasses import dataclass


@dataclass
class Node:
    data:str
    next:object = None
