import os
import inspect
import importlib

def generate_test_file(module_name, output_dir="my_autopybot_tests"):
    module = importlib.import_module(module_name)
    functions = [f for f in dir(module) if callable(getattr(module, f)) and not f.startswith("_")]
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    test_file_path = os.path.join(output_dir, f"test_{module_name.split('.')[-1]}.py")
    with open(test_file_path, "w") as test_file:
        test_file.write("import pytest\n")
        test_file.write(f"from {module_name} import *\n\n")
        for func in functions:
            test_file.write(f"def test_{func}():\n")
            test_file.write(f"    # TODO: Write test for {func}\n")
            test_file.write(f"    assert {func}() == 'expected_result'\n\n")
    print(f"Test file generated: {test_file_path}")

# Example usage
generate_test_file("AutoPybot.my_autopybot")