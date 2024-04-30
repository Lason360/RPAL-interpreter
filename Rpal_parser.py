import lexicalAnalyzer  #RPal Lexical analyzer
import stack            #stack and the tree implementation

class AbstractSyntaxTreeBuildError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.__class__.__name__}: {self.message}'

global s
s = stack.nodeStack()
global l
global keyWords
keyWords = ['let','fn','where','aug','or','gr','ge','ls','le','eq','ne','nil','false','true','dummy','in','within','and']
l = []
def get_T(item_type):
    'Pop tokens from the lexical list'
    if not l:
        raise ValueError('Input Empty')
    elif l[0].type != item_type:
        raise ValueError('Wrong type')
    else:
        return l.pop(0)
def isLempty():
    'Check token list is empty'
    if len(l) == 0:
        return True
    else:
        return False
def peek_T():
    'return the current token'
    return l[0]
def peek_second_T():
    'return the second upcoming token'
    return l[1]

def E():
    
    if not isLempty() and peek_T().type == '<IDENTIFIER>' and peek_T().content == 'let':
        get_T('<IDENTIFIER>')
        D()
        if not isLempty() and peek_T().type == '<IDENTIFIER>' and peek_T().content == 'in':
            inObject = get_T('<IDENTIFIER>')
            E()
        elif isLempty():
            raise AbstractSyntaxTreeBuildError("Token stack ended")
        elif peek_T().content != 'in':
            raise AbstractSyntaxTreeBuildError("in expected after let")
        s.build_tree('let',2)
    elif not isLempty() and peek_T().type == '<IDENTIFIER>' and peek_T().content == 'fn':
        get_T('<IDENTIFIER>')
        Vb()
        count = 1
        while not isLempty() and (not (peek_T().type == '<OPERATOR>' and peek_T().content == '.')):
            count += 1
            Vb()
        get_T('<OPERATOR>')
        E()
        s.build_tree('lambda',count+1)
    else:
        Ew()

def Ew():
    T()
    if not isLempty() and (peek_T().type == '<IDENTIFIER>') and (peek_T().content == 'where'):
        get_T('<IDENTIFIER>')
        Dr()
        s.build_tree('where',2)

def T():
    Ta()
    count = 1
    while not isLempty() and (peek_T().type == '<,>'):
        count += 1
        get_T('<,>')
        Ta()
    if count>1:
        s.build_tree('tau', count)

def Ta():
    Tc()
    while not isLempty() and (peek_T().type == '<IDENTIFIER>' and peek_T().content == 'aug'):
        get_T()
        Tc()
        s.build_tree('aug', 2)
def Tc():
    B()
    if not isLempty() and (peek_T().type == '<OPERATOR>' and peek_T().content == '->'):
        get_T('<OPERATOR>')
        Tc()
        if not isLempty() and (peek_T().type == '<OPERATOR>' and peek_T().content == '|'):
            get_T('<OPERATOR>')
        Tc()
        s.build_tree('->', 3)

def B():
    Bt()
    while not isLempty() and (peek_T().type == '<IDENTIFIER>' and peek_T().content == 'or'):
        orObj = get_T('<IDENTIFIER>')
        Bt()
        s.build_tree('or', 2)
def Bt():
    Bs()
    while not isLempty() and (peek_T().type == '<OPERATOR>' and peek_T().content == '&'):
        ampersonObj = get_T('<OPERATOR>')
        Bs()
        s.build_tree('&', 2)
def Bs():
    if not isLempty() and (peek_T().type == '<IDENTIFIER>' and peek_T().content == 'not'):
        notObj = get_T('<IDENTIFIER>')
        Bp()
        s.build_tree('not', 1)
    else:
        Bp()

def Bp():
    A()
    # greater than operations
    if not isLempty() and (peek_T().type == '<IDENTIFIER>' and peek_T().content == 'gr'):
        compObj = get_T('<IDENTIFIER>')
        A()
        s.build_tree('gr',2)
    elif not isLempty() and (peek_T().type == '<OPERATOR>' and peek_T().content == '>'):
        compObj = get_T('<OPERATOR>')
        A()
        s.build_tree('gr',2)

    # greater than or equal operation
    elif not isLempty() and (peek_T().type == '<IDENTIFIER>' and peek_T().content == 'ge'):
        compObj = get_T('<IDENTIFIER>')
        A()
        s.build_tree('ge',2)
    elif not isLempty() and (peek_T().type == '<OPERATOR>' and peek_T().content == '>='):
        compObj = get_T('<OPERATOR>')
        A()
        s.build_tree('ge',2)

    #Less than
    elif not isLempty() and (peek_T().type == '<IDENTIFIER>' and peek_T().content == 'ls'):
        compObj = get_T('<IDENTIFIER>')
        A()
        s.build_tree('ls',2)
    elif not isLempty() and (peek_T().type == '<OPERATOR>' and peek_T().content == '<'):
        compObj = get_T('<OPERATOR>')
        A()
        s.build_tree('ls',2)

    # Less than or equal
    elif not isLempty() and (peek_T().type == '<IDENTIFIER>' and peek_T().content == 'le'):
        compObj = get_T('<IDENTIFIER>')
        A()
        s.build_tree('le', 2)
    elif not isLempty() and (peek_T().type == '<OPERATOR>' and peek_T().content == '<='):
        compObj = get_T('<OPERATOR>')
        A()
        s.build_tree('le', 2)

    #equal
    elif not isLempty() and (peek_T().type == '<IDENTIFIER>' and peek_T().content == 'eq'):
        compObj = get_T('<IDENTIFIER>')
        A()
        s.build_tree('eq', 2)

    #not equal
    elif not isLempty() and (peek_T().type == '<IDENTIFIER>' and peek_T().content == 'ne'):
        compObj = get_T('<IDENTIFIER>')
        A()
        s.build_tree('ne', 2)


def A():

    if not isLempty() and peek_T().type =='<OPERATOR>' and (peek_T().content == '+'):

        posObj = get_T('<OPERATOR>')
        At()
        while not isLempty() and peek_T().type == '<OPERATOR>' and (peek_T().content == '+' or peek_T().content == '-'):
            rootObj = get_T('<OPERATOR>')
            At()
            s.build_tree(rootObj.content,2)
    elif not isLempty() and peek_T().type =='<OPERATOR>' and (peek_T().content == '-'):

        negObj = get_T('<OPERATOR>')
        At()
        s.build_tree('neg',1)
        while not isLempty() and peek_T().type == '<OPERATOR>' and (peek_T().content == '+' or peek_T().content == '-'):
            rootObj = get_T('<OPERATOR>')
            At()
            s.build_tree(rootObj.content,2)
    else:

        At()

        while not isLempty() and peek_T().type == '<OPERATOR>' and (peek_T().content == '+' or peek_T().content == '-'):
            rootObj = get_T('<OPERATOR>')
            At()
            s.build_tree(rootObj.content,2)

def At():

    Af()

    while not isLempty() and peek_T().type == '<OPERATOR>' and (peek_T().content == '*' or peek_T().content == '/'):
        rootObj = get_T('<OPERATOR>')
        Af()
        s.build_tree(rootObj.content,2)
def Af():
    Ap()

    while not isLempty() and peek_T().type == '<OPERATOR>' and peek_T().content == '**':
        rootObj = get_T('<OPERATOR>')
        Af()
        s.build_tree(rootObj.content,2)

def Ap():
    R()

    while not isLempty() and peek_T().type == '<OPERATOR>' and peek_T().content == '@':
        rootObj = get_T('<OPERATOR>')
        identifier = get_T('<IDENTIFIER>')
        s.build_tree('<ID:'+identifier.content+'>',0)
        R()
        s.build_tree(rootObj.content, 3)

def R():
    Rn()
    first = ['<IDENTIFIER>','<INTEGER>','<STRING>','<(>']
    firstKeyWords = ['true','false','nil','dummy']
    while not isLempty() and ((peek_T().type in first and peek_T().content not in keyWords) or (peek_T().content in firstKeyWords)) :
        Rn()
        s.build_tree('gamma', 2)
def Rn():

    if not isLempty() and peek_T().type == '<IDENTIFIER>' and not (peek_T().content in keyWords):
        identifier = get_T('<IDENTIFIER>')
        s.build_tree('<ID:'+identifier.content+'>',0)

    elif not isLempty() and peek_T().type == '<INTEGER>':
        integer = get_T('<INTEGER>')
        s.build_tree('<INT:'+integer.content+'>', 0)

    elif not isLempty() and peek_T().type == '<STRING>':
        string = get_T('<STRING>')
        s.build_tree(string.content, 0)

    elif not isLempty() and peek_T().type == '<IDENTIFIER>' and peek_T().content == 'true':
        true_identifier = get_T('<IDENTIFIER>')
        s.build_tree(true_identifier.content, 0)

    elif not isLempty() and peek_T().type == '<IDENTIFIER>' and peek_T().content == 'false':
        false_identifier = get_T('<IDENTIFIER>')
        s.build_tree(false_identifier.content, 0)

    elif not isLempty() and peek_T().type == '<IDENTIFIER>' and peek_T().content == 'nil':
        nil_identifier = get_T('<IDENTIFIER>')
        s.build_tree(nil_identifier.content, 0)
    elif not isLempty() and peek_T().type == '<(>':
        get_T('<(>')
        E()
        get_T('<)>')
    elif not isLempty() and peek_T().type == '<IDENTIFIER>' and peek_T().content == 'dummy':
        dummy_identifier = get_T('<IDENTIFIER>')
        s.build_tree(dummy_identifier.content, 0)

def D():

    Da()
    if not isLempty() and peek_T().type == '<IDENTIFIER>' and peek_T().content == 'within':
        D()
        s.build_tree('within',2)

def Da():
    Dr()
    count = 1
    while not isLempty() and peek_T().type == '<IDENTIFIER>' and peek_T().content == 'and':
        count += 1
        get_T('<IDENTIFIER>')
        Dr()
    if count>1:
        s.build_tree('and',count)

def Dr():
    if not isLempty() and peek_T().type == '<IDENTIFIER>' and peek_T().content == 'rec':
        get_T('<IDENTIFIER>')
        Db()
        s.build_tree('rec',1)
    elif not isLempty() and peek_T().type in ['<IDENTIFIER>','<(>']:
        Db()
def Db():

    if not isLempty() and peek_T().type == '<IDENTIFIER>':

        if peek_second_T().type in ['<IDENTIFIER>','<(>']:
            s.build_tree('<ID:'+get_T('<IDENTIFIER>').content+'>',0)
            count = 1
            while not isLempty() and peek_T().content != '=':
                count += 1
                Vb()
            get_T('<OPERATOR>')
            E()
            s.build_tree('fcn_form',count+1)
        else:
            Vl()
            get_T('<OPERATOR>')
            E()
            s.build_tree('=',2)
    elif not isLempty() and peek_T().type == '<(>':
        get_T('<(>')
        D()
        get_T('<)>')


def Vb():
    if not isLempty() and (peek_T().type == '<IDENTIFIER>') and peek_T().content not in keyWords:
        s.build_tree('<ID:'+get_T('<IDENTIFIER>').content+'>',0)
    elif not isLempty() and (peek_T().type == '<(>'):
        get_T('<(>')
        if not isLempty() and (peek_T().type == '<IDENTIFIER>'):
            Vl()
            get_T('<)>')
        else:
            get_T('<)>')
            s.build_tree('()',0)

def Vl():
    s.build_tree('<ID:'+get_T('<IDENTIFIER>').content+'>', 0)
    count = 0
    while not isLempty() and (peek_T().type == '<,>'):
        count += 1
        element = get_T('<,>')
        s.build_tree('<ID:'+get_T('<IDENTIFIER>').content+'>',0)
    if count>0:
        s.build_tree(',', count+1)

with open('tests/test_2') as file:
    file_content = file.read()
file.close()
l = lexicalAnalyzer.sendCharactersToLex(file_content)

E()
stack.preOrderTraversal(s.nodeList[0])