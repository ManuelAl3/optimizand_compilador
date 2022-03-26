import sys
sys.path.insert(0, '../..')

from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = { 
        'NAME',
        'NUMBER',
        'ASIGNAR',
        'SUMA',
        'RESTA',
        'MULT',
        'DIV',
        'PARIZQ',
        'PARDER',
    }
    ignore = ' \t'

    NUMBER = r'\d+'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    SUMA = r'\+'
    RESTA = r'-'
    # PUNTO = r'\.'
    MULT = r'\*'
    DIV = r'/'
    ASIGNAR = r'='
    # Expresiones Logicas
    PARIZQ = r'\('
    PARDER = r'\)'

    ignore_newline = r'\n+'

    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('right','ASIGNAR'),
        ('left', 'SUMA', 'RESTA'),
        ('left', 'MULT', 'DIV'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.names = { }

    @_('NAME ASIGNAR expr')
    def statement(self, p):
        self.names[p.NAME] = p.expr

    @_('expr')
    def statement(self, p):
        print(p.expr)

    @_('expr SUMA expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr RESTA expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr MULT expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIV expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('RESTA expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('PARIZQ expr PARDER')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)

    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print(f'Undefined name {p.NAME!r}')
            return 0

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('INTRODUCIR DATO:  ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))