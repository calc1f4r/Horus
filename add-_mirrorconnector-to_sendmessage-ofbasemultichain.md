---
# Core Classification
protocol: Connext
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7140
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Xiaoming90
  - Blockdev
  - Gerard Persoon
  - Sawmon and Natalie
  - Csanuragjain
---

## Vulnerability Title

Add _mirrorConnector to_sendMessage ofBaseMultichain

### Overview


This bug report is about the function _sendMessage() of BaseMultichain in the context of multichain cross-chain. The function sends the message to the address of the _amb, which is not the intended behavior. The first parameter should be the _mirrorConnector instead. The recommendation is to doublecheck the conclusion and change the code accordingly. The issue has been solved in PR 2386 and verified.

### Original Finding Content

## High Risk Report

## Severity: High Risk

### Context
BaseMultichain.sol#L39-L47

### Description
The function `_sendMessage()` of `BaseMultichain` sends the message to the address of the `_amb`. This doesn't seem right as the first parameter is the target contract to interact with according to multichain cross-chain. This should probably be the `_mirrorConnector`.

```solidity
function _sendMessage(address _amb, bytes memory _data) internal {
    Multichain(_amb).anyCall(
        _amb, // Same address on every chain, using AMB as it is immutable
        ...
    );
}
```

### Recommendation
Doublecheck the conclusion and change the code to:

```solidity
- function _sendMessage(address _amb, bytes memory _data) ... {
+ function _sendMessage(address _amb, address _mirrorConnector, bytes memory _data) ... {
    Multichain(_amb).anyCall(
        - _amb,
        + _mirrorConnector
        ...
    );
}
```

### Connext
Solved in PR 2386.

### Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | Xiaoming90, Blockdev, Gerard Persoon, Sawmon and Natalie, Csanuragjain |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation`

