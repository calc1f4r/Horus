# **Bluefin Spot**

Security Assessment


November 2nd, 2024 - Prepared by OtterSec


Robert Chen [r@osec.io](mailto:r@osec.io)


Michał Bochnak [embe221ed@osec.io](mailto:embe221ed@osec.io)


Sangsoo Kang [sangsoo@osec.io](mailto:sangsoo@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


**Scope** **3**


**Findings** **4**


**Vulnerabilities** **5**


OS-RPL-ADV-00 | Faulty Constant Definition 6


OS-RPL-ADV-01 | Reward Accumulation During Inactive Time Period 7


OS-RPL-ADV-02 | Absence of Version Update Functionality 9


OS-RPL-ADV-03 | Risk of Reentrancy During Flash Swap 10


OS-RPL-ADV-04 | Improper Oracle Update 11


OS-RPL-ADV-05 | Incorrect Price Boundary Checks 12


**General** **Findings** **14**


OS-RPL-SUG-00 | Initialization Price Validation 15


OS-RPL-SUG-01 | Code Refactoring 16


OS-RPL-SUG-02 | Missing Validation Logic 17


**Appendices**


**Vulnerability** **Rating** **Scale** **18**


**Procedure** **19**


© 2024 Otter Audits LLC. All Rights Reserved. 1 / 19


**01** **—** **Executive** **Summary**

## Overview


between October 22nd and November 1st, 2024. For more information on our auditing methodology,


refer to Appendix B.

## Key Findings


We produced 9 findings throughout this audit engagement.


In particular, we identified a critical vulnerability where the constant for storing the maximum value of


a 64-bit unsigned number is incorrectly defined, as it is missing a character in its declaration, resulting


in a length of 15 instead of the expected 16 characters, which may have adverse effects on the tick


calculation (OS-RPL-ADV-00). Additionally, when a reward distribution is restarted after a pause, the


system incorrectly includes the inactive periods in reward calculations, resulting in inaccurate reward


distribution (OS-RPL-ADV-01). Furthermore, the configuration module lacks a function to update the


version, which is essential for managing package upgrades and ensuring compatibility with newer versions


(OS-RPL-ADV-02).


We also recommended including validation during the pool creation process to ensure that the initial


square root price falls within a safe and operational range (OS-RPL-SUG-00), and advised incorporating


additional checks within the codebase for improved robustness and security (OS-RPL-SUG-02). We


further suggested modifying the codebase for improved functionality, efficiency, and maintainability


(OS-RPL-SUG-01).


© 2024 Otter Audits LLC. All Rights Reserved. 2 / 19


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/fireflyprotocol/bluefin-spot-](https://github.com/fireflyprotocol/bluefin-spot-contracts)


[contracts.](https://github.com/fireflyprotocol/bluefin-spot-contracts) This audit was performed against [68beb25.](https://github.com/fireflyprotocol/bluefin-spot-contracts/commit/68beb257615b54811842b8376d3034adb0511280)


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**


This module includes the Sui smart contracts for the Bluefin spot exbluefin-spot

change program.


© 2024 Otter Audits LLC. All Rights Reserved. 3 / 19


**03** **—** **Findings**


Overall, we reported 9 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.



© 2024 Otter Audits LLC. All Rights Reserved. 4 / 19


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


**ID** **Severity** **Status** **Description**



of 15 instead of the expected 16 characters.


When a reward distribution is restarted after


a pause, the system incorrectly includes the


inactive periods in the reward calculations,


resulting in inaccurate reward distribution.


The configuration module lacks a function


to update the version, which is essential for


managing package upgrades and ensuring


compatibility with newer versions.



OS-RPL-ADV-00


OS-RPL-ADV-01


OS-RPL-ADV-02


OS-RPL-ADV-03


OS-RPL-ADV-04


OS-RPL-ADV-05





The flash swap operation is vulnerable to


reentrancy attacks.





|In|update_pool_state|
|---|---|
|**`oracle::update`**|**`oracle::update`**|
|**`current_tick_index`**|**`current_tick_index`**|


which may result in inaccurate oracle


observations.


ity where the conditions for validating


the tick boundaries.



© 2024 Otter Audits LLC. All Rights Reserved. 5 / 19


Bluefin Spot Audit 04 - Vulnerabilities


**Description**


length of the constant being 15 characters instead of the required 16.


_>__ _sources/maths/bit_math.move_ move

```
  public fun least_significant_bit(mask: u256) : u8 {
    assert!(mask > 0, 0);
    let bit = 255;
    [...]
    if (mask & (constants::max_u64() as u256) > 0) {
      bit = bit - 64;
    } else {
      mask = mask >> 64;
    };
    [...]
    bit
  }

```

constant is one character short, it effectively ignores the highest bit (the most significant bit in the 64-bit


range) when performing this check. This is particularly critical because this function is utilized to search


for the next initialized tick, and thus, it may result in the calculation of an incorrect tick position.


**Remediation**


correct value and length of 16 characters.


**Patch**


Resolved in [f9025e9.](https://github.com/fireflyprotocol/bluefin-spot-contracts/commit/f9025e9d9d248d5b1ac97974b9968c69f9646843)


© 2024 Otter Audits LLC. All Rights Reserved. 6 / 19


Bluefin Spot Audit 04 - Vulnerabilities


**Description**


There is a vulnerability in how reward calculations are handled for liquidity positions after a reward


distribution has ended and then restarts. There is no way to correctly restart the distribution of the same


type after a reward distribution has finished. Specifically, the calculation incorrectly includes inactive time


(the time period after the distribution ended but before it restarts) in the reward accumulation, resulting in


inaccurate rewards for positions.


_>__ _sources/pool.move_ move

```
  public(friend) fun update_reward_infos<CoinTypeA, CoinTypeB>(pool: &mut Pool<CoinTypeA,
```

_�→_ `CoinTypeB>,` `current_timestamp_seconds:` `u64)` `:` `vector<u128>` `{`
```
    let reward_growth_globals = vector::empty<u128>();
    let current_index = 0;
    while (current_index < vector::length<PoolRewardInfo>(&pool.reward_infos)) {
      [...]
      if (current_timestamp_seconds > reward_info.last_update_time) {
        [...]
         if (pool.liquidity != 0 && min_timestamp > reward_info.last_update_time) {
              let rewards_accumulated = full_math_u128::full_mul(((min_timestamp

```


_�→_


```
-reward_info.last_update_time) as u128),

```


_�→_ `reward_info.reward_per_seconds);`
```
              [...]
              reward_info.total_reward_allocated = reward_info.total_reward_allocated +
```

_�→_ `((rewards_accumulated/` `(constants::q64()` `as` `u256))` `as` `u64);`
```
         };
         reward_info.last_update_time = current_timestamp_seconds;
      };
      vector::push_back<u128>(&mut reward_growth_globals, reward_info.reward_growth_global);
    };
    reward_growth_globals
  }

|difference between the|current_timestamp_seconds|Col3|
|---|---|---|
|**`pool::update_pool_reward_emission`**|**`pool::update_pool_reward_emission`**|is called to re|


```

for any time gap between the previous reward end and the new start time. As a result, liquidity providers


may receive extra rewards that do not correspond to any actual activity.


For example, if reward distribution ends at time _t_ 0, and a new distribution restarts at time _t_ 1, the reward


accumulation for liquidity positions incorrectly includes the inactive period [ _t_ 0, _t_ 1]. Ideally, rewards should


end up counting this inactive interval in reward calculations.


© 2024 Otter Audits LLC. All Rights Reserved. 7 / 19


Bluefin Spot Audit 04 - Vulnerabilities


**Remediation**


When calculating rewards, ensure that only the time intervals where rewards were actively distributed are


included.


**Patch**


Resolved in [f9025e9.](https://github.com/fireflyprotocol/bluefin-spot-contracts/commit/f9025e9d9d248d5b1ac97974b9968c69f9646843)


© 2024 Otter Audits LLC. All Rights Reserved. 8 / 19


Bluefin Spot Audit 04 - Vulnerabilities


**Description**


limitation will pose significant issues when deploying new versions of the protocol, especially if breaking


**Remediation**


**Patch**


Resolved in [f9025e9.](https://github.com/fireflyprotocol/bluefin-spot-contracts/commit/f9025e9d9d248d5b1ac97974b9968c69f9646843)


© 2024 Otter Audits LLC. All Rights Reserved. 9 / 19


Bluefin Spot Audit 04 - Vulnerabilities


**Description**


calls to be made via other functions, which might result in the manipulation of the pool values.


**Remediation**


Add a reentrancy guard to prevent the calling of other functions during the execution of a flash swap.


**Patch**


Resolved in [f9025e9.](https://github.com/fireflyprotocol/bluefin-spot-contracts/commit/f9025e9d9d248d5b1ac97974b9968c69f9646843)


© 2024 Otter Audits LLC. All Rights Reserved. 10 / 19


Bluefin Spot Audit 04 - Vulnerabilities


**Description**


the recording of inaccurate and misleading data in the oracle regarding the pool’s state before the swap


occurred, rendering the data inconsistent.


_>__ _sources/pool.move_ move

```
  fun update_pool_state<CoinTypeA, CoinTypeB>(pool: &mut Pool<CoinTypeA, CoinTypeB>, swap_result:
```

_�→_ `SwapResult,` `current_time:` `u64)` `{`
```
    // current tick index of pool is not the same as swap result
    if (!i32::eq(pool.current_tick_index, swap_result.current_tick_index)) {
      pool.current_sqrt_price = swap_result.end_sqrt_price;
      pool.current_tick_index = swap_result.current_tick_index;
      oracle::update(
         &mut pool.observations_manager,
         pool.current_tick_index,
         pool.liquidity,
         current_time,
      );
    } else {
      pool.current_sqrt_price = swap_result.end_sqrt_price;
    };
    [...]
  }

```

**Remediation**


**Patch**


Resolved in [f9025e9.](https://github.com/fireflyprotocol/bluefin-spot-contracts/commit/f9025e9d9d248d5b1ac97974b9968c69f9646843)


© 2024 Otter Audits LLC. All Rights Reserved. 11 / 19


Bluefin Spot Audit 04 - Vulnerabilities


**Description**

|sqrt_price_max_limit|Col2|Col3|
|---|---|---|
|wap from|**`CoinTypeB`**|to|



_>__ _sources/pool.move_ move

```
  fun swap_in_pool<CoinTypeA, CoinTypeB>(
    clock: &Clock,
    pool: &mut Pool<CoinTypeA, CoinTypeB>,
    a2b: bool,
    by_amount_in: bool,
    amount:u64,
    sqrt_price_max_limit: u128): SwapResult
  {
    [...]
    if (a2b) {
      assert!(pool.current_sqrt_price > sqrt_price_max_limit && sqrt_price_max_limit >=
```

_�→_ `tick_math::min_sqrt_price(),` `errors::invalid_price_limit());`
```
    } else {
      assert!(pool.current_sqrt_price < sqrt_price_max_limit && sqrt_price_max_limit <=
```

_�→_ `tick_math::max_sqrt_price(),` `errors::invalid_price_limit());`
```
    };
    [...]
  }

|However, if the current tick is at|MIN_TICK|(the|
|---|---|---|
|**`sqrt_price_max_limit`** **`>=`** **`min_sqrt_price`**|**`sqrt_price_max_limit`** **`>=`** **`min_sqrt_price`**|**`sqrt_price_max_limit`** **`>=`** **`min_sqrt_price`**|


```

to push the square root price beyond the maximum limit.


minimum or maximum boundaries will result in attempts to execute swaps that lead to invalid price states.


© 2024 Otter Audits LLC. All Rights Reserved. 12 / 19


Bluefin Spot Audit 04 - Vulnerabilities


**Remediation**


limit is strictly greater than the minimum square root price and strictly less than the maximum square root


price.


**Patch**


Resolved in [f9025e9.](https://github.com/fireflyprotocol/bluefin-spot-contracts/commit/f9025e9d9d248d5b1ac97974b9968c69f9646843)


© 2024 Otter Audits LLC. All Rights Reserved. 13 / 19


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.


OS-RPL-SUG-00

area that should remain unreachable.


Recommendation for modifying the codebase for improved functionality,

OS-RPL-SUG-01

efficiency, and maintainability.


There are several instances where proper validation is not done, resulting

OS-RPL-SUG-02

in potential security issues.


© 2024 Otter Audits LLC. All Rights Reserved. 14 / 19


Bluefin Spot Audit 05 - General Findings


**Initialization** **Price** **Validation** OS-RPL-SUG-00


**Description**


extreme prices.


_>__ _sources/maths/tick_math.move_ move

```
  public fun get_tick_at_sqrt_price(sqrt_price: u128): i32::I32 {
    assert!(sqrt_price >= MIN_SQRT_PRICE_X64 && sqrt_price <= MAX_SQRT_PRICE_X64,
```

_�→_ `EINVALID_SQRT_PRICE);`
```
    let r = sqrt_price;
    [...]
  }

```

**Remediation**


safe and operational range.


**Patch**


Resolved in [f9025e9.](https://github.com/fireflyprotocol/bluefin-spot-contracts/commit/f9025e9d9d248d5b1ac97974b9968c69f9646843)


© 2024 Otter Audits LLC. All Rights Reserved. 15 / 19


Bluefin Spot Audit 05 - General Findings


**Code** **Refactoring** OS-RPL-SUG-01


**Description**


1. For improved functionality and control, add functions to remove an address from the


externally, enabling users to easily retrieve their rewards from their liquidity positions in the pool.


_>__ _sources/gateway.move_ move

```
     /// Allows user to collect the rewards accrued on their position
     public fun collect_reward<CoinTypeA, CoinTypeB, RewardCoinType>(
       clock: &Clock,
       protocol_config: &GlobalConfig,
       pool: &mut Pool<CoinTypeA, CoinTypeB>,
       position: &mut Position,
       ctx: &mut TxContext
       ){
       [...]
     }

```

**Remediation**


Implement the above-mentioned suggestions.


**Patch**


Resolved in [f9025e9.](https://github.com/fireflyprotocol/bluefin-spot-contracts/commit/f9025e9d9d248d5b1ac97974b9968c69f9646843)


© 2024 Otter Audits LLC. All Rights Reserved. 16 / 19


Bluefin Spot Audit 05 - General Findings


**Missing** **Validation** **Logic** OS-RPL-SUG-02


**Description**


passed into these functions will result in nonsensical operations.


As a high fee rate will discourage users from providing liquidity or trading within the pool, and if


for traders to execute orders at desired prices.


**Remediation**


Incorporate the above validations.


**Patch**


Resolved in [f9025e9.](https://github.com/fireflyprotocol/bluefin-spot-contracts/commit/f9025e9d9d248d5b1ac97974b9968c69f9646843)


© 2024 Otter Audits LLC. All Rights Reserved. 17 / 19


**A** **—** **Vulnerability** **Rating** **Scale**


We rated our findings according to the following scale. Vulnerabilities have immediate security implications.


Informational findings may be found in the General Findings.


Examples:


         - Misconfigured authority or access control validation.


         - Improperly designed economic incentives leading to loss of funds.


Vulnerabilities that may result in a loss of user funds but are potentially difficult to exploit.


Examples:


         - Loss of funds requiring specific victim interactions.


         - Exploitation involving high capital requirement with respect to payout.


Examples:


         - Computational limit exhaustion through malicious input.


         - Forced exceptions in the normal user flow.


or undue risk.


Examples:


         - Oracle manipulation with large capital requirements and multiple transactions.


Examples:


         - Explicit assertion of critical internal invariants.


         - Improved input validation.


© 2024 Otter Audits LLC. All Rights Reserved. 18 / 19


**B** **—** **Procedure**


As part of our standard auditing procedure, we split our analysis into two main sections: design and


implementation.


When auditing the design of a program, we aim to ensure that the overall economic architecture is sound


in the context of an on-chain program. In other words, there is no way to steal funds or deny service,


ignoring any chain-specific quirks. This usually requires a deep understanding of the program’s internal


interactions, potential game theory implications, and general on-chain execution primitives.


One example of a design vulnerability would be an on-chain oracle that could be manipulated by flash


loans or large deposits. Such a design would generally be unsound regardless of which chain the oracle


is deployed on.


On the other hand, auditing the program’s implementation requires a deep understanding of the chain’s


execution model. While this varies from chain to chain, some common implementation vulnerabilities


include reentrancy, account ownership issues, arithmetic overflows, and rounding bugs.


As a general rule of thumb, implementation vulnerabilities tend to be more “checklist” style. In contrast,


design vulnerabilities require a strong understanding of the underlying system and the various interactions:


both with the user and cross-program.


As we approach any new target, we strive to comprehensively understand the program first. In our audits,


we always approach targets with a team of auditors. This allows us to share thoughts and collaborate,


picking up on details that others may have missed.


While sometimes the line between design and implementation can be blurry, we hope this gives some


insight into our auditing procedure and thought process.


© 2024 Otter Audits LLC. All Rights Reserved. 19 / 19


