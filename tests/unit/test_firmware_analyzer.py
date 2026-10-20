from services.firmware_analyzer import analyze_firmware


def test_single_token(tmp_path):
    firmware_dir = tmp_path / "firmware"
    firmware_dir.mkdir()

    test_file = firmware_dir / "app.txt"
    test_file.write_text(
        "<Tkn123ABCDETkn>",
        encoding="utf-8"
    )

    csv_path = tmp_path / "report.csv"

    summary = analyze_firmware(
        str(firmware_dir),
        str(csv_path)
    )

    assert summary == {
        "<Tkn123ABCDETkn>": 1
    }

    assert csv_path.exists()

def test_multiple_occurrences(tmp_path):
    firmware_dir = tmp_path / "firmware"
    firmware_dir.mkdir()

    test_file = firmware_dir / "app.txt"

    test_file.write_text(
        """
        <Tkn123ABCDETkn>
        <Tkn123ABCDETkn>
        <Tkn123ABCDETkn>
        """,
        encoding="utf-8"
    )

    csv_path = tmp_path / "report.csv"

    summary = analyze_firmware(
        str(firmware_dir),
        str(csv_path)
    )

    assert summary == {
        "<Tkn123ABCDETkn>": 3
    }

def test_multiple_tokens(tmp_path):
    firmware_dir = tmp_path / "firmware"
    firmware_dir.mkdir()

    test_file = firmware_dir / "config.json"

    test_file.write_text(
        """
        <Tkn123ABCDETkn>
        <Tkn123ABCDETkn>
        <Tkn999XYZABTkn>
        """,
        encoding="utf-8"
    )

    csv_path = tmp_path / "report.csv"

    summary = analyze_firmware(
        str(firmware_dir),
        str(csv_path)
    )

    assert summary == {
        "<Tkn123ABCDETkn>": 2,
        "<Tkn999XYZABTkn>": 1
    }

def test_nested_directories(tmp_path):
    firmware_dir = tmp_path / "firmware"
    firmware_dir.mkdir()

    nested = firmware_dir / "nested"
    nested.mkdir()

    (firmware_dir / "app.txt").write_text(
        "<Tkn123ABCDETkn>",
        encoding="utf-8"
    )

    (nested / "data.txt").write_text(
        "<Tkn999XYZABTkn>",
        encoding="utf-8"
    )

    csv_path = tmp_path / "report.csv"

    summary = analyze_firmware(
        str(firmware_dir),
        str(csv_path)
    )

    assert summary == {
        "<Tkn123ABCDETkn>": 1,
        "<Tkn999XYZABTkn>": 1
    }

def test_no_tokens(tmp_path):
    firmware_dir = tmp_path / "firmware"
    firmware_dir.mkdir()

    test_file = firmware_dir / "app.txt"

    test_file.write_text(
        "hello world",
        encoding="utf-8"
    )

    csv_path = tmp_path / "report.csv"

    summary = analyze_firmware(
        str(firmware_dir),
        str(csv_path)
    )

    assert summary == {}

def test_csv_output(tmp_path):
    firmware_dir = tmp_path / "firmware"
    firmware_dir.mkdir()

    (firmware_dir / "app.txt").write_text(
        """
        <Tkn123ABCDETkn>
        <Tkn123ABCDETkn>
        """,
        encoding="utf-8"
    )

    csv_path = tmp_path / "report.csv"

    analyze_firmware(
        str(firmware_dir),
        str(csv_path)
    )

    csv_content = csv_path.read_text(
        encoding="utf-8"
    )

    assert "Path,Token,Occurrences" in csv_content
    assert "app.txt" in csv_content
    assert "<Tkn123ABCDETkn>" in csv_content
    assert "2" in csv_content