---
# Core Classification
protocol: Earn V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51870
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/concrete/earn-v1
source_link: https://www.halborn.com/audits/concrete/earn-v1
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

Lack of validation on ProtectStrategy

### Overview

See description below for full details.

### Original Finding Content

##### Description

It has been observed that no parameter passed into the constructor was properly validated.

```
constructor(
        IERC20 baseAsset_,
        address feeRecipient_,
        address owner_,
        uint256 rewardFee_,
        address claimRouter_,
        address vault_
    ) {
        IERC20Metadata metaERC20 = IERC20Metadata(address(baseAsset_));

        rewardFee = rewardFee_;
        //This can be initially set to zero and then updated by the owner
        //slither-disable-next-line missing-zero-check
        claimRouter = claimRouter_;

        RewardToken[] memory rewardTokenEmptyArray = new RewardToken[](0);
        __StrategyBase_init(
            baseAsset_,
            string.concat("Concrete Earn Protect ", metaERC20.symbol(), " Strategy"),
            string.concat("ctPct-", metaERC20.symbol()),
            feeRecipient_,
            type(uint256).max,
            owner_,
            rewardTokenEmptyArray,
            vault_
        );
        //slither-disable-next-line unused-return
        //baseAsset_.approve(claimRouter, type(uint256).max);
    }

```

The only parameter that can be set again is `claimRouter_` through the `setClaimRouter` function by the owner.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

Consider implementing proper validation for all parameters passed into the constructor. This will enhance the security and robustness of the contract by ensuring that invalid or malicious input cannot compromise its functionality. Specifically, consider adding checks to verify the validity of addresses, ensuring they are not zero addresses, and confirming that the `rewardFee_` is within an acceptable range.

##### Remediation

**ACKNOWLEDGED:** The **Concrete team** acknowledged this finding.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Earn V1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/concrete/earn-v1
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/concrete/earn-v1

### Keywords for Search

`vulnerability`

