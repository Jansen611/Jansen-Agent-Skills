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
1. **Check if yt-dlp is available** - try `which yt-dlp`
2. **If not found, reload shell environment** - run `source ~/.zshrc` and check again (**do NOT skip this**)
3. **If still not found, check common install paths** - look in Python bin directories
4. **Only install yt-dlp as last resort** - after Steps 1-3 all failed
5. **List available subtitles** - see what's actually available
6. **Try manual subtitles first** (`--write-sub`) - highest quality
7. **Fallback to auto-generated** (`--write-auto-sub`) - usually available
8. **Last resort: Whisper transcription** - if no subtitles exist (requires user confirmation)
9. **Confirm the download** and show the user where the file is saved
10. **Optionally clean up** the VTT format if the user wants plain text

## Environment Setup

### Check yt-dlp Installation

**IMPORTANT: Follow these steps IN ORDER. Do NOT install yt-dlp until all PATH resolution steps have been tried.**

#### Step 1: Check if yt-dlp is available

```bash
which yt-dlp || command -v yt-dlp
```

#### Step 2: If not found, reload shell environment first (macOS)

On macOS, the terminal session may not have the latest PATH. **Always try this before installing:**

```bash
source ~/.zshrc && which yt-dlp
```

#### Step 3: If still not found, check common install locations manually

```bash
ls /Library/Frameworks/Python.framework/Versions/*/bin/yt-dlp 2>/dev/null || ls ~/Library/Python/*/bin/yt-dlp 2>/dev/null
```

If found in one of these paths, add it to PATH for this session:

```bash
export PATH="<found_directory>:$PATH"
```

#### Step 4: Only install if Steps 2 and 3 both failed

```bash
pip3 install yt-dlp
```

After installation, reload PATH:

```bash
source ~/.zshrc && which yt-dlp
```

## Usage

### Check Available Subtitles

**ALWAYS do this first** before attempting to download:

```bash
yt-dlp --list-subs "YOUTUBE_URL"
```

### Get Video Title

Use the video title as the output filename:

```bash
TITLE=$(yt-dlp --get-title "YOUTUBE_URL" | sed 's/[/:*?"<>|]/-/g')
```

### Download Manual Subtitles (Preferred)

Highest quality, human-created:

```bash
yt-dlp --write-sub --sub-langs en --skip-download --output "$TITLE" "YOUTUBE_URL"
```

### Download Auto-Generated Subtitles (Fallback)

If manual subtitles aren't available:

```bash
yt-dlp --write-auto-sub --sub-langs en --skip-download --output "$TITLE" "YOUTUBE_URL"
```

Both commands create a `.vtt` file named `<videoTitle>.en.vtt`.

## Post-Processing

### Convert VTT to Timestamped Transcript

VTT auto-generated subtitles contain duplicate lines. Extract clean text with timestamps.

Use the VTT filename from the download step (e.g. `<videoTitle>.en.vtt`).

**The first line of the output file must be a markdown link to the source video:**

```bash
echo "Source: [$TITLE](YOUTUBE_URL)" > "$TITLE.md"
echo >> "$TITLE.md"
python3 -c "
import re

with open('$TITLE.en.vtt', 'r') as f:
    lines = f.readlines()

seen = set()
i = 0
while i < len(lines):
    line = lines[i].strip()
    m = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})', line)
    if m:
        start, end = m.group(1), m.group(2)
        def to_ms(t):
            h, mn, rest = t.split(':')
            s, ms = rest.split('.')
            return int(h)*3600000 + int(mn)*60000 + int(s)*1000 + int(ms)
        if to_ms(end) - to_ms(start) <= 20:
            if i + 1 < len(lines):
                text = lines[i + 1].strip()
                text = re.sub('<[^>]*>', '', text)
                text = text.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
                if text and text not in seen:
                    print(f'[{start}] {text}')
                    seen.add(text)
    i += 1
" >> "$TITLE.md"
```
```
Source: [The AI Native Engineer](https://www.youtube.com/watch?v=xxxxx)

[00:00:01.670] there is this emergence of kind of like
[00:00:03.990] a new I would say class of like engineer
[00:00:05.884] which is like the AI native engineer
```

### Complete Workflow

```bash
VIDEO_URL="YOUTUBE_URL"
OUTPUT_DIR="/Users/jansen/OpenWork"

cd "$OUTPUT_DIR"

# Get video title and sanitize for filename
TITLE=$(yt-dlp --get-title "$VIDEO_URL" | sed 's/[/:*?"<>|]/-/g')

# Download auto-generated English subtitles
yt-dlp --write-auto-sub --sub-langs en --skip-download --output "$TITLE" "$VIDEO_URL"

# Find the VTT file
VTT_FILE="$TITLE.en.vtt"

# Write source link as first line
echo "Source: [$TITLE]($VIDEO_URL)" > "$TITLE.md"
echo >> "$TITLE.md"

# Convert to timestamped transcript
python3 -c "
import re

with open('$VTT_FILE', 'r') as f:
    lines = f.readlines()

seen = set()
i = 0
while i < len(lines):
    line = lines[i].strip()
    m = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})', line)
    if m:
        start, end = m.group(1), m.group(2)
        def to_ms(t):
            h, mn, rest = t.split(':')
            s, ms = rest.split('.')
            return int(h)*3600000 + int(mn)*60000 + int(s)*1000 + int(ms)
        if to_ms(end) - to_ms(start) <= 20:
            if i + 1 < len(lines):
                text = lines[i + 1].strip()
                text = re.sub('<[^>]*>', '', text)
                text = text.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
                if text and text not in seen:
                    print(f'[{start}] {text}')
                    seen.add(text)
    i += 1
" >> "$TITLE.md"

echo "Transcription complete: $TITLE.md"
```

## Output Formats

- **VTT format** (`.vtt`): Raw subtitle file with word-level timing markup
- **Timestamped transcript** (`.md`): Clean text with line-level timestamps, e.g. `[00:01:23.456] text here`

## Common Issues

| Error | Solution |
|-------|----------|
| `command not found: yt-dlp` | Run `source ~/.zshrc` first, then check common Python bin paths |
| `No subtitles for requested languages` | Try `--write-auto-sub` instead of `--write-sub` |
| Python 3.9 deprecated | Upgrade to Python 3.10+ |
