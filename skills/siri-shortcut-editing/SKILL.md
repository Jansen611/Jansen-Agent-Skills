---
name: siri-shortcut-editing
description: |
  Edit macOS Siri Shortcuts (.shortcut files) programmatically — decode to XML, modify, and re-sign.
  Handles AEA1 Apple Encrypted Archives, CMS signing, and bplist conversion.

  Triggers when user mentions:
  - "shortcut" or "shortcuts" or ".shortcut file"
  - "edit a shortcut" or "modify a shortcut"
  - "Siri shortcut"
  - wants to programmatically modify a signed .shortcut file
author: Jansen Lin
license: MIT
allowed-tools: Bash, Read, Write, Edit
---

# Siri Shortcut Editing Skill

Edit signed macOS Siri Shortcuts (`.shortcut` files) by decoding them to XML, making changes, and re-signing.

## File Format

A `.shortcut` file is a **signed Apple Encrypted Archive (AEA1)** containing:

```
[0-3]     "AEA1" magic
[4-7]     zeros (reserved)
[8-11]    plist length (uint32 LE)
[12-...]  auth plist (bplist) — signing certificate chain
[after]   CMS signature + encrypted payload (Apple Archive)
```

The actual shortcut workflow is a bplist inside the Apple Archive, named `Shortcut.wflow`.

## Prerequisites

- macOS with `aea`, `aa`, `shortcuts` CLI tools (all built-in)
- `plutil` (built-in)
- Python 3 with `plistlib` (built-in)

Verify:
```bash
which aea aa shortcuts plutil python3
```

---

## Workflow: Decode .shortcut → XML

Use the bundled `scripts/decode_shortcut.py`:

```bash
python3 scripts/decode_shortcut.py INPUT.shortcut OUTPUT.xml
```

This script performs all three steps automatically:
1. Extracts the signing certificate's public key from the AEA1 auth plist
2. Decrypts the Apple Archive via `aea decrypt -profile 0`
3. Locates the embedded bplist inside the decoded archive and converts to XML

If doing it manually, the steps are:

### Step 1: Extract signing certificate public key

The first 12 bytes of a `.shortcut` file are the AEA1 header (magic + zeros + plist length as uint32 LE). The auth plist starts at byte 12. Parse it, grab the leaf certificate from `SigningCertificateChain`, derive the public key with `openssl x509`.

### Step 2: Decrypt the Apple Archive

```bash
aea decrypt -profile 0 -sign-pub /tmp/signing_pub.pem \
  -i INPUT.shortcut -o /tmp/decoded.bin
```

### Step 3: Extract bplist → XML

The decoded archive starts with `AA01` metadata; the actual workflow bplist is embedded further in. Find the `bplist` marker and parse from there with `plistlib`.

---

## Workflow: Edit & Re-sign XML → .shortcut

> **⚠️ `shortcuts sign` requires the input file to use a `.wflow` extension, otherwise it fails.**

### Step 1: Convert XML back to bplist

```bash
plutil -convert binary1 -o /tmp/workflow.wflow OUTPUT.xml
```

### Step 2: Sign the shortcut

```bash
shortcuts sign -m anyone \
  -i /tmp/workflow.wflow \
  -o OUTPUT.shortcut
```

`shortcuts sign` accepts a bare bplist (old-format shortcut) and automatically wraps it in the AEA1 Apple Archive format with a new CMS signature.

Signing modes:
- `-m anyone` — anyone can import the shortcut
- `-m people-who-know-me` — only your contacts (default)

---

## XML Structure Overview

Key keys in the shortcut plist:

| Key | Description |
|-----|-------------|
| `WFWorkflowActions` | Array of action dicts — the core logic |
| `WFWorkflowActionIdentifier` | Action type, e.g. `is.workflow.actions.gettext` |
| `WFWorkflowActionParameters` | Per-action parameters |
| `WFWorkflowTypes` | Where shortcut appears (e.g. `WFWorkflowTypeShowInSearch`) |
| `WFWorkflowInputContentItemClasses` | Accepted input types |
| `WFWorkflowOutputContentItemClasses` | Output types |
| `WFWorkflowMinimumClientVersion` | Minimum iOS/macOS version |
| `WFWorkflowIcon` | Icon glyph & color |

Variable references use `WFTextTokenAttachment` serialization with `OutputUUID` and `OutputName` fields. Literal strings use `WFTextTokenString` with `string` field.

---

## Dictionary Action Reference

For `WFItemType` values, nested object syntax, and common failure modes, see:

→ **[references/dictionary-actions.md](references/dictionary-actions.md)**

Key points:
- `WFItemType=0` = Text, `1` = Nested Object, `2` = Array, `3` = Number, `5` = Variable Reference
- Nested objects require `WFItemType=1` with **double-wrapped** `WFDictionaryFieldValue`
- `WFItemType=5` + inline `WFDictionaryFieldValue` → crash

---

## Security Warning

Shortcuts often contain hardcoded secrets (API keys, tokens). Always warn the user if you find:
- API keys in `WFTextActionText` fields
- Bearer tokens in `Authorization` headers
- Any other credentials

After editing, advise rotating any exposed keys.

---

## Complete Round-Trip Example

```bash
# Decode
python3 scripts/decode_shortcut.py MyShortcut.shortcut MyShortcut.xml

# Edit MyShortcut.xml manually or programmatically...

# Re-sign
plutil -convert binary1 -o /tmp/workflow.wflow MyShortcut.xml
shortcuts sign -m anyone -i /tmp/workflow.wflow -o MyShortcut.shortcut
```

The full decode logic lives in `scripts/decode_shortcut.py` — read that file if you need to understand or modify the internals.
