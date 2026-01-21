---
# Core Classification
protocol: Hifi Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59642
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
source_link: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Zeeshan Meghji
  - Roman Rohleder
  - Souhail Mssassi
---

## Vulnerability Title

Usage of `transfer()` Instead of `safeTransfer()`

### Overview


The bug report states that a previous issue has been fixed by replacing a function with a safer alternative. The affected files are `packages/amm/HifiPool.sol` and `proxy-target\contracts\HifiProxyTarget.sol`. The problem was related to the ERC20 standard token implementation and checking for the transaction status. It is recommended to use the `safeTransfer` function from the safeERC20 Implementation to ensure the transaction fails if the intended token transfer does not succeed.

### Original Finding Content

**Update**
Fixed in commit [ae9459f](https://github.com/hifi-finance/hifi/commit/ae9459f) by replacing the unsafe transfer function with `safeTransferFrom()`, as suggested.

**File(s) affected:**`packages/amm/HifiPool.sol`, `proxy-target\contracts\HifiProxyTarget.sol`

**Description:** The ERC20 standard token implementation functions also returns the transaction status as a Boolean. It is good practice to check for the return status of the function call to ensure that the transaction was successful. It is the developer's responsibility to enclose these function calls with `require()` to ensure that when the intended ERC20 function call returns `false`, the caller transaction also fails. However, it is mostly missed by developers when they carry out checks; in effect, the transaction would always succeed, even if the token transfer didn't.

**Recommendation:** Use the `safeTransfer` function from the safeERC20 Implementation,.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Hifi Finance |
| Report Date | N/A |
| Finders | Zeeshan Meghji, Roman Rohleder, Souhail Mssassi |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html

### Keywords for Search

`vulnerability`

