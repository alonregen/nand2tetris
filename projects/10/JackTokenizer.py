import re

LT = '<'
GT = '>'
AMP = '&'
QUOT = '\"'

KEYWORD = "keyword"
SYMBOL = "symbol"
IDENTIFIER = "identifier"
INT_CONST = "integerConstant"
STRING_CONST = "stringConstant"


class JackTokenizer:
    keywords = "class|constructor|function|method|field|static|var|int|char |boolean|void|true|false|null|this|let|do |if|else|while|return"
    symbols = '{|}|\(|\)|\[|]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~'
    identifiers = '[a-zA-Z_]{1}[a-zA-Z_\d]*'
    intConst = '[\d]+'
    strConst = '\"[^\r\n]+\"'
    allTokens = keywords + '|' + symbols + '|' + identifiers + '|' + intConst + '|' + strConst
    comments = '//[^\n]*\n|/\*(.|\n)*?\*/'
    keywordP = re.compile(keywords)
    symbolP = re.compile(symbols)
    identifierP = re.compile(identifiers)
    intConstP = re.compile(intConst)
    strConstP = re.compile(strConst)
    allTokensP = re.compile(allTokens)
    commentsP = re.compile(comments)

    def __init__(self, input_file):
        self.tokens = []
        self.curToken = None
        self.curType = None
        self.processLines(input_file)
        self.curI = -1

    def processLines(self, input_file):
        with open(input_file, 'r') as f:
            content = re.sub(self.commentsP, ' ', f.read())
        self.tokens = re.findall(self.allTokensP, content)
        return

    def hasMoreTokens(self):
        return self.curI < (len(self.tokens) - 1)

    def advance(self):
        self.curI += 1
        self.curToken = self.tokens[self.curI]
        token_type_mapping = {
            self.keywordP: KEYWORD,
            self.symbolP: SYMBOL,
            self.identifierP: IDENTIFIER,
            self.intConstP: INT_CONST,
            self.strConstP: STRING_CONST
        }
        for pattern, token_type in token_type_mapping.items():
            if re.match(pattern, self.curToken):
                self.curType = token_type
                break

    def tokenType(self):
        return self.curType

    def keyword(self):
        return str(self.curToken)

    def symbol(self):
        special_symbols = {
            LT: "&lt;",
            GT: "&gt;",
            QUOT: "&quot;",
            AMP: "&amp;"
        }
        return special_symbols.get(self.curToken, str(self.curToken))

    def identifier(self):
        return str(self.curToken)

    def intVal(self):
        return str(self.curToken)

    def stringVal(self):
        return str(self.curToken)[1:-1]