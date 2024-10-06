class MyList(object):
    class Node(object):
        def __init__(self,value):
            self.next=None
            self.prev=None
            self.value = value
            pass
         
    def __init__(self):
        self.size=0
        self.head=None
        self.tail=None

    def append(self,data):
        new_node=self.Node(data)
        if self.head is None:
            self.head= new_node
            self.tail= new_node
        else:
            if self.tail is not None:
                self.tail.next= new_node
            new_node.prev= self.tail
            self.tail= new_node
            self.tail.next=self.head
            self.head.prev= self.tail
        self.size+=1

    def pop(self):
        ret=self.tail
        to_del=self.tail
        self.tail=self.tail.prev
        del to_del
        self.size-=1
        return ret.value

    def return_list(self,index:int):
        ret=self.head
        for _ in range(index):
            ret=ret.next
        return ret.value

    def size(self)->int:
        return self.size
