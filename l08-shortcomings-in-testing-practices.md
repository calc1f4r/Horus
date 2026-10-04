---
# Core Classification
protocol: Compound Open Price Feed – Uniswap Integration Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11394
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/compound-open-price-feed-uniswap-integration-audit/
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
  - dexes
  - cdp
  - services
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[L08] Shortcomings in testing practices

### Overview

See description below for full details.

### Original Finding Content

While doing a general review of the test suite of the project, a number of shortcomings were identified. In particular:


* There is no automated test coverage report. Without this report it is impossible to know whether there are parts of the code never executed by the automated tests; so for every change, a full manual test suite has to be executed to make sure that nothing is broken or misbehaving.
* There are relevant contracts and functions of the system that lack of unit tests. Some examples of this are [the `invalidateReporter` function](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/contracts/Uniswap/UniswapAnchoredView.sol#L258), some sections of the [`postPrices` function](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/contracts/Uniswap/UniswapAnchoredView.sol#L135) (specifically when calculating the anchor price of other assets aside from ETH), and the entire [`FixedPoint` library](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/contracts/Uniswap/UniswapLib.sol#L6-L29).
* Both unit and integration tests are placed in the same [`tests`](https://github.com/compound-finance/open-oracle/tree/d0a0d0301bff08457d9dfc5861080d3124d079cd/tests) directory and are executed together.
* After following the instructions in the [README file](https://github.com/compound-finance/open-oracle/blob/master/README.md) of the project, tests may fail due to Docker configuration errors that are not contemplated in the instructions.
* There are modifications in the architecture of the code only implemented for testing purposes, such as setting the [`fetchAnchorPrice` function](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/contracts/Uniswap/UniswapAnchoredView.sol#L203) as `virtual` in order to override its functionality in the [`MockUniswapAnchoredView`](https://github.com/compound-finance/open-oracle/blob/d0a0d0301bff08457d9dfc5861080d3124d079cd/tests/contracts/MockUniswapAnchoredView.sol#L21)  mock contract.


Having a healthy, well documented and comprehensive test suite is of utter importance for the project’s overall quality, helping specify the expected behavior of the system and identify bugs early in the development process.


Consider thoroughly reviewing the test suite to make sure all tests run successfully after following the instructions in the [README file](https://github.com/compound-finance/open-oracle/blob/master/README.md). Introducing an automated code coverage report is highly advised, so as to ensure all relevant functionality is rigorously tested, taking into consideration that code should only be merged if it neither breaks the existing tests nor decreases coverage. Additionally, consider running the unit tests and integration tests separately, defining different environments for each of them.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Compound Open Price Feed – Uniswap Integration Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/compound-open-price-feed-uniswap-integration-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

