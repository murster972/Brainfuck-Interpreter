#!/usr/bin/env python3
from argparse import ArgumentParser
import sys

""" A Brainfuck Interpreter -=- https://en.wikipedia.org/wiki/Brainfuck """

class BrainfuckInterpeter:
    def __init__(self, bf_file, cell_size=3000, show_cells=False):
        self.code = self.__get_code(bf_file)

        self.show_cells = show_cells

        self.cell_size = cell_size
        self.cells = [0 for i in range(self.cell_size)]


        self.interpreter()

    def __get_code(self, f_name):
        bf_chars = "<>+-.,[]"

        try:
            f = open(f_name, "r")
            code = f.read()
            f.close()

            return [i for i in code if i in bf_chars]

        except FileNotFoundError:
            print("[-] Invalid file name passed, file not found.")
        except PermissionError:
            print("[-] Invalid file name passed, incorrect permissions to access file.")
        except Exception as err:
            print("[-] Inavlid file, unable to open due to the following excpetion: {}".format(err))
        sys.exit(-1)

    def interpreter(self):
        cell_i = 0
        i = 0

        while 0 <= i < len(self.code) and 0 <= cell_i < self.cell_size:
            c = self.code[i]
            cur_cell = self.cells[cell_i]

            if c == "[" and cur_cell == 0:
                i = self.__match_bracket("[", 1, i + 1)
                continue

            elif c == "]":
                i = self.__match_bracket("]", -1, i - 1)
                continue

            elif c == ">": cell_i += 1
            elif c == "<": cell_i -= 1
            elif c == "+": self.cells[cell_i] += 1
            elif c == "-": self.cells[cell_i] -= 1
            elif c == ".": print(chr(self.cells[cell_i]), end="")
            elif c == ",": self.cells[cell_i] = self.__get_char()
            i += 1

        if self.show_cells:
            print("\n")
            print(*self.cells, sep=", ")

    def __match_bracket(self, b, inc, ind):
        b_count = 1
        i = ind
        while b_count != 0:
            c = self.code[i]
            if b == "]" and c == "]" or b == "[" and c == "[": b_count += 1
            elif b == "]" and c == "[" or b == "[" and c == "]": b_count -= 1
            i += inc
        return i if b == "[" else i + 1

    def __get_char(self):
        c = input()
        return 0 if len(c) == 0 else ord(c[0])

def main():
    parser = ArgumentParser()

    parser.add_argument("filename", help="Name of file containing Brainfuck code")
    parser.add_argument("--cellsize", type=int, help="Set cell size", default=100)
    parser.add_argument("--showcells", choices=["true", "True", "false", "False"], help="Show content of cells at end of program", default="False")

    args = parser.parse_args()

    BrainfuckInterpeter(args.filename, cell_size=args.cellsize, show_cells=eval(args.showcells.title()))

if __name__ == '__main__':
    main()
