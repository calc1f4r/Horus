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
solodit_id: 44056
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

[L-08] Missing `bytes32(0)` Check For `_jobid` Parameter in The `ChainlinkOracle.sol` Constructor And `setJobId()` Function

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

The current implementation allows for `_jobId` to be empty bytes set in the constructor and `setJobId()` function, which might lead to a wrong `jobId` verification.

## Location of Affected Code

File: [contracts/ChainlinkOracle.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkOracle.sol)

```solidity
constructor(
  address _tokenAddress,
  bytes32 _jobid,
  address _operator,
  uint256 _fee,
  address _lightClient
) ConfirmedOwner(msg.sender) {

function setJobId(bytes32 _jobId) public onlyOwner {
```

## Recommendation

Consider implementing a check for empty bytes.

```diff
+ error InvalidInputEmptyBytes32();

constructor(
  address _tokenAddress,
  bytes32 _jobid,
  address _operator,
  uint256 _fee,
  address _lightClient
) ConfirmedOwner(msg.sender) {
+ if (_jobId == bytes32(0)) revert InvalidInputEmptyBytes32();
}

function setJobId(bytes32 _jobId) public onlyOwner {
+ if (_jobId == bytes32(0)) revert InvalidInputEmptyBytes32();
}
```

## Team Response

Acknowledged and fixed by adding a non-zero verification when setting `_jobId`.

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

