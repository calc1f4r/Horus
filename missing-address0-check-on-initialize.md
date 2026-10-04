---
# Core Classification
protocol: bitsCrunch - NFTStaking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51254
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/bitscrunch/bitscrunch-smart-contract-assessment
source_link: https://www.halborn.com/audits/bitscrunch/bitscrunch-smart-contract-assessment
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
  - Halborn
---

## Vulnerability Title

Missing Address(0) Check On Initialize

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `initialize` function in the `ContributorNFTStaking` contract lacks validation checks for zero-address inputs for critical parameters such as `_bitscrunchnft` (the NFT contract address) and `_epochManager` (the Epoch Manager contract address). Even if these addresses are checked during script deployment, this oversight may lead to the contract being initialized with invalid addresses, rendering the staking mechanism non-operational and potentially compromising contract integrity.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:F/S:U (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:F/S:U)

##### Recommendation

Incorporate address validation checks within the `initialize` function to ensure non-zero addresses are provided for both the NFT contract and the Epoch Manager contract. This can be achieved by adding the following conditions:

```
require(_bitscrunchnft != address(0), "NFT contract address cannot be zero");
require(_epochManager != address(0), "Epoch Manager address cannot be zero");

```

  

Remediation Plan
----------------

**SOLVED:** The **bitsCrunch team** added address(0) checks.

##### Remediation Hash

<https://github.com/bitscrunch-protocol/smartcontracts/commit/5917c822838694f7d96951ec88286a0c15d82267>

##### References

[bitscrunch-protocol/smartcontracts/contracts/Contributor/NFTStaking/ContributorNFTStaking.sol#L62](https://github.com/bitscrunch-protocol/smartcontracts/blob/main/contracts/Contributor/NFTStaking/ContributorNFTStaking.sol#L62)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | bitsCrunch - NFTStaking |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/bitscrunch/bitscrunch-smart-contract-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/bitscrunch/bitscrunch-smart-contract-assessment

### Keywords for Search

`vulnerability`

