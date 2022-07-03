from io import TextIOWrapper
import sys
import os

name = ""
start = ""
end = ""
tokens = []
rules = {}

def parse_rule(head, body_list):
    global rules

    body = body_list.split(" ")
    rule_body = []
    for token in body:
        if token == "":
            continue
        elif token[0] == "\"":
            rule_body.append(token)
        else:
            tokens.append(token)
            rule_body.append(token)
    
    new_rule = rules.get(head, [])
    new_rule.append(tuple(rule_body))
    rules[head] = new_rule


def parse_rules(lines):
    global tokens

    last_token = ""
    for index, line in enumerate(lines):
        if line == "": continue

        head, body = (s.strip() for s in line.split("="))
        if head in tokens:
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

    file.seek(0)
    source = file.read()
    lines = source.split("\n")
    name_p, start_p, end_p = (line.split(":") for line in lines[:3])
    if name_p[0].strip() == "Grammar":
        name = name_p[1].strip()
    else:
        print(f"Expected 'Grammar' got '{name_p[0]}'")
        exit(1)

    if start_p[0].strip() == "Start":
        start = start_p[1].strip()
    else:
        print(f"Expected 'Start' got '{name_p[0]}'")
        exit(1)

    if end_p[0].strip() == "End":
        end = end_p[1].strip()
    else:
        print(f"Expected 'End' got '{name_p[0]}'")
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

    print(rules)
    


if __name__ == '__main__':
    main()