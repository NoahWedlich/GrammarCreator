from io import TextIOWrapper
from rule import Literal, Lexeme, LexemeList, Rule
import sys
import os

name: str = ""
start: Lexeme = Lexeme()
end: Lexeme = Lexeme()
tokens: list[Lexeme] = []
rules: dict[Lexeme, list[Rule]] = {}

def parse_rule(head: str, body_list: str):
    global rules
    head = Lexeme(head)

    body = body_list.split(" ")
    rule_body = []
    for token in body:
        if token == "":
            continue
        elif token[0] == "\"":
            rule_body.append(Literal(token))
        else:
            tokens.append(Lexeme(token))
            rule_body.append(Lexeme(token))
    rule_body = tuple(rule_body)
    
    new_rule = rules.get(head, [])
    new_rule.append(Rule(head, rule_body))
    rules[head] = new_rule


def parse_rules(lines):
    global tokens

    last_token = ""
    for index, line in enumerate(lines):
        if line == "": continue

        head, body = (s.strip() for s in line.split("="))
        if Lexeme(head) in tokens:
            last_token = head
        elif head == "" and last_token != "":
            head = last_token
        else:
            print(f"Unknown token '{head}'")
            exit(1)

        parse_rule(head, body)

def parse(file: TextIOWrapper):
    global name
    global start
    global end
    global tokens
    global rules

    file.seek(0)
    source = file.read()
    lines = source.split("\n")

    name_l, start_l, end_l = (line.split(":") for line in lines[:3])

    if name_l[0].strip() == "Grammar":
        name = name_l[1].strip()
    else:
        print(f"Expected 'Grammar' got '{name_l[0]}'")
        exit(1)

    if start_l[0].strip() == "Start":
        start = Lexeme(start_l[1].strip())
    else:
        print(f"Expected 'Start' got '{name_l[0]}'")
        exit(1)

    if end_l[0].strip() == "End":
        end = Lexeme(end_l[1].strip())
    else:
        print(f"Expected 'End' got '{name_l[0]}'")
        exit(1)

    tokens.append(start)

    parse_rules(lines[3:])

def main():
    # if len(sys.argv) != 2:
    #     print("Usage: python grammar_creator.py 'filename'")
    #     exit(1)
    
    # filename = sys.argv[1]

    filename = "test.txt"
    
    if os.path.exists(filename):
        with open(filename, "r") as h:
            if h.read(7) == "Grammar":
                parse(h)
            else:
                print("clear")
    else:
        print("new")

    print(name)
    print(start)
    print(end)

    for _, rule_list in rules.items():
        for rule in rule_list:
            print(str(rule))
    


if __name__ == '__main__':
    main()