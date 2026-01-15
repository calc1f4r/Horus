---
# Core Classification
protocol: Ninja Spin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50333
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/seascape/ninja-spin-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/seascape/ninja-spin-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

CONTRACT DOES NOT ALLOW MINTING NFT WITH THE ID 0

### Overview


The bug report states that the `BigBangNFT.sol` contract has a constructor that causes the IDs of the NFTs to start at 1 instead of 0. This may cause issues for some collections that start at ID 0. The impact and likelihood of this bug are both rated as 3 out of 5. The bug has been resolved in a recent commit.

### Original Finding Content

##### Description

The `BigBangNFT.sol` contract constructor contains an `increment` of the counter variable, making the IDs begin on 1.

#### ScapeStore.sol

```
    constructor() public ERC721("BigBang NFT", "BB") {
        nftId.increment();
    }

```

\color{black}
\color{white}

It is known that some collections start at the NFT ID 0.

##### Score

Impact: 3  
Likelihood: 3

##### Recommendation

**SOLVED**: The `Ninja Scape Game` can now start minting NFTs at ID 0. This issue was fixed in commit ID [63f46b35467cd3865416b1dae2aa99ea4363cf63](https://github.com/Seastarinteractive/moonscape-smartcontracts/tree/63f46b35467cd3865416b1dae2aa99ea4363cf63)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Ninja Spin |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/seascape/ninja-spin-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/seascape/ninja-spin-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

