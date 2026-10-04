---
# Core Classification
protocol: Darkmythos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44029
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/DarkMythos-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[L-02] Missing Zero Value Check for `_mintingCost` Might Lead to Loss of Funds

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

The `_mintingCost` variable in the constructor is missing a zero-value check. This variable serves as a fundamental parameter in the protocol's operation, dictating the cost associated with minting tokens. If it is set to 0 by mistake, the protocol's business logic could be severely impacted, as there will be no minting tax fees.

## Location of Affected Code

File: [`contracts/DarkMythos.sol#L77`](https://gitlab.vettersolutions.de/dark-mythos/web3-academy-smart-contract/-/blob/45d9a7fbccb7a647f649a3a14f9d3f2bfa1c5f73/contracts/DarkMythos.sol#L77)

```solidity
constructor(
  string memory _name,
  string memory _symbol,
  string memory _baseURI_,
  uint256 _mintingCost,
  uint256 _numberOfTokensPerMint,
  uint256 _maxBulkBuy,
  uint256 _maxMints,
  uint256 _allowMintingAfter,
  address _vendor
)
  ERC721(_name, _symbol)
{

.
.

  mintingCost = _mintingCost;
}
```

## Recommendation

To address this vulnerability, consider adding a check so that it is not possible for `_mintingCost` to be `0`.

```diff
constructor(
  string memory _name,
  string memory _symbol,
  string memory _baseURI_,
  uint256 _mintingCost,
  uint256 _numberOfTokensPerMint,
  uint256 _maxBulkBuy,
  uint256 _maxMints,
  uint256 _allowMintingAfter,
  address _vendor
)
  ERC721(_name, _symbol)
{
+ require(_mintingCost != 0, "@dev: mintingCost must not equal zero");

.
.

  mintingCost = _mintingCost;
}
```

## Team Response

Acknowledged and fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Darkmythos |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/DarkMythos-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

