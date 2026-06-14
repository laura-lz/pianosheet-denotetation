# pianosheet-denotetation

Convert audio recordings into piano sheet music.

This project is starting with the notation export layer: converting generated
MusicXML into a PDF score through MuseScore.

## Setup

Install MuseScore 4 from <https://musescore.org/>. The converter looks for the
MuseScore CLI in this order:

1. `MUSESCORE_PATH`
2. `mscore`, `musescore`, `mscore4`, or `MuseScore4` on `PATH`
3. Common macOS application paths under `/Applications`

If MuseScore is not on your `PATH`, set the environment variable explicitly:

```bash
export MUSESCORE_PATH="/Applications/MuseScore 4.app/Contents/MacOS/mscore"
```

## MusicXML to PDF

```python
from denotetation.musescore import convert_musicxml_to_pdf

convert_musicxml_to_pdf("build/song.musicxml", "build/song.pdf")
```

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```
