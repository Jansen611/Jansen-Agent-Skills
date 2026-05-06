---
name: markitdown-python
description: |
  Convert files to Markdown using Microsoft's MarkItDown tool.
  Supports PDF, Word, PowerPoint, Excel, images, audio, HTML, CSV, JSON, XML, ZIP, YouTube URLs, EPubs.

  Triggers when user mentions:
  - "convert to markdown" or "extract text"
  - "read this PDF/Word/Excel/PowerPoint"
  - "get markdown from file"
  - "summarize this document"
  - wants content extracted from a supported file format
---

# MarkItDown Skill

Convert various file formats to Markdown using [microsoft/markitdown](https://github.com/microsoft/markitdown).

## Pre-Check

Before converting any file, follow this check sequence:

### Step 1: Check if markitdown is already in PATH

```powershell
# Windows
Get-Command markitdown -ErrorAction SilentlyContinue
```

```bash
# macOS / Linux
which markitdown || command -v markitdown
```

**If found → skip to [Usage](#usage).**

### Step 2: Check if markitdown exists in ~/.venv

```powershell
# Windows
Test-Path "$env:USERPROFILE\.venv\Scripts\markitdown.exe"
```

```bash
# macOS / Linux
test -f ~/.venv/bin/markitdown && echo "found"
```

**If found → add to PATH for this session, then proceed to [Usage](#usage):**

```powershell
# Windows
$env:PATH = "$env:USERPROFILE\.venv\Scripts;$env:PATH"
```

```bash
# macOS / Linux
export PATH="$HOME/.venv/bin:$PATH"
```

### Step 3: Install (only if Steps 1 and 2 both failed)

```powershell
# Windows
python -m venv "$env:USERPROFILE\.venv"
& "$env:USERPROFILE\.venv\Scripts\pip" install "markitdown[all]"
$env:PATH = "$env:USERPROFILE\.venv\Scripts;$env:PATH"
```

```bash
# macOS / Linux
python3 -m venv ~/.venv
~/.venv/bin/pip install "markitdown[all]"
export PATH="$HOME/.venv/bin:$PATH"
```

---

## Installation Location

MarkItDown is installed in a dedicated venv at `~/.venv`:

| Platform      | Executable                        | pip                           |
|---------------|-----------------------------------|-------------------------------|
| Windows       | `~\.venv\Scripts\markitdown.exe`  | `~\.venv\Scripts\pip.exe`     |
| macOS / Linux | `~/.venv/bin/markitdown`          | `~/.venv/bin/pip`             |

## Supported Formats

- PDF
- PowerPoint (.pptx)
- Word (.docx)
- Excel (.xlsx, .xls)
- Images (EXIF metadata, OCR with plugin)
- Audio (EXIF metadata, speech transcription)
- HTML
- Text-based formats (CSV, JSON, XML)
- ZIP files (iterates over contents)
- YouTube URLs
- EPubs
- Outlook messages (.msg)

## Usage

### Command-Line (preferred for simple conversions)

```powershell
# Windows - convert a file to markdown (output to stdout)
markitdown "path\to\file.pdf"

# Save output to a file
markitdown "path\to\file.pdf" -o output.md
```

```bash
# macOS / Linux
markitdown path/to/file.pdf
markitdown path/to/file.pdf -o output.md
cat path/to/file.pdf | markitdown
```

### Python API (for advanced use cases)

```powershell
# Windows
& "$env:USERPROFILE\.venv\Scripts\python.exe" -c "
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert(r'path\to\file.pdf')
print(result.text_content)
"
```

```bash
# macOS / Linux
~/.venv/bin/python -c "
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert('path/to/file.pdf')
print(result.text_content)
"
```

### With LLM image descriptions

```python
from markitdown import MarkItDown
from openai import OpenAI
client = OpenAI()
md = MarkItDown(llm_client=client, llm_model='gpt-4o')
result = md.convert('path/to/image.jpg')
print(result.text_content)
```

### Azure Document Intelligence

```bash
markitdown "path/to/file.pdf" -d -e "<endpoint>"
```

## Notes

- The ffmpeg warning about pydub can be ignored unless audio transcription is needed
- For audio transcription, install ffmpeg and add to PATH
- Use `-o` flag to write directly to a file instead of stdout
- For large files, prefer writing to a file rather than capturing stdout
