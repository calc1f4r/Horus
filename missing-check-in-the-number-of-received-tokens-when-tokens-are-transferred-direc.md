---
# Core Classification
protocol: Sudoswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6775
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf
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

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_lending
  - payments

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Max Goodman
  - Mudit Gupta
  - Gerard Persoon
---

## Vulnerability Title

Missing check in the number of Received Tokens when tokens are transferred directly

### Overview


A bug report has been found in the LSSVM\contracts,LSSVMPairERC20.sol#L41-78 code. It is a medium risk bug and is related to the function _validateTokenInput(). This function has two methods to transfer tokens, one with a check on the number of received tokens and the other without a check. This could be exploited by malicious or rebalancing tokens, as seen in the Qubit Finance hack. Spearbit recommends Sudoswap to verify the number of tokens received when these are transferred directly. Sudoswap has acknowledged the risk but no changes are planned at this time. Spearbit has acknowledged this.

### Original Finding Content

## Security Analysis Report

## Severity
**Medium Risk**

## Context
- **Location**: `LSSVM\contracts`, `LSSVMPairERC20.sol#L41-78`

## Description
Within the function `_validateTokenInput()` of `LSSVMPairERC20`, two methods exist to transfer tokens. In the first method, via `router.pairTransferERC20From()`, a check is performed on the number of received tokens. In the second method, no checks are done.

Recent hacks (e.g., Qubit finance) have successfully exploited `safeTransferFrom()` functions which did not revert nor transfer tokens. Additionally, with malicious or re-balancing tokens, the number of transferred tokens might be different from the amount requested to be transferred.

```solidity
function _validateTokenInput(...) ... {
    ...
    if (isRouter) {
        // Call router to transfer tokens from user
        uint256 beforeBalance = _token.balanceOf(_assetRecipient);
        router.pairTransferERC20From(...)
        // Verify token transfer (protect pair against malicious router)
        require(_token.balanceOf(_assetRecipient) - beforeBalance == inputAmount, "ERC20 not transferred in");
    } else {
        // Transfer tokens directly
        _token.safeTransferFrom(msg.sender, _assetRecipient, inputAmount);
    }
}
```

## Recommendation
Spearbit recommends Sudoswap to verify the number of tokens received when these are transferred directly.

## Comments
- **Sudoswap**: Risks acknowledged but no changes at this time. Pair creators would have to willingly deploy an NFT/Token pair for a token using non-standard ERC20 token behavior to be at risk.
- **Spearbit**: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap |
| Report Date | N/A |
| Finders | Max Goodman, Mudit Gupta, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

