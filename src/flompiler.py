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
        self.satisfied = []
        words = line.split(" ")
        #start processing inputs, move to function, then outputs
        phase = "inputs"
        for w in words:
            if phase == "inputs":
                if w[0] >= "a" and w[0] <= "z": #if lowercase
                    self.inputs += [w]
                    self.satisfied += [0]
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

def nameofvar(name):
    temp = name
    if "<" in name:
        temp = name[:name.index("<")]
    return temp

def runline(scopes, scope, line, noruns):
    if line.function[0] == "'":
        for o in line.outputs:
            print(o + " = '" + line.function[1:] + "';")
            satisfy(scopes, scope, o, noruns)
    elif line.function[0] == "#":
        for o in line.outputs:
            print(o + " = " + line.function[1:] + ";")
            satisfy(scopes, scope, o, noruns)
    elif line.function == ">":
        for o in line.outputs:
            print(o + " = " + line.inputs[0] + ";")
            satisfy(scopes, scope, o, noruns)
    elif line.function == "<":
        print("if (" + line.inputs[0] + " < " + line.inputs[2] + ") {")
        temp = copy.deepcopy(scope) #copy scope
        print(line.outputs[0] + " = " + line.inputs[1] + ";")
        satisfy(scopes, scope, line.outputs[0], noruns)
        print("} else {")
        temp = copy.deepcopy(scope) #copy scope again
        print(line.outputs[1] + " = " + line.inputs[1] + ";")
        satisfy(scopes, scope, line.outputs[1], noruns)
        print("}")
    else:
        for operator in "+-*/%":
            if operator == line.function:
                for o in line.outputs:
                    out = o + " = "
                    for i in line.inputs:
                        out += i + " " + line.function + " "
                    out = out[:-2] + ";"
                    print(out)
                break
        else:
            print("{")
            for i in line.outputs:
                print(get_type(scopes, scope, i) + " *out_" + nameofvar(i) + " = NULL;")
            args = ""
            for i in line.inputs:
                args += "&" + nameofvar(i) + ", "
            for o in line.outputs:
                args += "out_" + nameofvar(o) + ", "
            args = args[:-2]
            print(line.function + "(" + args + ");")
            for o in line.outputs:
                n = nameofvar(o)
                print("if (out_" + n + ") {")
                print(n + " = *out_" + n + ";")
                satisfy(scopes, scope, o, noruns)
                print("}")
            print("}")
    #make sure you return right.
    for lo in line.outputs:
        for fo in scope[0].outputs:
            if lo == fo:
                print("return_" + lo + " = &" + lo + ";")
                break

def satisfy(scopes, scope, o, noruns):
    for l in scope[1:]:
        for i in range(len(l.inputs)):
            if l.inputs[i] == o:
                l.satisfied[i] += 1
                product = 1;
                for s in l.satisfied:
                    product *= s
                if product:
                    l.satisfied = [i - 1 for i in l.satisfied]
                    runline(scopes, scope, l, noruns);

for s in scopes:
    print(function_declaration(scopes, s))

print("")

for s in scopes:
    print(function_declaration(scopes, s)[:-1] + " {")
    variables = []
    for l in s[1:]:
        for o in l.outputs:
            variables += [nameofvar(o)]
    variables = list(set(variables))
    for v in variables:
        print(get_type(scopes, s, v) + " " + v + ";")
    for l in s[1:]:
        if len(l.inputs) == 0:
            runline(scopes, s, l, "")
    for o in s[0].outputs:
        satisfy(scopes, s, o, "")
    print("}")
