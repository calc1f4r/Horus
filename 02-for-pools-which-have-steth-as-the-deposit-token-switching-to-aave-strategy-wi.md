---
# Core Classification
protocol: Morpheus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62534
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-08-morpheus
source_link: https://code4rena.com/reports/2025-08-morpheus
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
finders_count: 0
finders:
---

## Vulnerability Title

[02] For pools which have stETH as the deposit token, switching to Aave strategy will not work

### Overview

See description below for full details.

### Original Finding Content


In the current implementation of the Distribution contracts onchain, only stETH have been staked by users thereby earning MOR in return. However, if the protocol were to try to switch to Aave strategy for these staked tokens, it would fail.

<https://github.com/code-423n4/2025-08-morpheus/blob/main/contracts/capital-protocol/Distributor.sol# L192-L248>
```

 function addDepositPool(
        uint256 rewardPoolIndex_,
        address depositPoolAddress_,
        address token_,
        string memory chainLinkPath_,
        Strategy strategy_
    ) external onlyOwner {
        IRewardPool rewardPool_ = IRewardPool(rewardPool);
        rewardPool_.onlyExistedRewardPool(rewardPoolIndex_);

        require(
            IERC165(depositPoolAddress_).supportsInterface(type(IDepositPool).interfaceId),
            "DR: the deposit pool address is invalid"
        );

        // Validate that pool is public in other cases.
        if (strategy_ == Strategy.NO_YIELD) {
            // Validate that pool is private.
            rewardPool_.onlyNotPublicRewardPool(rewardPoolIndex_);
            // Validate that deposit pool is not added for this `rewardPoolIndex_`.
            require(
                depositPoolAddresses[rewardPoolIndex_].length == 0,
                "DR: the deposit pool for this index already added"
            );

            // Skip `token_` and `chainLinkPath_` when `Strategy.NO_YIELD`.
            token_ = address(0);
            chainLinkPath_ = "";
        } else {
            require(!isDepositTokenAdded[token_], "DR: the deposit token already added");

            rewardPool_.onlyPublicRewardPool(rewardPoolIndex_);
        }

        // Set `aToken_` when `Strategy.AAVE`. Add allowance for Aave to transfer `token_` from the current
        // contract.
        address aToken_ = address(0);
        if (strategy_ == Strategy.AAVE) {
            (aToken_, , ) = AaveIPoolDataProvider(aavePoolDataProvider).getReserveTokensAddresses(token_);

            IERC20(token_).safeApprove(aavePool, type(uint256).max);
            IERC20(aToken_).approve(aavePool, type(uint256).max);
        }

        DepositPool memory depositPool_ = DepositPool(token_, chainLinkPath_, 0, 0, 0, strategy_, aToken_, true);

        depositPoolAddresses[rewardPoolIndex_].push(depositPoolAddress_);
        depositPools[rewardPoolIndex_][depositPoolAddress_] = depositPool_;
        isDepositTokenAdded[token_] = true;

        // Update prices for all `depositPools` by `rewardPoolIndex_`
        if (strategy_ != Strategy.NO_YIELD) {
            updateDepositTokensPrices(rewardPoolIndex_);
        }

        emit DepositPoolAdded(rewardPoolIndex_, depositPool_);
    }
```

One newer features of the v7 contracts such as DepositPool.sol is that it now sends the staked tokens to the Distributor contract. This allows the protocol to also have other yield strategies such as supplying user staked tokens to Aave markets.

1. If we were to upgrade from v6 to v7 for DepositPool A for the reward pool index of 0 which is a public pool.
2. Then, call `addRewardPool` in the RewardPool contract to add the reward pool index of 0.
3. Next call, `addDepositPool()` in the Distributor contract to whitelist reward pool index 0, it would fail.
4. The reason is because in the currently deployed v6 Distribution contracts (which the protocol will upgrade to use DepositPool implementation), only stETH is the token staked. Thus, the Distributor contract trying to call approve on the `aToken` address will fail. Because on Aave, there is no corresponding `aToken` for the stETH deposit token and for that reason, Aave will return the zero address which the contract will then try to call approve on.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Morpheus |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2025-08-morpheus
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2025-08-morpheus

### Keywords for Search

`vulnerability`

