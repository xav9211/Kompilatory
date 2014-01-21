
class Node(object):
    def accept(self, visitor):
        return visitor.visit(self)
    
    def __init__(self):
        self.children = ()

class Const(Node):
    def __init__(self, value):
        self.value = value

class Integer(Const):
    def __init__(self, value):
        self.value = value

class Float(Const):
    def __init__(self, value):
        self.value = value

class String(Const):
    def __init__(self, value):
        self.value = value

class Variable(Node):
    def __init__(self, name):
        self.name = name

class BinExpr(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        
        self.children(left, right)

class IfClause(Node):
    def __init__(self, cond, body, elseBody):
        self.cond = cond
        self.body = body
        self.elseBody = elseBody

class While(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class Repeat(Node):
    def __init__(self, body, untilCond):
        self.body = body
        self.untilCond = untilCond

class Block(Node):
    def __init__(self, clauses):
        self.clauses = clauses

class Return(Node):
    def __init__(self, expr):
        self.expr = expr

class Continue(Node):
    pass

class Break(Node):
    pass

class Funcall(Node):
    def __init__(self, funcName, args):
        self.funcName = funcName
        self.args = args

class Fundef(Node):
    def __init__(self, retType, funName, args, body):
        self.retType = retType
        self.funName = funName
        self.args = args
        self.body = body

class Funarg(Node):
    def __init__(self, type, name):
        self.type = type
        self.name = name

class LabeledInstr(Node):
    def __init__(self, label, instr):
        self.label = label
        self.instr = instr

class PrintInstr(Node):
    def __init__(self, expr):
        self.expr = expr

class Decl(Node):
    def __init__(self, type, vars):
        self.type = type
        self.vars = vars

class Program(Node):
    def __init__(self, decls, fundefs, instrs):
        self.decls = decls
        self.fundefs = fundefs
        self.instrs = instrs
