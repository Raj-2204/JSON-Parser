#Name: Rajveer Singh
#Banner id: B00959627
#parts of this project is referred from given course material for Parser:
# https://dal.brightspace.com/d2l/le/content/339151/viewContent/4537780/View

from scanner import Lexer, TokenType

class Node:
    def __init__(self,label=None, is_leaf=False):
        self.label = label
        self.children = []
        self.is_leaf = is_leaf

    def add_child(self, child):
        self.children.append(child)

    def print_tree(self,depth=0, file=None):
        indent = "    " * depth
        print(f"{indent} {self.label}", file=file)
        for child in self.children:
            child.print_tree(depth+1, file=file)

class Parser:
    def __init__(self,lexer):
        self.lexer = lexer
        self.current_token = None
        self.keys = []

    #this method pair keys to the keys list
    def add_key(self,key):
        self.keys.append(key)


    def get_next_token(self):
        self.current_token = self.lexer.recognize_terminals()
        if self.current_token is None:
            raise Exception("Unexpected EOF")

    def eat(self, token_type):
        """Consumes a token if it matches the expected type."""
        if self.current_token.type == token_type:
            self.get_next_token()
            """Raise an Error otherwise"""
        else:
            raise Exception('Different TokenType')

    def parse(self):
        """Starts the parsing process by fetching the first token and
        calling the first grammar rule."""
        self.get_next_token()
        return self.tree()

    def tree(self):
        """Parses the Tree rule: Subtree 'EOF'"""
        node = self.value()
        self.eat(TokenType.EOF)
        return node

    def value(self):
        """Add the node with the with 'value' label and
        return according to the type of token currently at position to
        childeren list"""
        node = Node(label=f'value:')
        if self.current_token.type == TokenType.STRING:
            node.add_child(self.string())
        elif self.current_token.type == TokenType.NUMBER:
            node.add_child(self.number())
        elif self.current_token.type == TokenType.TRUE:
            node.add_child(self.true())
        elif self.current_token.type == TokenType.FALSE:
            node.add_child(self.false())
        elif self.current_token.type == TokenType.NULL:
            node.add_child(self.null())
        elif self.current_token.type == TokenType.OCURLY:
            node.add_child(self.dict())
        elif self.current_token.type == TokenType.OBRACKET:
            node.add_child(self.list())
        else:
            raise Exception(f"Unexpected token found instead of value")
        return node

    """will return the node and eat that TokenType and update the label with Type and Value 
        of the token, set is_leaf to true if they are leaf"""
    def string(self):
        node = Node(label=self.current_token.type+': '+self.current_token.value, is_leaf=True)
        if self.reservedWord(self.current_token.value):
            raise Exception(f"Error Type 7 at {self.current_token.value}: Reserved Words as Strings")
        self.eat(TokenType.STRING)
        return node

    """This method will return the boolean if the decimal in input stream is in valid semantical
    format or not."""
    def valid_decimal(self, decimalNumber):
        if decimalNumber.startswith('.') or decimalNumber.endswith('.'):
            return False
        elif decimalNumber.startswith('+'):
            return False
        else:
            return True

    """This method will return the boolean if the number in input stream is in valid semantical
    format or not."""
    def valid_number(self, number):
        if number.startswith('0'):
            splitting = number.split('0')
            if len(splitting) == 2 and splitting[0]:
                return True
            return False
        return True

    def number(self):
        node= Node(label=self.current_token.type+': ', is_leaf=True)
        curr_token_value = self.current_token.value
        node.label+=str(float(curr_token_value))

        #error raised when not a valid number
        if not self.valid_number(curr_token_value):
            raise Exception(f'Error Type 3 at {curr_token_value}'
                            f': Invalid Numbers.')

        #error raised when not a valid decimal
        if not self.valid_decimal(curr_token_value):
            raise Exception(f'Error Type 1 at {curr_token_value} : Invalid Decimal Numbers')

        self.eat(TokenType.NUMBER)
        return node

    def true(self):
        node= Node(label='BOOLEAN: '+self.current_token.value, is_leaf=True)
        self.eat(TokenType.TRUE)
        return node

    def false(self):
        node= Node(label='BOOLEAN: '+self.current_token.value, is_leaf=True)
        self.eat(TokenType.FALSE)
        return node
    def null(self):
        node = Node(label=self.current_token.value, is_leaf=True)
        self.eat(TokenType.NULL)
        return node


    def list(self):
        node = Node(label='list:')
        self.eat(TokenType.OBRACKET)

        #for better formatting added [ to specify list
        node.add_child(Node(label='['))

        #creating a set for entering the type of element in the list
        element_types = set()
        if self.current_token.type is not TokenType.CBRACKET:
            value = self.value()
            node.add_child(value)

            #first element added to the set will set a benchmark for next sets
            element_types.add(value.children[0].label.split(':')[0])

        #This will eat the Commas present in list to differ values from each other
        while self.current_token.type is TokenType.COMMA:
            self.eat(TokenType.COMMA)
            value = self.value()
            node.add_child(value)

            #if the elements are same type as the first element in the set
            #they won't repeat as repeated entries are not allowed in sets.
            element_types.add(value.children[0].label.split(':')[0])

        #but if one more type of element is added to the list sets size will increase
        #which will indicate error
        if len(element_types) > 1:
            raise Exception(f'Error Type 6 at [{element_types.pop()}, { element_types.pop()}]: Consistent Types for List Element')


        if self.current_token.type == TokenType.CBRACKET:
            self.eat(TokenType.CBRACKET)
        else:
            raise Exception(f"Missing {']'} at the end of {self.current_token.type}")
        node.add_child(Node(label=']'))
        return node

    """This method specifies if the input word is in the reserve word or not"""
    def reservedWord(self, word):
        if(word in ['true','false']):
            return True
        return False

    def pair(self):
        node = Node(label='pair:')

        #this condition checks if the current token is string, not a empty space, not in reserve words
        #of the grammar and keys are not repeated
        if (self.current_token.type is TokenType.STRING and self.current_token.value and
                not self.current_token.value.isspace() and not self.reservedWord(self.current_token.value)
        and self.current_token.value not in self.keys):
            self.add_key(self.current_token.value)
            node.add_child(self.value())

        #If the keys repeat it will raise an error
        elif self.current_token.value in self.keys:
            raise Exception(f'Error Type 5 at {self.current_token.value}: No Duplicate Keys in Dictionary')

        #if its reserved word it will raise an error
        elif self.reservedWord(self.current_token.value):
            raise Exception(f'Error Type 4 at {self.current_token.value}: Reserved Words as Dictionary Key')

        #if the key is empty raise an error
        else:
            raise Exception(f'Error Type 2 at Key:'
                            f' Empty Key.')
        while self.current_token.type is TokenType.COLON:
            self.eat(TokenType.COLON)
            node.add_child(self.value())
        return node

    def dict(self):
        node = Node(label='dict')
        self.eat(TokenType.OCURLY)
        node.add_child(Node(label='{'))
        node.add_child(self.pair())
        while self.current_token.type is TokenType.COMMA:
            self.eat(TokenType.COMMA)
            node.add_child(self.pair())
        if self.current_token.type == TokenType.CCURLY:
            self.eat(TokenType.CCURLY)
        else:
            raise Exception(f"Expected token {'}'}, got {self.current_token.type}")
        node.add_child(Node(label='}'))
        return node

class InputRead:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    #read the type and return the element according to that, if the element has any
    #value in it only the value will be returned.
    def read(self, type, value=None):
        if type=="<[>":
            return '['
        elif type=="<]>":
            return ']'
        elif type=="<,>":
            return ','
        elif type=="<:>":
            return ':'
        elif type=="<{>":
            return '{'
        elif type=="<}>":
            return '}'
        elif type == 'str':
            return f' "{value}" '
        elif type == 'num':
            return value
        elif type == 'bool':
            return f" {value} "
        elif type == 'null':
            return 'null'
        return ''

    """This method is taking inputPath as its input which is tokenized input.
    Converting it into String for paser to use for ParseTree"""
    def write(self, inputPath):
        result_string = ""
        with open(inputPath, "r") as file:
            for line in file:
                #This reads line by line and update stripped_line by removing extra spaces or new line
                stripped_line = line.strip()
                if stripped_line:
                    if ", " in stripped_line and stripped_line.startswith("<") and stripped_line.endswith(">"):

                        #reffered from: https://www.tutorialspoint.com/what-does-do-in-python#:~:text=For%20negative%20indexing%2C%20to%20display,can%20slice%20strings%20like%20this.
                        #Remove the first and last element of stripped_content
                        stripped_content = stripped_line[1:-1]

                        #It splits the string stripped_content into two parts type_ and value
                        #reffered from: https://www.w3schools.com/python/ref_string_split.asp
                        parts = stripped_content.split(', ', 1)
                        type = parts[0]
                        value= parts[1]
                        token = InputRead(type,value)
                        result_string += token.read(type,value)

                    #adding characters which only have symbols like {,},[,],:,etc
                    elif stripped_line.startswith("<") and stripped_line.endswith(">"):
                        token = InputRead(stripped_line)
                        result_string+=token.read(stripped_line)
        return result_string

if __name__ == "__main__":
    String = InputRead(None)
    #Using write method of Input reader for reading and writing it into input_string
    input_string = String.write("input1.txt")

    lexer = Lexer(input_string)

    parser = Parser(lexer)

    with open("Output.txt", "w") as file1:
        try:
            tree = parser.parse()
            tree.print_tree(file=file1)
        except Exception as e:
            file1.write(f"Parsing Error: {e}")





