from string import whitespace

def filter_comments(string):
    output = ""
    for line in string.split("\n"):
        output += line.split(";")[0] + "\n"
    return output

def parse_sexp(string):
    output = [[]]
    buffer = ''
    in_string = False

    for char in string:
        # start sexp
        if char == "(" and not in_string:
            output.append([])
        # close an sexp, put into one context up
        elif char == ")" and not in_string:
            if buffer:
                output[-1].append(buffer)
                buffer = ''
            temp = output.pop()
            output[-1].append(temp)
        # handle tokens within an sexp
        elif char in whitespace and not in_string:
            if buffer:
                output[-1].append(buffer)
                buffer = ''
        # open or close strings, as appropriate
        elif char == "\"": in_string = not in_string
        # otherwise, just update the buffer
        else: buffer += char

    return output[0][0]

def clean_string(string):
    return "(" + filter_comments(string) + ")"
