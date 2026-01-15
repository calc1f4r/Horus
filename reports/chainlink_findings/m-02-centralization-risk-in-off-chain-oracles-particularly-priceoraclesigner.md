---
# Core Classification
protocol: Hook
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18711
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-04-15-Hook.md
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
  - Zach Obront
---

## Vulnerability Title

[M-02] Centralization risk in off chain oracles (particularly priceOracleSigner)

### Overview


This bug report is about the protocol that uses two off-chain oracles to verify asset prices and allow gasless cancellations. The first oracle, `priceOracleSigner`, submits the asset prices used in the Black Scholes calculation for option value. If a malicious actor were to gain control of this wallet, they could drain all the funds from every user with open bids by submitting high spot price values. The second oracle, `orderValidityOracleSigner`, submits confirmation that the buyer has not gaslessly cancelled their order. If a malicious actor were to gain control of this wallet, they could execute cancelled transactions, forcing buyers to buy assets they did not intend to. 

The report recommends that for `orderValidityOracleSigner`, the feature of gasless cancellations should be weighed against the key compromise risk. For `priceOracleSigner`, it is recommended to use a reputable, decentralized oracle such as Chainlink. However, Chainlink's NFT Floor Price feeds are only limited to 10 NFTs at the moment. The report was acknowledged. 

In conclusion, this bug report is about two off-chain oracles used by the protocol. It is suggested that for `orderValidityOracleSigner`, the feature of gasless cancellations should be weighed against the key compromise risk. For `priceOracleSigner`, it is recommended to use a reputable, decentralized oracle such as Chainlink. However, Chainlink's NFT Floor Price feeds are only limited to 10 NFTs at the moment.

### Original Finding Content

The protocol uses two off chain oracles to (a) verify asset prices and (b) allow gasless cancellations.

Each of these off chain signers pose a centralization risk for the protocol:

- `priceOracleSigner`: This signer submits the asset prices used in the Black Scholes calculation for option value. If a malicious actor were to get control of this wallet, they could drain all the funds from every the wallet of every user with open bids by submitting high spot price values that would push the option value up.

- `orderValidityOracleSigner`: This signer submits confirmation that the buyer has not gaslessly cancelled their order, and it is therefore valid to execute. If a malicious actor were to get control of this wallet, they could execute cancelled transactions, forcing buyers to buy assets they did not intend to.

Both off chain signers have their risks, but the `orderValidityOracleSigner` seems to be accomplishing an important goal (gasless cancellations) and the downsides are limited: orders that have no yet expired can be executed within the originally defined bounds, based on the accurate asset price.

The `priceOracleSigner`, on the other hand, seems to create an undue risk for users.

**Recommendation**

For `orderValidityOracleSigner`, consider whether the feature of gasless cancellations is worth the key compromise risk.

For `priceOracleSigner`, it is recommended to use a reputable, decentralized oracle such as Chainlink for such an important source of data. Unfortunately, [Chainlink's NFT Floor Price](https://docs.chain.link/data-feeds/nft-floor-price/addresses/) feeds are limited to only 10 NFTs at the moment, so I understand that this would pose a major trade off for the protocol.

**Review**

Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Hook |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-04-15-Hook.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

