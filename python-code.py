import os
import sys
import argparse
import json
import re

global DEBUG
global MAIN_DIR
global PROJ_DIR

DEBUG = "On"
# sys.argv is a list in Python that contains all the command-line arguments passed to the script.
# sys.argv[0] = script_name
# sys.argv = ['/home/bobi/Documents/Bosch/Zdravko09Jan/exercise-compile-commands/src/main.py']
# sys.argv[0] = '/home/bobi/Documents/Bosch/Zdravko09Jan/exercise-compile-commands/src/main.py'

# os.path.dirname --> gets the directory in which the file is located
MAIN_DIR = os.path.dirname(sys.argv[0])  # this is the directory of this python file 'main.py'
PROJ_DIR = os.path.abspath(os.path.join(os.pardir))  # this is the directory of the entire project


# os.pardir --> gets parent directory

class CompileCommands:
    sSearch = "# Compiling source file"
    dataLocation = 2
    symbolToStripFromLeft = "["
    symbolToStripFromRight = "]"

    def __init__(self, LOG_FILE, OUTPUT_FILE) -> None:
        self.LOG_FILE = LOG_FILE
        self.OUTPUT_FILE = OUTPUT_FILE

    def __call__(self) -> None:
        LOG_DATA = self.readLogFile()
        self.compileCommands(LOG_DATA)

        if DEBUG == "On":
            compile_commands_data = LOG_DATA
            compile_commands_data = self.parse_tree(LOG_DATA)
            print(compile_commands_data)

        print(f"::set-output name=init::{True}")

    def readLogFile(self) -> map:
        # returns a dictionary with required data for JSON file
        c_files = {}
        with open(self.LOG_FILE, 'r+', encoding="utf-8") as file:
            lines = file.readlines()
            for i in range(0, len(lines)):
                # Strip newlines from right (trailing newlines)
                current_row = lines[i]
                if current_row.startswith(self.sSearch) and (i < len(lines) - 2):
                    compilation = lines[i + self.dataLocation]
                    c_files[current_row] = compilation

        return c_files

    def parse_tree(self, map) -> map:
        # TODO 1: What is the idea of this? What is the point?
        return map

    def compileCommands(self, map) -> None:
        # map is the massive dictionary which will be stored in the json file
        pattern = re.compile("\[(.*?)\]")  # Matches everything between [] brackets
        with open(self.OUTPUT_FILE, 'w+', encoding='utf-8') as json_file:
            final_array = []
            for compiledFile, options in map.items():
                # TODO 2: A simplified version which I think works
                match = pattern.search(compiledFile)
                c_file = match.group(1).split('/')[-1]
                c_path = match.group(1)
                '''
                ## OLD
                c_file = match.group(0).split('/')[-1].rstrip(self.symbolToStripFromRight)
                c_path = match.group(0).lstrip(self.symbolToStripFromLeft).rstrip(self.symbolToStripFromRight)
                c_path = c_path.replace("/" + c_file, "")
                '''
                arguments = options.split("\n")[0]
                compile_commands_map = {}
                compile_commands_map["directory"] = c_path
                compile_commands_map["command"] = arguments
                compile_commands_map["file"] = c_file
                final_array.append(compile_commands_map)

            json_file.write(json.dumps(final_array, indent=4))
            json_file.close()

        return


def main():
    try:
        if len(sys.argv) > 1:
            parser = argparse.ArgumentParser(description='Process Log File.')
            parser.add_argument('--log', '-l', type=str, help='The path the log file')
            parser.add_argument('--output', '-o', type=str, help='The path to the output compile commands file')
            parser.add_argument('--config', '-c', type=str, help='The config folder name located in main folder')
            args = parser.parse_args()
            config_folder = args.config
            log_file = args.log
            output_file = args.output
        else:
            config_folder = "config"
            log_file = "build.log"
            output_file = "compile_commands.json"

        CONFIG_DIR = os.path.join(PROJ_DIR, config_folder)
        LOG_FILE = os.path.join(CONFIG_DIR, log_file)
        OUTPUT_FILE = os.path.join(CONFIG_DIR, output_file)
        compileCommandsInit = CompileCommands(LOG_FILE, OUTPUT_FILE)
        compileCommandsInit()
        # line above calls the __call__() method

    except Exception as e:
        raise Exception(f'Catching Exception error {e}')


if __name__ == "__main__":
    main()
