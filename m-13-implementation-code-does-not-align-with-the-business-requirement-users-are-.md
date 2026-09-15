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
solodit_id: 5606
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-holograph-contest
source_link: https://code4rena.com/reports/2022-10-holograph
github_link: https://github.com/code-423n4/2022-10-holograph-findings/issues/142

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
finders_count: 1
finders:
  - ladboy233
---

## Vulnerability Title

[M-13] Implementation code does not align with the business requirement: Users are not charged with withdrawn fee when user unbound token in `HolographOperator.sol`

### Overview


This bug report is about the HolographOperator.sol contract, which is part of the 2022-10-holograph project on Github. The bug is related to the unbondUtilityToken function, which is used to unstake tokens. The code does not charge a 0.1% fee for unstaking as specified in the documentation, which weakens the incentive for operators to stay bonded. This bug is confirmed with a manual review of the documentation. The recommended mitigation step is to charge the 0.1% fee to make the code align with the business requirement in the documentation.

### Original Finding Content


[HolographOperator.sol#L899](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/HolographOperator.sol#L899)<br>
[HolographOperator.sol#L920](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/HolographOperator.sol#L920)<br>
[HolographOperator.sol#L924](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/HolographOperator.sol#L924)<br>
[HolographOperator.sol#L928](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/HolographOperator.sol#L928)<br>
[HolographOperator.sol#L932](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/HolographOperator.sol#L932)<br>

When user call unbondUtilityToken to unstake the token, the function reads the available bonded amount, and transfers back to the operator.

<https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/HolographOperator.sol#L899>

```solidity
/**
 * @dev get current bonded amount by operator
 */
uint256 amount = _bondedAmounts[operator];
/**
 * @dev unset operator bond amount before making a transfer
 */
_bondedAmounts[operator] = 0;
/**
 * @dev remove all operator references
 */
_popOperator(_bondedOperators[operator] - 1, _operatorPodIndex[operator]);
/**
 * @dev transfer tokens to recipient
 */
require(_utilityToken().transfer(recipient, amount), "HOLOGRAPH: token transfer failed");
```

the logic is clean, but does not conform to the buisness requirement in the documentation, the doc said

<https://docs.holograph.xyz/holograph-protocol/operator-network-specification#operator-job-selection>

> To move to a different pod, an Operator must withdraw and re-bond HLG. Operators who withdraw HLG will be charged a 0.1% fee, the proceeds of which will be burned or returned to the Treasury.

The charge 0.1% fee is not implemented in the code.

there are two incentive for bounded operator to stay,

the first is the reward incentive, the second is to avoid penalty with unbonding.

Without chargin the unstaking fee, the second incentive is weak and the operator can unbound or bond whenver they want

### Proof of Concept

<https://docs.holograph.xyz/holograph-protocol/operator-network-specification#operator-job-selection>

### Recommended Mitigation Steps

We recommend charge the 0.1% unstaking fee to make the code align with the busienss requirement in the doc.

```solidity
/**
 * @dev get current bonded amount by operator
 */
uint256 amount = _bondedAmounts[operator];
uint256 fee = chargedFee(amount); // here
amount -= fee;  
/**
 * @dev unset operator bond amount before making a transfer
 */
_bondedAmounts[operator] = 0;
/**
 * @dev remove all operator references
 */
_popOperator(_bondedOperators[operator] - 1, _operatorPodIndex[operator]);
/**
 * @dev transfer tokens to recipient
 */
require(_utilityToken().transfer(recipient, amount), "HOLOGRAPH: token transfer failed");
```

**[alexanderattar (Holograph) commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/142#issuecomment-1307863427):**
 > This is true. The functionality is purposefully disabled for easier bonding/unbonding testing by team at the moment, but will be addressed in the upcoming release.

**[alexanderattar (Holograph) commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/142#issuecomment-1351786887):**
 > On initial mainnet beta launch, Holograph will be operating as the sole operator on the network so this is not an immediate concern, but before the launch of the public operator network, the fee will be added via upgrade.



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
| Finders | ladboy233 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-holograph
- **GitHub**: https://github.com/code-423n4/2022-10-holograph-findings/issues/142
- **Contest**: https://code4rena.com/contests/2022-10-holograph-contest

### Keywords for Search

`Business Logic`

