# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import copy

flprog = sys.stdin.read() #take input from stdin
output = "" #final thing to print out

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
    global output
    retval = []
    lines = string.split("\n")
    lf = 1 #line number starting over for each function
    for l in lines:
        if l == "" or l[0] == "#":
            continue
        current = Line(l)
        if current.function == "":
            sys.stderr.write("Every line must have a function.\n")
            exit(0)
        if current.function[0] == ";":
            lf = 1
            retval += [[]]
        elif lf == 1:
            sys.stderr.write("Programs must begin with lambdas.\n")
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
                if o[:o.index("<")+1] == name: #same variable
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

def variable_declaration(scopes, scope, line_number, output_number):
    """return a variable declaration if we are provided with the first
        occourence of the variable."""
    name = scope[line_number].outputs[output_number]
    #make sure we are the first
    for i in range(line_number):
        for j in range(output_number):
            if scope[i].outputs[j] == name:
                return ""
    return get_type(scopes, scope, name) + " " + name + ";\n"

def function_declaration(scopes, scope):
    start = "void " + scope[0].function + "("
    args = ""
    for i in scope[0].inputs:
        args += "void *input_" + i + ", "
    for o in scope[0].outputs:
        args += get_type(scopes, scope, o) + " *return_" + o + ", "
    return start + args[:-2] + ");\n"

def runline(scope, line, noruns):
    retval = ""
    if line.function[0] == "'":
        for o in line.outputs:
            retval += o + " = '" + line.function[1:] + "';\n"
            retval += satisfy(o)
    elif line.function[0] == "#":
        for o in line.outputs:
            retval += o + " = " + line.function[1:] + ";\n"
            retval += satisfy(o)
    elif line.function == ">":
        for o in line.outputs:
            retval += o + " = " + line.inputs[0] + ";\n"
            retval += satisfy(o)
    elif line.function == "<":
        retval += "if (" + line.inputs[0] + " < " + line.inputs[2] + ") {\n"
        temp = copy.deepcopy(scope) #copy scope
        retval += line.outputs[0] + " = " + line.inputs[1] + ";\n"
        retval += satisfy(line.outputs[0])
        retval += "} else {\n"
        temp = copy.deepcopy(scope) #copy scope again
        retval += line.outputs[1] + " = " + line.inputs[1] + ";\n"
        retval += satisfy(line.outputs[1])
        retval += "}\n"
    else:
        for operator in "+-*/%":
            if operator == line.function:
                for o in line.outputs:
                    retval += o + " = "
                    for i in line.inputs:
                        retval += i + " " + line.function + " "
                    retval = retval[:-2]
                    retval += ";\n"
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
            retval += args + ");\n"
    #make sure you return right.
    for lo in line.outputs:
        for fo in scope[0].outputs:
            if lo == fo:
                retval += "return_" + lo + " = &" + lo + ";\n"
                break
