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
| `WFInput` | attachment | ✅ | |
| `WFReplaceTextFind` | string | ✅ | Pattern to find (plain text or regex with isRegex=true) |
| `WFReplaceTextReplace` | string | No | Replacement string |
| `CustomOutputName` | string | No | |

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

---

## Dictionary Actions

### 1. is.workflow.actions.dictionary — Build Dictionary

| Param | Type | Required |
|-------|------|----------|
| `UUID` | string | ✅ |
| `WFItems` | object | ✅ |
| `CustomOutputName` | string | No |

The `WFItems` uses `WFDictionaryFieldValueItems` array. See [dictionary-actions.md](dictionary-actions.md) for complete WFItemType reference.

### 2. is.workflow.actions.getvalueforkey — Get Dictionary Value

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `UUID` | string | ✅ | |
| `WFInput` | attachment | ✅ | Dictionary to read from |
| `WFDictionaryKey` | string | ✅ | Key to extract |
| `WFGetDictionaryValueType` | string | No | `Value` to get single value; omit for first match |
| `CustomOutputName` | string | No | |

### 3. is.workflow.actions.setvalueforkey — Set Dictionary Value

| Param | Type | Required |
|-------|------|----------|
| `UUID` | string | ✅ |
| `WFDictionary` | attachment | ✅ |
| `WFDictionaryKey` | string | ✅ |
| `WFDictionaryValue` | attachment | ✅ |
| `CustomOutputName` | string | No |

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

---

## Math Actions

### 1. is.workflow.actions.number — Number

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
| `ShowHeaders` | boolean | No | `true` to include response headers in output |

Output: Returns a dictionary `{Contents: ..., Headers: {}}` when `ShowHeaders=true`, or just the content when `false`.

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
