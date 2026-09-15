---
# Core Classification
protocol: Futaba
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44055
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Futaba-Security-Review.md
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

[L-07] Missing Zero Address Checks

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

The functions `setOracle()`, `setClient()`, `setLinkToken()`, `setOracle()` and `constructor(_tokenAddress, address _operator, address _lightClient)` of `ChainlinkOracle.sol` do not perform verification to ensure that no addresses provided as parameters are the zero addresses. Consequently, there is a risk of accidentally setting an eligible holder's address to the zero address, leading to unintended behavior or potential vulnerabilities in the future.

## Location of Affected Code

File: [contracts/ChainlinkLightClient.sol#L278](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkLightClient.sol#L278)

```solidity
function setOracle(address _oracle) public onlyOwner {
```

File: [contracts/ChainlinkOracle.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkOracle.sol)

```solidity
constructor(
  address _tokenAddress,
  bytes32 _jobid,
  address _operator,
  uint256 _fee,
  address _lightClient
) ConfirmedOwner(msg.sender) {

function setClient(address _client) public onlyOwner {

function setLinkToken(address _tokenAddress) public onlyOwner {

function setOracle(address _oracle) public onlyOwner {
```

## Recommendation

Consider adding a check to ensure that the provided address is not the zero address.

File: [contracts/ChainlinkOracle.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkOracle.sol)

```diff
+ error InvalidInputZeroAddress();

constructor(
  address _tokenAddress,
  bytes32 _jobid,
  address _operator,
  uint256 _fee,
  address _lightClient
) ConfirmedOwner(msg.sender) {
+ if (_tokenAddress == address(0)) revert InvalidInputZeroAddress();
+ if (_operator == address(0)) revert InvalidInputZeroAddress();
+ if (_lightClient == address(0)) revert InvalidInputZeroAddress();
}

function setClient(address _client) public onlyOwner {
+ if (_client == address(0)) revert InvalidInputZeroAddress();
}

function setLinkToken(address _tokenAddress) public onlyOwner {
+ if (_tokenAddress == address(0)) revert InvalidInputZeroAddress();
}

function setOracle(address _oracle) public onlyOwner {
+ if (_oracle == address(0)) revert InvalidInputZeroAddress();
}
```

## Team Response

Acknowledged and fixed by adding a custom error of `ZERO ADDRESS` to each function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Futaba |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Futaba-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

