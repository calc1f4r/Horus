---
# Core Classification
protocol: Project
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49835
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm2mxcaoo000112pvkwt2nb8u
source_link: none
github_link: https://github.com/Cyfrin/2024-11-one-world

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - casinocompiler
  - wellbyt3
  - justawanderkid
  - leanlabiano
  - shikhar229169
---

## Vulnerability Title

Missing KYC and NFT Ownership Verification for Ecosystem Access

### Overview


The OneWorldProject website requires users to complete a KYC process and purchase an NFT membership in order to participate in the ecosystem. However, some functions within the smart contracts do not have checks for these requirements, allowing unverified users to access restricted features. This poses a high risk as it could lead to regulatory issues and unauthorized access. The recommended solution is to implement KYC and NFT ownership verification within the smart contracts to ensure secure access control.

### Original Finding Content

## Summary

The lack of contract-level KYC and NFT verification allows unverified users to interact with restricted features, bypassing the platform’s intended access controls. Adding these verifications at the contract level would reinforce secure access control.

## Vulnerability Details

According to [OneWorldProject’s website](https://www.oneworldproject.io/), to participate in the ecosystem, users must complete KYC and purchase an NFT membership.

However, current functions like `createNewDAOMembership` and `joinDAO` lack contract-level checks for either KYC verification or NFT ownership.

```solidity
    function joinDAO(address daoMembershipAddress, uint256 tierIndex) external {
        require(daos[daoMembershipAddress].noOfTiers > tierIndex, "Invalid tier.");
        require(daos[daoMembershipAddress].tiers[tierIndex].amount > daos[daoMembershipAddress].tiers[tierIndex].minted, "Tier full.");
        uint256 tierPrice = daos[daoMembershipAddress].tiers[tierIndex].price;
        uint256 platformFees = (20 * tierPrice) / 100;
        daos[daoMembershipAddress].tiers[tierIndex].minted += 1;
        IERC20(daos[daoMembershipAddress].currency).transferFrom(_msgSender(), owpWallet, platformFees);
        IERC20(daos[daoMembershipAddress].currency).transferFrom(_msgSender(), daoMembershipAddress, tierPrice - platformFees);
        IMembershipERC1155(daoMembershipAddress).mint(_msgSender(), tierIndex, 1);
        emit UserJoinedDAO(_msgSender(), daoMembershipAddress, tierIndex);
    }
```

This omission allows non-KYC-verified users to interact with the ecosystem, relying on front-end restrictions that are insufficient for robust access control.

## Impact

Without contract-level KYC and NFT verification, unverified users may bypass front-end checks and access restricted features within the ecosystem. This exposes the system to regulatory risks and potential unauthorized access.

## Tools Used

Manual

## Recommendations

Implement KYC and NFT ownership verification within the smart contracts, ensuring that access control requirements are enforced at the protocol level.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Project |
| Report Date | N/A |
| Finders | casinocompiler, wellbyt3, justawanderkid, leanlabiano, shikhar229169, 0xhals, jesjupyter, sakibcy |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-11-one-world
- **Contest**: https://codehawks.cyfrin.io/c/cm2mxcaoo000112pvkwt2nb8u

### Keywords for Search

`vulnerability`

