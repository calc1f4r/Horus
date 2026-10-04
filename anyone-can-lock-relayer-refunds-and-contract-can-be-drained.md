---
# Core Classification
protocol: Across Protocol SVM Solidity Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56784
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/across-protocol-svm-solidity-audit
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Anyone Can Lock Relayer Refunds and Contract Can Be Drained

### Overview


The `claimRelayerRefund` function in the SpokePool contract is not working as intended. This function allows relayers to claim outstanding repayments in certain situations, but there is a bug that allows malicious relayers to drain the entire balance of the contract. This is because the code uses the wrong key to reset the mapping value, making it possible for relayers to zero out each other's refunds. This bug has been fixed in a recent update.

### Original Finding Content

The `claimRelayerRefund` [function](https://github.com/across-protocol/contracts/blob/401e24ccca1b3af919dd521e58acd445297b65b6/contracts/SpokePool.sol#L1265) is meant to give relayers the option to claim outstanding repayments. This can happen in different edge cases, like blacklists not allowing token transfers. In such cases, the relayer can call this function and specify a different `refundAddress` to claim their funds.

The function [first](https://github.com/across-protocol/contracts/blob/401e24ccca1b3af919dd521e58acd445297b65b6/contracts/SpokePool.sol#L1266) reads the current outstanding refund from the `relayerRefund` mapping using the `l2TokenAddress` and `msg.sender` keys. If this value is greater than 0 then it is [transferred](https://github.com/across-protocol/contracts/blob/401e24ccca1b3af919dd521e58acd445297b65b6/contracts/SpokePool.sol#L1269) to the `refundAddress` and the appropriate event is emitted.

Before transferring out the tokens, the mapping value is [set](https://github.com/across-protocol/contracts/blob/401e24ccca1b3af919dd521e58acd445297b65b6/contracts/SpokePool.sol#L1268) to 0 for correct accounting. However, the key used to reset the mapping value is `refundAddress` and not `msg.sender`. This opens the door for any relayer with a small refund amount to zero out any other relayer's refund by specifying their `refundAddress`, effectively making the relayers lose their refunds. In addition, since the original mapping value is never reset, a malicious relayer can exploit this by repeatedly calling the function to drain the entire balance of the `l2TokenAddress` contract.

Consider using the proper `msg.sender` key instead of `refundAddress` to correctly set the refund amount to zero.

***Update:** Resolved in [pull request #826](https://github.com/across-protocol/contracts/pull/826). The code correctly resets the mapping value now.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Across Protocol SVM Solidity Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/across-protocol-svm-solidity-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

