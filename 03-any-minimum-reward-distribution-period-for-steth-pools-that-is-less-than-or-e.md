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
solodit_id: 62535
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

[03] Any minimum reward distribution period for stETH pools that is less than or equal to 24 hrs can be forced to be non-distributed by an attacker

### Overview

See description below for full details.

### Original Finding Content


In the current deployments of the v6 contracts (Distribution) onchain, the minimum stake amount is 0.01 stETH. Combined with the daily timeframe Lido reports and distribute’s rewards, an attacker could force the Distributor to not mint MOR token rewards for users from timestamp x to timestamp z.
```

 function distributeRewards(uint256 rewardPoolIndex_) public {
        ...
        //// Calculate the reward amount
@>        uint256 rewards_ = IRewardPool(rewardPool).getPeriodRewards(
            rewardPoolIndex_,
            lastCalculatedTimestamp_,
            uint128(block.timestamp)
        );

        if (rewards_ == 0) return;
        //// End

       ...

        // Validate that public reward pools await `minRewardsDistributePeriod`
@>        if (block.timestamp <= lastCalculatedTimestamp_ + minRewardsDistributePeriod) return;
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

            uint256 balance_ = IERC20(yieldToken_).balanceOf(address(this));
            uint256 decimals_ = IERC20Metadata(yieldToken_).decimals();
            uint256 underlyingYield_ = (balance_ - depositPool.lastUnderlyingBalance).to18(decimals_);
            uint256 yield_ = underlyingYield_ * depositPool.tokenPrice;

            depositPool.lastUnderlyingBalance = balance_;

            yields_[i] = yield_;
            totalYield_ += yield_;
        }

        if (totalYield_ == 0) {
 @>           undistributedRewards += rewards_;
            return;
        }

       ...
    }
```

1. Lido distributes rewards each day at 00:00 UTC (aka every 24 hours)
2. DepositPool A has 10k stETH staked by users
3. The `minRewardsDistributePeriod` is set to 1 hour for example
4. What an attacker can do is to stake just a little over the minimum stake (0.0105) since minimum is 0.01 stETH
5. Say 1 hours has elapsed, call the `distributeRewards()` directly or trigger a transaction such as `withdraw()` from the DepositPool to withdraw 1 wei stETH which will then trigger `distributeRewards()`
6. What happens is that if the reward pool index e.g 0 mints 3500 MOR rewards per day, that means we do 3500 / 24. Thus, `uint256 rewards_ = IRewardPool(rewardPool).getPeriodRewards(rewardPoolIndex_, lastCalculatedTimestamp_, uint128(block.timestamp));` will return 145.83 MOR, but since it is not yet past 00:00 UTC and stETH shares / balances have not gone up, these 145.83 MOR will not be minted and instead go into `undistributedRewards`.



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

