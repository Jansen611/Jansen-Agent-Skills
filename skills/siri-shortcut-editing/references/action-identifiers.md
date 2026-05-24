---
author: Jansen Lin
license: MIT
---

# Shortcut Action Reference

Known-valid `WFWorkflowActionIdentifier` values extracted from working shortcuts, with required parameters and XML templates.

---

## Variable Actions

### 1. is.workflow.actions.setvariable — Set Variable

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `WFVariableName` | string | ✅ | Variable name |
| `WFInput` | attachment | ✅ | Value to set. `Type=ExtensionInput` for shortcut input, `Type=Variable`+`VariableName` for existing vars |

```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.setvariable</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFInput</key>
    <dict>
      <key>Value</key>
      <dict>
        <key>Type</key>
        <string>ExtensionInput</string>
      </dict>
      <key>WFSerializationType</key>
      <string>WFTextTokenAttachment</string>
    </dict>
    <key>WFVariableName</key>
    <string>MyVariable</string>
  </dict>
</dict>
```

To reference a variable from another action's output:
```xml
<key>WFInput</key>
<dict>
  <key>Value</key>
  <dict>
    <key>OutputName</key>
    <string>SourceOutputName</string>
    <key>OutputUUID</key>
    <string>SOURCE-ACTION-UUID</string>
    <key>Type</key>
    <string>ActionOutput</string>
  </dict>
  <key>WFSerializationType</key>
  <string>WFTextTokenAttachment</string>
</dict>
```

To reference a named variable:
```xml
<key>WFInput</key>
<dict>
  <key>Value</key>
  <dict>
    <key>Type</key>
    <string>Variable</string>
    <key>VariableName</key>
    <string>MyVariable</string>
  </dict>
  <key>WFSerializationType</key>
  <string>WFTextTokenAttachment</string>
</dict>
```

### 2. is.workflow.actions.appendvariable — Add to Variable

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `WFVariableName` | string | ✅ | Target variable |
| `WFInput` | attachment | ✅ | Value to append |

---

## Text Actions

### 1. is.workflow.actions.gettext — Text (literal string)

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | Unique ID for referencing output |
| `WFTextActionText` | string | ✅ | The text content |
| `CustomOutputName` | string | No | Label in GUI |

```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.gettext</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>CustomOutputName</key>
    <string>MyText</string>
    <key>UUID</key>
    <string>11111111-2222-3333-4444-555555555555</string>
    <key>WFTextActionText</key>
    <string>Hello World</string>
  </dict>
</dict>
```

**With inline variable substitution** (`attachmentsByRange`):

When embedding a variable inside a text template, `WFTextActionText` uses `attachmentsByRange` to mark where the variable goes. The `￼` character in the `string` is the placeholder — Shortcuts replaces it with the variable value at runtime.

> **⚠️ If the template is JSON**: Shortcuts only inserts the value — it does NOT add JSON quotes. You must wrap the placeholder in quotes yourself: `"query":"￼"` not `"query":￼`.

The `{offset, length}` key is the 0-indexed position of `￼` in the `string` field.

```xml
<key>WFTextActionText</key>
<dict>
  <key>Value</key>
  <dict>
    <key>attachmentsByRange</key>
    <dict>
      <key>{12, 1}</key>                     <!-- ￼ is at character position 12 -->
      <dict>
        <key>Type</key>
        <string>Variable</string>
        <key>VariableName</key>
        <string>MyVariable</string>
      </dict>
    </dict>
    <key>string</key>
    <string>The value is ￼ here</string>      <!-- ￼ replaces at position 12 -->
  </dict>
  <key>WFSerializationType</key>
  <string>WFTextTokenString</string>
</dict>
```

### 2. is.workflow.actions.detect.text — Get Text from Input (coercion)

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFInput` | attachment | ✅ | Input to extract text from |
| `CustomOutputName` | string | No | |

### 3. is.workflow.actions.text.replace — Replace Text

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFInput` | attachment | ✅ | Uses `WFTextTokenString` + `attachmentsByRange` format (same pattern as `gettext` inline substitution) |
| `WFReplaceTextFind` | string | ✅ | Pattern to find (plain text or regex with isRegex=true) |
| `WFReplaceTextReplace` | string | No | Replacement string |
| `CustomOutputName` | string | No | |

```xml
<key>WFInput</key>
<dict>
  <key>Value</key>
  <dict>
    <key>attachmentsByRange</key>
    <dict>
      <key>{0, 1}</key>
      <dict>
        <key>OutputName</key>
        <string>SourceText</string>
        <key>OutputUUID</key>
        <string>SOURCE-UUID</string>
        <key>Type</key>
        <string>ActionOutput</string>
      </dict>
    </dict>
    <key>string</key>
    <string>￼</string>
  </dict>
  <key>WFSerializationType</key>
  <string>WFTextTokenString</string>
</dict>
```

### 4. is.workflow.actions.text.split — Split Text

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `text` | string/variable | ✅ | Text to split (used with attachmentsByRange) |
| `CustomOutputName` | string | No | |

### 5. is.workflow.actions.text.trimwhitespace — Trim Whitespace

| Param | Type | Required |
|-------|------|----------|
| `UUID` | string | ✅ |
| `WFInput` | attachment | ✅ |
| `CustomOutputName` | string | No |

### 6. is.workflow.actions.text.changecase — Change Case

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `text` | string/variable | ✅ | |
| `WFCaseType` | string | ✅ | `lowercase`, `uppercase`, `capitalize` |
| `CustomOutputName` | string | No | |

### 7. is.workflow.actions.text.match — Match Text (regex)

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFMatchTextPattern` | string | ✅ | Regex pattern |
| `text` | string/attachment | ✅ | Text to match against |
| `WFMatchTextCaseSensitive` | boolean | No | |
| `CustomOutputName` | string | No | |

```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.text.match</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>CustomOutputName</key>
    <string>MatchedText</string>
    <key>UUID</key>
    <string>MATCH-UUID</string>
    <key>WFMatchTextPattern</key>
    <string>pattern here</string>
    <key>text</key>
    <dict>
      <key>Value</key>
      <dict>
        <key>string</key>
        <string>input text</string>
      </dict>
      <key>WFSerializationType</key>
      <string>WFTextTokenString</string>
    </dict>
  </dict>
</dict>
```

### 8. is.workflow.actions.text.combine — Combine Text

Joins a list of text items with a separator.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `text` | attachment | ✅ | List of text items to join |
| `WFTextSeparator` | string | Yes | `Custom`, `New Lines`, `Spaces`, `Commas` |
| `WFTextCustomSeparator` | string/attachment | Yes (if Custom) | Separator string |
| `CustomOutputName` | string | No | |

---

## Dictionary Actions

### 1. is.workflow.actions.dictionary — Build Dictionary

| Param | Type | Required |
|-------|------|----------|
| `UUID` | string | ✅ |
| `WFItems` | object | ✅ |
| `CustomOutputName` | string | No |

The `WFItems` uses `WFDictionaryFieldValueItems` array. See [dictionary-actions.md](dictionary-actions.md) for complete WFItemType reference.

### 2. is.workflow.actions.detect.dictionary — Get Dictionary from Input

Parses a text input (e.g. JSON string) into a dictionary. Useful when a value from an API response is a JSON string rather than a parsed object.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFInput` | attachment | ✅ | Input to parse as dictionary |
| `CustomOutputName` | string | No | |

### 3. is.workflow.actions.getvalueforkey — Get Dictionary Value

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFInput` | attachment | ✅ | Dictionary to read from |
| `WFDictionaryKey` | string | ✅ | Key to extract |
| `WFGetDictionaryValueType` | string | No | `Value` to get single value; omit for first match |
| `CustomOutputName` | string | No | |

### 4. is.workflow.actions.setvalueforkey — Set Dictionary Value

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFDictionary` | attachment | ✅ | Dictionary to modify |
| `WFDictionaryKey` | string | ✅ | Key to set |
| `WFDictionaryValue` | attachment | ✅ | Value to set. Only supports text, number, or dictionary — arrays are not supported |
| `CustomOutputName` | string | No | |

> **Limitation**: `setvalueforkey` cannot set a key to an array value. Workaround: build two separate dictionaries (one with the array, one without) and select between them with an If block.

---

## List Actions

### 1. is.workflow.actions.list — Build List

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFItems` | array of dict | ✅ | Array of items with `WFItemType` and `WFValue` |
| `CustomOutputName` | string | No | |

```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.list</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>CustomOutputName</key>
    <string>MyList</string>
    <key>UUID</key>
    <string>11111111-2222-3333-4444-555555555555</string>
    <key>WFItems</key>
    <array>
      <dict>
        <key>WFItemType</key>
        <integer>0</integer>
        <key>WFValue</key>
        <dict>
          <key>Value</key>
          <dict>
            <key>string</key>
            <string>item1</string>
          </dict>
          <key>WFSerializationType</key>
          <string>WFTextTokenString</string>
        </dict>
      </dict>
    </array>
  </dict>
</dict>
```

### 2. is.workflow.actions.count — Count Items

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `Input` | attachment | ✅ | Collection to count |
| `WFCountType` | string | ✅ | `Items`, `Characters`, `Words`, `Sentences`, `Lines` |
| `CustomOutputName` | string | No | |

### 3. is.workflow.actions.getitemfromlist — Get Item from List

Gets a single item from a list by index or specifier.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFInput` | attachment | ✅ | List to pick from |
| `WFItemSpecifier` | string | No | `First Item`, `Last Item`, `Item at Index`, `Random Item` |
| `CustomOutputName` | string | No | |

---

## Math Actions

### 1. is.workflow.actions.math — Calculate

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFInput` | attachment | Yes | Left operand |
| `WFMathOperand` | string | Yes | Right operand |
| `WFMathOperation` | string | ✅ | `+`, `-`, `×`, `÷` |

### 2. is.workflow.actions.round — Round Number

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFInput` | attachment | ✅ | Number to round |
| `WFRoundMode` | string | ✅ | `Normal`, `Always Round Up`, `Always Round Down`, `Round to Nearest` |
| `CustomOutputName` | string | No | |

### 3. is.workflow.actions.number — Number (literal)

Use `is.workflow.actions.gettext` with a number string. Number values in dictionaries use `WFItemType=3`.

---

## HTTP / Network Actions

### 1. is.workflow.actions.downloadurl — Get Contents of URL

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFURL` | string/attachment | ✅ | URL to fetch |
| `WFHTTPMethod` | string | ✅ | `GET` or `POST` |
| `WFHTTPBodyType` | string | ✅ | `File` for custom body, `Form` for form data |
| `WFHTTPHeaders` | dictionary | ✅ | Headers as `WFDictionaryFieldValue` |
| `WFRequestVariable` | attachment | Yes (POST) | Request body |
| `ShowHeaders` | boolean | No | `true` to enable custom request headers (shows the "Headers" section in the action UI) |

Output: Returns the response body. The `Contents of URL` magic variable provides access to the downloaded content.

> **Content-Type handling**: Shortcuts only auto-imports known text MIME types (e.g. `application/json`, `text/plain`) from `Contents of URL`. Other types like `text/event-stream` are treated as binary and blocked from reading unless the response has a known file extension. Workaround: save to a `.txt` file with `documentpicker.save`, then read back with `detect.text`.

```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.downloadurl</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>ShowHeaders</key>
    <true/>
    <key>UUID</key>
    <string>11111111-2222-3333-4444-555555555555</string>
    <key>WFHTTPBodyType</key>
    <string>File</string>
    <key>WFHTTPHeaders</key>
    <dict>
      <key>Value</key>
      <dict>
        <key>WFDictionaryFieldValueItems</key>
        <array>
          <dict>
            <key>WFItemType</key>
            <integer>0</integer>
            <key>WFKey</key>
            <dict>
              <key>Value</key>
              <dict><key>string</key><string>Content-Type</string></dict>
              <key>WFSerializationType</key>
              <string>WFTextTokenString</string>
            </dict>
            <key>WFValue</key>
            <dict>
              <key>Value</key>
              <dict><key>string</key><string>application/json</string></dict>
              <key>WFSerializationType</key>
              <string>WFTextTokenString</string>
            </dict>
          </dict>
        </array>
      </dict>
      <key>WFSerializationType</key>
      <string>WFDictionaryFieldValue</string>
    </dict>
    <key>WFHTTPMethod</key>
    <string>POST</string>
    <key>WFRequestVariable</key>
    <dict>
      <key>Value</key>
      <dict>
        <key>OutputName</key>
        <string>Body</string>
        <key>OutputUUID</key>
        <string>BODY-DICT-UUID</string>
        <key>Type</key>
        <string>ActionOutput</string>
      </dict>
      <key>WFSerializationType</key>
      <string>WFTextTokenAttachment</string>
    </dict>
    <key>WFURL</key>
    <dict>
      <key>Value</key>
      <dict>
        <key>string</key>
        <string>https://example.com/api</string>
      </dict>
      <key>WFSerializationType</key>
      <string>WFTextTokenString</string>
    </dict>
  </dict>
</dict>
```

`WFURL` accepts a plain `<string>` as well (as produced by the Shortcuts GUI):

```xml
<key>WFURL</key>
<string>https://example.com/api</string>
```

---

## File Actions

### 1. is.workflow.actions.documentpicker.open — Get File

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFFile` | dict | ✅ | File reference |
| `WFGetFilePath` | string/attachment | ✅ | Path to file |
| `WFFileErrorIfNotFound` | boolean | Yes | `true`/`false` |
| `CustomOutputName` | string | No | |

### 2. is.workflow.actions.documentpicker.save — Save File

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFFolder` | dict | ✅ | Destination folder ref |
| `WFAskWhereToSave` | boolean | ✅ | |
| `WFFileDestinationPath` | attachment | ✅ | Path |
| `WFInput` | attachment | ✅ | Content to save |

### 3. is.workflow.actions.file.append — Append to File

| Param | Type | Required |
|-------|------|----------|
| `UUID` | string | ✅ |
| `WFFile` | dict | ✅ |
| `WFFilePath` | attachment | ✅ |
| `WFInput` | attachment | ✅ |

### 4. is.workflow.actions.setitemname — Set Name

Renames an item.

| Param | Type | Required |
|-------|------|----------|
| `UUID` | string | ✅ |
| `WFInput` | attachment | ✅ |
| `WFName` | string | ✅ |
| `CustomOutputName` | string | No |

---

## Control Flow

### 1. is.workflow.actions.conditional — If

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `GroupingIdentifier` | string | ✅ | Must match across If/Otherwise/End If |
| `WFCondition` | integer | ✅ | `101`=Equals, `4`=Contains, `0`=GreaterThan, `2`=LessThan, `100`=IsNotEmpty, etc. |
| `WFConditionalActionString` | attachment | No | Value to compare against |
| `WFInput` | attachment | Yes | Left side of comparison |
| `WFControlFlowMode` | integer | ✅ | `0`=start of block, `2`=end of block |
| `UUID` | string | Yes (for End If) | Only on the closing block |
| `WFConditions` | dict | No | For compound conditions |

> **Boolean checks**: When checking a boolean from a dictionary (`WFItemType=4`), the variable must include `Aggrandizements` with `WFCoercionVariableAggrandizement` → `CoercionItemClass=WFBooleanContentItem`. Without this coercion, Shortcuts defaults to text comparison and `true`/`false` won't match.

Start of If block (`WFControlFlowMode=0`):
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.conditional</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>GroupingIdentifier</key>
    <string>A809788C-131E-4B81-B1F8-292501ED043D</string>
    <key>WFCondition</key>
    <integer>101</integer>
    <key>WFControlFlowMode</key>
    <integer>0</integer>
    <key>WFInput</key>
    <dict>
      <key>Value</key>
      <dict>
        <key>Type</key>
        <string>Variable</string>
        <key>VariableName</key>
        <string>MyVariable</string>
      </dict>
      <key>WFSerializationType</key>
      <string>WFTextTokenAttachment</string>
    </dict>
  </dict>
</dict>
```

End of If block (`WFControlFlowMode=2`):
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.conditional</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>GroupingIdentifier</key>
    <string>A809788C-131E-4B81-B1F8-292501ED043D</string>
    <key>UUID</key>
    <string>11111111-2222-3333-4444-555555555555</string>
    <key>WFControlFlowMode</key>
    <integer>2</integer>
  </dict>
</dict>
```

### 2. is.workflow.actions.repeat.each — Repeat with Each

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `GroupingIdentifier` | string | ✅ | |
| `WFControlFlowMode` | integer | ✅ | `0`=start, `2`=end |
| `WFInput` | attachment | Yes (start) | Collection to iterate |
| `UUID` | string | Yes (end) | |

### 3. is.workflow.actions.repeat.count — Repeat (fixed count)

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `GroupingIdentifier` | string | ✅ | |
| `WFControlFlowMode` | integer | ✅ | `0`=start, `2`=end |
| `WFRepeatCount` | integer | Yes (start only) | Number of iterations |
| `UUID` | string | Yes (end) | |

```xml
<!-- Start of Repeat 3 times -->
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.repeat.count</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>GroupingIdentifier</key>
    <string>RepeatGroup1</string>
    <key>WFControlFlowMode</key>
    <integer>0</integer>
    <key>WFRepeatCount</key>
    <integer>3</integer>
  </dict>
</dict>
<!-- ... actions inside repeat ... -->
<!-- End of Repeat -->
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.repeat.count</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>GroupingIdentifier</key>
    <string>RepeatGroup1</string>
    <key>UUID</key>
    <string>REPEAT-END-UUID</string>
    <key>WFControlFlowMode</key>
    <integer>2</integer>
  </dict>
</dict>
```

### 4. is.workflow.actions.delay — Wait

| Param | Type | Required |
|-------|------|----------|
| `WFDelayTime` | integer | ✅ (seconds) |

### 5. is.workflow.actions.runworkflow — Run Shortcut

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFWorkflowName` | string | ✅ | |
| `WFWorkflow` | dict | ✅ | Contains `workflowIdentifier`, `workflowName`, `isSelf` |
| `WFInput` | attachment | Yes | Input to pass |
| `CustomOutputName` | string | No | |

### 6. is.workflow.actions.ask — Ask for Input

| Param | Type | Required |
|-------|------|----------|
| `UUID` | string | ✅ |
| `WFAskActionPrompt` | string | ✅ |
| `WFAskActionDefaultAnswer` | string | No |
| `WFAllowsMultilineText` | boolean | No |
| `CustomOutputName` | string | No |

---

## Output

### 1. is.workflow.actions.output — Stop and Output

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `WFOutput` | attachment | ✅ | Value to output |
| `WFNoOutputSurfaceBehavior` | string | ✅ | `Respond` for share sheet, `DoNothing` |
| `WFResponse` | string | No | |
| `UUID` | string | No | |

### 2. is.workflow.actions.showresult — Show Result

| Param | Type | Required |
|-------|------|----------|
| `Text` | attachment | ✅ |

---

## URL Actions

### 1. is.workflow.actions.url — URL

Creates a URL value (not a fetch — use `downloadurl` for actual HTTP requests).

| Param | Type | Required |
|-------|------|----------|
| `UUID` | string | ✅ |
| `WFURLActionURL` | string | ✅ |

```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.url</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>UUID</key>
    <string>URL-ACTION-UUID</string>
    <key>WFURLActionURL</key>
    <string>https://example.com</string>
  </dict>
</dict>
```

---

## Rich Text / HTML Actions

### 1. is.workflow.actions.gethtmlfromrichtext — Get HTML from Rich Text

Converts rich text (e.g. from `downloadurl` output) to HTML string.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFInput` | attachment | ✅ | Rich text input |
| `CustomOutputName` | string | No | |
| `WFMakeFullDocument` | boolean | No | `true` wraps in full `<html>` document |

```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.gethtmlfromrichtext</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>CustomOutputName</key>
    <string>HTMLBody</string>
    <key>UUID</key>
    <string>HTML-ACTION-UUID</string>
    <key>WFInput</key>
    <dict>
      <key>Value</key>
      <dict>
        <key>OutputName</key>
        <string>Contents of URL</string>
        <key>OutputUUID</key>
        <string>DOWNLOADURL-UUID</string>
        <key>Type</key>
        <string>ActionOutput</string>
      </dict>
      <key>WFSerializationType</key>
      <string>WFTextTokenAttachment</string>
    </dict>
  </dict>
</dict>
```

---

## Media Actions

### 1. is.workflow.actions.makespokenaudiofromtext — Make Spoken Audio from Text

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFInput` | string/attachment | ✅ | Text to speak |
| `WFSpeakTextLanguage` | string | ✅ | e.g. `zh-TW`, `en-US` |
| `WFSpeakTextVoice` | string | ✅ | Voice bundle ID |
| `WFSpeakTextRate` | real | No | Float, e.g. `0.5` |

```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.makespokenaudiofromtext</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>UUID</key>
    <string>SPEAK-UUID</string>
    <key>WFInput</key>
    <dict>
      <key>Value</key>
      <dict>
        <key>string</key>
        <string>Text to speak</string>
      </dict>
      <key>WFSerializationType</key>
      <string>WFTextTokenString</string>
    </dict>
    <key>WFSpeakTextLanguage</key>
    <string>zh-TW</string>
    <key>WFSpeakTextRate</key>
    <real>0.5</real>
    <key>WFSpeakTextVoice</key>
    <string>com.apple.ttsbundle.gryphon-neural_shufen_zh-TW_premium</string>
  </dict>
</dict>
```

---

## Notes Actions

### 1. com.apple.mobilenotes.SharingExtension — Create Note

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `AppIntentDescriptor` | dict | ✅ | `AppIntentIdentifier: CreateNoteLinkAction`, `BundleIdentifier: com.apple.mobilenotes` |
| `WFCreateNoteInput` | string/attachment | ✅ | Note body content |
| `WFNoteGroup` | dict | No | Folder reference with `Identifier` |
| `folder` | dict | No | Folder metadata (title, symbol, identifier) |
| `name` | string/attachment | No | Note title |
| `OpenWhenRun` | boolean | No | |

```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>com.apple.mobilenotes.SharingExtension</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>AppIntentDescriptor</key>
    <dict>
      <key>AppIntentIdentifier</key>
      <string>CreateNoteLinkAction</string>
      <key>BundleIdentifier</key>
      <string>com.apple.mobilenotes</string>
      <key>Name</key>
      <string>备忘录</string>
      <key>TeamIdentifier</key>
      <string>0000000000</string>
    </dict>
    <key>OpenWhenRun</key>
    <false/>
    <key>UUID</key>
    <string>NOTE-UUID</string>
    <key>WFCreateNoteInput</key>
    <dict>
      <key>Value</key>
      <dict>
        <key>string</key>
        <string>Note content</string>
      </dict>
      <key>WFSerializationType</key>
      <string>WFTextTokenString</string>
    </dict>
  </dict>
</dict>
```

### 2. is.workflow.actions.appendnote — Append to Note

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `AppIntentDescriptor` | dict | ✅ | `AppIntentIdentifier: AppendToNoteLinkAction` |
| `WFInput` | attachment | ✅ | Content to append |
| `WFNote` | attachment | Yes | Target note (from Create Note output) |
| `CustomOutputName` | string | No | |

---

## WFTextTokenString Templates

### Literal string value
```xml
<dict>
  <key>Value</key>
  <dict>
    <key>string</key>
    <string>my text here</string>
  </dict>
  <key>WFSerializationType</key>
  <string>WFTextTokenString</string>
</dict>
```

### String with variable interpolation
When a string contains `￼` (Object Replacement Character) to inline a variable:

```xml
<dict>
  <key>Value</key>
  <dict>
    <key>attachmentsByRange</key>
    <dict>
      <key>{7, 1}</key>
      <dict>
        <key>OutputName</key>
        <string>Token</string>
        <key>OutputUUID</key>
        <string>TOKEN-UUID</string>
        <key>Type</key>
        <string>ActionOutput</string>
      </dict>
    </dict>
    <key>string</key>
    <string>Bearer ￼</string>
  </dict>
  <key>WFSerializationType</key>
  <string>WFTextTokenString</string>
</dict>
```

### Variable reference (standalone)
```xml
<dict>
  <key>Value</key>
  <dict>
    <key>OutputName</key>
    <string>MyOutput</string>
    <key>OutputUUID</key>
    <string>SOURCE-UUID</string>
    <key>Type</key>
    <string>ActionOutput</string>
  </dict>
  <key>WFSerializationType</key>
  <string>WFTextTokenAttachment</string>
</dict>
```

### Named variable reference
```xml
<dict>
  <key>Value</key>
  <dict>
    <key>Type</key>
    <string>Variable</string>
    <key>VariableName</key>
    <string>MyVariable</string>
  </dict>
  <key>WFSerializationType</key>
  <string>WFTextTokenAttachment</string>
</dict>
```

### Extension Input (Shortcut Input)
```xml
<dict>
  <key>Value</key>
  <dict>
    <key>Type</key>
    <string>ExtensionInput</string>
  </dict>
  <key>WFSerializationType</key>
  <string>WFTextTokenAttachment</string>
</dict>
```

### Extension Input with Coercion (e.g. force to File)
```xml
<dict>
  <key>Value</key>
  <dict>
    <key>Aggrandizements</key>
    <array>
      <dict>
        <key>CoercionItemClass</key>
        <string>WFGenericFileContentItem</string>
        <key>Type</key>
        <string>WFCoercionVariableAggrandizement</string>
      </dict>
    </array>
    <key>Type</key>
    <string>ExtensionInput</string>
  </dict>
  <key>WFSerializationType</key>
  <string>WFTextTokenAttachment</string>
</dict>
```
