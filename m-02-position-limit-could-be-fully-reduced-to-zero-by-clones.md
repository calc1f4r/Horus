---
# Core Classification
protocol: Frankencoin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20023
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-frankencoin
source_link: https://code4rena.com/reports/2023-04-frankencoin
github_link: https://github.com/code-423n4/2023-04-frankencoin-findings/issues/932

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
finders_count: 15
finders:
  - rbserver
  - lil\_eth
  - bin2chen
  - Nyx
  - Josiah
---

## Vulnerability Title

[M-02] POSITION LIMIT COULD BE FULLY REDUCED TO ZERO BY CLONES

### Overview


A bug has been discovered in the code of the Frankencoin project. This bug affects the newly opened positions and could cause their limit to be reduced to zero as soon as the cooldown period has elapsed. The bug is in the function reduceLimitForClone() which is located in the Position.sol file (lines 97-101). This function is used to reduce the limit for a clone, but if the minimum parameter is equal to the limit, the reduction amount becomes zero and the limit is set to zero, leaving the original position owner with no limit to mint Frankencoin. 

To mitigate this bug, it is recommended to charge a fee to the cloners that is payable to the original owner. Additionally, a reserve limit should be left untouched allocated solely to the original owner. This bug has been acknowledged by the Frankencoin team, and they have suggested that if the position comes with a high enough fee, it should not be relevant in practice.

### Original Finding Content


### Lines of code

<https://github.com/code-423n4/2023-04-frankencoin/blob/main/contracts/MintingHub.sol#L126> <br><https://github.com/code-423n4/2023-04-frankencoin/blob/main/contracts/Position.sol#L97-L101>

### Impact

A newly opened position could have its limit fully reduced to zero as soon as the cooldown period has elapsed.

### Proof of Concept

As seen in the function below, a newly opened position with `0` Frankencoin minted could have its `limit` turn `0` if the function parameter, `_minimum`, is inputted with an amount equal to `limit`. In this case, `reduction` is equal to `0`, making `limit - _minimum = 0` while the cloner is assigned `reduction + _minimum = 0 + limit = limit`:

[Position.sol#L97-L101](https://github.com/code-423n4/2023-04-frankencoin/blob/main/contracts/Position.sol#L97-L101)

        function reduceLimitForClone(uint256 _minimum) external noChallenge noCooldown alive onlyHub returns (uint256) {
            uint256 reduction = (limit - minted - _minimum)/2; // this will fail with an underflow if minimum is too high
            limit -= reduction + _minimum;
            return reduction + _minimum;
        }

With the limit now fully allocated to the cloner, the original position owner is left with zero limit to mint Frankencoin after spending 1000 Frankencoin to open this position. This situation could readily happen especially when it involves popular position contracts.

### Recommended Mitigation Steps

It is recommended position contract charging fees to cloners. Additionally, a reserve limit should be left untouched allocated solely to the original owner to be in line with the context of position opening.

**[0xA5DF (lookout) commented](https://github.com/code-423n4/2023-04-frankencoin-findings/issues/932#issuecomment-1516037713):**
 > Setting this one as primary since it shows how a single clone can reduce the remaining limit to zero.

**[luziusmeisser (Frankencoin) acknowledged and commented](https://github.com/code-423n4/2023-04-frankencoin-findings/issues/932#issuecomment-1528894234):**
 > Charging clones a fee payable to the original is an interesting idea!
> 
> If the position comes with a high enough fee, this should not be relevant in practice as the limit will not be reached or new positions being created if there is enough demand. 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Frankencoin |
| Report Date | N/A |
| Finders | rbserver, lil\_eth, bin2chen, Nyx, Josiah, Ruhum, RaymondFam, Diana, Emmanuel, 0xDACA, nobody2018, \_\_141345\_\_, carlitox477, Kumpa |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-frankencoin
- **GitHub**: https://github.com/code-423n4/2023-04-frankencoin-findings/issues/932
- **Contest**: https://code4rena.com/reports/2023-04-frankencoin

### Keywords for Search

`vulnerability`

