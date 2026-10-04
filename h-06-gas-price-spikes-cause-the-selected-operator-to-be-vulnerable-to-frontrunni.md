---
# Core Classification
protocol: Holograph
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5591
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-holograph-contest
source_link: https://code4rena.com/reports/2022-10-holograph
github_link: https://github.com/code-423n4/2022-10-holograph-findings/issues/44

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - front-running
  - gas_price

protocol_categories:
  - dexes
  - bridge
  - services
  - launchpad
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Lambda  Trust
  - Chom
---

## Vulnerability Title

[H-06] Gas price spikes cause the selected operator to be vulnerable to frontrunning and be slashed

### Overview


This bug report is about the vulnerability of the HolographOperator.sol code on the code-423n4/2022-10-holograph GitHub repository. The vulnerability allows operators to be vulnerable to frontrunning and be slashed due to gas price spikes. This can be done by submitting a transaction to the mempool and queueing it with the gasPrice in bridgeInRequestPayload. If the selected operator does not submit a transaction, they risk being slashed. 

The recommended mitigation steps are to modify the operator node software to queue transactions immediately with gasPrice in bridgeInRequestPayload if a gas price spike happens, or allow gas fee loss tradeoff to prevent being slashed. 

In conclusion, the bug report is about a vulnerability in the HolographOperator.sol code that allows operators to be vulnerable to frontrunning and be slashed due to gas price spikes. The recommended mitigation steps are to modify the operator node software to queue transactions immediately with gasPrice in bridgeInRequestPayload if a gas price spike happens, or allow gas fee loss tradeoff to prevent being slashed.

### Original Finding Content


[HolographOperator.sol#L354](https://github.com/code-423n4/2022-10-holograph/blob/f8c2eae866280a1acfdc8a8352401ed031be1373/contracts/HolographOperator.sol#L354)<br>

```solidity
require(gasPrice >= tx.gasprice, "HOLOGRAPH: gas spike detected");
```

```solidity
        /**
         * @dev select operator that failed to do the job, is slashed the pod base fee
         */
        _bondedAmounts[job.operator] -= amount;
        /**
         * @dev the slashed amount is sent to current operator
         */
        _bondedAmounts[msg.sender] += amount;
```

Since you have designed a mechanism to prevent other operators to slash the operator due to "the selected missed the time slot due to a gas spike". It can induce that operators won't perform their job if a gas price spike happens due to negative profit.

But your designed mechanism has a vulnerability. Other operators can submit their transaction to the mempool and queue it using `gasPrice in bridgeInRequestPayload`. It may get executed before the selected operator as the selected operator is waiting for the gas price to drop but doesn't submit any transaction yet. If it doesn't, these operators lose a little gas fee. But a slashed reward may be greater than the risk of losing a little gas fee.

```solidity
require(timeDifference > 0, "HOLOGRAPH: operator has time");
```

Once 1 epoch has passed, selected operator is vulnerable to slashing and frontrunning.

### Recommended Mitigation Steps

Modify your operator node software to queue transactions immediately with `gasPrice in bridgeInRequestPayload` if a gas price spike happened. Or allow gas fee loss tradeoff to prevent being slashed.

**[alexanderattar (Holograph) confirmed and commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/44#issuecomment-1307886755):**
 > Valid, we have not fully finalized this mechanism and will consider mitigation strategies.

**[gzeon (judge) increased severity to High and commented](https://github.com/code-423n4/2022-10-holograph-findings/issues/44#issuecomment-1320927380):**
 > High risk because potential slashing.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Holograph |
| Report Date | N/A |
| Finders | Lambda  Trust, Chom |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-holograph
- **GitHub**: https://github.com/code-423n4/2022-10-holograph-findings/issues/44
- **Contest**: https://code4rena.com/contests/2022-10-holograph-contest

### Keywords for Search

`Front-Running, Gas Price`

