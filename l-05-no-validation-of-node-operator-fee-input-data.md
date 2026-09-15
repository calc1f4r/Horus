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
solodit_id: 44053
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

[L-05] No Validation Of Node Operator `fee` Input Data

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

Missing checks on the `_fee` input argument for the constructor and `setFee()` function in `ChainlinkOracle.sol` contract.

The missing checks are the following:

1. Missing zero check in the constructor
2. Missing min `_fee` check in the `setFee()` function
3. Missing max `_fee` check in the `setFee()` function

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
  jobId = _jobid;
  setChainlinkToken(_tokenAddress);
  setChainlinkOracle(_operator);
  fee = _fee;
  lightClient = _lightClient;
}

function setFee(uint256 _fee) public onlyOwner {
  uint256 oldFee = fee;
  fee = _fee;

  emit SetFee(_fee, oldFee, block.timestamp);
}
```

## Recommendation

Consider adding the following checks:

```diff
+ uint256 constant private MIN_NODE_OPERATOR_FEE = ?;
+ uint256 constant private MAX_NODE_OPERATOR_FEE = ?;

+ error NodeOperatorFeeCannotBeZero();
+ error MinNodeOperatorFee();
+ error MaxNodeOperatorFee();

constructor(
  address _tokenAddress,
- bytes32 _jobid,
+ bytes32 _jobId,
  address _operator,
  uint256 _fee,
  address _lightClient
) ConfirmedOwner(msg.sender) {
+ if (_fee == 0) revert NodeOperatorFeeCannotBeZero();

- jobId = _jobid;
+ jobId = _jobId;
  setChainlinkToken(_tokenAddress);
  setChainlinkOracle(_operator);
  fee = _fee;
  lightClient = _lightClient;
}

function setFee(uint256 _fee) public onlyOwner {
+ if (_fee < MIN_NODE_OPERATOR_FEE) revert MinNodeOperatorFee();
+ if (_fee > MAX_NODE_OPERATOR_FEE) revert MaxNodeOperatorFee();

  uint256 oldFee = fee;
  fee = _fee;

  emit SetFee(_fee, oldFee, block.timestamp);
}
```

## Team Response

Acknowledged and fixed by setting `MIN_NODE_OPERATOR_FEE` to `0.001` and `MAX_NODE_OPERATOR_FEE` to `0.1` and adding a custom error regarding the upper and lower limits of fee associated with it.

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

