#!/usr/bin/python

import ply
from scanner import Scanner
from AST import *



class Cparser(object):
    BINARY_OP_TOKENS = [ 'AND', 'OR', 'SHL', 'SHR', 'EQ', 'NEQ', 'LE', 'GE' ]

    @staticmethod
    def isBinaryOpToken(e):
        return isinstance(e, ply.lex.LexToken) and e.type in Cparser.BINARY_OP_TOKENS

    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens


    precedence = (
       ("nonassoc", 'IFX'),
       ("nonassoc", 'ELSE'),
       ("right", '='),
       ("left", 'OR'),
       ("left", 'AND'),
       ("left", '|'),
       ("left", '^'),
       ("left", '&'),
       ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
       ("left", 'SHL', 'SHR'),
       ("left", '+', '-'),
       ("left", '*', '/', '%'),
    )


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print('At end of input')



    def p_program(self, p):
        """program : declarations fundefs instructions"""
        p[0] = Program(p[1], p[2], p[3])

    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """
        if len(p) <= 1:
            p[0] = []
        else:
            p[0] = p[1] + [ p[2] ]

    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | error ';' """
        p[0] = Decl(p[1].value, p[2])

    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        if len(p) <= 2:
            p[0] = [ p[1] ]
        else:
            p[0] = p[1] + [ p[3] ]


    def p_init(self, p):
        """init : ID '=' expression """
        p[0] = BinExpr(p[1], '=', p[3])

    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        if len(p) <= 2:
            p[0] = [ p[1] ]
        else:
            p[0] = p[1] + [ p[2] ]

    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr
                       | repeat_instr
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr"""
        p[0] = p[1]

    def p_print_instr(self, p):
        """print_instr : PRINT expression ';'
                       | PRINT error ';' """
        p[0] = PrintInstr(p[2])

    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = LabeledInstr(p[1], p[3])

    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        p[0] = BinExpr(p[1], '=', p[3])

    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        p[0] = IfClause(p[3], p[5], p[7] if len(p) > 6 else None)

    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        p[0] = While(p[3], p[5])

    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        p[0] = Repeat(p[2], p[3])

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = Return(p[2])

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = Continue()

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = Break()

    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions '}' """
        p[0] = Block(p[2] + p[3])

    def p_condition(self, p):
        """condition : expression"""
        p[0] = p[1]

    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING"""
        if p[1].type == 'INTEGER':
            p[0] = Integer(p[1].value)
        elif p[1].type == 'FLOAT':
            p[0] = Float(p[1].value)
        elif p[1].type == 'STRING':
            p[0] = String(p[1].value)
        else:
            raise NotImplementedError('unrecognized const type')


    def p_expression(self, p):
        """expression : const
                      | ID
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'
                      | ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 5:
            p[0] = Funcall(p[1], p[3])
        elif len(p) > 2 and isinstance(p[2], str):
            p[0] = BinExpr(p[1], p[2], p[3])
        elif len(p) > 2 and Cparser.isBinaryOpToken(p[2]):
            p[0] = BinExpr(p[1], p[2].value, p[3])
        elif p[1] == '(' and p[3] == ')':
            p[0] = p[2]
        else:
            raise Exception("invalid expression")

    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """

        p[0] = [] if len(p) == 1 else p[1]

    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        if len(p) == 2:
            p[0] = [ p[1] ]
        else:
            p[0] = p[1] + [ p[3] ]

    def p_fundefs(self, p):
        """fundefs : fundef fundefs
                   |  """
        p[0] = [] if len(p) == 1 else [ p[1] ] + p[2]

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        p[0] = Fundef(p[1].value, p[2], p[4], p[6])

    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        p[0] = [] if len(p) == 1 else p[1]

    def p_args_list(self, p):
        """args_list : args_list ',' arg
                     | arg """
        if len(p) == 2:
            p[0] = [ p[1] ]
        else:
            p[0] = p[1] + [ p[3] ]

    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = Funarg(p[1].value, p[2])



