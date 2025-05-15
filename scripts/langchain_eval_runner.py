from langchain.evaluation import load_evaluator

# LangChain Eval script
def run_eval():
    from langchain.evaluation.qa import QAEvalChain
    print("Running offline evaluation...")
    
    #TODO: Integrate with async offline evaluation
    
    return {"score": 0.88}


examples = [{"query": "Why was my Azure Storage account access denied?", "expected": "Access policy violation"}]
predictions = [{"result": "Check IAM role assignments"}]

evaluator = load_evaluator("criteria", criteria="factuality")
results = [evaluator.evaluate(example, prediction) for example, prediction in zip(examples, predictions)]
print("Evaluation results:", results)