import io

import pytest


def test_uses_heuristic_without_tiktoken(meter):
    assert meter.METHOD.startswith("heuristic")


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", 0),
        ("hello world", 2),
        ("internationalization", 4),  # long word: ceil(20 / 5)
        ("12345", 2),  # digits: ceil(5 / 3)
        ("a, b.", 4),
        ("x\n\ny", 3),  # a blank line costs one token
    ],
)
def test_heuristic_count(meter, text, expected):
    assert meter.count(text) == expected


def test_stats(meter):
    assert meter.stats("hello world") == (2, 2, 11)


def test_help(meter, capsys):
    assert meter.main([]) == 0
    assert "Usage" in capsys.readouterr().out


def test_text_mode(meter, capsys):
    assert meter.main(["--text", "hello", "world"]) == 0
    assert capsys.readouterr().out.startswith("tokens=2 words=2 chars=11")


def test_compare_two_files(meter, tmp_path, capsys):
    before = tmp_path / "before.txt"
    after = tmp_path / "after.txt"
    before.write_text("one two three four", encoding="utf-8")
    after.write_text("one", encoding="utf-8")

    assert meter.main([str(before), str(after)]) == 0
    out = capsys.readouterr().out
    assert "baseline" in out
    assert "+75% saved" in out
    assert "saved 3 tokens (75%), 4.0x smaller" in out


def test_empty_files_do_not_divide_by_zero(meter, tmp_path, capsys):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("", encoding="utf-8")
    b.write_text("", encoding="utf-8")

    assert meter.main([str(a), str(b)]) == 0
    assert "inf" in capsys.readouterr().out


def test_table_for_many_files(meter, tmp_path, capsys):
    paths = []
    for i, text in enumerate(["a b c d", "a b", "a"]):
        path = tmp_path / f"{i}.md"
        path.write_text(text, encoding="utf-8")
        paths.append(str(path))

    assert meter.main(paths) == 0
    out = capsys.readouterr().out
    assert "+50% saved" in out
    assert "+75% saved" in out
    assert "smaller" not in out  # summary line is only for two files


def test_reads_stdin(meter, monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("hello world"))
    assert meter.main(["-"]) == 0
    assert "     2" in capsys.readouterr().out
