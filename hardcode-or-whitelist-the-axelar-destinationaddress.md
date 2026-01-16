---
# Core Classification
protocol: LI.FI
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7046
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
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
  - hardcoded_address

protocol_categories:
  - dexes
  - bridge
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Jonah1005
  - DefSec
  - Gerard Persoon
---

## Vulnerability Title

Hardcode or whitelist the Axelar destinationAddress

### Overview


This bug report is regarding a medium risk issue found in the AxelarFacet.sol#L30-L89 code. The functions executeCallViaAxelar() and executeCallWithTokenViaAxelar() call a destinationAddress on the destinationChain. The destinationAddress needs to have specific Axelar functions ( _execute() and_executeWithTokento()) in order to receive the calls. These functions are implemented in the Executor. If these functions do not exist at the destinationAddress, the transferred tokens will be lost. The comment for the parameter destinationAddress is not clear and it could be either the LiFi Diamond or the Executor. 

The recommendation to fix this issue is to hardcode or whitelist the destinationAddress and to doublecheck the comment for the destinationAddress for both functions. LiFi acknowledges the risk and recommends all users to utilize their API in order to pass correct data and pass invalid contract addresses at their own risk. Spearbit has acknowledged this recommendation.

### Original Finding Content

## Severity: Medium Risk

## Context
AxelarFacet.sol#L30-L89

## Description
The functions `executeCallViaAxelar()` and `executeCallWithTokenViaAxelar()` call a `destinationAddress` on the `destinationChain`. This `destinationAddress` needs to have specific Axelar functions (`_execute()` and `_executeWithTokento()`) to be able to receive the calls. This is implemented in the Executor. If these functions don’t exist at the `destinationAddress`, the transferred tokens will be lost.

```solidity
/// @param destinationAddress the address of the LiFi contract on the destinationChain
function executeCallViaAxelar(..., string memory destinationAddress, ...) ... {
    ...
    s.gateway.callContract(destinationChain, destinationAddress, payload);
}
```

**Note:** The comment "the address of the LiFi contract" isn’t clear; it could either be the LiFi Diamond or the Executor.

## Recommendation
Hardcode or whitelist the `destinationAddress`. Doublecheck the `@param` comment for `destinationAddress` (for both functions).

## LiFi
We acknowledge the risk and recommend all users utilize our API in order to pass correct data and enter invalid contract addresses at their own risk.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | LI.FI |
| Report Date | N/A |
| Finders | Jonah1005, DefSec, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation, Hardcoded Address`

