---
name: himalaya-email-rust
description: |
  CLI email client for terminal. Manage emails via shell commands in a stateless way.
  Supports IMAP, SMTP, Maildir, Notmuch, Sendmail, PGP encryption, OAuth 2.0.
  Outputs JSON for easy parsing by scripts and AI agents.

  Triggers when user mentions:
  - "check email" or "check inbox"
  - "read my emails" or "list emails"
  - "send email" or "compose email"
  - "reply to email" or "forward email"
  - "delete email" or "move email"
  - "search emails" or "filter emails"
  - "himalaya" explicitly
  - wants to manage email accounts from terminal
allowed-tools: Bash
---

# Himalaya Email CLI Skill

Manage emails from the terminal using [pimalaya/himalaya](https://github.com/pimalaya/himalaya), a stateless CLI email client written in Rust.

## Design Philosophy

Himalaya is a **CLI** (not a TUI). There is no event loop — each command runs and exits immediately, making it ideal for AI agent use:

```bash
himalaya envelope list --page 1 --output json
# → exits, returns JSON
```

Always prefer `--output json` when parsing results programmatically.

## Pre-Check

### Step 1: Check if himalaya is available

```bash
which himalaya || command -v himalaya
```

If found → skip to [Usage](#usage).

### Step 2: Check in ~/.cargo/bin (installed via cargo)

```bash
test -f ~/.cargo/bin/himalaya && echo "found"
```

If found → add to PATH:

```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

### Step 3: Install via Cargo (only if Steps 1-2 both failed)

```bash
cargo install himalaya --locked --features oauth2,keyring
```

OAuth 2.0 and keyring are optional features needed for modern email providers (Google, Microsoft). If already installed without them, reinstall with the features flag.

> **Microsoft Azure AD OAuth 2.0 registration**: the redirect URI platform type **must be "Web"** — "Mobile and desktop" (public client) causes `401 Unauthorized` during token exchange because Himalaya sends the client secret via Basic Auth.

After installation, verify:

```bash
himalaya --version
```

## Global Options

All commands support these flags:

| Flag | Description |
|------|-------------|
| `-o, --output json` | JSON output for machine parsing |
| `-c, --config <PATH>` | Override config file path |
| `-a, --account <NAME>` | Override the default account |
| `--quiet` | Disable all logs |
| `--debug` | Enable debug logs |

## Configuration

Config file locations:
- **macOS**: `~/Library/Application Support/himalaya/config.toml`
- **Linux**: `~/.config/himalaya/config.toml`

Run the interactive wizard:

```bash
himalaya
```

Or configure a specific account:

```bash
himalaya account configure <name>
```

List all configured accounts:

```bash
himalaya account list
```

Diagnose account connectivity:

```bash
himalaya account doctor <name>
```



---

## Email Operations

### List Envelopes (Inbox)

```bash
# List first page of INBOX (default folder)
himalaya envelope list --page 1 --output json

# List a specific folder
himalaya envelope list --folder "Sent Items" --page 1 --output json

# List with a specific account
himalaya envelope list --account work --page 1 --output json

# Control page size
himalaya envelope list --page 1 --page-size 20 --output json
```

### Search & Filter Envelopes

Powerful query syntax combining filters and sorting:

```bash
# Filter by subject — IMPORTANT: only a SINGLE WORD, see caveat below
himalaya envelope list "subject meeting" --output json

# Filter by sender
himalaya envelope list "from jane@example.com" --output json

# Filter by date
himalaya envelope list "after 2026-05-01" --output json
himalaya envelope list "before 2026-05-15" --output json
himalaya envelope list "date 2026-05-10" --output json

# Combined filters with operators
himalaya envelope list "subject foo and body bar" --output json
himalaya envelope list "from alice or from bob" --output json
himalaya envelope list "not flag seen" --output json

# Narrow results by combining subject + date
himalaya envelope list "subject invoice and after 2025-01-01" --output json

# Sorting
himalaya envelope list "order by date desc" --output json
himalaya envelope list "order by from asc" --output json
himalaya envelope list "order by subject" --output json

# Combined filter + sort
himalaya envelope list "subject report order by date desc" --output json

# Filter by flag
himalaya envelope list "flag seen" --output json
himalaya envelope list "flag flagged" --output json
```

#### ⚠️ Search Caveat: Single-Word Patterns Only

The query parser treats **spaces as separators** between filter conditions. Multi-word patterns will fail:

```bash
# ❌ FAILS — spaces are parsed as query separators
himalaya envelope list "subject quarterly report" --output json
# Error: found 'r' expected space between filters, `and`, `or`, or end of input

# ✅ WORKAROUND: use a single distinguishing word
himalaya envelope list "subject quarterly" --output json

# ✅ ALTERNATIVE: combine subject + sender + date to narrow results
himalaya envelope list "subject invoice and from billing@example.com and after 2025-01-01" --output json
```

When searching for a phrase, pick the most unique single word from it, and optionally add `from` or date filters to narrow down.

### Read a Message

```bash
# Read the full message by envelope ID
himalaya message read 42

# Export raw message to file
himalaya message export 42
```

### Compose & Send

```bash
# Compose a new message (opens $EDITOR)
himalaya message write

# Reply to a message
himalaya message reply 42

# Forward a message
himalaya message forward 42

# Edit an existing message
himalaya message edit 42
```

### Delete & Move

```bash
# Move message to target folder
himalaya message move 42 --folder "Archive"

# Copy message to target folder
himalaya message copy 42 --folder "Projects"

# Mark message as deleted
himalaya message delete 42
```

### Attachment Operations

```bash
# Download all attachments from a message
himalaya attachment download 42
```

#### ⚠️ Critical: Default Download Folder

himalaya **ignores `cwd`** and always downloads attachments to the **default download folder configured per account** during `himalaya account configure`. The `cd` command has NO effect on download location — do NOT use it before `himalaya attachment download`.

**Correct approach**: download first, then `mv` files to the desired target folder:

```bash
# Step 1: Download (files go to account's default download folder)
himalaya attachment download 42

# Step 2: Move files to target folder
mv downloaded_file.pdf /path/to/target/folder/

# Batch download, then move
for id in 42 43 44; do
    himalaya attachment download "$id"
done
mv *.pdf /path/to/target/folder/
```

To find out the current default download folder, check the account config:
```bash
# View account configuration
himalaya account list --output json
```

How to check which messages have attachments:

### Flag Management

```bash
# Add flags
himalaya flag add 42 --flag seen
himalaya flag add 42 --flag flagged

# Set (replace all) flags
himalaya flag set 42 --flag seen

# Remove flags
himalaya flag remove 42 --flag seen
```

### Folder/Mailbox Management

```bash
# List all folders
himalaya folder list --output json

# Create a folder
himalaya folder create "MyFolder"

# Delete a folder
himalaya folder delete "OldFolder"

# Expunge (remove deleted messages permanently)
himalaya folder expunge "INBOX"

# Purge (delete all messages)
himalaya folder purge "Trash"
```

### Templates (Advanced)

```bash
# Generate a template for composing
himalaya template write

# Generate a reply template
himalaya template reply 42

# Generate a forward template
himalaya template forward 42

# Save template to folder
himalaya template save

# Send a template
himalaya template send
```

---

## AI Agent Patterns

### Typical Workflow

```bash
# 1. Check recent emails (first page, most recent first)
RECENT=$(himalaya envelope list --page 1 --output json)

# 2. Search for specific emails
RESULTS=$(himalaya envelope list "subject invoice order by date desc" --output json)

# 3. Read a specific message by ID
himalaya message read 42

# 4. Reply to a message (opens $EDITOR with pre-filled template)
himalaya message reply 42
```

### Advanced Keyword Search via Python Pipeline

When built-in search is insufficient (single-word limitation, or need to search across multiple fields), pipe JSON output to Python:

```bash
# Search by multiple keywords across subject + from fields
himalaya envelope list --folder INBOX --page 1 --page-size 500 --output json | python3 -c "
import json, sys
data = json.load(sys.stdin)
matches = []
for e in data:
    subj = (e.get('subject') or '').lower()
    # IMPORTANT: 'from' is an OBJECT with 'name' and 'addr' keys, not a string
    frm_addr = ''
    frm_name = ''
    if isinstance(e.get('from'), dict):
        frm_addr = (e.get('from').get('addr') or '').lower()
        frm_name = (e.get('from').get('name') or '').lower()
    if any(kw in subj or kw in frm_addr or kw in frm_name for kw in ['microsoft', 'msbill', 'msft']):
        matches.append({
            'id': e.get('id'),
            'subject': e.get('subject'),
            'from': e.get('from'),
            'date': e.get('date'),
            'has_attachment': e.get('has_attachment')
        })
print(json.dumps(matches, indent=2))
print(f'Total: {len(data)}, Matched: {len(matches)}', file=sys.stderr)
"

# Paginate through large inboxes (increase --page for older emails)
himalaya envelope list --folder INBOX --page 2 --page-size 500 --output json | python3 -c "..."

# Also search Archive folder for old emails
himalaya envelope list --folder Archive --page 1 --page-size 500 --output json | python3 -c "..."
```

### Extract Links from Email Body

```bash
# message read returns raw text (not JSON), use grep to extract URLs
himalaya message read 42 2>&1 | grep -o 'https://admin\.microsoft\.com[^ ]*'

# Or extract all HTTPS links
himalaya message read 42 2>&1 | grep -oP 'https?://[^\s<>\"'\\'']+' 
```

### Collect Invoice Attachments from Email (End-to-End Workflow)

```bash
# 1. Search for invoice emails with attachments across multiple pages
himalaya envelope list --folder INBOX --page 1 --page-size 500 --output json | python3 -c "
import json, sys
for e in json.load(sys.stdin):
    subj = (e.get('subject') or '').lower()
    if 'invoice' in subj and e.get('has_attachment'):
        print(json.dumps({'id':e['id'],'date':e['date'],'subject':e['subject']}))
"

# 2. Download attachments (files land in account's default download folder)
mkdir -p /desired/target/folder
for id in 42 43 44; do
    himalaya attachment download "$id"
done

# 3. Move downloaded files to target folder
mv *.pdf /desired/target/folder/

# 4. Inspect downloaded PDFs (e.g., with markitdown)
cd /desired/target/folder
for f in *.pdf; do
    markitdown "$f" | head -10
done

# 5. Rename files with meaningful names based on content
```

### JSON Structure Caveats

- **`from` and `to` are objects**: `{"name": "Microsoft", "addr": "noreply@microsoft.com"}`, NOT strings. Always check `isinstance(e.get('from'), dict)` before accessing `.get('addr')`.
- **`message read` returns raw text**, not a JSON dict. Pipe directly to `grep` or string parsing. Use `--output json` only for `envelope list` and `folder list`.

---

## Supported Providers

| Provider | IMAP Host | SMTP Host | Auth |
|----------|-----------|-----------|------|
| Gmail | `imap.gmail.com:993` | `smtp.gmail.com:465` | App Password or OAuth 2.0 |
| Outlook/Office 365 | `outlook.office365.com:993` | `smtp.office365.com:587` (STARTTLS) | Password or OAuth 2.0 |
| Proton Mail | `127.0.0.1:1143` (via Bridge) | `127.0.0.1:1025` (via Bridge) | Bridge password |
| iCloud | `imap.mail.me.com:993` | `smtp.mail.me.com:587` (STARTTLS) | App-specific password |

## Version

Current installed: `himalaya v1.2.0` (installed via `cargo install himalaya --locked`)
Installed at: `~/.cargo/bin/himalaya`
