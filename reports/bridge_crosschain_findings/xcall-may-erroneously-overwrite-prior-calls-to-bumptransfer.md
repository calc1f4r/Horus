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
solodit_id: 7232
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

xcall() may erroneously overwrite prior calls to bumpTransfer()

### Overview


This bug report is about the bumpTransfer() function in the BridgeFacet.sol code. This function allows users to increase the relayer fee on a given transferId without checking if the transferId is valid. This can lead to lost funds when a subsequent call to xcall() is made. It is recommended to add a check in bumpTransfer() to make sure the transferId exists. Alternatively, it may be more efficient to modify xcall() such that the s.relayerFees is increased instead of being overridden. This issue has been solved in PR 1643 and verified by Spearbit. However, there is still a risk that bumpTransfer() allows adding funds to an invalid transferId, which is similar to transferring tokens to the wrong address.

### Original Finding Content

## Medium Risk Report

## Severity 
Medium Risk

## Context 
- BridgeFacet.sol#L380-L386
- BridgeFacet.sol#L313

## Description 
The `bumpTransfer()` function allows users to increment the relayer fee on any given `transferId` without checking if the unique transfer identifier exists. As a result, a subsequent call to `xcall()` will overwrite the `s.relayerFees` mapping, leading to lost funds.

## Recommendation 
Consider adding a check in `bumpTransfer()` to ensure `_transferId` exists. This mitigation can be implemented in a similar fashion to `PromiseRouter.bumpCallbackFee()`. It is important to note that checking for a non-zero `s.relayerFees` is not sufficient as `xcall()` accepts zero values. Alternatively, it may be more succinct to modify `xcall()` such that `s.relayerFees` is incremented instead of overridden.

## Connext 
Solved in PR 1643.

## Spearbit 
Verified.

## Note 
Remaining risk: `bumpTransfer()` allows adding funds to an invalid `transferId`. This is comparable to transferring tokens to the wrong address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | 0xLeastwood, Jonah1005 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation`

