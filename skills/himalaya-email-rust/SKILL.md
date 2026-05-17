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

### JSON Output Parsing

Envelope list in JSON format returns an array of objects with keys like:
`id`, `subject`, `from`, `to`, `date`, `flags`

Use `jq` to parse:

```bash
# Get IDs of all envelopes on first page
himalaya envelope list --page 1 --output json | jq '.[].id'

# Get subjects from a sender
himalaya envelope list "from alice" --output json | jq '.[].subject'
```

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
