import sys
import lexicalAnalyzer
import Rpal_parser
import stack
import cseMachine

if len(sys.argv) > 1:
    fileName = sys.argv[1]
else:
    print('Invalid input. Provide the file name saved in directory')

if fileName[-4:] == '-ast':
    fileName = fileName[:-4]

    with open(fileName) as file:
        file_content = file.read()
        
    file.close()
    l = lexicalAnalyzer.sendCharactersToLex(file_content)
    Rpal_parser.l = l

    #Parsing the tokens
    Rpal_parser.E()

    #AST
    ast = stack.tree(Rpal_parser.s.nodeList[0])

    #Pre order traversal of ast
    # print('-----------AST------------')
    stack.preOrderTraversal(ast.head)
    # print('-----------AST------------')


else:
# create the formatted standard tree. Just used for the ease of CSE machine
    with open(fileName) as file:
        file_content = file.read()
        
    file.close()
    l = lexicalAnalyzer.sendCharactersToLex(file_content)
    Rpal_parser.l = l

    #Parsing the tokens
    Rpal_parser.E()
    standardTree = Rpal_parser.s.nodeList[0].standardizeNode()
    st = stack.tree(standardTree)
    usable = stack.usableStandardizedTree(st.head)

    # Running CSE Machine
    # Generating control structures
    cseMachine.generateContrlStruct(usable, 0)

    cseMachine.control += cseMachine.controlStructs[0]
    cseMachine.ss.append(cseMachine.environments[0].name)

    # Print control structures if needed
    # print('-----------control structures------------')
    # print(cseMachine.controlStructs)


    cseMachine.applyRules()
    print(f"final output: {cseMachine.ss[0]}")