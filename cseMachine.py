import stack
# global controlStructs
controlStructs = []

# global count
count = 0

def generateContrlStruct(root, i):
    global count
    global controlStructs
    while(len(controlStructs) <= i):
        controlStructs.append([])
        
    if (root.content == "lambda"):
        count += 1
        childL = root.childList[0]
        if (childL.content == ","):
            temp = "lambda" + "_" + str(count) + "_"
            for child in childL.childList:
                temp += child.content[4:-1] + ","
            temp = temp[:-1]
            controlStructs[i].append(temp)
        else:
            temp = "lambda" + "_" + str(count) + "_" + childL.content[4:-1]
            controlStructs[i].append(temp)

        for child in root.childList[1:]:
            generateContrlStruct(child, count)
    
    elif (root.content == "->"):
        count += 1
        temp = "delta" + "_" + str(count)
        controlStructs[i].append(temp)
        generateContrlStruct(root.childList[1], count)
        count += 1
        temp = "delta" + "_" + str(count)
        controlStructs[i].append(temp)
        generateContrlStruct(root.childList[2], count)
        controlStructs[i].append("beta")
        generateContrlStruct(root.childList[0], i)

    elif (root.content == "tau"):
        n = len(root.childList)
        temp = "tau" + "_" + str(n)
        controlStructs[i].append(temp)
        for child in root.childList:
            generateContrlStruct(child, i)

    else:
        controlStructs[i].append(root.content)
        for child in root.childList:
            generateContrlStruct(child, i)

class EnvironmentNode(object):
    def __init__(self, n, parent):
        self.name = "e_" + str(n)
        self.variables = {}
        self.childList = []
        self.parent = parent
    def addChild(self, child):
        self.childList.append(child)
        child.variables.update(self.variables)
    def addVariable(self, key, value):
        self.variables[key] = value

def lookup(name):
    global environments
    global builtInFuncs
    global ss
    if (name.startswith("INT", 1)):
        return int(name[5:-1])
    elif (name.startswith("STR", 1)):
        return name[5:-1].strip("'")
    elif (name.startswith("ID", 1)):
        variable = name[4:-1]
        if (variable in builtInFuncs):
            return variable
        else:
            value = environments[currentEnvironment].variables[variable]
            return value
    elif (name.startswith("Ystar", 1)):
        return "Ystar"
    elif (name.startswith("nil", 1)):
        return ()
    elif (name.startswith("true", 1)):
        return True
    elif (name.startswith("false", 1)):
        return False
    
def applyRules():
    binop = ["+", "-", "*", "/", "**", "gr", "ge","ls", "le", "eq", "ne", "or", "&", "aug"]
    unop = ["neg", "not"]

    global control
    global ss
    global environments
    global currentEnvironment

    while(len(control) > 0):

        symbol = control.pop()

        # rule 1
        if (symbol.startswith("<") and symbol.endswith(">")):
            ss.append(lookup(symbol))
        
        # rule 2
        elif (symbol.startswith("lambda")):
            ss.append(symbol + "_" + str(currentEnvironment))

        # rule 4
        elif (symbol == "gamma"):
            stackSymbol1 = ss.pop()
            stackSymbol2 = ss.pop()

            if (type(stackSymbol1) == str and stackSymbol1.startswith("lambda")):
                currentEnvironment = len(environments)
                # print(f"currentEnv: {currentEnvironment}")
                lambdaData = stackSymbol1.split("_")

                parent = environments[int(lambdaData[3])]
                child = EnvironmentNode(currentEnvironment, parent)
                parent.addChild(child)
                environments.append(child)

                # rule 11
                variableList = lambdaData[2].split(",")
                if(len(variableList) > 1):
                    for i in range(len(variableList)):
                        child.addVariable(variableList[i], stackSymbol2[i])
                else:
                    child.addVariable(lambdaData[2], stackSymbol2)

                ss.append(child.name)
                control.append(child.name)
                control += controlStructs[int(lambdaData[1])]
            
            # rule 10
            elif (type(stackSymbol1) == tuple):
                ss.append(stackSymbol1[stackSymbol2 - 1])

            # rule 12
            elif(stackSymbol1 == "Ystar"):
                temp = "eta" + stackSymbol2[6:]
                ss.append(temp)

            # rule 13
            elif(type(stackSymbol1) == str and stackSymbol1.startswith("eta")):
                temp = "lambda" + stackSymbol1[3:]
                control.append("gamma")
                control.append("gamma")
                ss.append(stackSymbol2)
                ss.append(stackSymbol1)
                ss.append(temp)

            # built in funcs
            elif (stackSymbol1 == "Order"):
                order = len(stackSymbol2)
                ss.append(order)
            
            elif (stackSymbol1 == "Print" or stackSymbol1 == "print"):
                ss.append(stackSymbol2)

            elif (stackSymbol1 == "Conc"):
                stackSymbol3 = ss.pop()
                control.pop()
                temp = stackSymbol2 + stackSymbol3
                ss.append(temp)

            elif(stackSymbol1 == "Stern"):
                ss.append(stackSymbol2[1:])

            elif (stackSymbol1 == "Stem"):
                ss.append(stackSymbol2[0])

            elif (stackSymbol1 == "Isinteger"):
                if (type(stackSymbol2) == int):
                    ss.append(True)
                else:
                    ss.append(False)

            elif (stackSymbol1 == "Isstring"):
                if (type(stackSymbol2) == str):
                    ss.append(True)
                else:
                    ss.append(False)

            elif (stackSymbol1 == "Istruthvalue"):
                if (type(stackSymbol2) == bool):
                    ss.append(True)
                else:
                    ss.append(False)

            elif (stackSymbol1 == "Istuple"):
                if (type(stackSymbol2) == tuple):
                    ss.append(True)
                else:
                    ss.append(False)

            elif (stackSymbol1 == "Isfunction"):
                if (stackSymbol2 in builtInFuncs):
                    return True
                else:
                    False

        # rule 5
        elif (symbol.startswith("e_")):
            stackSymbol = ss.pop()
            ss.pop()
            if (currentEnvironment != 0):
                for element in reversed(ss):
                    if (type(element) == str and element.startswith("e_")):
                        currentEnvironment = int(element[2:])
                        break
            ss.append(stackSymbol)

        # rule 6
        elif (symbol in binop):
            rand1 = ss.pop()
            rand2 = ss.pop()
            if (symbol == "+"):
                ss.append(rand1+rand2)
            elif (symbol == "-"):
                ss.append(rand1-rand2)
            elif (symbol == "*"):
                ss.append(rand1*rand2)
            elif (symbol == "/"):
                ss.append(rand1/rand2)
            elif (symbol == "**"):
                ss.append(rand1**rand2)
            elif (symbol == "gr"):
                ss.append(rand1 > rand2)
            elif (symbol == "ge"):
                ss.append(rand1 >= rand2)
            elif (symbol == "ls"):
                ss.append(rand1 < rand2)
            elif (symbol == "le"):
                ss.append(rand1 <= rand2)
            elif (symbol == "eq"):
                ss.append(rand1 == rand2)
            elif (symbol == "ne"):
                ss.append(rand1 != rand2)
            elif (symbol == "or"):
                ss.append(rand1 or rand2)
            elif (symbol == "&"):
                ss.append(rand1 and rand2)
            elif (symbol == "aug"):
                if (type(rand2) == tuple):
                    ss.append(rand1 + rand2)
                else:
                    ss.append(rand1 + (rand2,))
        
        # rule 7
        elif (symbol in unop):
            rand = ss.pop()
            if (symbol == "not"):
                ss.append(not rand)
            elif (symbol == "neg"):
                ss.append(-rand)

        # rule 8
        elif (symbol == "beta"):
            B = ss.pop()
            deltaElse = control.pop()
            deltaThen = control.pop()
            if (B):
                control += controlStructs[int(deltaThen.split("_")[1])]
            else:
                control += controlStructs[int(deltaElse.split("_")[1])]

        # rule 9
        elif (symbol.startswith("tau_")):
            n = int(symbol.split("_")[1])
            tauList = []
            for i in range(n):
                tauList.append(ss.pop())
            tauTuple = tuple(tauList)
            ss.append(tauTuple)

        elif(symbol == "Ystar"):
            ss.append(symbol)

        elif(symbol == "nil"):
            ss.append(())

builtInFuncs = ["Order", "Print", "print", "Conc", "Stern", "Stem", "Isinteger", "Istruthvalue", "Isstring", "Istuple", "Isfunction"]

control = []
ss = []
environments = [EnvironmentNode(0, None)]
currentEnvironment = 0

control.append(environments[0].name)