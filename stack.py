class nodeStack:
    def __init__(self):
        self.nodeList = []
    def build_tree (self, parent ,n):
        curr_node = node(parent)
        for x in range (n):
            popped = self.nodeList.pop()
            curr_node.addChild(popped)
        self.nodeList.append(curr_node)


class node:
    def __init__(self,obj):
        self.content = obj
        self.childList = []
    def addChild(self,child):
        self.childList.insert(0,child)

def preOrderTraversal(Node,str=''):
    print(str+Node.content)
    for c in Node.childList:
        preOrderTraversal(c,str+'.')