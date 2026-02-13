# DB/index.json Update Guide

Every new or modified vulnerability entry MUST have a corresponding `DB/index.json` update.

## What to Update

### 1. Categories

Add file to `categories.{category}.subcategories.{subcategory}.files[]`:

```json
{
  "name": "NEW_VULNERABILITY.md",
  "path": "DB/{category}/{subcategory}/NEW_VULNERABILITY.md",
  "focus": ["key aspect 1", "key aspect 2", "key aspect 3"]
}
```

### 2. Keywords

Add technical terms to `categories.{category}.subcategories.{subcategory}.keywords[]`:
- Function names (`latestRoundData`, `lzReceive`, `convertToShares`)
- Attack pattern names (`inflation attack`, `sandwich`, `read-only reentrancy`)

### 3. Search Index

Add to `searchIndex.mappings`:

```json
"new_function_name": ["DB/{path}/NEW_VULNERABILITY.md"],
"new_attack_pattern": ["DB/{path}/NEW_VULNERABILITY.md"]
```

### 4. Protocol Context

If applicable, add to `protocolContext.mappings.{protocol_type}.priority_files[]`.

### 5. Audit Checklist

Add new check items to `auditChecklist.{category}` if the vulnerability introduces new patterns.

### 6. Version

Bump `meta.version` for significant structural changes.

## Update Checklist

```
Index Update:
- [ ] File path in categories.{cat}.subcategories.{subcat}.files[]
- [ ] focus array populated with 3+ key aspects
- [ ] Technical keywords added to subcategory keywords[]
- [ ] Function/method names in searchIndex.mappings
- [ ] Attack pattern names in searchIndex.mappings
- [ ] Protocol context updated if applicable
- [ ] Audit checklist items added if applicable
- [ ] Version bumped if structural change
```
