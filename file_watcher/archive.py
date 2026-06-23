import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ArchiveResult:
    source_path: str
    destination_path: str
    status: str
    message: str


def ensure_directory(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def build_archive_destination(
    file_path: str,
    archive_dir: str,
) -> str:
    source = Path(file_path)
    destination_dir = Path(archive_dir)
    destination = destination_dir / source.name

    if not destination.exists():
        return str(destination)

    stem = source.stem
    suffix = source.suffix

    counter = 1

    while True:
        candidate = destination_dir / f"{stem}-{counter}{suffix}"

        if not candidate.exists():
            return str(candidate)

        counter += 1


def archive_file(
    file_path: str,
    archive_dir: str,
) -> ArchiveResult:
    source = Path(file_path)

    if not source.exists():
        return ArchiveResult(
            source_path=str(source),
            destination_path="",
            status="missing",
            message=f"Source file not found: {source}",
        )

    ensure_directory(archive_dir)

    destination = build_archive_destination(
        file_path=str(source),
        archive_dir=archive_dir,
    )

    shutil.move(str(source), destination)

    return ArchiveResult(
        source_path=str(source),
        destination_path=destination,
        status="archived",
        message=f"Archived file to: {destination}",
    )
