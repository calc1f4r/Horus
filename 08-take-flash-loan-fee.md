---
# Core Classification
protocol: Opus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30440
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-01-opus
source_link: https://code4rena.com/reports/2024-01-opus
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[08] Take flash loan fee

### Overview

See description below for full details.

### Original Finding Content


Although the fee for yin flash loans is currently zero ([`FLASH_FEE = 0`](https://github.com/code-423n4/2024-01-opus/blob/4720e9481a4fb20f4ab4140f9cc391a23ede3817/src/core/flash_mint.cairo#L32)), it should still be accounted for when [withdrawing the loan `amount` from the borrower](https://github.com/code-423n4/2024-01-opus/blob/4720e9481a4fb20f4ab4140f9cc391a23ede3817/src/core/flash_mint.cairo#L141), just to make sure this step is not forgotten once the flash fee becomes non-zero in the future. 

```diff
diff --git a/src/core/flash_mint.cairo b/src/core/flash_mint.cairo
index d2114d8..97c21d9 100644
--- a/src/core/flash_mint.cairo
+++ b/src/core/flash_mint.cairo
@@ -138,7 +138,7 @@ mod flash_mint {
             assert(borrower_resp == ON_FLASH_MINT_SUCCESS, 'FM: on_flash_loan failed');
 
             // This function in Shrine takes care of balance validation
-            shrine.eject(receiver, amount_wad);
+            shrine.eject(receiver, amount_wad + FLASH_FEE.try_into().unwrap());
 
             if adjust_ceiling {
                 shrine.set_debt_ceiling(ceiling);
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Opus |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-01-opus
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-01-opus

### Keywords for Search

`vulnerability`

