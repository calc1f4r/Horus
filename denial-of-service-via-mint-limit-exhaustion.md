---
# Core Classification
protocol: Lombard
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53234
audit_firm: OtterSec
contest_link: https://www.lombard.finance/
source_link: https://www.lombard.finance/
github_link: https://github.com/lombard-finance/sui-contracts

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
finders_count: 2
finders:
  - Robert Chen
  - Tuyết Dương
---

## Vulnerability Title

Denial of Service via Mint Limit Exhaustion

### Overview


The bug report discusses an issue with the claim_native and return_native functions in the bridge, which allow users to swap wrapped tokens for native tokens and vice versa. However, an attacker can exploit this by repeatedly swapping a small amount of tokens between minting and burning, leading to the exhaustion of the treasury's capacity. The suggested solution is to remove the ability for users to wrap and unwrap tokens within the same chain and instead force them to go cross-chain, which should slow down such attacks. This issue has been resolved in the patch with the code a58183d.

### Original Finding Content

## Token Swap Vulnerability

`claim_native` and `return_native` in bridge allow users to swap wrapped tokens (WT) for native tokens and vice versa. However, an attacker can repeatedly cycle a small token amount between minting (`claim_native`) and burning (`return_native`). Since each minting operation contributes to the epoch’s minting limit, this exploitation will exhaust the treasury’s capacity within an epoch, preventing legitimate users from minting new tokens.

## Remediation

Remove the ability for the user to wrap and unwrap purely inside Sui and force them to go cross-chain, which should significantly slow down such an attack.

## Patch

Resolved in `a58183d`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Lombard |
| Report Date | N/A |
| Finders | Robert Chen, Tuyết Dương |

### Source Links

- **Source**: https://www.lombard.finance/
- **GitHub**: https://github.com/lombard-finance/sui-contracts
- **Contest**: https://www.lombard.finance/

### Keywords for Search

`vulnerability`

