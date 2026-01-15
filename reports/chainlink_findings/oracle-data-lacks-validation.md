---
# Core Classification
protocol: Ion Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32712
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/ion-protocol-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Oracle Data Lacks Validation

### Overview


This bug report discusses an issue with the Ion Protocol codebase where certain functions that use on-chain oracles to retrieve price data do not have proper validation in place. This means that the data returned by these oracles may not be accurate or recent. The report suggests adding checks to validate the data to ensure it is not zero and is recent. However, the Ion Protocol team has acknowledged the issue but has not yet resolved it. They state that even if the oracle returns a zero value, it will not cause any loss of funds for users. They also mention that they will monitor the oracle behavior offchain and pause when necessary.

### Original Finding Content

Throughout the [codebase](https://github.com/Ion-Protocol/ion-protocol/tree/98e282514ac5827196b49f688938e1e44709505a/), there are several functions that use on-chain oracles to retrieve price data. These oracles consistently lack validation of the returned data. In particular:


* The `WstEthSpotOracle` contract uses a Chainlink oracle to get the [price of stETH in ETH](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/oracles/spot/WstEthSpotOracle.sol#L38) within the `getPrice` function.
* The `EthXSpotOracle` contract uses a Redstone oracle to get the [price of ETHx in USD](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/oracles/spot/EthXSpotOracle.sol#L42) and a Chainlink oracle to get the [price of ETH in USD](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/oracles/spot/EthXSpotOracle.sol#L45) within the `getPrice` function.


Consider adding checks which validate the returned data to ensure a non-zero price is returned and that the price is recent.


***Update:** Acknowledged, not resolved. Ion Protocol team stated:*



> *Please refer to the M-07 response stating that underreported and overreported spot oracle values do not cause user loss of funds.*
> 
> 
> *The suggested validation above is to check the returned value against a zero value. However, even if the oracle returns a zero value, the zero value will simply not allow any issuance of debt and therefore is not a risk for the protocol. Therefore validating the zero value or not validating the zero value does not introduce a meaningful difference to user safety.*
> 
> 
> *As stated in M-07, similar malfunctioning of oracle behavior will be monitored offchain to trigger pauses when necessary.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Ion Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/ion-protocol-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

