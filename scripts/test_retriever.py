import sys
sys.path.append(r'c:/Users/pratiksha daphal/Desktop/agentic-customer-decision-platform')

from app.rag import retriever

print('retriever module loaded successfully')
print('retrieve_insights example:', retriever.retrieve_insights('test'))
