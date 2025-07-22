from get_files_info import get_files_info

print("Expecting:") 
print("Result for current directory:")
print("R- main.py: file_size=576 bytes, is_dir=False")
print("R- tests.py: file_size=1343 bytes, is_dir=False")
print("R- pkg: file_size=92 bytes, is_dir=True")
print("R- lorem.txt: file_size=28 bytes, is_dir=False")

print("Actual:")
print("Result for current directory:")
print(get_files_info("calculator", "."))
