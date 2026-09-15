---
# Core Classification
protocol: Mode Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42119
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/ef8bb8d1-8234-4914-ba83-8c7cf9543c83
source_link: https://cdn.cantina.xyz/reports/cantina_solo_mode_lock_may2024.pdf
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
finders_count: 1
finders:
  - Alex The Entreprenerd
---

## Vulnerability Title

MED - Not using safeTransfer may cause sweep to fail for some tokens 

### Overview


The bug report is about a program called ModeStaking, which uses a tool called IERC20 from a library called forge-std. The report explains that there is a problem with this tool when it is used with certain types of tokens, specifically mentioning USDT as an example. The report suggests that the program should use a different tool called safeTransfer instead. The issue has been fixed by the Mode team using a different tool called safeERC20. The report rates the risk of this bug as low.

### Original Finding Content

## ModeStaking and IERC20

ModeStaking uses `IERC20` from `forge-std`:

```solidity
import {IERC20} from "forge-std/interfaces/IERC20.sol";
```

## The Interface

The interface is defined as follows:

```solidity
function transfer(address to, uint256 amount) external returns (bool);
```

**Note:** This will fail for tokens that do not return a boolean (e.g., USDT).

## Recommendation

It is recommended to use `safeTransfer`.

## Resolution

The Mode team fixed this issue by using `safeERC20`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Mode Network |
| Report Date | N/A |
| Finders | Alex The Entreprenerd |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_solo_mode_lock_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/ef8bb8d1-8234-4914-ba83-8c7cf9543c83

### Keywords for Search

`vulnerability`

