---
# Core Classification
protocol: Paladin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6871
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - DefSec
  - Jay Jonah8
  - Gerard Persoon
---

## Vulnerability Title

Prevent dual entry point tokens

### Overview

See description below for full details.

### Original Finding Content

## Security Report

## Severity
**Low Risk**

## Context
`QuestBoard.sol#L986-L991`

## Description
The function `recoverERC20()` in contract `QuestBoard.sol` only allows the retrieval of non-whitelisted tokens. Recently, an issue has been found that can circumvent these checks with so-called dual entry point tokens. See a description here: [compound-tusd-integration-issue-retrospective](link-to-description).

```solidity
function recoverERC20(address token, uint256 amount) external onlyOwner returns(bool) {
    require(!whitelistedTokens[token], "QuestBoard: Cannot recover whitelisted token");
    IERC20(token).safeTransfer(owner(), amount);
    return true;
}
```

## Recommendation
Ensure that dual entry point tokens are not whitelisted in the protocol. 

## Paladin
It is noted in our methodology to check if an ERC20 can be whitelisted as a reward token in the protocol to avoid this type of issue.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Paladin |
| Report Date | N/A |
| Finders | DefSec, Jay Jonah8, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

