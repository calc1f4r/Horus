---
# Core Classification
protocol: The Standard
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41594
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clql6lvyu0001mnje1xpqcuvl
source_link: none
github_link: https://github.com/Cyfrin/2023-12-the-standard

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - kodyvim
  - t0x1c
  - haxatron
  - Tricko
  - greatlake
---

## Vulnerability Title

No incentive to liquidate small positions could result in protocol going underwater

### Overview


This bug report discusses a potential issue with the protocol that allows users to create vaults and provide collateral for EUROs without a lower limit. The problem is that there is no incentive for liquidators to liquidate small value vaults due to high gas costs, which could result in the protocol becoming undercollateralized and potentially losing all funds. This has been identified as a high risk issue and has been seen before on similar platforms. The recommended solution is to set a minimum threshold for collateral value to prevent this issue from occurring.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-12-the-standard/blob/main/contracts/SmartVaultV3.sol#L114">https://github.com/Cyfrin/2023-12-the-standard/blob/main/contracts/SmartVaultV3.sol#L114</a>


## Summary
The protocol allows to create vaults and provide collateral for minting EUROs with no lower limit. As such, multiple low value vaults can exist. However, there is no incentive to liquidate low value vaults because of gas cost.

## Vulnerability Details
Liquidators liquidate users for the profit they can make. If there is no profit to be made than there will be no one to call the liquidate function. For example a vault could exist with a very low collateral value. This user is undercollateralized and must be liquidated in order to ensure that the protocol remains overcollateralized. If a liquidator wishes to liquidate this user, they will first need to stake some TST/EUROs which involves gas cost. Because the value of the collateral is so low, after gas costs, liquidators will not make a profit liquidating this user. In the end these low value vaults will never get liquidated, leaving the protocol with bad debt and can even cause the protocol to be undercollateralized with enough small value accounts being underwater.

## Attack Vector & Similar Issues
- See a [similar issue raised in the past](https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/issues/1096) rated as **high impact** & **high likelihood**. It additionally highlights how this can become an attack vector (even by non-whales) on chains which aren't costly. The attack can be done by a malicious actor/group of actors who **_short the protocol and then open multiple such positions to attack the protocol_**.

- [Another description](https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/issues/397) of the same issue.

## Impact
- The protocol can go underwater, complete loss of funds.

## Tools Used
Manual review

## Recommendations
- A potential fix would be to set a minimum threshold for collateral value which has to be exceeded in order for a user to mint EUROs

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Codehawks |
| Protocol | The Standard |
| Report Date | N/A |
| Finders | kodyvim, t0x1c, haxatron, Tricko, greatlake |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-12-the-standard
- **Contest**: https://codehawks.cyfrin.io/c/clql6lvyu0001mnje1xpqcuvl

### Keywords for Search

`vulnerability`

