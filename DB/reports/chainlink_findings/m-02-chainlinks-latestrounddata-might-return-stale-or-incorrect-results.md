---
# Core Classification
protocol: Phuture Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2034
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-phuture-finance-contest
source_link: https://code4rena.com/reports/2022-04-phuture
github_link: https://github.com/code-423n4/2022-04-phuture-findings/issues/1

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
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 17
finders:
  - fatimanaz
  - IllIllI
  - reassor
  - 0xkatana
  - WatchPug_
---

## Vulnerability Title

[M-02] Chainlink's `latestRoundData` might return stale or incorrect results

### Overview


This bug report is about the ChainlinkPriceOracle.sol, a Solidity contract, located at the given URL. The issue is that the contract is using latestRoundData, but there is no check if the return value indicates stale data. This could lead to stale prices according to the Chainlink documentation. The proof of concept is the URL provided. This bug does not require any tools to be used. The recommended mitigation steps are to consider adding missing checks for stale data. The example code provided is to check if the BaseAnsweredInRound is greater than or equal to the baseRoundID, and if the quoteAnsweredInRound is greater than or equal to the quoteRoundID, as well as checking that the baseTimestamp and quoteTimestamp are not equal to 0, and that the basePrice and quotePrice are greater than 0.

### Original Finding Content

_Submitted by cccz, also found by 0xDjango, 0xkatana, berndartmueller, defsec, Dravee, fatima_naz, IllIllI, jah, kebabsec, kenta, pedroais, peritoflores, rayn, reassor, tabish, and WatchPug_

On ChainlinkPriceOracle.sol, we are using latestRoundData, but there is no check if the return value indicates stale data.

            (, int basePrice, , , ) = baseAggregator.latestRoundData();
            (, int quotePrice, , , ) = assetInfo.aggregator.latestRoundData();

This could lead to stale prices according to the Chainlink documentation:

<https://docs.chain.link/docs/historical-price-data/#historical-rounds><br>
<https://docs.chain.link/docs/faq/#how-can-i-check-if-the-answer-to-a-round-is-being-carried-over-from-a-previous-round>

### Proof of Concept

[ChainlinkPriceOracle.sol#L83-L84](https://github.com/code-423n4/2022-04-phuture/blob/main/contracts/ChainlinkPriceOracle.sol#L83-L84)<br>

### Recommended Mitigation Steps

Consider adding missing checks for stale data.

For example:

        (uint80 baseRoundID, int256 basePrice, , uint256 baseTimestamp, uint80 BaseAnsweredInRound) = baseAggregator.latestRoundData();
        (uint80 quoteRoundID, int256 quotePrice, , uint256 quoteTimestamp, uint80 quoteAnsweredInRound) = assetInfo.aggregator.latestRoundData();
        require(BaseAnsweredInRound >= baseRoundID && quoteAnsweredInRound >=  quoteRoundID, "Stale price");
        require(baseTimestamp != 0 && quoteTimestamp != 0 ,"Round not complete");
        require(basePrice > 0 && quotePrice > 0,"Chainlink answer reporting 0");

**[olivermehr (Phuture Finance) confirmed](https://github.com/code-423n4/2022-04-phuture-findings/issues/1)**

**[moose-code (judge) commented](https://github.com/code-423n4/2022-04-phuture-findings/issues/1#issuecomment-1135808518):**
 > Confirming medium issue across the board. 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Phuture Finance |
| Report Date | N/A |
| Finders | fatimanaz, IllIllI, reassor, 0xkatana, WatchPug_, cccz, jah, Dravee, 0xDjango, rayn, berndartmueller, pedroais, peritoflores, tabish, kebabsec, kenta, defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-phuture
- **GitHub**: https://github.com/code-423n4/2022-04-phuture-findings/issues/1
- **Contest**: https://code4rena.com/contests/2022-04-phuture-finance-contest

### Keywords for Search

`vulnerability`

