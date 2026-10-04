---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7315
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - business_logic

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

Call to Royalty Engine can block NFT auction

### Overview


This bug report is about the CollateralToken.sol#L481. It states that the function _generateValidOrderParameters() calls the ROYALTY_ENGINE.getRoyaltyView() twice. The first call is wrapped in a try/catch, which allows Astaria to continue even if the getRoyaltyView() reverts. The second call, however, is not safe from this. Both calls have the same parameters passed to it, except for the price (startingPrice vs endingPrice). If these are different, there is a possibility that the second call can revert.

The recommendation is to wrap the second call in a try/catch. If it reverts, the execution will be transferred to an empty catch block. Astaria has acknowledged this and has a change pending that removes the royalty engine as part of multi token. Spearbit has also acknowledged this.

### Original Finding Content

## Severity: Medium Risk

## Context
`CollateralToken.sol#L481`

## Description
`_generateValidOrderParameters()` calls `ROYALTY_ENGINE.getRoyaltyView()` twice. The first call is wrapped in a try/catch. This allows Astaria to continue even if the `getRoyaltyView()` reverts. However, the second call is not safe from this.

Both these calls have the same parameters passed to them except the price (`startingPrice` vs `endingPrice`). In case they are different, there exists a possibility that the second call can revert.

## Recommendation
Wrap the second call in a try/catch. In case of a revert, the execution will be transferred to an empty catch block. Here is a sample:

```solidity
if (foundRecipients.length > 0) {
    try
        s.ROYALTY_ENGINE.getRoyaltyView(
            underlying.tokenContract,
            underlying.tokenId,
            endingPrice
        ) returns (, uint256[] memory foundEndAmounts) {
            recipients = foundRecipients;
            royaltyStartingAmounts = foundAmounts;
            royaltyEndingAmounts = foundEndAmounts;
        } catch {}
}
```

## Astaria
Acknowledged. We have a change pending that removes the royalty engine as a part of multi token.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic`

