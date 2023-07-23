import fitz
import sys
import os
from logging import getLogger, DEBUG, INFO, StreamHandler
logger = getLogger(__name__)
logger.setLevel(INFO)
handler = StreamHandler()
handler.setLevel(INFO)
logger.addHandler(handler)

args = sys.argv
BLANK_BETWEEN_PAGES = 2

def fix_extension(filename):
    have_extension = filename.endswith('.txt')
    if not have_extension:
        filename += '.txt'
    return filename

def solve_output_conflict(output_name):
    file_mode = 'x'
    while os.path.isfile(output_name):
        print("The output file already exists. Continue? r[Rename]/a[Append]/o[Overwrite]/q[Quit]")
        ans = input().lower()
        while ans not in ['r', 'a', 'o', 'q']:
            print("Continue? r[Rename]/a[Append]/o[Overwrite]/q[Quit]")
            ans = input()
        if ans == 'q':
            sys.exit()
        elif ans == 'r':
            print("Please input a new name")
            output_name = fix_extension(input())
        elif ans == 'o':
            file_mode = 'w'
            return output_name, file_mode
        elif ans == 'a':
            file_mode = 'a'
            return output_name, file_mode
    return output_name, file_mode

if __name__ == '__main__':
    input_name = args[1]
    logger.debug(input_name)    
    output_name = fix_extension(args[2])
    logger.debug(output_name)
       
    if not os.path.isfile(input_name):
        print("The input file doesn't exist. Please check the input")
        sys.exit()
        
    output_name, file_mode = solve_output_conflict(output_name)
    
    pdf = fitz.open(input_name)
    text = ""
    for page in pdf:
        text += page.get_text()+'\n'*BLANK_BETWEEN_PAGES+'-'*60+'\n'*BLANK_BETWEEN_PAGES
    with open(output_name, file_mode) as f:
        f.write(text)
