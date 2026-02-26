with open('pyproject.toml','rb') as f:
    for i, line in enumerate(f, 1):
        print(i, repr(line))
