---
# Core Classification
protocol: Florence Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20566
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-04-01-Florence Finance.md
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
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[M-01] The Chainlink price feed's input is not properly validated

### Overview


This bug report is about the code in `LoanVault::getFundingTokenExchangeRate`, which uses a Chainlink price oracle to retrieve the asset price. The code does not check if the answer received was actually a stale one, which can lead to wrong calculations in the vault shares math and can result in an exploit from a bad actor. The impact of this bug is high, but the likelihood is low as Chainlink oracles are mostly reliable.

The report recommends changing the code to check for negative price (as it is of type `int256`) and also for stale price. To implement the pausing mechanism, some other changes will be needed as well, or the code can just revert there.

### Original Finding Content

**Impact:**
High, as it can result in the application working with an incorrect asset price

**Likelihood:**
Low, as Chainlink oracles are mostly reliable, but there has been occurrences of this issue before

**Description**

The code in `LoanVault::getFundingTokenExchangeRate` uses a Chainlink price oracle in the following way:

```solidity
(, int256 exchangeRate, , , ) = fundingTokenChainLinkFeeds[fundingToken].latestRoundData();

if (exchangeRate == 0) {
    revert Errors.ZeroExchangeRate();
}
```

This has some validation but it does not check if the answer (or price) received was actually a stale one. Reasons for a price feed to stop updating are listed [here](https://ethereum.stackexchange.com/questions/133242/how-future-resilient-is-a-chainlink-price-feed/133843#133843). Using a stale price in the application can result in wrong calculations in the vault shares math which can lead to an exploit from a bad actor.

**Recommendations**

Change the code in the following way:

```diff
- (, int256 exchangeRate, , , ) = fundingTokenChainLinkFeeds[fundingToken].latestRoundData();
+ (, int256 exchangeRate, , uint256 updatedAt , ) = fundingTokenChainLinkFeeds[fundingToken].latestRoundData();

- if (exchangeRate == 0) {
+ if (exchangeRate <= 0) {
    revert Errors.ZeroExchangeRate();
}

+ if (updatedAt < block.timestamp - 60 * 60 /* 1 hour */) {
+   pause();
+}
```

This way you will also check for negative price (as it is of type `int256`) and also for stale price. To implement the pausing mechanism I proposed some other changes will be needed as well, another option is to just revert there.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Florence Finance |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-04-01-Florence Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

