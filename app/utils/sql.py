def load_sql(filename: str) -> str:
    path = f"sql/{filename}"
    with open(path) as f:
        return f.read()
