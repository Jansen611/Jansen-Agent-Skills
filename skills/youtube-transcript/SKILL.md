---
name: youtube-transcript
description: Download YouTube video transcripts when user provides a YouTube URL or asks to download/get/fetch a transcript from YouTube. Also use when user wants to transcribe or get captions/subtitles from a YouTube video.
allowed-tools: Bash,Read,Write
---

# YouTube Transcript Downloader

This skill helps download transcripts (subtitles/captions) from YouTube videos using yt-dlp.

## When to Use This Skill

Activate this skill when the user:
- Provides a YouTube URL and wants the transcript
- Asks to "download transcript from YouTube"
- Wants to "get captions" or "get subtitles" from a video
- Asks to "transcribe a YouTube video"
- Needs text content from a YouTube video

## How It Works

### Priority Order:
1. **Check if yt-dlp is installed** - install if needed
2. **List available subtitles** - see what's actually available
3. **Try manual subtitles first** (`--write-sub`) - highest quality
4. **Fallback to auto-generated** (`--write-auto-sub`) - usually available
5. **Last resort: Whisper transcription** - if no subtitles exist (requires user confirmation)
6. **Confirm the download** and show the user where the file is saved
7. **Optionally clean up** the VTT format if the user wants plain text

## Environment Setup

### Check yt-dlp Installation

```bash
which yt-dlp || command -v yt-dlp
```

### If Not Installed

```bash
pip3 install yt-dlp
```

### PATH Issue on macOS

If yt-dlp is installed but not found, add Python 3.13 path to ~/.zshrc:
```bash
echo 'export PATH="/Library/Frameworks/Python.framework/Versions/3.13/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### SSL Certificate Issue (macOS)

If you get `CERTIFICATE_VERIFY_FAILED` error, run:
```bash
/Applications/Python\ 3.13/Install\ Certificates.command
```

## Usage

### Check Available Subtitles

**ALWAYS do this first** before attempting to download:

```bash
yt-dlp --list-subs "YOUTUBE_URL"
```

### Download Manual Subtitles (Preferred)

Highest quality, human-created:

```bash
yt-dlp --write-sub --sub-langs en --skip-download --output "transcript" "YOUTUBE_URL"
```

### Download Auto-Generated Subtitles (Fallback)

If manual subtitles aren't available:

```bash
yt-dlp --write-auto-sub --sub-langs en --skip-download --output "transcript" "YOUTUBE_URL"
```

Both commands create a `.vtt` file (WebVTT subtitle format).

### Download to Specific Directory

```bash
yt-dlp --write-auto-sub --sub-langs en --skip-download --output "/path/to/output" "YOUTUBE_URL"
```

## Post-Processing

### Convert VTT to Plain Text

VTT files contain duplicate lines. Convert to clean text:

```bash
python3 -c "
import sys, re
seen = set()
with open('transcript.en.vtt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and '-->' not in line:
            clean = re.sub('<[^>]*>', '', line)
            clean = clean.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
            if clean and clean not in seen:
                print(clean)
                seen.add(clean)
" > transcript.txt
```

### Complete Workflow

```bash
VIDEO_URL="YOUTUBE_URL"
OUTPUT_DIR="/Users/jansen/OpenWork"

# Download auto-generated English subtitles
cd "$OUTPUT_DIR"
yt-dlp --write-auto-sub --sub-langs en --skip-download --output "transcript" "$VIDEO_URL"

# Find the VTT file
VTT_FILE=$(ls transcript.*.vtt | head -n 1)

# Convert to plain text with deduplication
python3 -c "
import sys, re
seen = set()
with open('$VTT_FILE', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and '-->' not in line:
            clean = re.sub('<[^>]*>', '', line)
            clean = clean.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
            if clean and clean not in seen:
                print(clean)
                seen.add(clean)
" > transcript.txt

echo "Transcription complete: transcript.txt"
```

## Output Formats

- **VTT format** (`.vtt`): Includes timestamps and formatting
- **Plain text** (`.txt`): Just the text content, good for reading or analysis

## Common Issues

| Error | Solution |
|-------|----------|
| `command not found: yt-dlp` | Add Python 3.13 to PATH, or run with full path |
| `CERTIFICATE_VERIFY_FAILED` | Run Install Certificates.command |
| `No subtitles for requested languages` | Try `--write-auto-sub` instead of `--write-sub` |
| Python 3.9 deprecated | Upgrade to Python 3.10+ |
