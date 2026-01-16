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
solodit_id: 13845
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

Slashes do not affect bounty distribution ✓ Addressed

### Overview


This bug report is about a problem in the DelegationController.sol contract of the skale-manager project. When slashes are processed, only the `_delegatedByHolderToValidator` and `_delegatedByHolder` values are reduced. The `_effectiveDelegatedByHolderToValidator` value remains the same, which is used to distribute bounties amongst delegators. As a result, the slashing does not affect the distribution. The code snippet in the report shows the code responsible for this bug.

The recommendation to fix the bug is to reduce the `_effectiveDelegatedByHolderToValidator` and `_effectiveDelegatedToValidator` values when slashes are processed. The bug was mitigated in skale-manager pull request #118.

### Original Finding Content

#### Resolution



Mitigated in [skalenetwork/skale-manager#118](https://github.com/skalenetwork/skale-manager/pull/118)


#### Description


When slashes are processed by a holder, only `_delegatedByHolderToValidator` and `_delegatedByHolder` values are reduced. But `_effectiveDelegatedByHolderToValidator` value remains the same. This value is used to distribute bounties amongst delegators. So slashing will not affect that distribution.


**contracts/delegation/DelegationController.sol:L863-L873**



```
uint oldValue = getAndUpdateDelegatedByHolderToValidator(holder, validatorId);
if (oldValue > 0) {
    uint month = \_slashes[index].month;
    reduce(
        \_delegatedByHolderToValidator[holder][validatorId],
        \_delegatedByHolder[holder],
        \_slashes[index].reducingCoefficient,
        month);
    slashingSignals[index.sub(begin)].holder = holder;
    slashingSignals[index.sub(begin)].penalty = oldValue.sub(getAndUpdateDelegatedByHolderToValidator(holder, validatorId));
}

```
#### Recommendation


Reduce `_effectiveDelegatedByHolderToValidator` and `_effectiveDelegatedToValidator` when slashes are processed.

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

