import lexicalAnalyzer
import Rpal_parser
import stack
import cseMachine


#save the file in the code directory and paste the name of the file here
with open('tests/test_9') as file:
    file_content = file.read()
    
file.close()
l = lexicalAnalyzer.sendCharactersToLex(file_content)
Rpal_parser.l = l

#uncomment to check the output of the lexical analyzer
# for token in l:
#     print(token.content,token.type)

#Parsing the tokens
Rpal_parser.E()

#AST
ast = stack.tree(Rpal_parser.s.nodeList[0])

#Pre order traversal of ast
stack.preOrderTraversal(ast.head)

#Standardize AST
standardTree = Rpal_parser.s.nodeList[0].standardizeNode()
st = stack.tree(standardTree)

#pre order traversal of standardized tree
# stack.preOrderTraversal(st.head)

# create the formatted standard tree. Just used for the ease of CSE machine
usable = stack.usableStandardizedTree(st.head)

#Print usable tree if needed
# stack.preOrderTraversalUsable(usable)
