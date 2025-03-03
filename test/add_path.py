import sys
import os

def add_path_f():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    module_dir = os.path.join(current_dir, '..', 'app')
    sys.path.insert(0, module_dir)