class nodeStack:
    #stack of nodes to build the tree
    def __init__(self):
        self.nodeList = []
    def build_tree (self, parent ,n):
        #building a perticular node, extending the tree
        curr_node = node(parent)
        for x in range (n):
            popped = self.nodeList.pop()
            curr_node.addChild(popped)
        self.nodeList.append(curr_node)

class tree:
    #ref to the head of the tree
    def __init__(self, N):
        self.head = N
    


class node:
    #nodes to hold the token objects
    def __init__(self,obj):
        self.content = obj
        self.childList = []
    def addChild(self,child):
        #adds a child to a node. used in standardization
        self.childList.insert(0,child)
    def appendChild(self,child1,child2):
        #adds 2 child to a node. used in standardization
        self.childList.append(child1)
        self.childList.append(child2)

    def standardizeNode(self):
        #standardize the node tree part
        newNodeChilds = []
        for c in self.childList:
            #standardize children of node
            newNodeChilds.append(c.standardizeNode())
        self.childList = newNodeChilds

        if self.content == 'let':
            #let standardization
            gammaNode = node('gamma')
            lambdaNode = node('lambda')
            X = self.childList[0].childList[0]
            E = self.childList[0].childList[1]
            P = self.childList[1]
            lambdaNode.appendChild(X,P)
            gammaNode.appendChild(lambdaNode,E)
            return gammaNode
        
        elif self.content == 'where':
            #where standardization
            gammaNode = node('gamma')
            lambdaNode = node ('lambda')
            P = self.childList[0]
            X = self.childList[1].childList[0]
            E = self.childList[1].childList[1]
            lambdaNode.appendChild(X,P)
            gammaNode.appendChild(lambdaNode,E)
            return gammaNode

        elif self.content == 'within':
            #within standardization
            eqNode = node('=')
            gammaNode = node('gamma')
            lambdaNode = node('lambda')
            X1 = self.childList[0].childList[0]
            E1 = self.childList[0].childList[1]
            X2 = self.childList[1].childList[0]
            E2 = self.childList[1].childList[1]

            lambdaNode.appendChild(X1,E2)
            gammaNode.appendChild(lambdaNode,E1)
            eqNode.appendChild(X2,gammaNode)

            return eqNode
        
        elif self.content == 'rec':
            #rec standardization
            eqNode = node('=')
            gammaNode = node('gamma')
            lambdaNode = node('lambda')
            YstarNode = node('Ystar')
            X = self.childList[0].childList[0]
            E = self.childList[0].childList[1]

            lambdaNode.appendChild(X,E)
            gammaNode.appendChild(YstarNode,lambdaNode)
            eqNode.appendChild(X,gammaNode)
            
            return eqNode
        
        elif self.content == 'fcn_form':
            #fcn_form standardization
            eqNode = node('=')
            numVar = len(self.childList)-2
            P = self.childList[0]
            E = self.childList[-1]
            eqNode.childList.append(P)
            head = eqNode
            for x in range (0,numVar):
                head.childList.append(node('lambda'))
                head.childList[1].childList.append(self.childList[1+x])
                head = head.childList[1]
            head.childList.append(E)
            return eqNode

        elif self.content == 'and':
            #and standardization
            eqNode = node('=')
            xList = []
            eList = []
            for eq in self.childList:
                xList.append(eq.childList[0])
                eList.append(eq.childList[1])
            eqNode.appendChild(node(','),node('tau'))
            self.childList[0].childList = xList
            self.childList[1].childList = eList
            return eqNode
        
        elif self.content == '@':
            #@ standardization
            gammaNode1 = node('gamma')
            gammaNode2 = node('gamma')
            E1 = self.childList[0]
            N = self.childList[1]
            E2 = self.childList[2]
            gammaNode1.appendChild(gammaNode2,E2)
            gammaNode2.appendChild(N,E1)
            return gammaNode2

        elif self.content == 'lambda':
            #lambda standardization
            numVar = len(self.childList)-1
            lambdaNode = node('lambda')
            E = self.childList[-1]
            head = lambdaNode
            for x in range (numVar):
                head.childList.append(self.childList[x])
                if x<numVar-1:
                    head.childList.append(node('lambda'))
                    head = head.childList[1]
            head.childList.append(E)
            return lambdaNode
         
        else:
            return self
        
def usableStandardizedTree(root):
    #creates a tree that is usable by the cse Machine. Nodes are refered directly to object content
    definedNodes = ['let','lambda','where','tau','aug','->','or', '&','not','gr','ge','ls','le','eq','ne','neg','gamma','true','dummy','within','and','rec','=','fcn_form','()',',','+','-','*','/','**','@','nil','Ystar']
    #defined nodes are diretly refferenced from node.content

    if root.content not in definedNodes:
        
        if root.content.type == '<IDENTIFIER>':
            #identifier node content
            newRoot = node('<ID:'+ root.content.content +'>')
            return newRoot
        elif root.content.type == '<INTEGER>':
            #int node content
            newRoot = node('<INT:'+ root.content.content +'>')
            return newRoot
        elif root.content.type == '<STRING>':
            #string node content
            newRoot = node('<STR:'+ root.content.content +'>' )
            return newRoot
    
    else:

        #formating the child list of the node
        newChildList=[]
        for c in root.childList:
            newC = usableStandardizedTree(c)
            newChildList.append(newC)
        newRoot = node(root.content)
        newRoot.childList = newChildList
        return newRoot


def preOrderTraversal(Node,str=''):
    #Preorder traversal for ast
    definedNodes = ['let','lambda','where','tau','aug','->','or', '&','not','gr','ge','ls','le','eq','ne','neg','gamma','true','dummy','within','and','rec','=','fcn_form','()',',','+','-','*','/','**','@','nil','Ystar']
    if Node.content not in definedNodes:
        if Node.content.type == '<IDENTIFIER>':
            printFormat = '<ID:'+ Node.content.content +'>'
        elif Node.content.type == '<INTEGER>':
            printFormat = '<INT:'+ Node.content.content +'>'
        elif Node.content.type == '<STRING>':
            printFormat = '<STR:'+ Node.content.content +'>' 
    else:
        printFormat = Node.content          
        print(str+printFormat)
    for c in Node.childList:
        preOrderTraversal(c,str+'.')

def preOrderTraversalUsable(head,str=''):
    #pre order traversal for usable standard tree
    print(str+head.content)
    for c in head.childList:
        preOrderTraversalUsable(c,str+'.')