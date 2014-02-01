#!/usr/bin/python

class Node:

    def __str__(self):
        return  self.printTree(0)


    def accept(self, visitor):
        className = self.__class__.__name__
        # return visitor.visit_<className>(self)
        meth = getattr(visitor, 'visit_' + className, None)
        if meth!=None:
            return meth(self)


class Program(Node):
    def __init__(self,lineno, declarations, fundefs, instructions):
        self.lineno = lineno
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions


class Declarations(Node):
    def __init__(self,lineno,  declarations = None , declaration = None ):
        self.lineno = lineno
        self.declarations = declarations
        self.declaration = declaration


class Declaration(Node):
    def __init__(self,lineno,  type, inits = None):
        self.lineno = lineno
        self.type = type
        self.inits = inits


class Inits(Node):
    def __init__(self,lineno,  init, inits = None):
        self.lineno = lineno
        self.init = init
        self.inits = inits


class Init(Node):
    def __init__(self,lineno, id, expression):
        self.lineno = lineno
        self.id = id
        self.expression = expression


class Instructions(Node):
    def __init__(self,lineno,  instruction ,instructions = None):
        self.lineno = lineno
        self.instructions = instructions
        self.instruction = instruction


class Instruction(Node):
    def __init__(self,lineno,  instruction):
        self.lineno = lineno
        self.instruction = instruction


class PrintInstr(Node):
    def __init__(self,lineno, expression):
        self.lineno = lineno
        self.expression = expression


class LabeledInstr(Node):
    def __init__(self,lineno, id, instruction):
        self.lineno = lineno
        self.id = id
        self.instruction = instruction


class Assignment(Node):
    def __init__(self,lineno, id, expression):
        self.lineno = lineno
        self.id = id
        self.expression = expression


class ChoiceInstr(Node):
    def __init__(self,lineno, condition, instruction, elseinstruction = None):
        self.lineno = lineno
        self.condition = condition
        self.instruction = instruction
        self.elseinstruction = elseinstruction


class WhileInstr(Node):
    def __init__(self,lineno, condition, instruction):
        self.lineno = lineno
        self.condition = condition
        self.instruction = instruction


class RepeatInstr(Node):
    def __init__(self,lineno, instructions, condition):
        self.lineno = lineno
        self.instructions = instructions
        self.condition = condition


class ReturnInstr(Node):
    def __init__(self,lineno, expression):
        self.lineno = lineno
        self.expression = expression


class ContinueInstr(Node):
    pass

class BreakInstr(Node):
    pass


class CompoundInstr(Node):
    def __init__(self,lineno, declarations, instructions):
        self.lineno = lineno
        self.declarations = declarations
        self.instructions = instructions


class Condition(Node):
    def __init__(self,lineno, expression):
        self.lineno = lineno
        self.expression = expression

class Const(Node):
    def __init__(self,lineno, constValue):
        self.lineno = lineno
        self.constValue = constValue


class Expression(Node):
    def __init__(self,lineno, expression1, typeexpr, expression2, idOrConst = None):
        self.lineno = lineno
        self.expression1 = expression1
        self.typeexpr = typeexpr
        self.expression2 = expression2
        self.idOrConst = idOrConst

class Funcalls(Node):
    def __init__(self,lineno, id, exprListOrEmpty):
        self.lineno = lineno
        self.id = id
        self.exprListOrEmpty = exprListOrEmpty


class ExprInBrackets(Node):
    def __init__(self,lineno, expression):
        self.lineno = lineno
        self.expression = expression

class ExprListOrEmpty(Node):
    def __init__(self,lineno, exprList = None):
        self.lineno = lineno
        self.exprList = exprList


class ExprList(Node):
    def __init__(self,lineno, expression, exprList=None):
        self.lineno = lineno
        self.exprList = exprList
        self.expression = expression


class Fundefs(Node):
    def __init__(self,lineno, fundef = None, fundefs = None):
        self.lineno = lineno
        self.fundef = fundef
        self.fundefs = fundefs


class Fundef(Node):
    def __init__(self,lineno, type, id, argsListOrEmpty, compoundInstruction):
        self.lineno = lineno
        self.type = type
        self.id = id
        self.argList = argsListOrEmpty
        self.compoundInstr = compoundInstruction


class ArgsListOrEmpty(Node):
    def __init__(self,lineno, argsList = None):
        self.lineno = lineno
        self.argsList = argsList

class ArgsList(Node):
    def __init__(self,lineno, arg, argsList = None):
        self.lineno = lineno
        self.argsList = argsList
        self.arg = arg

class Arg(Node):
    def __init__(self,lineno, type, id):
        self.lineno = lineno
        self.type = type
        self.id = id