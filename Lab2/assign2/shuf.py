#!/usr/bin/python

"""
Output lines randomly shuffled. Partial Python implementation of GNU "shuf"

Roland Yang 506053914
"""

import random, sys, argparse

class shuf:
    def __init__(self, lines):
        self.lines = lines
        random.shuffle(self.lines)
    
    def chooseline(self):
        return random.choice(self.lines)

    def getshuf(self):
        return self.lines

def main():
    parser = argparse.ArgumentParser(description="Write a random permutation of the input lines to standard output. With no FILE, or when FILE is -, read standard input.")
    parser.add_argument("-e", "--echo", nargs="*", help="treat each ARG as an input line")
    parser.add_argument("-i", "--input-range", metavar="LO-HI", type=str, help="treat each number LO through HI as an input line")
    parser.add_argument("-n", "--head-count", metavar="COUNT", type=int, help="output at most COUNT lines")
    parser.add_argument("-r", "--repeat", action="store_true", help="get random bytes from FILE")
    parser.add_argument("filename", nargs="?", help="name of file to read from")
    
    # Namespace(echo=[], input_range="", head_count=int, repeat=True, filename="")
    args = parser.parse_args()

    # CHECK ARGS (for debugging)
    # print(args)

    lines = []

    ######################################################################################################

    # Cannot combine -i and -e (mimic behavior of GNU)
    if args.input_range != None and args.echo != None:
        parser.error("Arguments Error: Cannot combine -i and -e options")

    # Cannot combine file and range, confused which to use as input (mimic behavior of GNU version)
    if args.filename != None and args.input_range != None:
        parser.error("Arguments Error: Extra operand ({0})".format(args.filename))

    # No range or echo input, assume reading from stdin or file
    if args.echo == None and args.input_range == None:
        # Read from stdin
        if (args.filename == '-' or args.filename == None):
            try:
                lines = sys.stdin.readlines() # Use CTRL-D as the EOF
            except:
                parser.error("I/O Error: STDIN Failure")
        else: # attempt to read from file
            try:
                f = open(args.filename, 'r')
                lines = f.readlines()
                f.close()
            except:
                parser.error("I/O Error: File reading error ({0})".format(args.filename))
    
    # Strip newlines from lines to prevent printing errors
    lines = [x.rstrip() for x in lines]

    # Check headcount
    if args.head_count != None:
        if args.head_count < 0:
            parser.error("Headcount Error: Can't be negative number ({0})".format(args.filename))

    # Check range
    if args.input_range != None:
        try:
            lo, hi = map(int, args.input_range.split("-"))
            assert(lo <= hi)
            lines = list(range(lo, hi + 1)) # Range is INCLUSIVE
        except:
            parser.error("Input Range Error: Invalid values")

    # Set lines to echo (echo has precendence over file input to mimic GNU version)
    if args.echo != None:
        lines = args.echo
        if args.filename != None: # Count the filename in the echo if specified (mimic behavior of GNU version)
            lines.append(args.filename)

    ######################################################################################################

    generator = shuf(lines)
    output = generator.getshuf()

    # Repeat case
    if args.repeat == True:
        # Give error if no lines to repeat (mimic behavior of GNU version)
        if len(lines) == 0:
            parser.error("Input Error: No lines to repeat")

        if args.head_count == None:
            while True:
                print(generator.chooseline())
        else:
            for x in range(args.head_count):
                print(generator.chooseline())
            exit() # Prevent running further if statements

    # Headcount case
    if args.head_count != None:
        if args.head_count > len(lines):
            args.head_count = len(lines)
        for i in range(args.head_count):
            print(output[i])

    # Normal case, just output all the shuffled lines
    if args.repeat == False and args.head_count == None:
        for line in output:
            print(line)

if __name__ == "__main__":
    main()