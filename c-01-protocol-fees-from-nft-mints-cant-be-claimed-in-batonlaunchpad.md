---
# Core Classification
protocol: Baton Launchpad
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26451
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-07-01-Baton Launchpad.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:
  - business_logic

protocol_categories:
  - launchpad

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[C-01] Protocol fees from NFT mints can't be claimed in `BatonLaunchpad`

### Overview


This bug report is about a protocol fee that is sent to the `BatonLaunchpad` contract in the `Nft::mint` method, but there is no way to get the ETH balance out of it. The severity of this bug is high, as it results in a loss of value for the protocol, and the likelihood of it happening is also high. The recommendation for this bug is to add a method by which the `owner` of the contract can withdraw its ETH balance from `BatonLaunchpad`.

### Original Finding Content

**Severity**

**Impact:**
High, as it results in a loss of value for the protocol

**Likelihood:**
High, as it certain to happen

**Description**

In `Nft::mint` the `msg.value` expected is the price of an NFT multiplied by the amount of NFTs to mint plus a protocol fee. This protocol fee is sent to the `BatonLaunchpad` contract in the end of the `mint` method like this:

```solidity
if (protocolFee != 0) {
    address(batonLaunchpad).safeTransferETH(protocolFee);
}
```

`BatonLaunchpad` defines a `receive` method that is marked as `payable`, which is correct. The problem is that in `BatonLaunchpad` there is no way to get the ETH balance out of it - it can't be spent in any way possible, leaving it stuck in the contract forever.

**Recommendations**

In `BatonLaunchpad` add a method by which the `owner` of the contract can withdraw its ETH balance.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Baton Launchpad |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-07-01-Baton Launchpad.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Business Logic`

