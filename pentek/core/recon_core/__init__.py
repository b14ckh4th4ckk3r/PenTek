import os
import importlib
import inspect

# Get the current module name dynamically
module_name = __name__

# Get the directory of this module
current_dir = os.path.dirname(os.path.abspath(__file__))

# Iterate over all Python files in the module directory
for filename in os.listdir(current_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_file = filename[:-3]  # Remove .py extension
        module = importlib.import_module(f".{module_file}", package=module_name)
        
        # Import all functions from the file
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            globals()[name] = obj  # Add function to module's global scope
