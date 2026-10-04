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
solodit_id: 62533
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

[01] An attacker can force the distributor to mint MOR rewards in a period of no new generated yield

### Overview

See description below for full details.

### Original Finding Content


The `distributeRewards()` function of the Distributor contract determines reward amounts to be distributed to DepositPool appropriately. The reward token minted is MOR tokens in this case. In the current implementation of the onchain distribution contracts, over 3k MOR is being minted/distributed daily.

The issue is that once we upgrade the contracts to v7, each deposit pool will now have a portion of MOR based on the yield they contributed from timestamp x to timestamp y. This leaves room for an attacker to force the Distributor into minting MOR tokens even on days where there was no actual yield gains.

<https://github.com/code-423n4/2025-08-morpheus/blob/main/contracts/capital-protocol/Distributor.sol# L330-L410>
```

 function distributeRewards(uint256 rewardPoolIndex_) public {
        //// Base validation
        IRewardPool rewardPool_ = IRewardPool(rewardPool);
        rewardPool_.onlyExistedRewardPool(rewardPoolIndex_);

        uint128 lastCalculatedTimestamp_ = rewardPoolLastCalculatedTimestamp[rewardPoolIndex_];
        require(lastCalculatedTimestamp_ != 0, "DR: `rewardPoolLastCalculatedTimestamp` isn't set");
        //// End

        //// Calculate the reward amount
        uint256 rewards_ = IRewardPool(rewardPool).getPeriodRewards(
            rewardPoolIndex_,
            lastCalculatedTimestamp_,
            uint128(block.timestamp)
        );

        if (rewards_ == 0) return;
        //// End

        // Stop execution when the reward pool is private
        if (!rewardPool_.isRewardPoolPublic(rewardPoolIndex_)) {
            _onlyExistedDepositPool(rewardPoolIndex_, depositPoolAddresses[rewardPoolIndex_][0]);
            distributedRewards[rewardPoolIndex_][depositPoolAddresses[rewardPoolIndex_][0]] += rewards_;

            rewardPoolLastCalculatedTimestamp[rewardPoolIndex_] = uint128(block.timestamp);

            return;
        }

        // Validate that public reward pools await `minRewardsDistributePeriod`
        if (block.timestamp <= lastCalculatedTimestamp_ + minRewardsDistributePeriod) return;
        rewardPoolLastCalculatedTimestamp[rewardPoolIndex_] = uint128(block.timestamp);

        //// Update prices
        updateDepositTokensPrices(rewardPoolIndex_);
        //// End

        //// Calculate `yield` from all deposit pools
        uint256 length_ = depositPoolAddresses[rewardPoolIndex_].length;
        uint256 totalYield_ = 0;
        uint256[] memory yields_ = new uint256[](length_);

        for (uint256 i = 0; i < length_; i++) {
            DepositPool storage depositPool = depositPools[rewardPoolIndex_][depositPoolAddresses[rewardPoolIndex_][i]];

            address yieldToken_;
            if (depositPool.strategy == Strategy.AAVE) {
                yieldToken_ = depositPool.aToken;
            } else if (depositPool.strategy == Strategy.NONE) {
                // The current condition coverage cannot be achieved in the current version.
                // Added to avoid errors in the future.
                yieldToken_ = depositPool.token;
            }

@>            uint256 balance_ = IERC20(yieldToken_).balanceOf(address(this));
            uint256 decimals_ = IERC20Metadata(yieldToken_).decimals();
@>            uint256 underlyingYield_ = (balance_ - depositPool.lastUnderlyingBalance).to18(decimals_);
            uint256 yield_ = underlyingYield_ * depositPool.tokenPrice;

            depositPool.lastUnderlyingBalance = balance_;

            yields_[i] = yield_;
            totalYield_ += yield_;
        }

        if (totalYield_ == 0) {
            undistributedRewards += rewards_;
            return;
        }
        //// End

        //// Calculate `depositPools` shares and reward amount for each `depositPool`
        for (uint256 i = 0; i < length_; i++) {
            if (yields_[i] == 0) continue;

            distributedRewards[rewardPoolIndex_][depositPoolAddresses[rewardPoolIndex_][i]] +=
                (yields_[i] * rewards_) /
                totalYield_;
        }
        //// End
    }
```

**Proper scenario:**

1. DepositPool A is connected to reward pool 0 which is a public reward pool and have Aave strategy connected to it in the Distributor when we call `addDepositPool()`.
2. Users deposit 10k wstETH or wBTC etc on day 1. 10k wBTC is minted to the distributor contract.
3. On day 2, the total shares grow from 10k to 10.01 wBTC because now the liquidity index in Aave have grown, interest has accrued etc but the idea is that from day 1 to day 2, the distributor has earned 0.01 wBTC yield.
4. Now, the distributor will mint e.g 3k MOR tokens for that day in which yield was earned and users each get a claim of that based on their stake.

**Attack scenario:**

1. Suppose the strategy in this case is not Aave but rather another strategy such as `NONE`. This means there is a strategy, it is not `NO_YIELD` but it also isn’t Aave. For example, stETH would be one such strategy.
2. If users stake 10k stETH on day 1, then a slash occur that forces stETH to rebase negative slightly, let’s assume a -0.001 stETH.
3. On day 2, the shares/balance of the distributor in stETH becomes 10k stETH - -0.001 stETH, this means no yield and instead a negative rebase and users would have to wait for another day or 2 for the rebase to become positive again and exceed total deposit (10k stETH) before MOR tokens being minted will then resume
4. However, an attacker can donate 0.0011 stETH to the distributor and force all 3k MOR tokens to be minted for that zero-yield day.



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

