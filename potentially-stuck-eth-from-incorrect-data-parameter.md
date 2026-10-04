---
# Core Classification
protocol: Scroll GasSwap, Multiple Verifier, Wrapped Ether and Diff Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32907
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/scroll-gasswap-multiple-verifier-wrapped-ether-and-diff-audit
github_link: none

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
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Potentially Stuck ETH from Incorrect Data Parameter

### Overview


The report discusses a bug in the protocol that allows users to bridge their assets between L1 and L2. The issue arises when the `_executeMessage` function is called and the `_to` address is an EOA or the message is in an incorrect format. This causes the L2 transaction to fail and the user's assets to be stuck on L1. The suggested solution is to add a refund feature for users when the bridging transaction cannot be completed. The Scroll team has acknowledged the bug and stated that they will resolve it by implementing the refund feature.

### Original Finding Content

The protocol allows users to bridge their assets to the L2 rollup and back through the `L1ScrollMessenger` and the `L2ScrollMessenger`. When bridging from L1 to L2, the [`_executeMessage`](https://github.com/scroll-tech/scroll/blob/2eb458cf4224d82fc56254e91e297a9ed261cefb/contracts/src/L2/L2ScrollMessenger.sol#L182) will be called. On [line 198](https://github.com/scroll-tech/scroll/blob/2eb458cf4224d82fc56254e91e297a9ed261cefb/contracts/src/L2/L2ScrollMessenger.sol#L198) of this function, the `_to` address is called and the `_message` is passed to this function. If a user accidentally sets a value in the `_message` field, but either the `_to` address is an EOA, the message is in an incorrect format, or the address is a contract that does not support the data in this field, the user's assets will be stuck on L1, as the L1 transaction has succeeded but the L2 transaction will fail.


The replaying of this message will not help, as the `_message` field cannot be changed for a replay, and assuming that the transaction was not skipped, [`dropMessage`](https://github.com/scroll-tech/scroll/blob/2eb458cf4224d82fc56254e91e297a9ed261cefb/contracts/src/L1/L1ScrollMessenger.sol#L241) cannot be called to get a refund.


To avoid funds being lost when bridging, consider adding a way for users to be refunded when the bridging transaction cannot be completed (for example when the transaction reverts or is skipped), and when the gas limit exceeds the gas effectively consumed.


***Update:** Acknowledged, will resolve. The Scroll team stated that they will resolve the issue:*



> *This will be resolved if we implement the refund feature.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Scroll GasSwap, Multiple Verifier, Wrapped Ether and Diff Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/scroll-gasswap-multiple-verifier-wrapped-ether-and-diff-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

