---
# Core Classification
protocol: StationX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41403
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-07] Cross-Chain and KYCed users will only pay a portion of the fees

### Overview


The factory contract is not charging the correct fees for cross-chain DAOs and KYC users. Currently, the factory charges a fee of 125 when a DAO is both cross-chain and KYCed, but it should be charging 250. This is because KYC is a separate functionality and should have its own fees. The recommended solution is to update the function to charge the correct fees based on whether the DAO is cross-chain, KYCed, or both.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The factory contract calculates fees for cross-chain DAOs and KYC users as follows:

```solidity
    function checkDepositFeesSent(address _daoAddress, uint256 _totalAmount) internal {
        if (ccDetails[_daoAddress].depositChainIds.length > 1 || isKycEnabled[_daoAddress]) {
            require(msg.value >= _totalAmount + ((depositFees * platformFeeMultiplier) / 100), "Insufficient fees");
        } else {
            require(msg.value >= _totalAmount + depositFees, "Insufficient fees");
        }
    }
```

For example, if `depositFees` is 100 and the `platformFeeMultiplier` is 125, the factory will charge 125 as fees when the DAO is either cross-chain or KYCed. The sponsor indicated that KYC is a separate functionality, and the factory should charge additional fees when KYC is enabled. However, this is not the case currently. If the DAO is both cross-chain and KYCed, the factory only applies the `platformFeeMultiplier` once instead of twice.

## Recommendations

Consider updating the function as follows:

```solidity
    function checkDepositFeesSent(address _daoAddress, uint256 _totalAmount) internal {
        uint256 fees = (depositFees * platformFeeMultiplier) / 100;
        if (ccDetails[_daoAddress].depositChainIds.length > 1 && isKycEnabled[_daoAddress]) {
            require(msg.value >= _totalAmount + (fees * 2)), "Insufficient fees";
        } else if (ccDetails[_daoAddress].depositChainIds.length > 1 || isKycEnabled[_daoAddress]) {
            require(msg.value >= _totalAmount + fees, "Insufficient fees");
        } else {
            require(msg.value >= _totalAmount + depositFees, "Insufficient fees");
        }
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StationX |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

