---
# Core Classification
protocol: BracketX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50787
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/bracket-fi/bracketx-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/bracket-fi/bracketx-smart-contract-security-assessment
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

LACK OF PRICE FEED DECIMALS CHECK

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `PricingSequencer` contract contains the `getLatestPrice()` function to return the latest price from a given Chainlink price feed address. This is intended to be used with USDC pairs, which will return an 8 decimals price which is later on converted to 18 decimals by multiplying it by 1e10. However, a funder can create an offer sending an asset that would return an 18-decimals price; this would lead to the function returning a 28-decimals price.

#### PricingSequencer.sol

```
function getLatestPrice(address asset) override public view returns (uint) {
    // TODO: Add the Sequencer offline check when moving to production
    // this is not supported on the testnet

    if (checkSequencerState()) {
        // If the sequencer is down, do not perform any critical operations
        revert("L2 sequencer down: Chainlink feeds are not being updated");
    }

    //        uint80 roundID,
    //            int price,
    //            uint startedAt,
    //            uint timeStamp,
    //            uint80 answeredInRound
    AggregatorV2V3Interface priceFeed = AggregatorV2V3Interface(asset);
    (, int price, ,,) = priceFeed.latestRoundData();
    return uint256(price).mul(1e10);
}

```

\color{black}
\color{white}

##### Score

Impact: 3  
Likelihood: 1

##### Recommendation

**SOLVED**: The `Bracket.fi team` fixed the issue by adding code to the `setOfferX` function in the `Offersx` contract that checks that oracle uses 8 decimals before setting an offer. Although the code is commented out like oracles, it cannot be tested in local environments. Comments should be removed before deploying to production.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | BracketX |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/bracket-fi/bracketx-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/bracket-fi/bracketx-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

