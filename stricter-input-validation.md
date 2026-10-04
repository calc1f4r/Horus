---
# Core Classification
protocol: Ax Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48252
audit_firm: OtterSec
contest_link: github.com/Ax-Protocol/usx/.
source_link: github.com/Ax-Protocol/usx/.
github_link: github.com/Ax-Protocol/usx/.

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
finders_count: 4
finders:
  - Robert Chen
  - Shiva Shankar
  - YoungJoo Lee
  - OtterSec
---

## Vulnerability Title

Stricter Input Validation

### Overview

See description below for full details.

### Original Finding Content

## Recommendations for Input Validation Improvement

The following are recommendations to improve input validation for key functions:

1. **In `UERC20.sol`**, validate that the address inputs to the following functions are nonzero:
    - `transfer`
    - `transferFrom`
    - `approve`
    
2. **In `WormholeBridge::setSendFees`**, validate that the lengths of `_destChainIds` and `_fees` are equal.

3. **In `WormholeBridge` and `LayerZeroBridge`**, validate the length of `_toAddress`. Otherwise, this may potentially allow unsafe address parsing.
   ```solidity
   LayerZeroBridge.sol
   assembly {
       toAddress := mload(add(toAddressBytes, 20))
   }
   ```

4. **In `Treasury`**, ensure a non-zero amount in the following functions:
    - `mint`
    - `redeem`
    - `stakeCrv`

## Remediation
Add the described checks as a defense-in-depth measure.

## Patch
Resolved in commits `777ba1d` and `dac44d6`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Ax Protocol |
| Report Date | N/A |
| Finders | Robert Chen, Shiva Shankar, YoungJoo Lee, OtterSec |

### Source Links

- **Source**: github.com/Ax-Protocol/usx/.
- **GitHub**: github.com/Ax-Protocol/usx/.
- **Contest**: github.com/Ax-Protocol/usx/.

### Keywords for Search

`vulnerability`

