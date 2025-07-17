#Name: Rajveer Singh
#Banner id: B00959627
#parts of this project is referred from given course material for Scaner:
# https://dal.brightspace.com/d2l/le/content/339151/viewContent/4537780/View


class TokenType:
    OBRACKET = 'OBRACKET'  #'['
    CBRACKET = 'CBRACKET'  #']'
    COMMA = 'COMMA'        #','
    COLON = 'COLON'        #':'
    OCURLY = 'OCURLY'      #'{'
    CCURLY = 'CCURLY'      #'}'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    NULL = 'NULL'
    LIST = 'LIST'          # value of list
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    PAIR = 'PAIR'
    DICT = 'DICT'
    EOF = 'EOF'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.type == TokenType.OBRACKET:
            return "<[>"
        elif self.type == TokenType.CBRACKET:
            return "<]>"
        elif self.type == TokenType.COMMA:
            return "<,>"
        elif self.type == TokenType.COLON:
            return "<:>"
        elif self.type == TokenType.OCURLY:
            return "<{>"
        elif self.type == TokenType.CCURLY:
            return "<}>"
        elif self.type == TokenType.TRUE:
            return f"<bool, {self.value}>"
        elif self.type == TokenType.FALSE:
            return f"<bool, {self.value}>"
        elif self.type == TokenType.NULL:
            return "<null>"
        elif self.type == TokenType.LIST:
            return f"<lis, {self.value}>"
        elif self.type == TokenType.STRING:
            return f"<str, {self.value}>"
        elif self.type == TokenType.NUMBER:
            return f"<num, {self.value}>"
        elif self.type == TokenType.PAIR:
            return f"<pair, {self.value}>"
        elif self.type == TokenType.DICT:
            return f"<dict, {self.value}>"
        else:
            return f"<{self.type}>"

# Lexer error
class LexerError(Exception):
    def __init__(self, position, character):
        self.position = position
        self.character = character
        super().__init__(f"Invalid character '{character}' at position {position}")


class Lexer:
    def __init__(self, input_text):
        # Input string
        self.input_text = input_text
        # Current position
        self.position = 0
        if self.input_text:
            self.curr_char = self.input_text[self.position]
        else:
            self.curr_char = None

    # Input Buffering with amount as number of position to move ahead
    def advance(self, amount=None):

        if amount is None:
            self.position += 1
        else:
            self.position += amount

        if self.position >= len(self.input_text):
            # End of input
            self.curr_char = None
        else:
            self.curr_char = self.input_text[self.position]

    # Skip whitespace
    def white_space(self):
        while self.curr_char is not None and self.curr_char.isspace():
            self.advance()
    # Recognize all terminals in the grammar
    def recognize_terminals(self):
        while self.curr_char is not None:
            if self.curr_char.isspace():
                #skip white spaces if needed and continue
                self.white_space()
                continue

            if self.curr_char == '[':
                self.advance()
                return Token(TokenType.OBRACKET)
            if self.curr_char == ']':
                self.advance()
                return Token(TokenType.CBRACKET)
            if self.curr_char == ',':
                self.advance()
                return Token(TokenType.COMMA)
            if self.curr_char == ':':
                self.advance()
                return Token(TokenType.COLON)
            if self.curr_char == '{':
                self.advance()
                return Token(TokenType.OCURLY)
            if self.curr_char == '}':
                self.advance()
                return Token(TokenType.CCURLY)

            #for booleans
            if self.curr_char == 't' or self.curr_char == 'f' or self.curr_char == 'n':
                return self.recognize_boolean_or_Null()


            if self.curr_char == '"' :
                return self.recognize_string()
            if self.curr_char.isdigit()or self.curr_char in ['.', 'e', 'E', '-', '+']:
                return self.recognize_number()

            raise LexerError(self.position, self.curr_char)
        return Token(TokenType.EOF)

    #recognize booleans and null character
    def recognize_boolean_or_Null(self):
        if self.curr_char == 't':
            #taking temp text as from current position to 4 index of that
            tempTxt = self.input_text[self.position:self.position+4]
            if tempTxt == 'true':
                value = 'true'
                self.advance(4)
                return Token(TokenType.TRUE, value)
            else:
                #error if not true
                raise LexerError(self.position, self.curr_char)
        if self.curr_char == 'f':
            #taking temp text as from current position to 5 index of that
            tempTxt = self.input_text[self.position:self.position+5]
            if tempTxt == 'false':
                value = 'false'
                self.advance(5)
                return Token(TokenType.FALSE, value)
            else:
                #error if not false
                raise LexerError(self.position, self.curr_char)
        if self.curr_char == 'n':
            #taking temp text as from current position to 4 index of that
            tempTxt = self.input_text[self.position:self.position+4]
            if tempTxt == 'null':
                self.advance(4)
                return Token(TokenType.NULL, None)
            else:
                #error if not null
                raise LexerError(self.position, self.curr_char)

    # Recognize string
    def recognize_string(self):
        if self.curr_char != '"':
            raise LexerError(self.position, self.curr_char)
        self.advance()
        final = ''
        while self.curr_char is not None and self.curr_char != '"':
            final += self.curr_char
            self.advance()
        if self.curr_char != '"':
            #if string doesn't end with "
            raise LexerError(self.position, self.curr_char)
        self.advance()
        return Token(TokenType.STRING, final)

    # Recognize numbers
    def recognize_number(self):
        final = ''
        while self.curr_char is not None and (self.curr_char.isdigit() or self.curr_char in ['.', 'e', 'E', '-', '+']):
            final += self.curr_char
            self.advance()
        try:
            return Token(TokenType.NUMBER, final)
        except ValueError:
            #error if can't converted to float or is not numerical
            raise LexerError(self.position, final)

    # Tokenize the input
    def tokenize(self):
        tokens = []
        while True:
            try:
                token = self.recognize_terminals()
            except LexerError as e:
                print(f"Lexical Error: {e}")
                break

            if token.type == TokenType.EOF:
                break
            tokens.append(token)
        return tokens


# Testing the Lexer with input
if __name__ == "__main__":

    # the file reading part was referred from: https://stackoverflow.com/questions/8369219/how-can-i-read-a-text-file-into-a-string-variable-and-strip-newlines
    with open('inputTokenizer.txt', 'r') as file:
        input_string = file.read()
    lexer = Lexer(input_string)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)