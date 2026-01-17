---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7287
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - don't_update_state
  - business_logic

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

VaultImplementation.buyoutLien does not update the new public vault's parameters and does not transfer assets between the vault and the borrower

### Overview


This bug report is about an issue with the transfer of assets between a vault and a borrower. The severity of this bug is rated as High Risk. The bug is found in the source code of VaultImplementation.sol#L305, LienToken.sol#L102, LienToken.sol#L116 and LienToken.sol#L165-L174. 

The issue is that when VaultImplementation.buyoutLien is called, the accounting for the vault is not updated. This includes the slope, yIntercept and s.epochData[...].liensOpenForEpoch for the new lien's end epoch. The buyout amount is also paid out by the vault itself, and the difference between the new lien amount and the buyout amount is not worked out between the msg.sender and the new vault.

The recommendation for this bug is to update the slope, yIntercept and s.epochData[...].liensOpenForEpoch for the new lien's end epoch if the vault that VaultImplementation.buyoutLien is called into is a public vault. Additionally, the difference between the new lien amount and the buyout amount must be worked out between the msg.sender that called VaultImplementation.buyoutLien and the vault. If the buyout amount is higher than the new lien amount, the msg.sender also needs to transfer some assets (wETH) to the vault. If the new lien amount is higher than the buyout amount, the vault needs to transfer some assets (wETH) to the borrower/msg.sender.

### Original Finding Content

## Severity: High Risk

## Context:
- VaultImplementation.sol#L305
- LienToken.sol#L102
- LienToken.sol#L116
- LienToken.sol#L165-L174

## Description:
`VaultImplementation.buyoutLien` does not update the accounting for the vault (if it's public). The `slope`, `yIntercept`, and `epochData[...].liensOpenForEpoch` (for the new lien's end epoch) are not updated. They are updated for the payee of the swapped-out lien if the payee is a public vault by calling `handleBuyoutLien`. Also, the buyout amount is paid out by the vault itself. The difference between the new lien amount and the buyout amount is not worked out between the `msg.sender` and the new vault.

## Recommendation:
1. If the vault that `VaultImplementation.buyoutLien` endpoint was called into is a public vault, make sure to update its `slope`, `yIntercept`, and `epochData[...].liensOpenForEpoch` (for the new lien's end epoch) when the new lien is created.
2. The difference between the new lien amount and the buyout amount is not worked out between the `msg.sender` that called `VaultImplementation.buyoutLien` and the vault. If the buyout amount is higher than the new lien amount, we need to make sure the `msg.sender` also transfers some assets (wETH) to the vault. And the other way around, if the new lien amount is higher than the buyout amount, the vault needs to transfer some assets (wETH) to the borrower / `msg.sender`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Don't update state, Business Logic`

