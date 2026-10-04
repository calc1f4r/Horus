---
# Core Classification
protocol: Mozaic Archimedes
chain: everychain
category: uncategorized
vulnerability_type: layerzero

# Attack Vector Details
attack_type: layerzero
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19007
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-23-Mozaic Archimedes.md
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
  - layerzero

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-11 No slippage protection for cross-chain swaps in StargatePlugin

### Overview


A bug was found in the StargatePlugin, which calls StargateRouter's swap() function to do a cross-chain swap. This function was passing 0 as the minimum amount of tokens to receive, making it vulnerable to sandwich attacks, where the fee or conversion rate is pumped to make the user receive hardly any tokens. The team responded to the bug and fixed the issue by removing the affected function and calculating accepted slippage off-chain, which is then passed to the `_swapRemote()` function for validation.

### Original Finding Content

**Description:**
The StargatePlugin calls StargateRouter's swap() function to do a cross-chain swap.
```solidity 
            // Swaps
            IStargateRouter(_router).swap(_dstChainId, _srcPoolId, _dstPoolId, 
                  payable(address(this)), _amountLD, 0, IStargateRouter.lzTxObj(0, 0, "0x"), abi.encodePacked(_to), bytes(""));
``` 
It will pass 0 as the minimum amount of tokens to receive. This pattern is vulnerable to 
sandwich attacks, where the fee or conversion rate is pumped to make the user receive hardly 
any tokens. In Layer Zero, the equilibrium fee can be manipulated to force such losses.

**Recommended mitigation:**
Calculate accepted slippage off-chain, and pass it to the `_swapRemote()` function for 
validation.

**Team response:**
Fixed.

**Mitigation review:**
Affected function has been removed

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Mozaic Archimedes |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-23-Mozaic Archimedes.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`LayerZero`

