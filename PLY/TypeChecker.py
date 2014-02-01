#!/usr/bin/python


from SymbolTable import FunctionsTable
from SymbolTable import SymbolTable

class TypeChecker(object):
    errors = []
    
    
    def __init__(self):
        self.ttype = {'+': {'string': {'string': 'string'}, 'int': {'float': 'float', 'int': 'int'}, 'float': {'int': 'float', 'float': 'float'}},
                      '-': {'int': {'int': 'int','float': 'float'}, 'float': {'int': 'float', 'float': 'float'}},
                      '*': {'string': {'int': 'string'}, 'int': {'int': 'int', 'float': 'float', 'string': 'string'}, 'float': {'int:':'float' , 'float':'float'}},
                      '/': {'int': {'int': 'float', 'float': 'float'}, 'float': {'float': 'float'} },
                      '!=': {'string': {'string': 'string'}, 'int': {'float': 'int', 'int': 'int'}, 'float': {'int': 'int', 'float': 'int'}},
                      '<': {'string': {'string': 'string'}, 'int': {'float': 'int', 'int': 'int'}, 'float': {'int': 'int', 'float': 'int'}},
                      '<=': {'string': {'string': 'string'}, 'int': {'float': 'int', 'int': 'int'}, 'float': {'int': 'int', 'float': 'int'}},
                      '>': {'string': {'string': 'string'}, 'int': {'float': 'int', 'int': 'int'}, 'float': {'int': 'int', 'float': 'int'}},
                      '>=': {'string': {'string': 'string'}, 'int': {'float': 'int', 'int': 'int'}, 'float': {'int': 'int', 'float': 'int'}},
                      '==': {'string': {'string': 'string'}, 'int': {'float': 'int', 'int': 'int'}, 'float': {'int': 'int', 'float': 'int'}},
                      '%': {'int': {'int': 'int'}},
                      '^': {'int': {'int': 'int', 'float' : 'float'}, 'float':{'int':'float' , 'float':'float'}},
                      '&': {'int': {'int': 'int'}},
                      'AND': {'int': {'int': 'int'}},
                      'OR': {'int': {'int': 'int'}},
                      'SHL': {'int': {'int': 'int'}},
                      'SHR': {'int': {'int': 'int'}},
                      'EQ': {'int': {'int': 'int'}},
                      'NEQ': {'int': {'int': 'int'}},
                      'LE': {'int': {'int': 'int'}},
                      'GE': {'int': {'int': 'int'}},
                      }
        
    

    def visit_Program(self, node):
        node.Functions = FunctionsTable(None, "Functions")
        node.Variables = SymbolTable(None, "Variables")
        node.declarations.Functions = node.Functions
        node.declarations.Variables = node.Variables
        node.fundefs.Functions = node.Functions
        node.fundefs.Variables = node.Variables
        node.instructions.Functions = node.Functions
        node.instructions.Variables = node.Variables
        
        node.declarations.accept(self)
        node.fundefs.accept(self)
        node.instructions.accept(self)
        return self.errors

    def visit_Declarations(self, node):
        if node.declarations != None:
            node.declarations.Functions = node.Functions
            node.declarations.Variables = node.Variables
            node.declarations.accept(self)
        
        if node.declaration != None:
            node.declaration.Functions = node.Functions
            node.declaration.Variables = node.Variables
            node.declaration.accept(self)

            
    def visit_Declaration(self, node):
        node.inits.Functions = node.Functions
        node.inits.Variables = node.Variables
        self.visit_Inits(node.inits, node.type)


    def visit_Inits(self, node, type):
        node.init.Functions = node.Functions
        node.init.Variables = node.Variables
        self.visit_Init(node.init, type)
        if node.inits != None:
            node.inits.Functions = node.Functions
            node.inits.Variables = node.Variables
            self.visit_Inits(node.inits, type)
                       
    def visit_Init(self, node, type):
        # add declaration name = node.id, symbol = type
        if node.Variables.put(node.id, type)==-1:
            self.errors.append("In line "+ str(node.lineno) + ": variable "+ node.id + " was initialized")
            
    def visit_Instructions(self, node):
        if node.instructions != None:
            node.instructions.Functions = node.Functions
            node.instructions.Variables = node.Variables
            node.instructions.accept(self)
        node.instruction.Functions = node.Functions
        node.instruction.Variables = node.Variables
        node.instruction.accept(self)
        
    def visit_Instruction(self, node):
        node.instruction.Functions = node.Functions
        node.instruction.Variables = node.Variables
        node.instruction.accept(self)
        
    def visit_PrintInstr(self, node):
        node.expression.Functions = node.Functions
        node.expression.Variables = node.Variables
        node.expression.accept(self)
        
    def visit_LabeledInstr(self, node):
        node.instruction.Functions = node.Functions
        node.instruction.Variables = node.Variables
        node.instruction.accept(self)
    
    def visit_Assignment(self, node):
        node.expression.Functions = node.Functions
        node.expression.Variables = node.Variables
        type2 = node.expression.accept(self)
        type1 = node.Variables.get(node.id)
        if type1 == -1:
            self.errors.append("In line "+ str(node.lineno) + ": variable " + node.id +" wasn't declared")
        elif type2 == -1:
            self.errors.append("In line "+ str(node.lineno) + ": incorrect expression")
        elif type1 != type2:
            self.errors.append("In line "+ str(node.lineno) + ": can't assign " + str(type2) + " to "+str(type1))
        
    def visit_ChoiceInstr(self, node):
        node.condition.Functions = node.Functions
        node.condition.Variables = node.Variables
        node.condition.accept(self)
        node.instruction.Functions = FunctionsTable(node.Functions, "Functions")
        node.instruction.Variables = SymbolTable(node.Variables, "Variables")
        node.instruction.accept(self)
        
        if node.elseinstruction != None:
            node.elseinstruction.Functions = FunctionsTable(node.Functions, "Functions")
            node.elseinstruction.Variables = SymbolTable(node.Variables, "Variables")
            node.elseinstruction.accept(self)
            
    def visit_WhileInstr(self, node):
        node.condition.Functions = node.Functions
        node.condition.Variables = node.Variables
        node.condition.accept(self)
        node.instruction.Functions = FunctionsTable(node.Functions, "Functions")
        node.instruction.Variables = SymbolTable(node.Variables, "Variables")
        node.instruction.accept(self)
        
    def visit_RepeatInstr(self, node):
        Functions = FunctionsTable(node.Functions, "Functions")
        Variables = SymbolTable(node.Variables, "Variables")
        node.instructions.Functions = Functions
        node.instructions.Variables = Variables
        node.instructions.accept(self)
        node.condition.Functions = Functions
        node.condition.Variables = Variables
        node.condition.accept(self)
        
    def visit_ReturnInstr(self, node):
        node.expression.Functions = node.Functions
        node.expression.Variables = node.Variables
        node.expression.accept(self)
        
    def visit_CompoundInstr(self, node):
        Functions = FunctionsTable(node.Functions, "Functions")
        Variables = SymbolTable(node.Variables, "Variables")
        node.declarations.Functions = Functions
        node.declarations.Variables = Variables
        node.declarations.accept(self)
        node.instructions.Functions = Functions
        node.instructions.Variables = Variables
        node.instructions.accept(self)
        
    def visit_Condition(self, node):
        node.expression.Functions = node.Functions
        node.expression.Variables = node.Variables
        node.expression.accept(self)
        
    def visit_Expression(self, node):
        if node.idOrConst != None:
            if node.idOrConst.__class__.__name__ == "Const":
                node.idOrConst.Functions = node.Functions
                node.idOrConst.Variables = node.Variables
                return node.idOrConst.accept(self)
            if node.Variables.get(node.idOrConst)== -1:
                self.errors.append("In line "+ str(node.lineno) + ": couldn't find variable" +node.idOrConst+ " in the current scope")
                return 'int'
            return node.Variables.get(node.idOrConst)
        node.expression1.Functions = node.Functions
        node.expression1.Variables = node.Variables
        type1 = node.expression1.accept(self)
        node.expression2.Functions = node.Functions
        node.expression2.Variables = node.Variables
        type2 = node.expression2.accept(self)
        #print type1 + str(node.typeexpr) +type2
        if node.typeexpr in self.ttype.keys() and type1 in self.ttype[node.typeexpr].keys() and type2 in self.ttype[node.typeexpr][type1].keys():
            return  self.ttype[node.typeexpr][type1][type2]
        else:
            print str(type1) + node.typeexpr + str(type2)
            self.errors.append("In line "+ str(node.lineno) + ": invalid expression")
            return 'int'

    def visit_ExprInBrackets(self,node):
        node.expression.Functions = node.Functions
        node.expression.Variables = node.Variables
        return node.expression.accept(self)

    def visit_Const(self, node):
        return node.constValue[1]
    
    def visit_Funcalls(self, node):
        type1 = node.Functions.get(node.id)
        node.exprListOrEmpty.Functions = node.Functions
        node.exprListOrEmpty.Variables = node.Variables
        type2 = node.exprListOrEmpty.accept(self)      
        if type1[0] != type2:
            self.errors.append("In line "+ str(node.lineno) + ": function call arguments don't match the definition")
        return type1[1]
            

    def visit_ExprListOrEmpty(self, node):
        node.exprList.Functions = node.Functions
        node.exprList.Variables = node.Variables
        if node.exprList != None:
            return node.exprList.accept(self)
        else:
            return None
        
    def visit_ExprList(self, node):
        l1 = []
        if node.exprList != None:
            node.exprList.Functions = node.Functions
            node.exprList.Variables = node.Variables
            l1.extend(node.exprList.accept(self))
        node.expression.Functions = node.Functions
        node.expression.Variables = node.Variables
        l1.append(node.expression.accept(self))
        return l1

    def visit_Fundefs(self, node):
        if node.fundef != None:
            node.fundef.Functions = node.Functions
            node.fundef.Variables = node.Variables
            node.fundef.accept(self)
        
        if node.fundefs != None:
            node.fundefs.Functions = node.Functions
            node.fundefs.Variables = node.Variables
            node.fundefs.accept(self)

    def visit_Fundef(self, node):
        node.Functions.putNewFun(node.id, node.type) 
        Functions = FunctionsTable(node.Functions, "Functions")
        Variables = SymbolTable(node.Variables, "Variables")
        node.argList.Functions = Functions
        node.argList.Variables = Variables
        listOfArguments = node.argList.accept(self)
        for element in listOfArguments:
            if element!= None:
                node.Functions.put(node.id, element[1])
                if Variables.put(element[0], element[1])==-1:
                    self.errors.append("In line "+ str(node.lineno) + ": variable "+ element.name + " was initialized")
        node.compoundInstr.Functions = Functions
        node.compoundInstr.Variables = Variables
        node.compoundInstr.accept(self)
                
    def visit_ArgsListOrEmpty(self, node):
        node.argsList.Functions = node.Functions
        node.argsList.Variables = node.Variables
        if node.argsList != None:
            return node.argsList.accept(self) 
        else:
            return None
        
    def visit_ArgsList(self, node):
        l1 = []
        if node.argsList != None:
            node.argsList.Functions = node.Functions
            node.argsList.Variables = node.Variables
            l1.extend(node.argsList.accept(self))
        node.arg.Functions = node.Functions
        node.arg.Variables = node.Variables
        l1.append(node.arg.accept(self))
        return l1
    
    def visit_Arg(self,node):
        return node.id, node.type