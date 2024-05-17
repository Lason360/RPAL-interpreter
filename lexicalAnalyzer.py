class element:
    #lexical token object definition
    content = ''

    def __init__(self, token, type):

        self.content = token
        self.type = '<' + type + '>'


def lexAnalyzer(characters):
#converts text to a list of lexical tokens
    
    # common characters
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
               't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    undersCore = '_'
    operator_symbols = ['+', '-', '*', '<', '>', '&', '.', '@', '/', ':', '=', '˜', '|', '$', '!', '#', '%', 'ˆ', '_',
                        '[',
                        ']', '{', '}', '"', '?','‘']
    lexicans = []
    punctions = ['(', ')', ';', ',']
    
    # initializing configurations
    currentToken = ''
    currentType = None
    skip = 0

    cCount = 0
    for c in characters:
        if skip > 0:
            skip -= 1
            continue

        try:
            if currentType is None:
                # Defining a new token
                if (c in letters):
                    # Start of identifier token
                    currentType = 'IDENTIFIER'
                    currentToken = c
                    try:
                        if (characters[cCount + 1] not in letters):
                            newLex = element(currentToken, currentType)
                            lexicans.append(newLex)
                            currentToken = ''
                            currentType = None
                    except:
                        continue
                elif (c in digits):
                    #start of integer token
                    currentType = 'INTEGER'
                    currentToken = c
                    try:
                        if (characters[cCount + 1] not in digits):
                            newLex = element(currentToken, currentType)
                            lexicans.append(newLex)
                            currentToken = ''
                            currentType = None
                    except:
                        continue
                elif (c in operator_symbols) and (c != '/' and characters[cCount + 1] != '/'):
                    #defining operators // signifies comments
                    currentType = 'OPERATOR'
                    currentToken = c
                    try:
                        if (characters[cCount + 1] not in operator_symbols):
                            newLex = element(currentToken, currentType)
                            lexicans.append(newLex)
                            currentToken = ''
                            currentType = None
                    except:
                        continue
                elif (c == '/') and (characters[cCount + 1] == '/'):
                    #start of comment token
                    currentType = 'COMMENT'
                    currentToken = '//'
                    skip = 1
                elif (c == ' ' or c == '\n' or c == '\t'):
                    #types of spaces that are rejected when parsing
                    currentType = 'SPACES'
                    currentToken = c
                    try:
                        if characters[cCount + 1] not in [' ','\n','\t']:
                            newLex = element(currentToken, 'DELETE')
                            lexicans.append(newLex)
                            currentToken = ''
                            currentType = None
                    except:
                        continue

                elif c == "'" and characters[cCount + 1] == "'":
                    #start of string. strings have to start with '' and end with ''
                    currentType = 'STRING'
                    currentToken = ''
                    skip = 1
                elif (c in punctions):
                    currentToken = c
                    currentType = c
                    newLex = element(currentToken, currentType)
                    lexicans.append(newLex)
                    currentToken = ''
                    currentType = None

            elif currentType == 'IDENTIFIER':
                #extension of identifier token
                if c in letters or c in digits or c == '_':
                    currentToken += c

                # to avoid truncation errors
                try:
                    if c in letters and characters[cCount + 1] not in letters + digits + ['_']:
                        newLex = element(currentToken, currentType)
                        lexicans.append(newLex)
                        currentToken = ''
                        currentType = None
                except:
                    continue


            elif currentType == 'INTEGER':
                #extension of integer token
                if c in digits:
                    currentToken += c
                try:
                    if c in digits and characters[cCount + 1] not in digits:
                        newLex = element(currentToken, currentType)
                        lexicans.append(newLex)
                        currentToken = ''
                        currentType = None
                except:
                    continue

            elif currentType == 'OPERATOR':
                #extension of operator token
                if c in operator_symbols:
                    currentToken += c
                try:
                    if c in operator_symbols and characters[cCount + 1] not in operator_symbols:

                        newLex = element(currentToken, currentType)
                        lexicans.append(newLex)
                        currentToken = ''
                        currentType = None
                except:
                    continue

            elif currentType == 'STRING':
                #extension of string token

                if c in letters + digits + operator_symbols + [' '] + punctions:
                    currentToken += c

                try:
                    if characters[cCount:cCount + 2] in ['\t', '\n', '\\']:
                        skip = 1
                        currentToken += characters[cCount:cCount + 2]

                except:
                    continue

                try:
                    if characters[cCount:cCount + 3] == "\''":
                        skip = 2
                        currentToken += characters[cCount:cCount + 3]

                except:
                    continue

                try:
                    if c == "'" and characters[cCount + 1] == "'":
                        skip = 1
                        newLex = element(currentToken, currentType)
                        lexicans.append(newLex)
                        currentToken = ''
                        currentType = None
                except:
                    continue

            elif currentType == 'SPACES':
                #extension of spaces
                if c in [' ','\t','\n']:
                    currentToken += c
                try:
                    if characters[cCount + 1] not in [' ','\n','\t']:
                        newLex = element(currentToken, 'DELETE')
                        lexicans.append(newLex)
                        currentToken = ''
                        currentType = None
                except:
                    continue
            elif currentType == 'COMMENT':
                #extension of comments
                if c in letters + digits + operator_symbols + [' ','\t']:
                    currentToken += c
                try:
                    if characters[cCount:cCount + 2] == "''":
                        skip = 1
                        currentToken += "''"
                except:
                    continue
                try:
                    if c == "\n":
                        currentToken += '\n'
                        newLex = element(currentToken, 'DELETE')
                        lexicans.append(newLex)
                        currentToken = ''
                        currentType = None
                except:
                    continue

            cCount += 1 + skip
        except:
            cCount += 1 + skip
            continue
    if currentType != None:
        #adding final lexical
        newLex = element(currentToken, currentType)
        lexicans.append(newLex)
        currentToken = ''
        currentType = None

    #step of the parser, rejecting comments and spaces
    new_lexican = [x for x in lexicans if x.type != '<DELETE>']
    return new_lexican


def sendCharactersToLex(string):
    #list the input and send to be tokenized
    characters = list(string)
    lexicanList = lexAnalyzer(characters)
    return lexicanList

