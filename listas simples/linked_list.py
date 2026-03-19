
class Node:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.next = None


class TaskList:
    def __init__(self):
        self.head = None


    def add_task(self, title, description):
        new_node = Node(title, description)

        if self.head is None:
            self.head = new_node
            return True

        current = self.head
        while current.next is not None:
            current = current.next

        current.next = new_node
        return True


    def get_size(self):
        count = 0
        current = self.head

        while current is not None:
            count += 1
            current = current.next

        return count


    def get_task_at(self, position):
        if position < 0:
            return None

        current = self.head
        index = 0

        while current is not None and index < position:
            current = current.next
            index += 1

        return current


    def update_task(self, position, new_title, new_description):
        node = self.get_task_at(position)

        if node is None:
            return False

        node.title = new_title
        node.description = new_description
        return True

    def delete_task(self, position):
        if self.head is None:
            return False

        if position < 0:
            return False

        if position == 0:
            self.head = self.head.next
            return True

        current = self.head
        previous = None
        index = 0

        while current is not None and index < position:
            previous = current
            current = current.next
            index += 1

        if current is None:
            return False

        previous.next = current.next
        return True

    # ------------------------------
    # MOVE TASK BY POSITION
    # ------------------------------
    def move_task(self, from_position, to_position):
        size = self.get_size()

        if size == 0:
            return False

        if from_position < 0 or to_position < 0:
            return False

        if from_position >= size or to_position >= size:
            return False

        if from_position == to_position:
            return True

        
        current = self.head
        previous = None
        index = 0

        while current is not None and index < from_position:
            previous = current
            current = current.next
            index += 1

        if current is None:
            return False

        moved_node = current

        if previous is None:
            self.head = moved_node.next
        else:
            previous.next = moved_node.next


        if to_position == 0:
            moved_node.next = self.head
            self.head = moved_node
            return True

        insert_current = self.head
        insert_index = 0

        while insert_current.next is not None and insert_index < to_position - 1:
            insert_current = insert_current.next
            insert_index += 1

        moved_node.next = insert_current.next
        insert_current.next = moved_node

        return True

    
    def iter_tasks(self):
        current = self.head
        index = 0

        while current is not None:
            yield index, current.title, current.description
            current = current.next
            index += 1
