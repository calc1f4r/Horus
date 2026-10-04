---
# Core Classification
protocol: Frax Solidity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17928
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
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
  - Samuel Moelius Maximilian Krüger Troy Sargent
---

## Vulnerability Title

Convex_AMO_V2 custodian can withdraw rewards

### Overview


This bug report is about the Convex_AMO_V2 custodian being able to withdraw rewards. This violates the conventions established by other Frax Solidity contracts, which only allow the custodian to pause operations. The relevant code appears in Figure 15.1. The exploit scenario is that Eve tricks Frax Finance into making her the custodian for the Convex_AMO_V2 contract and when the unclaimed rewards are high, she withdraws them and vanishes. 

The short-term recommendation is to determine whether the Convex_AMO_V2 custodian requires the ability to withdraw rewards and document this as a security concern. This will help users to understand the risks associated with depositing funds into the Convex_AMO_V2 contract. The long-term recommendation is to implement a mechanism that allows rewards to be distributed without requiring the intervention of an intermediary. This will increase users' overall confidence in the system.

### Original Finding Content

## Frax Solidity Security Assessment

## Difficulty
**Undetermined**

## Type
**Configuration**

## Target
**Convex_AMO_V2.sol**

## Description
The `Convex_AMO_V2` custodian can withdraw rewards. This violates conventions established by other Frax Solidity contracts in which the custodian is only able to pause operations.

The relevant code appears in figure 15.1. The `withdrawRewards` function is callable by the contract owner, governance, or the custodian. This provides significantly more power to the custodian than other contracts in the Frax Solidity repository.

```solidity
function withdrawRewards(
    uint256 crv_amt,
    uint256 cvx_amt,
    uint256 cvxCRV_amt,
    uint256 fxs_amt
) external onlyByOwnGovCust {
    if (crv_amt > 0) TransferHelper.safeTransfer(crv_address, msg.sender, crv_amt);
    if (cvx_amt > 0) TransferHelper.safeTransfer(address(cvx), msg.sender, cvx_amt);
    if (cvxCRV_amt > 0) TransferHelper.safeTransfer(cvx_crv_address, msg.sender, cvxCRV_amt);
    if (fxs_amt > 0) TransferHelper.safeTransfer(fxs_address, msg.sender, fxs_amt);
}
```

**Figure 15.1:** `contracts/Misc_AMOs/Convex_AMO_V2.sol#L425-L435`

## Exploit Scenario
Eve tricks Frax Finance into making her the custodian for the `Convex_AMO_V2` contract. When the unclaimed rewards are high, Eve withdraws them and vanishes.

## Recommendations
Short term, determine whether the `Convex_AMO_V2` custodian requires the ability to withdraw rewards. If so, document this as a security concern. This will help users to understand the risks associated with depositing funds into the `Convex_AMO_V2` contract.

Long term, implement a mechanism that allows rewards to be distributed without requiring the intervention of an intermediary. Reducing human involvement will increase users’ overall confidence in the system.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Solidity |
| Report Date | N/A |
| Finders | Samuel Moelius Maximilian Krüger Troy Sargent |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf

### Keywords for Search

`vulnerability`

