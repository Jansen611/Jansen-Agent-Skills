---
author: Jansen Lin
license: MIT
---

# Dictionary Action — WFItemType Reference

## WFItemType Values

| Type | Meaning | WFSerializationType |
|------|---------|---------------------|
| `0` | Text (string) | `WFTextTokenString` |
| `1` | Nested Object | `WFDictionaryFieldValue` (double-wrapped) |
| `2` | Array | `WFArraySubstitutableParameterState` or `WFArrayParameterState` |
| `3` | Number | `WFTextTokenString` |
| `4` | Boolean | `WFNumberSubstitutableState` with `<true/>` or `<false/>` |
| `5` | Variable Reference | `WFTextTokenAttachment` |

> **⚠️ `WFItemType=5` with inline `WFDictionaryFieldValue` will crash Shortcuts.** Type 5 is only for variable references (pointing to another action's output).
>
> **⚠️ `WFItemType=0` with inline `WFDictionaryFieldValue` shows as an empty string `""`.**

---

## Nested Object Syntax (`WFItemType=1`)

When a dictionary value needs to be a nested object (e.g. `"key": {"child": "value"}`), use `WFItemType=1` with **double-wrapped** `WFDictionaryFieldValue`.

### Pattern

```
WFItemType: 1
WFKey → "parentKey"
WFValue:
  Value:
    WFSerializationType: WFDictionaryFieldValue   ← outer wrapper
    Value:
      WFDictionaryFieldValueItems:                ← inner children
        - WFItemType: 0
          WFKey → "childKey"
          WFValue → "childValue"
      WFSerializationType: WFDictionaryFieldValue  ← inner wrapper
```

### Generic XML Template

Replace `PARENT_KEY`, `CHILD_KEY`, and `CHILD_VALUE` with actual values:

```xml
<dict>
  <key>WFItemType</key>
  <integer>1</integer>
  <key>WFKey</key>
  <dict>
    <key>Value</key>
    <dict>
      <key>string</key>
      <string>PARENT_KEY</string>
    </dict>
    <key>WFSerializationType</key>
    <string>WFTextTokenString</string>
  </dict>
  <key>WFValue</key>
  <dict>
    <key>Value</key>
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
              <dict>
                <key>string</key>
                <string>CHILD_KEY</string>
              </dict>
              <key>WFSerializationType</key>
              <string>WFTextTokenString</string>
            </dict>
            <key>WFValue</key>
            <dict>
              <key>Value</key>
              <dict>
                <key>string</key>
                <string>CHILD_VALUE</string>
              </dict>
              <key>WFSerializationType</key>
              <string>WFTextTokenString</string>
            </dict>
          </dict>
        </array>
      </dict>
      <key>WFSerializationType</key>
      <string>WFDictionaryFieldValue</string>
    </dict>
    <key>WFSerializationType</key>
    <string>WFDictionaryFieldValue</string>
  </dict>
</dict>
```

### Multiple Children

Add more `<dict>` entries inside the `WFDictionaryFieldValueItems` array:

```xml
<array>
  <dict><!-- child 1 --></dict>
  <dict><!-- child 2 --></dict>
</array>
```

### Common Failure Modes

| What | Result |
|------|--------|
| `WFItemType=0` + `WFDictionaryFieldValue` | Displays as empty string |
| `WFItemType=5` + `WFDictionaryFieldValue` | Shortcuts crash on open |
| Single-layer `WFDictionaryFieldValue` (missing outer) | Incorrect serialization |
| Using `setdictionaryvalue` action | May not be available on all versions |

---

## Arrays of Objects: Two Approaches

When a dictionary key needs an array of objects (e.g. an API body with a list of structured items), there are two ways to build it.

### Approach A: Inline (`WFArrayParameterState`)

Nest the array and objects directly inside the dictionary. Works for simple, fixed arrays.

```xml
<!-- Inside a dictionary value -->
<key>WFItemType</key><integer>2</integer>
<key>WFValue</key>
<dict>
  <key>Value</key>
  <array>
    <dict>
      <key>WFItemType</key><integer>1</integer>
      <!-- nested dict inline -->
    </dict>
  </array>
  <key>WFSerializationType</key>
  <string>WFArrayParameterState</string>
</dict>
```

### Approach B: Composed (`WFAArraySubstitutableParameterState`)

Build each object as a standalone dictionary, collect them in a `list` action, set to a variable, then reference that variable. This is the recommended approach for maintainable, extensible arrays.

```xml
<!-- Step 1: Build each tool as a standalone dictionary -->
<!-- dictionary → WebSearchTool -->
<!-- dictionary → AnotherTool -->
<!-- ... -->

<!-- Step 2: Collect in a list -->
<!-- list → Tools     → contains: WebSearchTool, AnotherTool -->

<!-- Step 3: Set to variable -->
<!-- SetVariable → ToolsList -->

<!-- Step 4: Reference in the target dictionary -->
<key>WFItemType</key><integer>2</integer>
<key>WFValue</key>
<dict>
  <key>Value</key>
  <dict>
    <key>Value</key>
    <dict>
      <key>Type</key>
      <string>Variable</string>
      <key>VariableName</key>
      <string>ToolsList</string>
    </dict>
    <key>WFSerializationType</key>
    <string>WFTextTokenAttachment</string>
  </dict>
  <key>WFSerializationType</key>
  <string>WFArraySubstitutableParameterState</string>
</dict>
```

Use Approach B when you need to add/remove items without digging through deeply nested XML.
