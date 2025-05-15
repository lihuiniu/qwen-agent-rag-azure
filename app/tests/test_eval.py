def test_eval_score():
    from scripts.langchain_eval_runner import run_eval
    assert run_eval()["score"] > 0.8