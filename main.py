
import sys

String  = str
Integer = int
Atom    = (String, Integer)
Exp     = (Atom, List)

class Tokenizer:
    def __init__(self, data):
        self.input = data
        self.tokens = []

    def tokenize(self):
        temp = ""
        for char in self.input:
            if char == "(" or char == ")":
                if temp != "" and temp != " ":
                    self.tokens.append(temp)
                    temp = ""
                self.tokens.append(char)
            elif char != " " and char != "":
                temp += char
            elif char == " ":
                if temp != "" and temp != " ":
                    self.tokens.append(temp)
                temp = ""

    def get_input(self):
        return self.input
    
    def get_tokens(self):
        return self.tokens

    def print_tokens(self):
        for t in self.tokens:
            print(t)

    def is_correct(self):
        stack = []
        if self.tokens[0] != "(":
            return False
        for token in self.tokens:
            if token == "(":
                stack.append(token)
            elif token == ")":
                if len(stack) == 0:
                    return False
                char = stack.pop()
                if char != "(":
                    return False
        if len(stack) == 0:
            return True
        return False


class Parser:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.parsed_tokens = None

    def parse(self):
        self.parsed_tokens = self.read_token(self.tokenizer.get_tokens())
        
    def read_token(self, tokens):
        if len(tokens) == 0:
            print("unexpected EOF")
        token = tokens.pop(0)
        left = []
        if token == '(':
            while tokens[0] != ')':
                left.append(self.read_token(tokens))
            tokens.pop(0)
            return left
        else:
            return self.atom(token)
    
    def atom(self, token):
        try: return int(token)
        except ValueError:
            try: 
                return float(token)
            except ValueError:
                return String(token)
    
    def get_parsed_tokens(self):
        return self.parsed_tokens    

class Input:
    def __init__(self, inp):
        self.inp = inp
        self.commands = []

    def save_command(self, command):
        self.commands.append(command)

    def get_input(self):
        return self.inp

    def save_input(self, inp):
        self.inp = inp

if __name__ == "__main__":
    inp = Input("")
    if len(sys.argv) == 1:
        while True:
            val = input("<< ")
            if val == "q" or val == "quit()" or val == "exit":
                break
            inp.save_input(val)
            tokenizer = Tokenizer(inp.get_input())
            tokenizer.tokenize()
            if tokenizer.is_correct() == False:
                print("Brackets are not properly aligned. Make sure every ( contains a )")         
            parser = Parser(tokenizer)
            parser.parse()
            print(parser.get_parsed_tokens())
    elif len(sys.argv) == 3:
        in_file = open(sys.argv[1], "r")
        out_file = open(sys.argv[2], "w")
        inp.save_input(in_file.read())
        tokenizer = Tokenizer(inp.get_input())
        tokenizer.tokenize()
        if tokenizer.is_correct() == False:
            print("Brackets are not properly aligned. Make sure every ( contains a )")         
        parser = Parser(tokenizer)
        parser.parse()
        out_file_content = parser.get_parsed_tokens()
        print(parser.get_parsed_tokens())
        for tok in parser.get_parsed_tokens():
            out_file.write('%s ' % tok)
        out_file.close()
        in_file.close()
    else:
        print("Unexpected usage. Expected 0 or 2 arguments but received "
                + str(len(sys.argv) - 1))

