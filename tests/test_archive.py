from pathlib import Path

from file_watcher.archive import (
    archive_file,
    build_archive_destination,
    ensure_directory,
)


def test_ensure_directory(tmp_path):
    target = tmp_path / "processed"

    ensure_directory(str(target))

    assert target.exists()
    assert target.is_dir()


def test_build_archive_destination_new_file(tmp_path):
    archive_dir = tmp_path / "processed"
    archive_dir.mkdir()

    destination = build_archive_destination(
        file_path="sample.txt",
        archive_dir=str(archive_dir),
    )

    assert destination == str(archive_dir / "sample.txt")


def test_build_archive_destination_avoids_overwrite(tmp_path):
    archive_dir = tmp_path / "processed"
    archive_dir.mkdir()

    existing = archive_dir / "sample.txt"
    existing.write_text("existing", encoding="utf-8")

    destination = build_archive_destination(
        file_path="sample.txt",
        archive_dir=str(archive_dir),
    )

    assert destination == str(archive_dir / "sample-1.txt")


def test_archive_file_moves_file(tmp_path):
    inbox = tmp_path / "inbox"
    processed = tmp_path / "processed"
    inbox.mkdir()

    source = inbox / "sample.txt"
    source.write_text("RADAR archive test", encoding="utf-8")

    result = archive_file(
        file_path=str(source),
        archive_dir=str(processed),
    )

    assert result.status == "archived"
    assert not source.exists()
    assert Path(result.destination_path).exists()
    assert (
        Path(result.destination_path).read_text(encoding="utf-8")
        == "RADAR archive test"
    )


def test_archive_file_missing_source(tmp_path):
    processed = tmp_path / "processed"
    missing = tmp_path / "missing.txt"

    result = archive_file(
        file_path=str(missing),
        archive_dir=str(processed),
    )

    assert result.status == "missing"
    assert result.destination_path == ""
    assert "Source file not found" in result.message
