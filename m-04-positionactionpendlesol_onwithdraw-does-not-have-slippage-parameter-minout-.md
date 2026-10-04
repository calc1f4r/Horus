---
# Core Classification
protocol: LoopFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49116
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-10-loopfi
source_link: https://code4rena.com/reports/2024-10-loopfi
github_link: https://github.com/code-423n4/2024-10-loopfi-findings/issues/10

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
finders_count: 3
finders:
  - pkqs90
  - ZanyBonzy
  - Bauchibred
---

## Vulnerability Title

[M-04] `PositionActionPendle.sol#_onWithdraw` does not have slippage parameter `minOut` set

### Overview


This report discusses a bug that can cause users to lose funds when withdrawing from `PositionActionPendle` and exiting Pendle pools. This issue was introduced in the latest code update and occurs because the `minOut` parameter is set to 0, which means users may receive less output tokens than expected. This is similar to a previous issue found in a Loopfi audit, but this specific code is new and was not present in the previous audit. To mitigate this issue, users should be able to set a `minOut` parameter for withdraw functions for Pendle and ERC4626 positions. The team behind Loopfi has confirmed this bug and recommended the mitigation steps.

### Original Finding Content


When performing withdraws on `PositionActionPendle` and exiting Pendle pools, users may lose funds due to not setting slippage.

### Bug Description

*Note: This is a new issue that was introduced by the latest code diff.*

The dataflow for withdrawing on `PositionActionPendle` is:
1. User withdraws collateral (which is a Pendle token) from CDPVault.
2. User performs pendle pool exit.

The issue is in step 2; since `minOut` is set to 0, users may receive less output tokens than expected.

```solidity
    function _onWithdraw(
        address vault,
        address position,
        address dst,
        uint256 amount
    ) internal override returns (uint256) {
        uint256 collateralWithdrawn = ICDPVault(vault).withdraw(address(position), amount);
        address collateralToken = address(ICDPVault(vault).token());

        if (dst != collateralToken && dst != address(0)) {
            PoolActionParams memory poolActionParams = PoolActionParams({
                protocol: Protocol.PENDLE,        
@>              minOut: 0, // @audit-bug: No slippage.
                recipient: address(this),     
                args: abi.encode(
                    collateralToken,          
                    collateralWithdrawn,       
                    dst                        
                )
            });

            bytes memory exitData = _delegateCall(
                address(poolAction),
                abi.encodeWithSelector(poolAction.exit.selector, poolActionParams)
            );

            collateralWithdrawn = abi.decode(exitData, (uint256));
        }
        return collateralWithdrawn;
    }
```

Also note that this is similar to the 2024-07 Loopfi audit finding [M-39](https://github.com/code-423n4/2024-07-loopfi-findings/issues/38), which also talks about slippage in ERC4626. However, this Pendle withdraw exit pool code is new, and not existant in the last audit. Thus this should be considered a new bug.

### Recommended Mitigation Steps

Allow user to set a `minOut` parameter for withdraw functions, especially for Pendle position and ERC4626 position.

**[amarcu (LoopFi) confirmed](https://github.com/code-423n4/2024-10-loopfi-findings/issues/13#event-14870931535)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | LoopFi |
| Report Date | N/A |
| Finders | pkqs90, ZanyBonzy, Bauchibred |

### Source Links

- **Source**: https://code4rena.com/reports/2024-10-loopfi
- **GitHub**: https://github.com/code-423n4/2024-10-loopfi-findings/issues/10
- **Contest**: https://code4rena.com/reports/2024-10-loopfi

### Keywords for Search

`vulnerability`

