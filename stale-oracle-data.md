---
# Core Classification
protocol: Block
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60652
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/block/75a52b15-92ea-4d24-a91e-811cf93ba287/index.html
source_link: https://certificate.quantstamp.com/full/block/75a52b15-92ea-4d24-a91e-811cf93ba287/index.html
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
finders_count: 4
finders:
  - Danny Aksenov
  - Adrian Koegl
  - Hytham Farah
  - Guillermo Escobero
---

## Vulnerability Title

Stale Oracle Data

### Overview


Summary: A bug was found in the protocol's use of the Chainlink price feed contract. The protocol relies on the `latestRoundData()` function to get the token's price, but this data may be out of date if Chainlink does not update it quickly enough. This can lead to the protocol overvaluing the token in the event of a market drop. The recommendation is to verify the values returned by Chainlink and add a validation for the `updatedAt` value to prevent using outdated data. 

### Original Finding Content

**Update**
Addressed in: `86d0d8895e42e37525b841eb29022365f872963d` and `1164b56be2cbe6850b16ce955356f4b52abb8860`. The client added additional checks for chainlink feed.

**File(s) affected:**`Utils.sol`

**Description:** The protocol just calls `latestRoundData()` to get the ether price from the Chainlink price feed contract. However, the data could be out of date. In the event of a rapid drop in the market price of the token, if Chainlink's feed is not updated in a timely manner, the smart contract may continue to believe that the token is worth more than its actual market value.

**Recommendation:** Verify the values returned by Chainlink oracle ([documentation](https://docs.chain.link/data-feeds/historical-data#getrounddata-return-values)). `timestamp` should not be zero and `answeredInRound` should be equal or greater than `roundID`. Also consider adding a validation for `updatedAt` value and compare it with `block.timestamp + acceptableDelay` to avoid old rounds.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Block |
| Report Date | N/A |
| Finders | Danny Aksenov, Adrian Koegl, Hytham Farah, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/block/75a52b15-92ea-4d24-a91e-811cf93ba287/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/block/75a52b15-92ea-4d24-a91e-811cf93ba287/index.html

### Keywords for Search

`vulnerability`

