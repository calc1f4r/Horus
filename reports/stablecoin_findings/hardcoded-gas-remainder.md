---
# Core Classification
protocol: InstaDApp Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11797
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/instadapp-audit/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Hardcoded gas remainder

### Overview

See description below for full details.

### Original Finding Content

The `execute` function of the `UserWallet` contract [uses a `delegatecall`](https://github.com/InstaDApp/contract-v2/blob/4863c0c4156af7ded9cdb38b66e5f5e527c4a6d0/contracts/UserWallet.sol#L152) to a user-inputted logic proxy contract. This appears to be a clone of [MakerDAO’s delagate call pattern](https://ethereum.stackexchange.com/questions/68810/difference-in-delegate-call-via-assembly).


In that `delegatecall`, the gas parameter is set to `sub(gas, 5000)`. The reason for this value is not documented. Presumably, this is to ensure there is enough gas (*i.e.* at least 5000) remaining to finish executing the rest of the assembly block. This could potentially be a problematic approach because the gas cost of opcodes can change (see [EIP 1884](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1884.md) as an example), which could result in insufficient gas issues in the future.


Consider setting the value to `sub(gas, minRemainingGas)`, where `minRemainingGas` is either a user-inputted parameter or a user-settable global variable.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | InstaDApp Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/instadapp-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

