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
2. **If not found, reload shell environment** - `source ~/.zshrc && which yt-dlp` (macOS terminal may not auto-load rc files)
3. **If still not found, check ~/.venv** - try `test -f ~/.venv/bin/yt-dlp`
4. **If found in ~/.venv, add to PATH** - `export PATH="$HOME/.venv/bin:$PATH"`
5. **Only install yt-dlp as last resort** - after Steps 1-4 all failed
6. **List available subtitles** - see what's actually available
7. **Try manual subtitles first** (`--write-sub`) - highest quality
8. **Fallback to auto-generated** (`--write-auto-sub`) - usually available
9. **Last resort: Whisper transcription** - if no subtitles exist (requires user confirmation)
10. **Confirm the download** and show the user where the file is saved
11. **Optionally clean up** the VTT format if the user wants plain text

## Environment Setup

### Check yt-dlp Installation

**IMPORTANT: Follow these steps IN ORDER. Do NOT install yt-dlp until all PATH resolution steps have been tried.**

#### Step 1: Check if yt-dlp is in PATH

```bash
which yt-dlp || command -v yt-dlp
```

If found → skip to [Usage](#usage).

#### Step 2: Reload shell environment and re-check (macOS)

On macOS, VS Code's terminal may not auto-load `~/.zshrc`, so environment variables (like PATH additions for `~/.venv`) are missing. **Always try this before checking other paths:**

```bash
source ~/.zshrc && which yt-dlp
```

If found → skip to [Usage](#usage).

#### Step 3: Check if yt-dlp exists in ~/.venv

```bash
test -f ~/.venv/bin/yt-dlp && echo "found"
```

If found → add to PATH for this session, then proceed to [Usage](#usage):

```bash
export PATH="$HOME/.venv/bin:$PATH"
```

#### Step 4: Only install if Steps 1-3 all failed

Install yt-dlp into the shared virtual environment:

```bash
~/.venv/bin/pip install yt-dlp
```

Then add to PATH:

```bash
export PATH="$HOME/.venv/bin:$PATH"
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

### Derive Snake Case Filename

Convert the title to snake_case, removing special characters (`.` `,` `'` etc.), and prefix with `Youtube-Transcript-`:

```bash
SNAKE_TITLE=$(echo "$TITLE" | sed "s/[^a-zA-Z0-9 ]//g" | sed 's/  */ /g' | sed 's/ /_/g')
OUTPUT_MD="Youtube-Transcript-$SNAKE_TITLE.md"
```

Example: `From Writing Code to Managing Agents. Most Engineers Aren't Ready - Stanford University, Mihail Eric` becomes `Youtube-Transcript-From_Writing_Code_to_Managing_Agents_Most_Engineers_Arent_Ready__Stanford_University_Mihail_Eric.md`

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
echo "Source: [$TITLE](YOUTUBE_URL)" > "$OUTPUT_MD"
echo >> "$OUTPUT_MD"
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
" >> "$OUTPUT_MD"
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

# Derive snake_case output filename with Youtube-Transcript- prefix
SNAKE_TITLE=$(echo "$TITLE" | sed "s/[^a-zA-Z0-9 ]//g" | sed 's/  */ /g' | sed 's/ /_/g')
OUTPUT_MD="Youtube-Transcript-$SNAKE_TITLE.md"

# Download auto-generated English subtitles
yt-dlp --write-auto-sub --sub-langs en --skip-download --output "$TITLE" "$VIDEO_URL"

# Find the VTT file
VTT_FILE="$TITLE.en.vtt"

# Write source link as first line
echo "Source: [$TITLE]($VIDEO_URL)" > "$OUTPUT_MD"
echo >> "$OUTPUT_MD"

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
" >> "$OUTPUT_MD"

echo "Transcription complete: $OUTPUT_MD"
```

## Output Formats

- **VTT format** (`.vtt`): Raw subtitle file with word-level timing markup
- **Timestamped transcript** (`.md`): Named `Youtube-Transcript-<Snake_Case_Title>.md`. Clean text with line-level timestamps, e.g. `[00:01:23.456] text here`

## Common Issues

| Error | Solution |
|-------|----------|
| `command not found: yt-dlp` | Run `source ~/.zshrc` first, then check common Python bin paths |
| `No subtitles for requested languages` | Try `--write-auto-sub` instead of `--write-sub` |
| Python 3.9 deprecated | Upgrade to Python 3.10+ |
