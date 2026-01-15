---
# Core Classification
protocol: Bretton Woods Digital Gold
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60847
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/bretton-woods-digital-gold/6a607c09-57af-4640-97bd-ee122e1ed0a6/index.html
source_link: https://certificate.quantstamp.com/full/bretton-woods-digital-gold/6a607c09-57af-4640-97bd-ee122e1ed0a6/index.html
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
finders_count: 4
finders:
  - Guillermo Escobero
  - Ruben Koch
  - Jeffrey Kam
  - Gelei Deng
---

## Vulnerability Title

No Documentation on the Funding of the Chainlink Upkeep Contract

### Overview

See description below for full details.

### Original Finding Content

**Update**
The team has provided documentation that the _"system admin needs to maintain a positive balance of LINK tokens in the keepers account"_. We recommend using more active wording, i.e. _"we will assure that the Upkeep will maintain a positive balance"_. In some instances, the words upkeep, keep, keeper, and upkeeper are used interchangeably, we recommend unifying them to Upkeep.

**File(s) affected:**`HotWalletTransferer.sol`

**Description:** As part of a separate exchange platform, the developers plan to launch a Chainlink Upkeep based on the `HotWalletTransferer` contract on the Chainlink Automation Network that enables the funds in some `hotWallet` address to be relatively low but automatically resupplied if it falls below some threshold by transferring over tokens from some `holder` address through an ERC777-operator.

This service offered by the Chainlink Automation Network requires a service fee to be paid in `LINK` for every on-chain call of `performUpkeep()`. If the Upkeep `LINK` balance drops below this amount, the Upkeep will no longer be performed, resulting in the `hotWallet` address no longer being supplied if it drops below a threshold.

Therefore, there should be some documented process in place to assure that the Upkeep continuously has a `LINK` balance exceeding the minimum link balance, even better exceeding that amount by a factor of three to five, as [recommended by Chainlink](https://docs.chain.link/chainlink-automation/manage-upkeeps/#maintain-a-minimum-balance).

**Recommendation:** Document the process to assure that the Upkeep continuously has a high enough `LINK` balance.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Bretton Woods Digital Gold |
| Report Date | N/A |
| Finders | Guillermo Escobero, Ruben Koch, Jeffrey Kam, Gelei Deng |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/bretton-woods-digital-gold/6a607c09-57af-4640-97bd-ee122e1ed0a6/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/bretton-woods-digital-gold/6a607c09-57af-4640-97bd-ee122e1ed0a6/index.html

### Keywords for Search

`vulnerability`

