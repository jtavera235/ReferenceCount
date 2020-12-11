
import sys

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

class Counter:

    def __init__(self, tokens):
        self.tokens = tokens
        self.count_list = {}

    def save_variables(self):
        next_is_var = False
        for tok in self.tokens:
            if tok == "define":
                next_is_var = True
            elif next_is_var == True:
                if tok in self.count_list.keys():
                    entry = self.count_list.get(tok)
                    entry = entry + 1
                    self.count_list.update({ tok: entry }) 
                elif tok != "\n":
                    self.count_list.update({ tok: 1 })
                next_is_var = False

    def print_counter(self):
        for entry in self.count_list:
            print(entry + " " + str(self.count_list.get(entry)))

    def get_count(self):
        return self.count_list

class ReferenceCounter:

    def __init__(self, tokens, counter):
        self.tokens = tokens
        self.counter = counter
        self.summary = {}

    def analyze(self):
        index = 1
        for tok in self.tokens:
            if tok == "\n":
                index = index + 1
            elif tok in self.counter.keys():
                entry = self.counter.get(tok)
                entry = entry - 1
                if entry == 0:
                    self.summary.update({ tok: ("Reference to variable " + tok + " was dropped at line " + str(index)) })
                else:
                    self.counter.update({ tok: entry })

    def print_summary(self):
        for entry in self.summary:
            print(entry + " " + str(self.summary.get(entry)))

    def get_summary_as_str(self):
        sumry = ""
        for entry in self.summary:
            sumry = sumry + " " + str(self.summary.get(entry)) + "\n"
        return sumry

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
    if len(sys.argv) == 3:
        in_file = open(sys.argv[1], "r")
        out_file = open(sys.argv[2], "w")
        inp.save_input(in_file.read())
        tokenizer = Tokenizer(inp.get_input())
        tokenizer.tokenize()
        if tokenizer.is_correct() == False:
            print("Brackets are not properly aligned. Make sure every ( contains a )")         
        counter = Counter(tokenizer.get_tokens())
        counter.save_variables()
        reference_counter = ReferenceCounter(tokenizer.get_tokens(), counter.get_count())
        reference_counter.analyze()
        out_file_content = reference_counter.get_summary_as_str()
        out_file.write(out_file_content)
        out_file.close()
        in_file.close()
    else:
        print("Unexpected usage. Expected 2 arguments but received "
                + str(len(sys.argv) - 1))

