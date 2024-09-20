import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from Node import Node
class DoublyLinkedList:
    def __init__(self):
        """
        Initializes an empty doubly linked list.
        """
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        """
        Checks if the list is empty.

        Returns:
            True if the list is empty, False otherwise.
        """
        return self.size == 0

    def first(self):
        """
        Retrieves the first element's data in the list.

        Returns:
            The data of the first element in the list.

        Raises:
            ValueError: If the list is empty.
        """
        if self.is_empty():
            raise ValueError("List is empty")
        return self.head.data

    def last(self):
        """
        Retrieves the last element's data in the list.

        Returns:
            The data of the last element in the list.

        Raises:
            ValueError: If the list is empty.
        """
        if self.is_empty():
            raise ValueError("List is empty")
        return self.tail.data

    def insert_head(self, data):
        """
        Inserts a new element at the beginning of the list.

        Parameters:
            data: The data to be inserted at the head of the list.
        """
        newNode = Node(data)
        if self.is_empty():
            #Note you dont have to explicitly set newNode.prev to None because it is already None by default
            self.head = self.tail = newNode
        else:
            newNode.next = self.head
            self.head.prev = newNode
            self.head = newNode
        self.size += 1

    def insert_tail(self, data):
        """
        Inserts a new element at the end of the list.

        Parameters:
            data: The data to be inserted at the tail of the list.
        """
        newNode = Node(data)
        if self.is_empty():
            self.head = self.tail = newNode
        else:
            self.tail.next = newNode
            newNode.prev = self.tail
            self.tail = newNode
        self.size += 1

    def remove_head(self):
        """
        Removes and returns the first element from the list.

        Returns:
            The data of the removed head element.

        Raises:
            ValueError: If the list is empty.
        """
        if self.is_empty():
            raise ValueError("List is empty")
        data = self.head.data
        self.head = self.head.next
        if self.head is not None:
            self.head.prev = None
        else:
            self.tail = None
        self.size -= 1
        return data

    def remove_tail(self):
        """
        Removes and returns the last element from the list.

        Returns:
            The data of the removed tail element.

        Raises:
            ValueError: If the list is empty.
        """
        if self.is_empty():
            raise ValueError("List is empty")
        data = self.tail.data
        self.tail = self.tail.prev
        if self.tail is not None:
            self.tail.next = None
        else:
            self.head = None
        self.size -= 1
        return data

    def insert_after(self, target_data, data):
        """
        Inserts a new element after a specified target element.

        Parameters:
            target_data: The data of the target element to insert after.
            data: The data to be inserted.

        Raises:
            ValueError: If the target data is not found in the list.
        """
        current = self.head
        while current:
            if current.data == target_data:
                if current == self.tail:
                    self.insert_tail(data)
                else:
                    newNode = Node(data)
                    newNode.prev = current
                    newNode.next = current.next
                    current.next.prev = newNode
                    current.next = newNode
                    self.size += 1
                return
            current = current.next
        raise ValueError(f"{target_data} not found in the list")

    def insert_before(self, target_data, data):
        """
        Inserts a new element before a specified target element.

        Parameters:
            target_data: The data of the target element to insert before.
            data: The data to be inserted.

        Raises:
            ValueError: If the target data is not found in the list.
        """
        current = self.head
        while current:
            if current.data == target_data:
                if current == self.head:
                    self.insert_head(data)
                else:
                    newNode = Node(data)
                    newNode.next = current
                    newNode.prev = current.prev
                    current.prev.next = newNode
                    current.prev = newNode
                    self.size += 1
                return
            current = current.next
        raise ValueError(f"{target_data} not found in the list")

    def remove(self, target_data):
        """
        Removes the first node containing the target data from the list.

        Parameters:
            target_data: The data of the node to be removed.

        Raises:
            ValueError: If the target data is not found in the list.
        """
        current = self.head
        while current:
            if current.data == target_data:
                # If the node to remove is the head
                if current == self.head:
                    self.remove_head()
                # If the node to remove is the tail
                elif current == self.tail:
                    self.remove_tail()
                else:
                    # Adjust the pointers of the previous and next nodes
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    self.size -= 1
                return
            current = current.next
        # If the loop completes without finding the target, raise an error
        raise ValueError(f"Node with data {target_data} not found in the list.")

    def display(self):
        """
        Prints the contents of the list from head to tail.
        """
        current = self.head
        while current:
            print(current.data, end=' <=> ' if current.next else '')
            current = current.next  # Update this line to move to the next node
        print()  # Ensure you move to a new line after printing the list
