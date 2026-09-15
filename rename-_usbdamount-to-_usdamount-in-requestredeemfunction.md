---
# Core Classification
protocol: Bima
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46151
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/0e4d03d9-b8c4-4cd7-ab20-15a480096d49
source_link: https://cdn.cantina.xyz/reports/cantina_bima_december2024.pdf
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
  - ladboy233
---

## Vulnerability Title

Rename _usbdAmount to _usdAmount in requestRedeemfunction 

### Overview

See description below for full details.

### Original Finding Content

## Design Proposal for BTC Derivatives and USBD Minting

## Context
(No context files were provided by the reviewer)

## Description
The design proposes that users lock BTC derivatives to mint USBD. Users can then stake their USBD to receive Staked USBD, which accrues positive rebasing rewards at a rate set by the protocol owner. 

User can burn their staked USBD and start the redemption process; the protocol will recover USBD from the contract and send both USBD and additional yield to the user.

## Recommendation
It is recommended to rename the `_usbdAmount` parameter to `_usdAmount` to highlight that both USBD and the yield will be sent to the user.

### Function Code
```solidity
function requestRedeem(uint256 _susbdAmount, address _receiver) external returns (uint256 _usbdAmount) {
    susbd.burnFrom(msg.sender, _susbdAmount);
    _usdAmount = _previewRedeem(_susbdAmount);
    emit EventsLib.RequestRedeem(msg.sender, _receiver, _susbdAmount, _usdAmount, block.timestamp);
}
```

## Bima
Fixed in commit `593c8da9`.

## Cantina Managed
Verified. The `_usbdAmount` variable has been renamed to `_usdAmount`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Bima |
| Report Date | N/A |
| Finders | ladboy233 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_bima_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/0e4d03d9-b8c4-4cd7-ab20-15a480096d49

### Keywords for Search

`vulnerability`

