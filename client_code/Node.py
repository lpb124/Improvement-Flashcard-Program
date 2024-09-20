import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
class Node:
    def __init__(self, data=None):
        self.data = data # data node holds actual data
        self.next = None # the pointer points to the next node in the DLL
        self.prev = None # the pointer points to the previous node in the DLL
# the Node class is seperate from the DoublyLinkedList class
