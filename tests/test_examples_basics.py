"""
Tests for the course examples 1-11: basics, files, CSV/JSON, HTTP requests, HTML parsing and AI APIs.

Each example gets a happy-path test (normal input works) and, where it makes sense,
an unhappy-path test (bad input, missing file, server error) that checks the right error happens.
"""
import json

import pytest

from conftest import FakeResponse


# ---------- example_1_review.py ----------

@pytest.fixture
def no_sleep(monkeypatch):
    """example_1 counts down with sleep(1) - skip the waiting in tests."""
    monkeypatch.setattr("time.sleep", lambda seconds: None)


@pytest.mark.parametrize("temperature, expected", [
    ("-5", "freezing"),
    ("0", "freezing"),
    ("25", "alright"),
    ("100", "boiling"),
])
def test_example_1_temperature_messages(run_script, no_sleep, capsys, temperature, expected):
    namespace = run_script("examples/example_1_review.py", inputs=[temperature])
    output = capsys.readouterr().out
    assert expected in output
    assert "Lift off!" in output
    assert namespace["populous_countries"][2] == "United States"
    assert namespace["squared"](12) == 144


def test_example_1_non_number_input_raises(run_script, no_sleep):
    with pytest.raises(ValueError):
        run_script("examples/example_1_review.py", inputs=["warm"])


# ---------- example_2_dictionaries.py ----------

def test_example_2_dictionary_operations(run_script):
    namespace = run_script("examples/example_2_dictionaries.py")
    capitals = namespace["canadian_capitals"]
    assert "AB" not in capitals          # Deleted
    assert capitals["NU"] == "Bob"       # Updated
    assert capitals["XX"] == "New"       # Added
    assert [book["title"] for book in namespace["books"]] == ["1984", "Jane Eyre", "To Kill a Mockingbird"]


def test_example_2_missing_keys(run_script):
    capitals = run_script("examples/example_2_dictionaries.py")["canadian_capitals"]
    assert capitals.get("AA") is None
    assert capitals.get("AA", "N/A") == "N/A"
    with pytest.raises(KeyError):
        capitals["AB"]  # Square brackets raise for a missing key


# ---------- example_3_exceptions.py / example_3b_advanced_exceptions.py ----------

def test_example_3_division_by_zero_is_handled(run_script, capsys):
    run_script("examples/example_3_exceptions.py")
    assert "Inverse of 0 is not defined" in capsys.readouterr().out


def test_example_3b_valid_number(run_script, capsys):
    # The script deliberately ends by raising its own MyCustomError
    with pytest.raises(Exception) as error:
        run_script("examples/example_3b_advanced_exceptions.py", inputs=["4"])
    assert type(error.value).__name__ == "MyCustomError"
    output = capsys.readouterr().out
    assert "Inverse of 4 is 0.25" in output
    assert "Everything worked" in output
    assert "This always happens" in output


@pytest.mark.parametrize("bad_input", ["0", "abc"])
def test_example_3b_bad_input_is_handled(run_script, capsys, bad_input):
    with pytest.raises(Exception) as error:
        run_script("examples/example_3b_advanced_exceptions.py", inputs=[bad_input])
    assert type(error.value).__name__ == "MyCustomError"  # Did not crash earlier with ZeroDivisionError/ValueError
    assert f"Inverse of {bad_input} is not defined" in capsys.readouterr().out


# ---------- example_4_read_file.py ----------

def test_example_4_sums_numbers(run_script, capsys):
    namespace = run_script("examples/example_4_read_file.py", files={"data/input.txt": "1\n2\n-3\n10\n"})
    assert namespace["sum_"] == 10
    assert "The sum is 10" in capsys.readouterr().out


def test_example_4_real_data_file(run_script, workdir):
    namespace = run_script("examples/example_4_read_file.py")
    numbers = (workdir / "data" / "input.txt").read_text().split()
    assert namespace["sum_"] == sum(int(n) for n in numbers)


def test_example_4_non_number_line_raises(run_script):
    with pytest.raises(ValueError):
        run_script("examples/example_4_read_file.py", files={"data/input.txt": "1\ntwo\n3\n"})


def test_example_4_missing_file_raises(run_script):
    with pytest.raises(FileNotFoundError):
        run_script("examples/example_4_read_file.py", remove=["data/input.txt"])


# ---------- example_5_write_file.py ----------

def test_example_5_writes_poem(run_script, workdir):
    run_script("examples/example_5_write_file.py")
    lines = (workdir / "data" / "output.txt").read_text(encoding="utf-8").splitlines()
    assert lines == ["I have eaten", "the plums", "that were in", "the icebox"]


def test_example_5_missing_folder_raises(run_script):
    with pytest.raises(FileNotFoundError):  # open(..., "w") creates files, not folders
        run_script("examples/example_5_write_file.py", remove=["data"])


# ---------- example_6_csv_files.py ----------

def test_example_6_prints_capitals(run_script, capsys):
    run_script("examples/example_6_csv_files.py", files={"data/input.csv": "Country,Capital\nCanada,Ottawa\nChile,Santiago\n"})
    output = capsys.readouterr().out
    assert "The capital of Canada is Ottawa" in output
    assert "The capital of Chile is Santiago" in output


def test_example_6_missing_column_raises(run_script):
    with pytest.raises(KeyError):
        run_script("examples/example_6_csv_files.py", files={"data/input.csv": "Country,City\nCanada,Toronto\n"})


# ---------- example_7_json.py ----------

def test_example_7_csv_to_json_round_trip(run_script, workdir):
    namespace = run_script("examples/example_7_json.py", files={"data/input.csv": "Country,Capital\nPeru,Lima\n"})
    saved = json.loads((workdir / "data" / "output.json").read_text(encoding="utf-8"))
    assert saved == [{"Country": "Peru", "Capital": "Lima"}]
    assert namespace["data"] == saved


def test_example_7_missing_csv_raises(run_script):
    with pytest.raises(FileNotFoundError):
        run_script("examples/example_7_json.py", remove=["data/input.csv"])


# ---------- example_8_requests.py ----------

def test_example_8_saves_page(run_script, workdir, monkeypatch):
    calls = []

    def fake_get(url, **kwargs):
        calls.append((url, kwargs))
        return FakeResponse(text="<html>Chapter 13</html>")

    monkeypatch.setattr("requests.get", fake_get)
    run_script("examples/example_8_requests.py")

    assert (workdir / "data" / "request.html").read_text(encoding="utf-8") == "<html>Chapter 13</html>"
    url, kwargs = calls[0]
    assert kwargs["params"] == {"param1": 123, "param2": 456}
    assert "timeout" in kwargs


def test_example_8_http_error_raises_and_saves_nothing(run_script, workdir, monkeypatch):
    import requests
    monkeypatch.setattr("requests.get", lambda url, **kwargs: FakeResponse(status_code=404))
    with pytest.raises(requests.HTTPError):
        run_script("examples/example_8_requests.py")
    assert not (workdir / "data" / "request.html").exists()


# ---------- example_9_beautiful_soup.py ----------

def test_example_9_finds_elements(run_script):
    pytest.importorskip("bs4")
    ns = run_script("examples/example_9_beautiful_soup.py")
    assert len(ns["a"]) == 3                       # All <a> tags
    assert len(ns["c"]) == 3                       # class_="sister"
    assert ns["h"]["id"] == "link1"
    assert ns["k"] == "Elsie"
    assert ns["m"] == "http://example.com/elsie"


def test_example_9_find_returns_none_when_missing(run_script):
    pytest.importorskip("bs4")
    soup = run_script("examples/example_9_beautiful_soup.py")["soup"]
    assert soup.find("a", id="does-not-exist") is None
    assert soup.find_all("table") == []
    assert soup.a.get("missing-attribute") is None  # .get() is safe...
    with pytest.raises(KeyError):
        soup.a["missing-attribute"]                 # ...square brackets are not


def test_example_9_missing_file_raises(run_script):
    pytest.importorskip("bs4")
    with pytest.raises(FileNotFoundError):
        run_script("examples/example_9_beautiful_soup.py", remove=["data/sample.html"])


# ---------- example_10_ollama.py ----------

def test_example_10_prints_model_replies(run_script, monkeypatch, capsys):
    ollama = pytest.importorskip("ollama")
    monkeypatch.setattr(ollama, "generate", lambda **kw: ollama.GenerateResponse(model=kw["model"], response="Hi there"))
    monkeypatch.setattr(ollama, "chat", lambda **kw: ollama.ChatResponse(
        model=kw["model"], message=ollama.Message(role="assistant", content="print('hello world')")))

    run_script("examples/example_10_ollama.py")
    output = capsys.readouterr().out
    assert "Hi there" in output
    assert output.count("print('hello world')") == 2  # Accessed by key AND by attribute


def test_example_10_ollama_not_running_raises(run_script, monkeypatch):
    ollama = pytest.importorskip("ollama")

    def not_running(**kwargs):
        raise ConnectionError("Failed to connect to Ollama")

    monkeypatch.setattr(ollama, "generate", not_running)
    with pytest.raises(ConnectionError):
        run_script("examples/example_10_ollama.py")


# ---------- example_11_hf_api_requests.py / example_11_hf_api_library.py ----------

HF_FILES = ["examples/example_11_hf_api_requests.py", "examples/example_11_hf_api_library.py"]


def _load_hf(load_module, path, **kwargs):
    if "library" in path:
        pytest.importorskip("huggingface_hub")
    return load_module(path, **kwargs)


@pytest.mark.parametrize("path", HF_FILES)
def test_example_11_load_api_key(load_module, path):
    module = _load_hf(load_module, path, files={"secrets/hf.txt": "  hf_secret123\n"})
    assert module.load_api_key() == "hf_secret123"  # Whitespace stripped


@pytest.mark.parametrize("path", HF_FILES)
def test_example_11_missing_key_file_raises(load_module, path):
    module = _load_hf(load_module, path)
    with pytest.raises(FileNotFoundError, match="secrets/hf.txt"):
        module.load_api_key()


@pytest.mark.parametrize("path", HF_FILES)
def test_example_11_empty_key_file_raises(load_module, path):
    module = _load_hf(load_module, path, files={"secrets/hf.txt": "\n"})
    with pytest.raises(ValueError, match="empty"):
        module.load_api_key()


def test_example_11_requests_returns_reply(load_module, monkeypatch):
    module = load_module("examples/example_11_hf_api_requests.py")
    sent = {}

    def fake_post(url, headers, json, timeout):
        sent.update(headers=headers, json=json)
        return FakeResponse(json_data={"choices": [{"message": {"content": "Hello back!"}}]})

    monkeypatch.setattr(module.requests, "post", fake_post)
    assert module.query_huggingface_ai("Hello", api_key="abc") == "Hello back!"
    assert sent["headers"]["Authorization"] == "Bearer abc"
    assert sent["json"]["messages"][0]["content"] == "Hello"


def test_example_11_requests_bad_token_raises(load_module, monkeypatch):
    import requests
    module = load_module("examples/example_11_hf_api_requests.py")
    monkeypatch.setattr(module.requests, "post", lambda *a, **kw: FakeResponse(status_code=401))
    with pytest.raises(requests.HTTPError):
        module.query_huggingface_ai("Hello", api_key="wrong")


def test_example_11_library_returns_reply(load_module, monkeypatch):
    module = _load_hf(load_module, "examples/example_11_hf_api_library.py")

    class FakeClient:
        def __init__(self, api_key):
            self.chat = self
            self.completions = self

        def create(self, model, messages):
            from types import SimpleNamespace
            message = SimpleNamespace(content=f"echo: {messages[0]['content']}")
            return SimpleNamespace(choices=[SimpleNamespace(message=message)])

    monkeypatch.setattr(module, "InferenceClient", FakeClient)
    assert module.query_huggingface_ai("Hi", api_key="abc") == "echo: Hi"
