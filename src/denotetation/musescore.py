"""MusicXML to PDF conversion through the MuseScore desktop CLI."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Iterable


class MuseScoreNotFoundError(RuntimeError):
    """Raised when MuseScore cannot be found on PATH or via MUSESCORE_PATH."""


DEFAULT_EXECUTABLE_NAMES = ("mscore", "musescore", "mscore4", "MuseScore4")
DEFAULT_MACOS_PATHS = (
    "/Applications/MuseScore 4.app/Contents/MacOS/mscore",
    "/Applications/MuseScore 4.app/Contents/MacOS/MuseScore 4",
    "/Applications/MuseScore.app/Contents/MacOS/mscore",
)


def find_musescore_executable(
    *,
    env_var: str = "MUSESCORE_PATH",
    executable_names: Iterable[str] = DEFAULT_EXECUTABLE_NAMES,
) -> Path:
    """Return the MuseScore executable path, or raise with setup guidance."""

    configured_path = os.environ.get(env_var)
    if configured_path:
        path = Path(configured_path).expanduser()
        if path.exists():
            return path

        raise MuseScoreNotFoundError(
            f"{env_var} points to '{path}', but that file does not exist."
        )

    for executable_name in executable_names:
        discovered_path = shutil.which(executable_name)
        if discovered_path:
            return Path(discovered_path)

    for macos_path in DEFAULT_MACOS_PATHS:
        path = Path(macos_path)
        if path.exists():
            return path

    names = ", ".join(executable_names)
    raise MuseScoreNotFoundError(
        "MuseScore was not found. Install MuseScore 4, add its CLI to PATH "
        f"as one of: {names}, or set MUSESCORE_PATH to the executable."
    )


def convert_musicxml_to_pdf(
    musicxml_path: str | Path,
    pdf_path: str | Path | None = None,
    *,
    musescore_path: str | Path | None = None,
) -> Path:
    """Convert a MusicXML file to PDF using MuseScore's command-line export."""

    input_path = Path(musicxml_path).expanduser().resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"MusicXML file not found: {input_path}")

    output_path = (
        Path(pdf_path).expanduser().resolve()
        if pdf_path is not None
        else input_path.with_suffix(".pdf")
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    executable = (
        Path(musescore_path).expanduser()
        if musescore_path is not None
        else find_musescore_executable()
    )

    subprocess.run(
        [str(executable), "-o", str(output_path), str(input_path)],
        check=True,
    )
    return output_path
