---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17906
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Di�ferences between public repository, deployed contracts, and private repository

### Overview

See description below for full details.

### Original Finding Content

## Data Validation Report

**Type:** Data Validation  
**Target:** Frax.sol  

---

**Difficulty:** Low  

**Description**  
The Frax Finance team provided Trail of Bits with a list of deployed contract addresses to review in addition to commits `3f0993` and `6e0352` of the FraxFinance/frax-solidity repository. The Frax Finance team also mentioned a second private repository. During our review, we identified discrepancies between certain deployed contracts and the versions of those contracts in the repository. This resulted in cross-checking overhead.

**Exploit Scenario**  
Reviewer Alice performs an audit of the file `Frax.sol` at commit `3f0993`. It differs from the version of the contract deployed on Etherscan. As a result, Alice’s findings may be outdated, or she may overlook issues present in the newer version.

**Recommendations**  
- **Short term:** Clearly communicate the differences between the public repository and the deployed contracts to auditors. If possible, instruct auditors to work either solely from the contracts deployed on Etherscan or solely from the repository.  

- **Long term:** Maintain consistency between deployed contracts and their files in the Git repository. Each time a contract is deployed to the mainnet, “freeze” the file and its dependencies in GitHub. Instead of modifying the file of the deployed version, create a copy with a suffix (e.g., V2, V3, etc.) and work on that version until it is deployed to the mainnet. Then, repeat the process. This will simplify future reviews and increase their precision.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels, Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf

### Keywords for Search

`vulnerability`

