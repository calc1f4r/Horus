---
# Core Classification
protocol: Bundles/Airdrop
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50304
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/nftfi/bundles-airdrop-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/nftfi/bundles-airdrop-smart-contract-security-assessment
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

MISSING PARAMETER VALIDATION

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `childContractByIndex` and `childTokenByIndex` functions of the `ERC998TopDown` contract did not validate their parameters. Setting invalid values may result in reverts without error messages.

`contracts/NftfiBundler.sol`:

* The constructor of the contract does not validate that the `_permittedNfts` parameter is not a zero address.
* The constructor of the contract does not validate that the `_airdropFlashLoan` parameter is not a zero address.

`contracts/ImmutableBundle.sol`:

* The constructor of the contract does not validate that the `_bundler` parameter is not a zero address.
* The constructor of the contract does not validate that the `_personalBundlerFactory` parameter is not a zero address.

`contracts/PersonalBundlerFactory.sol`:

* The constructor of the contract does not validate that the `_personalBundlerImplementation` parameter is not a zero address.

`contracts/ERC998TopDown.sol`:

* The `childContractByIndex` function does not validate that the `_index` parameter is a valid index.
* The `childTokenByIndex` function does not validate that the `_index` parameter is a valid index.

`contracts/utils/Ownable.sol`:

* The constructor of the contract does not validate that the `_initialOwner` parameter is not a zero address.

##### Score

Impact: 2  
Likelihood: 2

##### Recommendation

**RISK ACCEPTED**: The `NFTfi team` accepted the risk of this finding.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Bundles/Airdrop |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/nftfi/bundles-airdrop-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/nftfi/bundles-airdrop-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

