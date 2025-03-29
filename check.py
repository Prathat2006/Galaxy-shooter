import os

def get_terminal_size():
     size = os.get_terminal_size()
     print(f"Terminal size: {size.columns} columns, {size.lines} lines")
     return size.columns, size.lines
get_terminal_size()