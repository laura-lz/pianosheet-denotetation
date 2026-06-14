from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from denotetation.musescore import (
    MuseScoreNotFoundError,
    convert_musicxml_to_pdf,
    find_musescore_executable,
)


def test_find_musescore_executable_uses_env_path(tmp_path, monkeypatch):
    executable = tmp_path / "mscore"
    executable.touch()
    monkeypatch.setenv("MUSESCORE_PATH", str(executable))

    assert find_musescore_executable() == executable


def test_find_musescore_executable_rejects_missing_env_path(monkeypatch):
    monkeypatch.setenv("MUSESCORE_PATH", "/missing/mscore")

    with pytest.raises(MuseScoreNotFoundError, match="does not exist"):
        find_musescore_executable()


def test_convert_musicxml_to_pdf_runs_musescore_command(tmp_path):
    musicxml = tmp_path / "song.musicxml"
    musicxml.write_text("<score-partwise version='4.0' />")
    pdf = tmp_path / "song.pdf"

    with patch("denotetation.musescore.subprocess.run") as run:
        result = convert_musicxml_to_pdf(
            musicxml,
            pdf,
            musescore_path=Path("/opt/MuseScore/mscore"),
        )

    assert result == pdf
    run.assert_called_once_with(
        ["/opt/MuseScore/mscore", "-o", str(pdf), str(musicxml)],
        check=True,
    )
