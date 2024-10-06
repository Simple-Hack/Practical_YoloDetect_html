class MyQueue(object):
    class Node(object):
        def __init__(self,value):
            self.next=None
            self.value=value
    
    def __init__(self):
        self.head=None
        self.tail=None

    def empty(self)->bool:
        return self.head is None

    def put(self,value):
        new_node=self.Node(value)
        if self.head is None:
            self.head=self.tail=new_node
        else:
            self.tail.next=new_node
            self.tail=new_node

    def get(self):
        if self.head is None:
            return None
        del_node=self.head
        self.head=self.head.next
        return del_node.value
