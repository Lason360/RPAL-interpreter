import sys
import lexicalAnalyzer
import Rpal_parser
import stack
import cseMachine

if len(sys.argv) > 1:
    fileName = sys.argv[1]
else:
    print('Invalid input. Provide the file name saved in directory')

with open(fileName) as file:
    file_content = file.read()
    
file.close()
l = lexicalAnalyzer.sendCharactersToLex(file_content)
Rpal_parser.l = l

#uncomment to check the output of the lexical analyzer
#print('-----------Lexical Tokens------------')
# for token in l:
#     print(token.content,token.type)
#print('-----------Lexical Tokens------------')

#Parsing the tokens
Rpal_parser.E()

#AST
# ast = stack.tree(Rpal_parser.s.nodeList[0])

#Pre order traversal of ast
# print('-----------AST------------')
# stack.preOrderTraversal(ast.head)
# print('-----------AST------------')

#Standardize AST
standardTree = Rpal_parser.s.nodeList[0].standardizeNode()
st = stack.tree(standardTree)

#pre order traversal of standardized tree
# print('-----------Standardized tree------------')
# stack.preOrderTraversal(st.head)
# print('-----------Standardized tree------------')

# create the formatted standard tree. Just used for the ease of CSE machine
usable = stack.usableStandardizedTree(st.head)

#Print usable tree if needed
#print('-----------usable st----------------')
# stack.preOrderTraversalUsable(usable)
