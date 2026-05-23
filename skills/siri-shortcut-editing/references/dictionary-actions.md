# Dictionary Action — WFItemType Reference

## WFItemType Values

| Type | Meaning | WFSerializationType |
|------|---------|---------------------|
| `0` | Text (string) | `WFTextTokenString` |
| `1` | Nested Object | `WFDictionaryFieldValue` (double-wrapped) |
| `2` | Array | `WFArraySubstitutableParameterState` |
| `3` | Number | `WFTextTokenString` |
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
