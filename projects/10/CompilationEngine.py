import re

SPACE_AMOUNT = 2
INCREASE = 1
DECREASE = -1

# print values
CLASS = "class"
SUBROUTINE_DEC = "subroutineDec"
SUBROUTINE_BOD = "subroutineBody"
IF = "ifStatement"
WHILE = "whileStatement"
DO = "doStatement"
LET = "letStatement"
ELSE = "else"
CLASS_VAR_DEC = "classVarDec"
PARAM_LIST = "parameterList"
VAR_DEC = "varDec"
STATEMENTS = "statements"
RETURN = "returnStatement"
SUBROUTINE_CALL = "subroutineCall"
EXPRESSION = 'expression'
EXP_LIST = 'expressionList'
TERM = 'term'
KEYWORD = "keyword"
SYMBOL = "symbol"
IDENTIFIER = "identifier"
INT_CONST = "integerConstant"
STRING_CONST = "stringConstant"


import re

SPACE_AMOUNT = 2 
INCREASE = 1 
DECREASE = -1 #

# Definitions of XML tags and token types
CLASS = "class"
SUBROUTINE_DEC = "subroutineDec"
SUBROUTINE_BOD = "subroutineBody"
IF = "ifStatement"
WHILE = "whileStatement"
DO = "doStatement"
LET = "letStatement"
ELSE = "else"
CLASS_VAR_DEC = "classVarDec"
PARAM_LIST = "parameterList"
VAR_DEC = "varDec"
STATEMENTS = "statements"
RETURN = "returnStatement"
SUBROUTINE_CALL = "subroutineCall"
EXPRESSION = 'expression'
EXP_LIST = 'expressionList'
TERM = 'term'
KEYWORD = "keyword"
SYMBOL = "symbol"
IDENTIFIER = "identifier"
INT_CONST = "integerConstant"
STRING_CONST = "stringConstant"

class CompilationEngine:
    ops = '\+|-|\*|\/|&|\||<|>|=' # Operators in Jack language
    unary_ops = '-|~' # Unary operators in Jack language
    keyword_consts = 'true|false|null|this' # Keyword constants in Jack language
    statements = 'let|if|while|do|return' # Statements in Jack language

    # Compile regular expression patterns
    operations_p = re.compile(ops)
    unary_op_p = re.compile(unary_ops)
    keyword_const_p = re.compile(keyword_consts)
    statements_p = re.compile(statements)

    def writeOpenTerminal(self, name):
        self.output_file.write(" " * self.curIndent * SPACE_AMOUNT + "<" + name + ">\n") # Write open terminal
        self.modIndent(INCREASE)
        return

    def writeCloseTerminal(self, name):
        self.modIndent(DECREASE)
        to_write = " " * self.curIndent * SPACE_AMOUNT + "</" + name + ">" + "\n" # Write close terminal
        self.output_file.write(to_write)
        return

    def modIndent(self, action):
        self.curIndent += action # Modify indentation
        return

    def writeXml(self):
        key = self.tokenizer.tokenType()
        start = "<" + key + "> " # Start XML tag
        end = " </" + key + ">" if self.get_token() != "do " else "</" + key + ">" # End XML tag
        space = self.curIndent * SPACE_AMOUNT * " "
        self.output_file.write(space + start + str(self.get_token()) + end + "\n")
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        return

    def compileSubroutineCall(self):
        # Handle subroutineName / className / varName
        if not self.get_token() in '(.':
            self.writeXml()
        if self.get_token() == '(':
            self.writeXml() # Write '('
            self.compileExpressionList() # Compile expressionList
            self.writeXml() # Write ")"
            return
        self.writeXml() # Write '.'
        self.writeXml() # Write SubName
        self.writeXml() # Write '('
        self.compileExpressionList() # Compile expressionList
        self.writeXml() # Write ')'
        return

    def __init__(self, tokenizer, output_file):
        self.curIndent = 0
        self.output_file = open(output_file, 'w')
        self.tokenizer = tokenizer
        self.compileClass() # Compile class based on tokenizer to output_file


    def compileClass(self):
        self.tokenizer.advance() # Start reading from JACK file
        self.writeOpenTerminal(CLASS) # Declare the class
        self.writeXml() # write 'class'
        self.writeXml() # write className
        self.writeXml() # write '{'
        while self.get_token() in 'static|field':
            self.compileClassVarDec() # Write classVarDec until subroutine declaration
        while self.get_token() != "}":
            self.compileSubroutine() # Write Subroutines until the end of the class
        self.writeXml() # write '}'
        self.writeCloseTerminal(CLASS)
        return

    def compileClassVarDec(self):
        self.writeOpenTerminal(CLASS_VAR_DEC) # write classVarDec
        self.writeXml() # write 'static'/'field'
        self.writeXml() # write type
        self.writeXml() # write varName
        while self.get_token() == ',':
            self.writeXml() # write ','
            self.writeXml() # write varName
        self.writeXml() # write ";"
        self.writeCloseTerminal(CLASS_VAR_DEC)
        return

    def compileSubroutine(self):
        self.writeOpenTerminal(SUBROUTINE_DEC) # write subroutine
        self.writeXml() # write 'constructor' | 'function' | 'method
        self.writeXml() # write 'void' | type
        self.writeXml() # write subroutineName
        self.writeXml() # write "("
        self.compileParameterList() # write parameterList
        self.writeXml() # write ")"
        self.compileSubroutineBody() # write subroutineBody
        self.writeCloseTerminal(SUBROUTINE_DEC)
        return

    def compileParameterList(self):
        self.writeOpenTerminal(PARAM_LIST) # write parameterList
        if self.get_token() != ')':
            self.writeXml() # write type
            self.writeXml() # write varName
            while self.get_token() == ',':
                self.writeXml() # write ','
                self.writeXml() # write type
                self.writeXml() # write varName
        self.writeCloseTerminal(PARAM_LIST)
        return

    def compileSubroutineBody(self):
        self.writeOpenTerminal(SUBROUTINE_BOD) # write subroutineBody
        self.writeXml() # write "{"
        while self.get_token() == "var":
            self.compileVarDec() # write varDec
        self.compileStatements() # write statements
        self.writeXml() # write "}" after the last statement (end of method body)
        self.writeCloseTerminal(SUBROUTINE_BOD)
        return

    def compileVarDec(self):
        self.writeOpenTerminal(VAR_DEC) # write varDec
        self.writeXml() # write 'var'
        self.writeXml() # write type
        self.writeXml() # write varName
        while self.get_token() == ',':
            self.writeXml() # write ','
            self.writeXml() # write varName
        self.writeXml() # write ';'
        self.writeCloseTerminal(VAR_DEC)
        return

    def compileStatements(self):
        self.writeOpenTerminal(STATEMENTS) # Compiles statements
        while re.match(self.statements_p, self.get_token()):
            if self.get_token() == "let":
                self.compileLet() # Compile 'let'
            elif self.get_token() == "if":
                self.compileIf() # Compile 'if'
            elif self.get_token() == "while":
                self.compileWhile() # Compile 'while'
            elif self.get_token() == "do ":
                self.compileDo() # Compile 'do'
            elif self.get_token() == 'return':
                self.compileReturn() # Compile 'return'
        self.writeCloseTerminal(STATEMENTS)
        return

    def compileDo(self):
        self.writeOpenTerminal(DO) # write doStatement
        self.writeXml() # write 'do'
        self.compileSubroutineCall() # write subroutine
        self.writeXml() # write ';'
        self.writeCloseTerminal(DO)
        return

    def compileLet(self):
        self.writeOpenTerminal(LET) # write letStatement
        self.writeXml() # write 'let'
        self.writeXml() # write varName
        if self.get_token() == '[':
            self.writeXml() # write '['
            self.compileExpression() # Compile expression
            self.writeXml() # write ']'
        self.writeXml() # write '='
        self.compileExpression() # Compile expression
        self.writeXml() # write ';'
        self.writeCloseTerminal(LET)
        return

    def compileWhile(self):
        self.writeOpenTerminal(WHILE) # write whileStatement
        self.writeXml() # write 'while'
        self.writeXml() # write '('
        self.compileExpression() # Compile expression
        self.writeXml() # write ')'
        self.writeXml() # write '{'
        self.compileStatements() # Compile statements
        self.writeXml() # write '}'
        self.writeCloseTerminal(WHILE)
        return

    def compileReturn(self):
        self.writeOpenTerminal(RETURN) # write returnStatement
        self.writeXml() # write 'return'
        if self.get_token() != ';':
            self.compileExpression() # Compile expression
        self.writeXml() # write ';'
        self.writeCloseTerminal(RETURN)
        return

    def compileIf(self):
        self.writeOpenTerminal(IF) # write ifStatement
        self.writeXml() # write 'if'
        self.writeXml() # write '('
        self.compileExpression() # Compile expression
        self.writeXml() # write ')'
        self.writeXml() # write '{'
        self.compileStatements() # Compile statements
        self.writeXml() # write '}'
        if self.get_token() != "else":
            self.writeCloseTerminal(IF)
            return
        self.writeXml() # write 'else'
        self.writeXml() # write '{'
        self.compileStatements() # Compile statements
        self.writeXml() # write '}'
        self.writeCloseTerminal(IF)
        return
    def compileExpression(self):
        # Compiles the XML representation of an expression
        self.writeOpenTerminal(EXPRESSION) # write expression
        self.compileTerm() # compile the first term
        while re.match(self.operations_p, self.get_token()):
            self.writeXml() # write operator
            self.compileTerm() # compile the next term
        self.writeCloseTerminal(EXPRESSION)
        return

    def compileTerm(self):
        # Compiles the XML representation of a term
        self.writeOpenTerminal(TERM) # write term
        if self.get_token() == '(':
            self.writeXml() # write '('
            self.compileExpression() # compile expression inside parentheses
            self.writeXml() # write ')'
        elif re.match(self.tokenizer.intConstP, self.get_token()) or \
             re.match(self.tokenizer.strConstP, self.get_token()) or \
             re.match(self.keyword_const_p, self.get_token()):
            self.writeXml() # write integerConstant, stringConstant, or keywordConstant
        elif re.match(self.unary_op_p, self.get_token()):
            self.writeXml() # write unary operator
            self.compileTerm() # compile term after unary operator
        else:
            # compile varName, subroutineName, or an array indexing
            self.writeXml() 
            if self.get_token() == '[':
                self.writeXml() # write '['
                self.compileExpression() # compile expression for array indexing
                self.writeXml() # write ']'
            elif self.get_token() in '(.':
                self.compileSubroutineCall() # compile subroutine call
        self.writeCloseTerminal(TERM)
        return

    def compileExpressionList(self):
        # Compiles the XML representation of an expression list
        self.writeOpenTerminal(EXP_LIST) # write expressionList
        if self.get_token() != ')':
            self.compileExpression() # compile the first expression
            while self.get_token() == ',':
                self.writeXml() # write ','
                self.compileExpression() # compile subsequent expressions
        self.writeCloseTerminal(EXP_LIST)
        return
    
    def get_token(self):
    # Returns the current token based on its type
        token_type_to_method = {
            KEYWORD: self.tokenizer.keyword,
            SYMBOL: self.tokenizer.symbol,
            IDENTIFIER: self.tokenizer.identifier,
            INT_CONST: self.tokenizer.intVal,
            STRING_CONST: self.tokenizer.stringVal
        }
        token_type = self.tokenizer.tokenType()
        return token_type_to_method.get(token_type, lambda: None)()