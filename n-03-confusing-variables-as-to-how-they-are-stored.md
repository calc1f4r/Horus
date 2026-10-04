---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24852
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-08-frax
source_link: https://code4rena.com/reports/2022-08-frax
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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[N-03] Confusing variables as to how they are stored

### Overview

See description below for full details.

### Original Finding Content


The `FraxlendPairCore` contract constructor takes two arguments, `_configData` and `_immutables`, however, there are immutables in `_configData` and variables in `_immutables`.

This may seem confusing, since for example one expects the `TIME_LOCK_ADDRESS` to be immutable as it is defined in the `_immutables` variable, however it is possible to change it with [setTimeLock](https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPair.sol#L204).

**Affected source code:**

- [FraxlendPairCore.sol#L174](https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPairCore.sol#L174)
- [FraxlendPairCore.sol#L190-L191](https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPairCore.sol#L190-L191)
- [FraxlendPairCore.sol#L193-L197](https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPairCore.sol#L193-L197)


**[gititGoro (judge) commented](https://github.com/code-423n4/2022-08-frax-findings/issues/191#issuecomment-1269063966):**
 > Very good report quality!
> There were some invalid points:
> - L-02. Misconfigured or misbehaving tokens are out of scope
> - L-06. The precision cap is intentional. This issue was reported as a Medium risk bug by another warden and marked invalid.
> - L-07. Owners resigning seems beyond the scope of the audit. FraxLend will be managed by a DAO like other Frax products. Even without explicit documentation, for a Frax product, this should be the assumed default. This is if you were unable to contact the sponsor and verify explicitly that a human controlled EOA would be the owner, a very uncommon circumstance for a large mainnet dapp.




***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-frax
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-08-frax

### Keywords for Search

`vulnerability`

