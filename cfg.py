import os
import sys
import platform
import subprocess
import re

# Getting the base details
current_path = os.path.abspath((os.getcwd()))
OS = platform.system()

# The base dirs
godot_dir = current_path + '\godot'
rust_dir = current_path + '\\rust'

# Setting concrete folders
rust_compiling_folder = rust_dir + '\\target\debug'
rust_project_name = 'learn_programming_with_godot'

# Setting actions based on what OS is currently running
if OS == 'Windows':
    desired_extension = '.dll'
    command = 'copy'
    silently_override_file_switch = '/Y'
elif OS == 'Linux':
    desired_extension = '.dylib'
    command = 'cp'
else:
    pass # Not interested in working with Mac nowadays...

# This will give us back a list with all files inside
rust_files = os.listdir(rust_compiling_folder)

# Finding out target dynamic library
candidates = [file for file in rust_files if re.search(rf'\{desired_extension}$', file)]
library = candidates[0]

# The final path of the desired dynamic lib
rust_dll_path = rust_compiling_folder + '\\' + library

# Setting our base commands, flags and paths
subprocess_args = [command, rust_dll_path, godot_dir]

def replace_rust_dll():
    if OS == 'Windows':
        from rust.autocompiler import compile_rust

        # First gonna autocompile the Rust .dll
        compile_rust(rust_compiling_folder)

        subprocess_args.insert(1, silently_override_file_switch)
        process = subprocess.Popen(
            subprocess_args, 
            shell=True, 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        process_stderr = process.stderr.read(100)
        # //TODO: Still have to write the code to handle stderr
        
        if not process_stderr:
            process_stdout = process.stdout.read(100)
            execution_result = process_stdout.decode('UTF-8').strip()
            print('Coping files, wait...')
            print('\t' + execution_result)

        '''To avoid use PIPES on stdout and stderr...
        and in W10, prompt gets waiting if no PIPE de process... so...'''
        subprocess.call(['exit'], shell=True)
    else:
        pass
    
if __name__ == '__main__':
    replace_rust_dll()





