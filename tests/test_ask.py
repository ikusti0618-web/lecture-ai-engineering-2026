from types import SimpleNamespace

from app import ask as ask_module


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        text="answer",
        usage_metadata=SimpleNamespace(
            prompt_token_count=12,
            candidates_token_count=5,
        ),
    )

    class FakeClient:
        def __init__(self, api_key):
            self.models = SimpleNamespace(
                generate_content=lambda **kwargs: response
            )

    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    assert ask_module.ask("question") == "answer"
    assert capsys.readouterr().out == "[トークン数] 入力: 12 / 出力: 5\n"


def test_ask_reports_missing_usage_metadata(monkeypatch, capsys):
    response = SimpleNamespace(text="answer", usage_metadata=None)

    class FakeClient:
        def __init__(self, api_key):
            self.models = SimpleNamespace(
                generate_content=lambda **kwargs: response
            )

    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    assert ask_module.ask("question") == "answer"
    assert capsys.readouterr().out == "[トークン数] 使用量情報はありません\n"
