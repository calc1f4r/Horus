---
# Core Classification
protocol: Futaba
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44043
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Futaba-Security-Review.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.20
financial_impact: high

# Scoring
quality_score: 1
rarity_score: 2

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[C-02] Protocol Misses Upgradability Mechanism, Hindering the Proper Implementation of The Custom Relayer

### Overview


The `Gateway.sol` contract currently only allows queries from the Gelato relayer, which goes against the protocol's future plans to have an independent relayer. This is due to a modifier in the `receiveQuery()` function and the contract is also not upgradeable. Additionally, the `estimateFee()` function always returns 0 and cannot be changed. The team recommends exploring upgradeability options, specifically the UUPS upgradeability pattern, to align with the protocol's vision and allow for future adjustments. The team has acknowledged the issue and plans to fix it by adding a custom relayer and implementing the UUPS upgradeability pattern.

### Original Finding Content

## Severity

Critical Risk

## Description

The current implementation of the `Gateway.sol` contract restricts the reception of queries exclusively to the Gelato relayer. This is not in alignment with the protocol's broader vision, as stated in the documentation, which includes the intention to develop an independent relayer in the future.

This limitation stems from the `onlyGelatoRelayERC2771` modifier imposed on the `receiveQuery()` function, which mandates interactions exclusively from the designated Gelato relayer. Additionally, the current contract lacks upgradeability, rendering it immutable and impervious to any form of modification.

Furthermore, the `estimateFee()` function's current implementation returns 0. Since there is no corresponding setter function for the fee, there will not be a possibility for it to be changed, upon implementing the custom relayer. 

This modification aligns with the protocol's future goals and lays the groundwork for the potential development of an independent relayer.

## Location of affected code

File: [contracts/Gateway.sol#L206](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/Gateway.sol#L206)

```solidity
function receiveQuery(
  QueryType.QueryResponse memory response
) external payable onlyGelatoRelayERC2771 {
```

## Recommendation

Exploring upgradeability options for the `Gateway.sol` contract is a prudent step towards enabling future adjustments and enhancements. This strategy not only aligns with the protocol's long-term vision but also ensures the contract's adaptability and scalability in response to evolving requirements.

While weighing the advantages and disadvantages, it's crucial to approach the topic with diligence. We would recommend sticking to the UUPS upgradeability pattern. For further insights, you may refer to these insightful articles: [Proxies - UUPSUpgradeable](https://docs.openzeppelin.com/contracts/4.x/api/proxy#UUPSUpgradeable) and [Using uups proxy pattern upgrade smart contracts](https://blog.logrocket.com/using-uups-proxy-pattern-upgrade-smart-contracts/).

## Team Response

Acknowledged. Will be fixed by adding a custom relayer and UUPS upgradeability pattern.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 1/5 |
| Rarity Score | 2/5 |
| Audit Firm | Shieldify |
| Protocol | Futaba |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Futaba-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

