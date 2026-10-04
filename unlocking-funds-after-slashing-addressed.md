---
# Core Classification
protocol: Skale Token
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13823
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/01/skale-token/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Sergii Kravchenko
  - Shayan Eskandari
---

## Vulnerability Title

Unlocking funds after slashing ✓ Addressed

### Overview


This bug report is about an issue with the TokenState.sol contract, which is part of the Skale Network. The problem is that when the initial funds are delegated, they can only be unlocked if 51+% of them are delegated. However, if any portion of the funds are slashed, the rest of the funds will not be unlocked at the end of the delegation period. The recommendation is to consider slashed tokens as delegated, or include them in the calculation for process to unlock in `endingDelegatedToUnlocked`. The issue has been fixed as part of the major code changes in [skalenetwork/skale-manager#92](https://github.com/skalenetwork/skale-manager/pull/92).

### Original Finding Content

#### Resolution



Issue is fixed as a part of the major code changes in [skalenetwork/skale-manager#92](https://github.com/skalenetwork/skale-manager/pull/92)


#### Description


The initial funds can be unlocked if 51+% of them are delegated. However if any portion of the funds are slashed, the rest of the funds will not be unlocked at the end of the delegation period.


**code/contracts/delegation/TokenState.sol:L258-L263**



```
if (\_isPurchased[delegationId]) {
    address holder = delegation.holder;
    \_totalDelegated[holder] += delegation.amount;
    if (\_totalDelegated[holder] >= \_purchased[holder]) {
        purchasedToUnlocked(holder);
    }

```
#### Recommendation


Consider slashed tokens as delegated, or include them in the calculation for process to unlock in `endingDelegatedToUnlocked`

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Skale Token |
| Report Date | N/A |
| Finders | Sergii Kravchenko, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/01/skale-token/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

