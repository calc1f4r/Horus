---
# Core Classification
protocol: LI.FI
chain: everychain
category: logic
vulnerability_type: bypass_limit

# Attack Vector Details
attack_type: bypass_limit
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7055
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
  - bypass_limit
  - business_logic

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

FeeCollector not well integrated

### Overview


The FeeCollector contract is used to pay fees for using the bridge. It is currently being used by crafting a transaction by the frontend API, which then calls the contract via _executeAndCheckSwaps(). This way, no fees are paid if a developer is using the LiFi contracts directly. The issue is that this approach is complicated and non-transparent, and the _executeAndCheckSwaps() function is not well-suited for this purpose. It is also possible that future checks on balances could interfere with the fee payments.

The project has recommended using a dedicated mechanism to pay for fees, and if _executeAndCheckSwaps() is intended to be a multicall mechanism, then it should be renamed. LiFi has acknowledged the risk and encouraged integrators to utilize their API. Spearbit has also acknowledged the issue.

### Original Finding Content

## Severity: Medium Risk

## Context: FeeCollector.sol

### Description
There is a contract to pay fees for using the bridge: **FeeCollector**. This is used by crafting a transaction via the frontend API, which then calls the contract through `_executeAndCheckSwaps()`. 

Here is an example of the contract of such a transaction. It is whitelisted, so no fees are paid if a developer is using the LiFi contracts directly. However, the current mechanism isn't suited for this purpose. The `_executeAndCheckSwaps()` function is geared for swaps and has several checks on balances. These (and future) checks could interfere with fee payments. Additionally, this is a complicated and non-transparent approach. The project has suggested viewing `_executeAndCheckSwaps()` as a multicall mechanism.

### Recommendation
- Use a dedicated mechanism to pay for fees.
- If `_executeAndCheckSwaps()` is intended to be a multicall mechanism, then rename the function.

## LiFi
We acknowledge the risk and encourage integrators to utilize our API at this time.

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

`Bypass limit, Business Logic`

