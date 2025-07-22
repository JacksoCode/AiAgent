from functions.get_files_content import get_file_content

print("=====================================================")
print("Result for lorum.txt file:")
print(get_file_content("calculator", "lorum.txt"))
print("=====================================================")

print("=====================================================")
print("Result for main.py file:")
print(get_file_content("calculator", "main.py"))
print("=====================================================")

print("=====================================================")
print("Result for 'pkg/calculator.py' file:")
print(get_file_content("calculator", "pkg/calculator.py"))
print("=====================================================")

print("=====================================================")
print("Result for '/bin/cat' file:")
print(get_file_content("calculator", "/bin/cat"))
print("=====================================================")

print("=====================================================")
print("Result for 'pkg/does_not_exist.py' file:")
print(get_file_content("calculator", "pkg/does_not_exist.py"))
print("=====================================================")
