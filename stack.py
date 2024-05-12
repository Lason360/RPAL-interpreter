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
    definedNodes = ['let','lambda','where','tau','aug','->','or', '&','not','gr','ge','ls','le','eq','ne','neg','gamma','true','dummy','within','and','rec','=','fcn_form','()',',','+','-','*','/','**','@']
    if Node.content not in definedNodes:
        if Node.content.type == '<IDENTIFIER>':
            printFormat = '<ID: '+ Node.content.content +'>'
        elif Node.content.type == '<INTEGER>':
            printFormat = '<INT: '+ Node.content.content +'>'
        elif Node.content.type == '<STRING>':
            printFormat = '<STR: '+ Node.content.content +'>' 
    else:
        printFormat = Node.content           
    print(str+printFormat)
    for c in Node.childList:
        preOrderTraversal(c,str+'.')