import argparse
import ast
import re
import copy

class DFA():
    def __init__(self, states, transitions, alpha, final_states, start, labels, expressions):
        self.states = states
        self.transitions = transitions
        self.alpha = alpha
        self.final_states = final_states
        self.start = start
        self.labels = labels
        self.expressions = expressions

def str2tupleList(s):
    arr = s.replace("\n","").replace(",,",", ,")
    arr = re.sub("[ ]*\,[ ]*", ",", arr)
    arr = re.split(r'[ ]*\)[ ]*\,[ ]*\([ ]*', arr)
    return list(tuple(x.split(',')) for x in arr)

def execute(state, fb_dfa, string, right, left, output_file):
    output_file.write(string[right:left+1]+", "+fb_dfa.expressions[fb_dfa.labels[state]]+'\n')

def fallback_DFA(string, fb_dfa, right, output_file):
    stack = []
    stack.append(fb_dfa.start)
    for left in range(right, len(string)):
        l = string[left]
        for t in fb_dfa.transitions:
            if l == t[1] and stack[-1] == t[0]:
                stack.append(t[2])
                break
    if stack[-1] in fb_dfa.final_states:
        return execute(stack[-1], fb_dfa, string, right, left, output_file)
    else:
        while len(stack) != 0 and left>=right:
            stack = stack[:-1 or None]
            left = left - 1
            if len(stack)>0 and stack[-1] in fb_dfa.final_states:
                execute(stack[-1], fb_dfa, string, right, left, output_file)
                left = left + 1
                right = copy.deepcopy(left)
                fallback_DFA(string, fb_dfa, right, output_file)
                return
        if len(stack) == 0:
            return execute("DEAD", fb_dfa, string, right, len(string)-1, output_file)
    return execute("DEAD", fb_dfa, string, right, len(string)-1, output_file)


def main():
    with open(args.dfa_file, "r") as file:
        lines = file.readlines()
    states = lines[0].replace("\n","").replace(" ", "").split(",")
    alpha = lines[1].replace("\n","").replace(" ", "").replace(",,"," ").split(",")
    start = lines[2].replace("\n","")   
    final_states = lines[3].replace("\n","").replace(" ", "").split(",")
    transitions = str2tupleList(lines[4].replace("\n","")[1:-1])
    labels = str2tupleList(lines[5].replace("\n","")[1:-1])
    labels_dict = dict((x, y) for x, y in labels)
    expressions = str2tupleList(lines[6].replace("\n","")[1:-1])
    expressions_dict = dict((x, y) for x, y in expressions)

    fb_DFA = DFA(states, transitions, alpha, final_states, start, labels_dict, expressions_dict)

    output_file = open("task_3_1_result.txt", "w+")
    with open(args.input_file, "r") as file:
        lines = file.readlines()
    for line in lines:
        fallback_DFA(line.strip(), fb_DFA, 0, output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--dfa-file', action="store", help="path of file to construct dfa", nargs="?", metavar="dfa")
    parser.add_argument('--input-file', action="store", help="path of file to take as input", nargs="?", metavar="input")

    args = parser.parse_args()

    print(args.input_file)
    print(args.dfa_file)

    main()