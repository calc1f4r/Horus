---
# Core Classification
protocol: prePO
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1658
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-prepo-contest
source_link: https://code4rena.com/reports/2022-03-prepo
github_link: https://github.com/code-423n4/2022-03-prepo-findings/issues/54

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.40
financial_impact: high

# Scoring
quality_score: 2
rarity_score: 3

# Context Tags
tags:
  - validation
  - bypass_limit

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cmichel
  - IllIllI  leastwood
---

## Vulnerability Title

[H-03] Withdrawal delay can be circumvented

### Overview


A bug was found in the code of the Collateral token, which is used for withdrawals. After initiating a withdrawal with the `initiateWithdrawal` function, it is still possible to transfer the collateral tokens. This bug can be exploited in two ways. First, an attacker can create two accounts and initiate withdrawals at different times such that one of the accounts is always in a valid withdrawal window, no matter what time it is. Second, the attacker can create several accounts and initiate withdrawals with all of them to withdraw larger amounts even at the same block. This bug can have a high severity as it breaks core functionality of the Collateral token.

To mitigate this bug, it is recommended to disable transfers for the token owner if there is a withdrawal request for them. This can be done by adding a check to the `beforeTransfer` function to check if the withdrawal request is still in the withdrawal window. If it is, the transfer should be reverted.

### Original Finding Content

_Submitted by cmichel, also found by IllIllI and leastwood_

[Collateral.sol#L97](https://github.com/code-423n4/2022-03-prepo/blob/f63584133a0329781609e3f14c3004c1ca293e71/contracts/core/Collateral.sol#L97)<br>

After initiating a withdrawal with `initiateWithdrawal`, it's still possible to transfer the collateral tokens.
This can be used to create a second account, transfer the accounts to them and initiate withdrawals at a different time frame such that one of the accounts is always in a valid withdrawal window, no matter what time it is.
If the token owner now wants to withdraw they just transfer the funds to the account that is currently in a valid withdrawal window.

Also, note that each account can withdraw the specified `amount`. Creating several accounts and circling & initiating withdrawals with all of them allows withdrawing larger amounts **even at the same block** as they are purchased in the future.

I consider this high severity because it breaks core functionality of the Collateral token.

### Proof of Concept

For example, assume the `_delayedWithdrawalExpiry = 20` blocks. Account A owns 1000 collateral tokens, they create a second account B.

*   At `block=0`, A calls `initiateWithdrawal(1000)`. They send their balance to account B.
*   At `block=10`, B calls `initiateWithdrawal(1000)`. They send their balance to account A.
*   They repeat these steps, alternating the withdrawal initiation every 10 blocks.
*   One of the accounts is always in a valid withdrawal window (`initiationBlock < block && block <= initiationBlock + 20`). They can withdraw their funds at any time.

### Recommended Mitigation Steps

If there's a withdrawal request for the token owner (`_accountToWithdrawalRequest[owner].blockNumber > 0`), disable their transfers for the time.

```solidity
// pseudo-code not tested
beforeTransfer(from, to, amount) {
  super();
  uint256 withdrawalStart =  _accountToWithdrawalRequest[from].blockNumber;
  if(withdrawalStart > 0 && withdrawalStart + _delayedWithdrawalExpiry < block.number) {
    revert(); // still in withdrawal window
  }
}
```

**[ramenforbreakfast (prePO) commented](https://github.com/code-423n4/2022-03-prepo-findings/issues/54#issuecomment-1075791543):**
 > This is a valid claim.

**[gzeon (judge) commented](https://github.com/code-423n4/2022-03-prepo-findings/issues/54#issuecomment-1086869763):**
 > Agree with sponsor.



***

 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 2/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | prePO |
| Report Date | N/A |
| Finders | cmichel, IllIllI  leastwood |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-prepo
- **GitHub**: https://github.com/code-423n4/2022-03-prepo-findings/issues/54
- **Contest**: https://code4rena.com/contests/2022-03-prepo-contest

### Keywords for Search

`Validation, Bypass limit`

