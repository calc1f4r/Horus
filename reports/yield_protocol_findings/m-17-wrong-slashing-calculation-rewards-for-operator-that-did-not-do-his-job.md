---
# Core Classification
protocol: Holograph
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5610
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-holograph-contest
source_link: https://code4rena.com/reports/2022-10-holograph
github_link: https://github.com/code-423n4/2022-10-holograph-findings/issues/307

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - services
  - launchpad
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Jeiwan
  - ctf_sec
  - peanuts
  - imare
---

## Vulnerability Title

[M-17] Wrong slashing calculation rewards for operator that did not do his job

### Overview


This bug report is about an issue with the Holograph Operator contract code, where the wrong slashing calculation is being used. This could lead to unfair punishment for operators who accidentally forget to execute their job. The bug occurs when the whole getBaseBondAmount() fee is slashed from the job.operator instead of the documented percentage of slashing. The documentation states that only a portion should be slashed and the number of slashes should be noted down. The bug was found using manual review. The recommended mitigation steps are to implement the correct percentage of slashing and include a mapping to note down the number of slashes that an operator has.

### Original Finding Content


Wrong slashing calculation may create unfair punishment for operators that accidentally forgot to execute their job.

### Proof of Concept

[Docs](https://docs.holograph.xyz/holograph-protocol/operator-network-specification): If an operator acts maliciously, a percentage of their bonded HLG will get slashed. Misbehavior includes (i) downtime, (ii) double-signing transactions, and (iii) abusing transaction speeds. 50% of the slashed HLG will be rewarded to the next operator to execute the transaction, and the remaining 50% will be burned or returned to the Treasury.

The docs also include a guide for the number of slashes and the percentage of bond slashed. However, in the contract, there is no slashing of percentage fees. Rather, the whole \_getBaseBondAmount() fee is [slashed from the job.operator instead.](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/HolographOperator.sol#L374-L382)

            uint256 amount = _getBaseBondAmount(pod);
            /**
             * @dev select operator that failed to do the job, is slashed the pod base fee
             */
            _bondedAmounts[job.operator] -= amount;
            /**
             * @dev the slashed amount is sent to current operator
             */
            _bondedAmounts[msg.sender] += amount;

Documentation states that only a portion should be slashed and the number of slashes should be noted down.

### Recommended Mitigation Steps

Implement the correct percentage of slashing and include a mapping to note down the number of slashes that an operator has.

**[alexanderattar (Holograph) commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/307#issuecomment-1306684590):**
 > Valid. The docs are not in sync with the code, but it will be adjusted to handle this correctly.

**[alexanderattar (Holograph) resolved and commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/307#issuecomment-1351759231):**
 > We have changed the slashing logic to use base bonding amount instead of percentage based approach.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Holograph |
| Report Date | N/A |
| Finders | Jeiwan, ctf_sec, peanuts, imare |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-holograph
- **GitHub**: https://github.com/code-423n4/2022-10-holograph-findings/issues/307
- **Contest**: https://code4rena.com/contests/2022-10-holograph-contest

### Keywords for Search

`Business Logic`

