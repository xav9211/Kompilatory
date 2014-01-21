
import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

def indent(s, indentString = '| '):
    return indentString + s.replace('\n', '\n' + indentString)

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self):
        return ('%s%s%s' % (
            '' if not self.decls else 'DECL\n' + indent('\n'.join(map(str, self.decls))),
            '' if not self.fundefs else '\n' + '\n'.join(map(str, self.fundefs)),
            '' if not self.instrs else '\n' + '\n'.join(map(str, self.instrs)))
        ).strip()

    @addToClass(AST.Decl)
    def printTree(self):
        return '%s\n%s' % (
            self.type,
            indent('\n'.join(map(str, self.vars))))

    @addToClass(AST.PrintInstr)
    def printTree(self):
        return 'PRINT\n%s' % indent(str(self.expr))

    @addToClass(AST.LabeledInstr)
    def printTree(self):
        return "LABEL %s\n%s" % (
            self.label,
            indent(str(self.expr)))

    @addToClass(AST.Funarg)
    def printTree(self):
        return 'ARG %s %s' % (self.type, self.name)

    @addToClass(AST.Fundef)
    def printTree(self):
        return 'FUNDEF\n%s\n%s%s%s' % (
            indent(self.funName),
            indent('RET ' + self.retType),
            '' if not self.args else '\n' + indent('\n'.join(map(str, self.args))),
            '' if not self.body else '\n' + indent(str(self.body)))

    @addToClass(AST.Funcall)
    def printTree(self):
        return 'FUNCALL\n%s%s' % (
            indent(self.funcName),
            '' if not self.args else '\n' + indent('\n'.join(map(str, self.args))))

    @addToClass(AST.Break)
    def printTree(self):
        return 'BREAK'

    @addToClass(AST.Continue)
    def printTree(self):
        return 'CONTINUE'

    @addToClass(AST.Return)
    def printTree(self):
        return 'RETURN\n%s' % indent(str(self.expr))

    @addToClass(AST.Block)
    def printTree(self):
        return '\n'.join(map(str, self.clauses))

    @addToClass(AST.Repeat)
    def printTree(self):
        return 'REPEAT\n%s%s' % (
            indent(str(self.untilCond)),
            '' if not self.body else '\n' + indent(str(self.body)))

    @addToClass(AST.While)
    def printTree(self):
        return 'WHILE\n%s%s' % (
            indent(str(self.cond)),
            '' if not self.body else '\n' + indent(str(self.body)))

    @addToClass(AST.IfClause)
    def printTree(self):
        return 'IF\n%s%s%s' % (
            indent(str(self.cond)),
            '' if not self.body else '\n' + indent(str(self.body)),
            '' if not self.elseBody else '\nELSE\n' + indent(str(self.elseBody)))

    @addToClass(AST.BinExpr)
    def printTree(self):
        return '%s\n%s\n%s' % (
            self.op,
            indent(str(self.left)),
            indent(str(self.right)))

    @addToClass(AST.Variable)
    def printTree(self):
        return self.name

    @addToClass(AST.String)
    def printTree(self):
        return '"%s"' % self.value

    @addToClass(AST.Float)
    def printTree(self):
        return '%s' % self.value

    @addToClass(AST.Integer)
    def printTree(self):
        return '%s' % self.value

    @addToClass(AST.Const)
    def printTree(self):
        return '%s' % self.value
