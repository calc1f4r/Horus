---
# Core Classification
protocol: Sushi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19620
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf
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
  - yield
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

sgReceive Could Run Out of Gas

### Overview


The development team found a potential bug in the Stargate's tosgReceive() function. If the call were to revert, the tokens transferred from Stargate would be left in the SushiXSwap contract on the destination chain, and any user could transfer them away freely. This could happen if the sequence of actions in the payload is too long and complex, causing the transaction to run out of gas. 

To mitigate this, the team recommends checking that large payload values are not sent in with insufficient gas. They also suggest setting an explicit gas limit on the trycall on line 91. If the limit is reached, the transaction will execute the catch block, and if there is no explicit gas value, the entire transaction reverts if it runs out of gas. However, this wastes gas, as the exitGas state variable would be excess gas sent to every call to sgReceive, regardless of whether it runs out of gas or not. The value should be high enough to ensure execution of the rest of the sgReceive() function.

### Original Finding Content

## Description

The development team pointed out that, if the call by Stargate to `sgReceive()` were to revert, the tokens transferred from Stargate would be left in the SushiXSwap contract on the destination chain, where they could be transferred away freely by any user.

One possible condition under which this transaction could revert is if the sequence of actions in the payload is long and complex enough that the transaction runs out of gas.

## Recommendations

This can be mitigated by carefully checking that large payload values are not sent in with insufficient gas. A more programmatic approach to mitigate this would be to set an explicit gas limit on the `try` call on line [91]. If there is an explicit gas limit set in the `try` call, the transaction will execute the `catch` block when this limit is reached. If there is no explicit gas value, then the entire transaction reverts if it runs out of gas.

```solidity
uint256 limit = gasleft() - exitGas;
try
    ISushiXSwap(payable(address(this))).cook{gas: limit}(actions, values, datas)
{} catch (bytes memory) {
    IERC20(_token).safeTransfer(to, amountLD);
}
```

This does waste gas, however, as the `exitGas` state variable would be excess gas sent to every call to `sgReceive`, regardless of whether it ran out of gas or not. This value would need to be high enough to ensure execution of the rest of the `sgReceive()` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf

### Keywords for Search

`vulnerability`

