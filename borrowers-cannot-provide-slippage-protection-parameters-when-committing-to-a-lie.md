---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21845
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf
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

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Saw-Mon and Natalie
  - Jonah1005
  - Blockdev
---

## Vulnerability Title

Borrowers cannot provide slippage protection parameters when committing to a lien

### Overview


This bug report is related to the AstariaRouter.sol#L497-L504 code. When a borrower commits to a lien, AstariaRouter calls the strategy validator to fetch the lien details which include the rate, duration and liquidationInitialAsk. The problem is that the borrower cannot provide slippage protection parameters to make sure these 3 values cannot enter into some undesired ranges. The recommendation is to allow the borrower to provide slippage protection parameters to prevent the details parameters to be set to some undesired values. For rate, the borrower can provide an upper bound. For duration, the borrower can provide a lower and upper bound with the lower bound protection being more important. For liquidationInitialAsk, the borrower can provide a lower and upper bound but the protocol still checks that this value is not less than the to-be-owed amount at the end of the lien's term.

### Original Finding Content

## Severity: Medium Risk

## Context
- **Location**: AstariaRouter.sol#L497-L504

## Description
When a borrower commits to a lien, `AstariaRouter` calls the strategy validator to fetch the lien details:

```solidity
(bytes32 leaf, ILienToken.Details memory details) = IStrategyValidator(
    strategyValidator
).validateAndParse(
    commitment.lienRequest,
    msg.sender,
    commitment.tokenContract,
    commitment.tokenId
);
```

The `details` include:
```solidity
struct Details {
    uint256 maxAmount;
    uint256 rate; // rate per second
    uint256 duration;
    uint256 maxPotentialDebt; // not used anymore
    uint256 liquidationInitialAsk;
}
```

The borrower cannot provide slippage protection parameters to ensure these three values do not enter undesired ranges.

## Recommendation
Allow the borrower to provide slippage protection parameters to prevent the `details` parameters from being set to undesired values:
- **Rate**: Borrower provides an upper bound.
- **Duration**: Borrower can provide lower and upper bounds. Lower bound protection is more important.
- **Liquidation Initial Ask**: Borrower can provide lower and upper bounds. The protocol still checks that this value is not less than the amount owed at the end of the lien's term.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Jonah1005, Blockdev |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf

### Keywords for Search

`vulnerability`

