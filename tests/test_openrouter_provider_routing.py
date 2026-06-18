import pytest

from tradingagents.llm_clients.factory import create_llm_client
from tradingagents.llm_clients.openai_client import _openrouter_extra_body_from_env


@pytest.mark.unit
def test_openrouter_provider_controls_from_env(monkeypatch):
    monkeypatch.setenv("TRADINGAGENTS_OPENROUTER_PROVIDER_ORDER", "baidu/fp8, wafer/fp4")
    monkeypatch.setenv("TRADINGAGENTS_OPENROUTER_ALLOW_FALLBACKS", "false")
    monkeypatch.setenv("TRADINGAGENTS_OPENROUTER_REQUIRE_PARAMETERS", "true")
    monkeypatch.setenv("TRADINGAGENTS_OPENROUTER_DATA_COLLECTION", "deny")
    monkeypatch.setenv("TRADINGAGENTS_OPENROUTER_MAX_PROMPT_PRICE", "0.10")
    monkeypatch.setenv("TRADINGAGENTS_OPENROUTER_MAX_COMPLETION_PRICE", "0.20")
    monkeypatch.setenv("TRADINGAGENTS_OPENROUTER_SESSION_ID", "scbam-etf-mvp")

    extra_body = _openrouter_extra_body_from_env()

    assert extra_body == {
        "provider": {
            "order": ["baidu/fp8", "wafer/fp4"],
            "allow_fallbacks": False,
            "require_parameters": True,
            "data_collection": "deny",
            "max_price": {"prompt": 0.10, "completion": 0.20},
        },
        "session_id": "scbam-etf-mvp",
    }


@pytest.mark.unit
def test_openrouter_client_receives_extra_body(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test")
    monkeypatch.setenv("TRADINGAGENTS_OPENROUTER_PROVIDER_ORDER", "baidu/fp8,wafer/fp4")
    monkeypatch.setenv("TRADINGAGENTS_OPENROUTER_ALLOW_FALLBACKS", "false")
    monkeypatch.setenv("TRADINGAGENTS_OPENROUTER_SESSION_ID", "scbam-etf-mvp")

    llm = create_llm_client(
        provider="openrouter",
        model="deepseek/deepseek-v4-flash",
    ).get_llm()

    assert llm.extra_body["provider"]["order"] == ["baidu/fp8", "wafer/fp4"]
    assert llm.extra_body["provider"]["allow_fallbacks"] is False
    assert llm.extra_body["session_id"] == "scbam-etf-mvp"


@pytest.mark.unit
def test_openrouter_env_does_not_affect_other_providers(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test")
    monkeypatch.setenv("TRADINGAGENTS_OPENROUTER_PROVIDER_ORDER", "baidu/fp8,wafer/fp4")

    llm = create_llm_client(provider="deepseek", model="deepseek-v4-flash").get_llm()

    assert not getattr(llm, "extra_body", None)


@pytest.mark.unit
def test_openrouter_extra_body_merges_with_caller_extra_body(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test")
    monkeypatch.setenv("TRADINGAGENTS_OPENROUTER_ALLOW_FALLBACKS", "false")

    llm = create_llm_client(
        provider="openrouter",
        model="deepseek/deepseek-v4-flash",
        extra_body={"provider": {"sort": "price"}, "metadata": {"source": "test"}},
    ).get_llm()

    assert llm.extra_body["provider"]["sort"] == "price"
    assert llm.extra_body["provider"]["allow_fallbacks"] is False
    assert llm.extra_body["metadata"] == {"source": "test"}
