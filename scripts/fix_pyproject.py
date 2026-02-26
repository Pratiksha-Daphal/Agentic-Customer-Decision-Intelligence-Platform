content="""[project]
name = "agentic-customer-decision-platform"
version = "0.1.0"
description = "Agentic AI platform for customer decision intelligence"
requires-python = ">=3.10"

dependencies = [
    "fastapi",
    "uvicorn",
    "sqlalchemy",
    "psycopg2-binary",
    "pydantic",
    "python-dotenv",
    # retrieval-augmented generation packages
    "faiss-cpu",
    "sentence-transformers",
]
"""
with open('pyproject.toml','w') as f:
    f.write(content)
print('pyproject overwritten')
