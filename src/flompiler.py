# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import copy

flprog = sys.stdin.read() #take input from stdin

class Line():
    #line of flang code
    def __init__(self, line):
        self.inputs = []
        self.function = ""
        self.outputs = []
        words = line.split(" ")
        #start processing inputs, move to function, then outputs
        phase = "inputs"
        for w in words:
            if phase == "inputs":
                if w[0] >= "a" and w[0] <= "z": #if lowercase
                    self.inputs += [w]
                else:
                    phase = "function"
            if phase == "function":
                self.function = w
                phase = "outputs"
            elif phase == "outputs":
                self.outputs += [w]

def parse(string):
    #will give a list of scopes, each a list of lines e.g. [[Line(), Line()], [Line()]]
    retval = []
    lines = string.split("\n")
    lf = 1 #line number starting over for each function
    for l in lines:
        if l == "" or l[0] == "#":
            continue
        current = Line(l)
        if current.function == "":
            sys.stderr.write("Every line must have a function.")
            exit(0)
        if current.function[0] == ";":
            lf = 1
            retval += [[]]
        elif lf == 1:
            sys.stderr.write("Programs must begin with lambdas.")
            exit(0)
        retval[-1] += [current]
        lf += 1
    return retval

scopes = parse(flprog)

def get_type(scopes, scope, name):
    #find the type of a variable with the provided name in the provided scope.
    t = "" #type
    for l in scope:
        for o in l.outputs:
            #determine the type
            if "<" in o:
                if o[:o.index("<")] == name: #same variable
                    #if the type is explicit, use it.
                    return o[o.index("<")+1:-1]
            elif o == name:
                if l.function[0] == "'":
                    if t == "":
                        t = "char"
                    elif t != "char":
                        print("mismatched type of " + name)
                        exit(0)
                elif l.function[0] == "#":
                    if t == "":
                        t = "double"
                    elif t != "double":
                        print("mismatched type of " + name)
                        exit(0)
                else:
                    for s in scopes:
                        if s[0].function[1:] == l.function:
                            for funout in s[0].outputs:
                                temp = get_type(scopes, s, funout)
                                if t == "":
                                    t = temp
                                elif t != temp:
                                    print("mismached type of " + name)
                                    exit(0)
    if t != "":
        return t
    return "double /*type not found*/"

def function_declaration(scopes, scope):
    start = "void " + scope[0].function[1:] + "("
    args = ""
    for i in scope[0].inputs:
        args += "void *" + i + ", "
    for o in scope[0].outputs:
        args += get_type(scopes, scope, o) + " *return_" + o + ", "
    return start + args[:-2] + ");"

def runline(scope, line, noruns):
    retval = ""
    if line.function[0] == "'":
        for o in line.outputs:
            retval += o + " = '" + line.function[1:] + "';"
            retval += satisfy(o)
    elif line.function[0] == "#":
        for o in line.outputs:
            retval += o + " = " + line.function[1:] + ";"
            retval += satisfy(o)
    elif line.function == ">":
        for o in line.outputs:
            retval += o + " = " + line.inputs[0] + ";"
            retval += satisfy(o)
    elif line.function == "<":
        retval += "if (" + line.inputs[0] + " < " + line.inputs[2] + ") {"
        temp = copy.deepcopy(scope) #copy scope
        retval += line.outputs[0] + " = " + line.inputs[1] + ";"
        retval += satisfy(line.outputs[0])
        retval += "} else {"
        temp = copy.deepcopy(scope) #copy scope again
        retval += line.outputs[1] + " = " + line.inputs[1] + ";"
        retval += satisfy(line.outputs[1])
        retval += "}"
    else:
        for operator in "+-*/%":
            if operator == line.function:
                for o in line.outputs:
                    retval += o + " = "
                    for i in line.inputs:
                        retval += i + " " + line.function + " "
                    retval = retval[:-2]
                    retval += ";"
                break
        else:
            args = ""
            if len(line.outputs) < 2:
                retval += line.outputs[0] + " = " + line.function + "("
            else:
                retval += line.function + "("
                for o in line.outputs:
                    args += "&" + o + ", "
            for i in line.inputs:
                args += i + ", "
            args = args[:-2]
            retval += args + ");"
    #make sure you return right.
    for lo in line.outputs:
        for fo in scope[0].outputs:
            if lo == fo:
                retval += "return_" + lo + " = &" + lo + ";"
                break

for s in scopes:
    print(function_declaration(scopes, s))

print("")

def nameofvar(name):
    temp = name
    if "<" in name:
        temp = name[:name.index("<")]
    return temp

for s in scopes:
    print(function_declaration(scopes, s)[:-1] + " {")
    variables = []
    for l in s:
        for o in l.outputs:
            variables += [nameofvar(o)]
    variables = list(set(variables))
    for v in variables:
        print(get_type(scopes, s, v) + " " + v + ";")
    print("}")
