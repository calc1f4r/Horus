---
# Core Classification
protocol: Solidex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28138
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Solidex/Solidex/README.md#1-spoofed-initial-deposits-in-sexpartnerssol-and-lpdepositorsol
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
  - MixBytes
---

## Vulnerability Title

Spoofed initial deposits in `SexPartners.sol` and `LpDepositor.sol`

### Overview


This bug report is about a vulnerability in a contract called SexPartners.sol and LpDepositor.sol. This vulnerability allows an attacker to call the function onERC721Received and supply an NFT id that was not actually transferred or owned by the attacker. This may cause the contract to malfunction, leading to a contract unusability or incorrect calculation of rewards. This attack can only affect a contract at the initial stage, before the initial deposit was made, and any spoofing attempts for deposits after the initial deposit will be reverted. To prevent this attack, explicit checks should be added to the contracts.

### Original Finding Content

##### Description
The **initial** deposit of NFT is vulnerable to a spoofing attack.
The attacker can directly call `onERC721Received` and supply NFT id that was not actually transferred/not owned by the attacker. It may cause a contract malfunction, including contract unusability or incorrect calculation of the rewards. A contract malfunction cannot be fixed without a contract replacement.

Please note, this attack can only affect a contract at the initial stage, before the initial deposit was made. Spoofing attempts for any deposits except the initial deposit will be reverted or will not change the state of the contract. Thus a contract at the production stage (after the initial deposit) is not vulnerable anymore.


Location of the affected code:
- https://github.com/solidex-fantom/solidex/blob/8b420ed8bed4b714695d51de2a0f82e38a72e1b2/contracts/SexPartners.sol#L95
- https://github.com/solidex-fantom/solidex/blob/8b420ed8bed4b714695d51de2a0f82e38a72e1b2/contracts/LpDepositor.sol#L351
##### Recommendation
Although an attack can be easily detected and mitigated by redeploying of the contracts, we recommend to add explicit checks for the known attack vector.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Solidex |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Solidex/Solidex/README.md#1-spoofed-initial-deposits-in-sexpartnerssol-and-lpdepositorsol
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

