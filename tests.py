from functions.run_python import run_python_file

print("=====================================================")
print("SHOULD PRINT CACLULATOR INSTRUCTIONS")
print(run_python_file("calculator", "main.py"))
print("=====================================================")

print("=====================================================")
print("SHOULD RUN CACLULATOR INSTRUCTIONS")
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print("=====================================================")

print("=====================================================")
print(run_python_file("calculator", "tests.py"))
print("=====================================================")

print("=====================================================")
print("SHOULD RETURN ERROR")
print(run_python_file("calculator", "../main.py"))
print("=====================================================")

print("=====================================================")
print("SHOULD RETURN ERROR")
print(run_python_file("calculator", "nonexistent.py"))
print("=====================================================")
