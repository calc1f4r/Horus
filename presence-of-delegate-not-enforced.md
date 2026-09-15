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
solodit_id: 7151
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/ConnextNxtp-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation
  - delegate

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

Presence of delegate not enforced

### Overview


This bug report is about the BridgeFacet.sol, a contract that allows users to transfer tokens from one chain to another. The issue is that a delegate address on the destination chain can be used to fix stuck transactions, however the presence of a delegate address is not checked in _xcall(). This is considered to be a medium risk issue, as tokens could get lost.

The recommendation is to enforce the presence of a delegate address in _xcall() or at least document the behavior explicitly. It is always necessary to have a delegate if you want to have a strategy for handling destination-side slippage conditions being unfavorable. Without one, users are taking on the bet that unfavorable slippage conditions won't be maintained indefinitely, which could lead to funds being frozen in transit.

The report has been acknowledged and more clarity will be added to the documentation.

### Original Finding Content

## Security Issue Report

**Severity:** Medium Risk  
**Context:** 
- BridgeFacet.sol#L395-L414 
- BridgeFacet.sol#L563-L567 
- BridgeFacet.sol#L337-L369  

**Description:**  
A delegate address on the destination chain can be used to fix stuck transactions by changing the slippage limits and by re-executing transactions. However, the presence of a delegate address isn't checked in `_xcall()`.

**Note:** Set to medium risk because tokens could get lost.

### Relevant Functions:

```solidity
function forceUpdateSlippage(TransferInfo calldata _params, uint256 _slippage) external onlyDelegate(_params) {
    ...
}
```

```solidity
function execute(ExecuteArgs calldata _args) external nonReentrant whenNotPaused returns (bytes32) {
    (bytes32 transferId, DestinationTransferStatus status) = _executeSanityChecks(_args);
    ...
}
```

```solidity
function _executeSanityChecks(ExecuteArgs calldata _args) private view returns (bytes32, DestinationTransferStatus) {
    // If the sender is not an approved relayer, revert
    if (!s.approvedRelayers[msg.sender] && msg.sender != _args.params.delegate) {
        revert BridgeFacet__execute_unapprovedSender();
    }
}
```

**Recommendation:**  
Enforce the presence of a delegate address in `_xcall()`. Or at least document the behavior explicitly.

### Connext:
Yes, it's always going to be necessary to have a delegate if you want to have a strategy for handling destination-side slippage conditions being unfavorable. If you don't have one, you are taking on the bet that unfavorable slippage conditions won't be maintained indefinitely. Some groups see having any EOA or multisig that can impact these parameters as a huge no-no, and requiring one to be defined would be a nonstarter for them. So we allow not providing an option on that front, even if it is more risky and could lead to funds being frozen in transit.  

We should add more clarity around this in the documentation though.

### Spearbit:
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

`Validation, Delegate`

