# **Echelon**

Security Assessment


May 8th, 2025 - Prepared by OtterSec


Andreas Mantzoutas [andreas@osec.io](mailto:andreas@osec.io)


Bartłomiej Wierzbiński [dark@osec.io](mailto:dark@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **3**


Overview 3


Key Findings 3


**Scope** **4**


**Findings** **5**


**Vulnerabilities** **6**


OS-TEH-ADV-00 | Incorrect Reward Initialization 8


OS-TEH-ADV-01 | Missing Solvency Check 9


OS-TEH-ADV-02 | DOS Due to Blocking of Primary Store Creation 10


OS-TEH-ADV-03 | Front-Running Pair/Market Creation 12


OS-TEH-ADV-04 | Inconsistency in Swap Route Validation 13


OS-TEH-ADV-05 | Unchecked Liquidation Parameters 14


OS-TEH-ADV-06 | Irregularity in Fee Comment Annotation 16


OS-TEH-ADV-07 | Insufficient Liquidation Incentive Check 17


OS-TEH-ADV-08 | Flaw in Reward Withdrawal Logic 18


OS-TEH-ADV-09 | Lack of Unfreeze Functionality 19


**General** **Findings** **20**


OS-TEH-SUG-00 | Failed Liquidations Due to Flashloan Asset Mismatch 21


OS-TEH-SUG-01 | Code Optimization 22


OS-TEH-SUG-02 | Code Refactoring 24


OS-TEH-SUG-03 | Missing Validation Logic 25


OS-TEH-SUG-04 | Error Handling 27


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 33


Echelon Audit


TABLE OF CONTENTS


OS-TEH-SUG-05 | Code Maturity 28


OS-TEH-SUG-06 | Unutilized/Redundant Code 30


**Appendices**


**Vulnerability** **Rating** **Scale** **32**


**Procedure** **33**


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 33


**01** **—** **Executive** **Summary**

## Overview


between April 1st and April 16th, 2025. For more information on our auditing methodology, refer to


Appendix B.

## Key Findings


We produced 17 findings throughout this audit engagement.


In particular, we identified a high-risk vulnerability where the current implementation allows unauthorized


creation of a primary store at the package address or for the pool’s asset, which may prevent the addition of


farming rewards and block pool creation by making a valid primary store unavailable (OS-TEH-ADV-02).


Additionally, a missing solvency check allows users to withdraw supply shares even when their position


has bad debt, risking protocol insolvency (OS-TEH-ADV-01), and a lack of functionality to unfreeze coin


stores post a freeze operation may result in permanent lockups (OS-TEH-ADV-09).


Furthermore, the pair creation process fails to ensure whether the liquidation incentive BPS is within safe


bounds, allowing overly high incentives (OS-TEH-ADV-05), and it is possible to font-run the creation


of a new lending pair and market by registering an Aptos account at the pair’s or the market’s expected


address (OS-TEH-ADV-03).


We also made recommendations for implementing proper validations (OS-TEH-SUG-03) and explicit


checks to improve overall error handling (OS-TEH-SUG-04). We further suggested updating the codebase


for improved functionality (OS-TEH-SUG-02) and efficiency (OS-TEH-SUG-01). Lastly, we advised ad

hering to coding best practices (OS-TEH-SUG-05) and removing redundant or unutilized code instances


(OS-TEH-SUG-06).


© 2025 Otter Audits LLC. All Rights Reserved. 3 / 33


**02** **—** **Scope**


The source code was delivered to us in a Git repository at


[https://github.com/EchelonMarket/echelon-modules.](https://github.com/EchelonMarket/echelon-modules) This audit was performed against commit [d5b0dd2.](https://github.com/EchelonMarket/echelon-modules/commit/d5b0dd26bd7b6e7c510ae75fc8824aa9e79733df)


**A** **brief** **description** **of** **the** **programs** **is** **as** **follows:**


It implements isolated lending markets, enabling users supply collateral,
echelon-modules

borrow assets, and earn interest within independent asset pairs.


© 2025 Otter Audits LLC. All Rights Reserved. 4 / 33


**03** **—** **Findings**


Overall, we reported 17 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.



© 2025 Otter Audits LLC. All Rights Reserved. 5 / 33


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


is initialized to the current





users with an existing stake from accruing


rewards retroactively when a new reward is


added. This delays their reward accumulation


called for them.



OS-TEH-ADV-00


OS-TEH-ADV-01


OS-TEH-ADV-02


OS-TEH-ADV-03


OS-TEH-ADV-04



supply shares even when their position has bad


debt, risking protocol insolvency.


The current implementation allows unauthorized


creation of a primary store at the package ad




dress or for the pool’s asset, which may prevent


the addition of farming rewards and block pool


creation by making a valid primary store un

available.


It is possible to front-run the creation of a new


lending pair and market by registering an Aptos


account at the pair’s or the market’s expected


address.


validates the swap route by asserting that


the first asset matches the input and the last


matches the output.



© 2025 Otter Audits LLC. All Rights Reserved. 6 / 33


Echelon Audit 04 - Vulnerabilities


The pair creation process lacks validation of


critical risk parameter. Also, there is a lack





of boundary checks on liquidation parameters


during market creation, risking invalid market


configurations that may disrupt liquidation be

havior.



OS-TEH-ADV-05


OS-TEH-ADV-06


OS-TEH-ADV-07


OS-TEH-ADV-08


OS-TEH-ADV-09



is mislabeled as 0 _._ 01% in the comment, though





it actually represents 0 _._ 10%.


check if a market’s liquidation incentive is higher


than the efficiency mode’s, allowing markets


with weaker liquidation incentives to enter.

|claim_reward_fa|incor|
|---|---|
|**`fungible_asset::withdraw`**|**`fungible_asset::withdraw`**|



reward claims if the reward FA is dispatchable.


There is a lack of functionality to un

freeze coin stores after a freeze operation in



© 2025 Otter Audits LLC. All Rights Reserved. 7 / 33


Echelon Audit 04 - Vulnerabilities


**Description**


The issue in the lending core farming module occurs when a user is accruing a specific reward for


ward was introduced will not receive any rewards for the period between their staking and their first







This results in lost rewards for users who had an existing stake balance before the reward program was


introduced. A similar issue also exists in the isolated lending farming module.


**Remediation**


full entitled rewards.


**Patch**


Fixed in [a8c9301.](https://github.com/EchelonMarket/echelon-modules/commit/a8c930178cfd1e119662a9a166ffcc1f1e947270)


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 33


Echelon Audit 04 - Vulnerabilities


**Description**


supplied assets even if their position is underwater. This creates a vulnerability where users may extract


value even though they are insolvent. If the borrowed value exceeds collateral, supply shares should not


be withdrawable, as they may be needed to cover the shortfall.


**Remediation**


Enforce a solvency check before permitting withdrawals.


**Patch**


Fixed in [15a9dd7.](https://github.com/EchelonMarket/echelon-modules/commit/15a9dd76c5880c232e25e0bedf483f35284ed3b2)


© 2025 Otter Audits LLC. All Rights Reserved. 9 / 33


Echelon Audit 04 - Vulnerabilities


**Description**


already exists at the address before creating a new one.





the address. As anyone may create a primary store at any address since it is permissionless, it enables an


attacker to create a primary store for an asset at the package address. This action will block any subsequent


farms.









sufficient information to derive the address and preemptively create a primary store for the pool’s asset


transaction executes.


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 33


Echelon Audit 04 - Vulnerabilities


**Remediation**


attempt to create a new store if one already exists at the address.


**Patch**


Fixed in [a8c9301.](https://github.com/EchelonMarket/echelon-modules/commit/a8c930178cfd1e119662a9a166ffcc1f1e947270)


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 33


Echelon Audit 04 - Vulnerabilities


**Description**


pair with a jump interest rate model. However, it is vulnerable to front-running. An attacker may observe a


pending pair creation and preemptively register their Aptos account to the to-be-created pair’s address


before the pair is fully initialized.


_>__ _isolated_lending/sources/isolated_lending.move_ rust

```
    public fun create_pair_with_jump_model<LiabilityCoinType, CollateralCoinType>(manager:

```


_�→_


_�→_


_�→_


_�→_


```
&signer, collateral_factor_bps: u64, liquidation_incentive_bps: u64,
initial_liquidity: u64, base_rate_bps: u64, multiplier_bps: u64,
jump_multiplier_bps: u64, utilization_kink_bps: u64, collateral_dust_amount: u64):
Object<Pair> acquires IsolatedLending, Pair, AccountPositions, CoinInfo,
JumpInterestRateModel {

```


_�→_
```
[...]
let (pair_signer, pair_obj) = create_pair_with_jump_model_internal(manager,

```


_�→_


_�→_


_�→_


```
collateral_factor_bps, liquidation_incentive_bps, initial_liquidity,
liability_info, collateral_info, base_rate_bps, multiplier_bps,
jump_multiplier_bps, utilization_kink_bps, collateral_dust_amount);

```

```
      aptos_account::create_account(signer::address_of(&pair_signer));
      [...]
  }

```

front-run with a call to register the Aptos account at the address of the market that it is going to be created,


resulting in a denial-of-service scenario.


**Remediation**


Aptos account for the pair and market signer, respectively, only if it does not exist.


**Patch**


Fixed in [a966e7f.](https://github.com/EchelonMarket/echelon-modules/commit/a966e7f61f70119d6d5d527264d85deedc23c358)


© 2025 Otter Audits LLC. All Rights Reserved. 12 / 33


Echelon Audit 04 - Vulnerabilities


**Description**

|Col1|Y|
|---|---|
|**`loop_supply_x_borrow_y_fa`**|c|



parameter. This logic is reversed and unnecessary. The route should instead start with the borrowed


original collateral.


_>__ _lending_leverage/sources/leverage.move_ rust

```
  public fun loop_supply_x_borrow_y_fa(account: &signer, supply_market: Object<Market>,

```


_�→_


_�→_


```
borrow_market: Object<Market>, pool_route: vector<Object<Pool>>, asset_out_route:
vector<Object<Metadata>>, target_health_factor_bps: u64, num_loop: u64, in:
FungibleAsset, out_metadata: Object<Metadata>): FungibleAsset {

```


_�→_
```
assert!(vector::length(&pool_route) == vector::length(&asset_out_route),

```


_�→_ `ERR_LEVERAGE_MALFORMED_ROUTE);`
```
    assert!(*vector::borrow(&asset_out_route, vector::length(&asset_out_route) - 1) ==
```

_�→_ `out_metadata,` `ERR_LEVERAGE_MALFORMED_ROUTE);`
```
    assert!(*vector::borrow(&asset_out_route, 0) == fungible_asset::asset_metadata(&in),
```

_�→_ `ERR_LEVERAGE_MALFORMED_ROUTE);`
```
    [...]
  }

```

**Remediation**


the input token, rather than the first.


**Patch**


Fixed in [26996e5.](https://github.com/EchelonMarket/echelon-modules/commit/26996e55ec60a639f26e9e40e6e828a408849307)


© 2025 Otter Audits LLC. All Rights Reserved. 13 / 33


Echelon Audit 04 - Vulnerabilities


**Description**


liquidate a position. A reasonable incentive encourages liquidators to help maintain protocol health. Since


high liquidation rewards. This may result in unfair liquidations where liquidators extract much more value


_>__ _isolated_lending/sources/isolated_lending.move_ rust

```
  fun create_pair_internal(manager: &signer, collateral_factor_bps: u64,

```


_�→_


_�→_


```
liquidation_incentive_bps: u64, initial_liquidity: u64, interest_rate_model_type: u64,
collateral_dust_amount: u64, liability_info: AssetInfo, collateral_info: AssetInfo):
(signer, Object<Pair>) acquires IsolatedLending, AccountPositions {

```


_�→_
```
// validate collateral_factor_bps
assert!(collateral_factor_bps <= BPS_BASE,

```


_�→_ `ERR_ISOLATED_LENDING_INVALID_COLLATERAL_FACTOR_BPS);`
```
    validate_liquidation_collateral_coverage(collateral_factor_bps, liquidation_incentive_bps);

    // check initial_liquidity
    assert!(initial_liquidity >= MINIMUM_INITIAL_LIQUIDITY,
```

_�→_ `ERR_ISOLATED_LENDING_INVALID_INITIAL_LIQUIDITY);`

```
    // create pair
    let constructor_ref = object::create_sticky_object(package::package_address());
    let pair_signer = object::generate_signer(&constructor_ref);
    [...]
  }

```

zero, as a collateral factor of zero implies no borrowing power, which may render the pair useless. Also,

|lending_core::create_market_with_jump_model_internal|Col2|Col3|Col4|lacks sufficient boun|
|---|---|---|---|---|
|key parameters.<br>Specifically, it does not ensure that<br>**`liquidation_threshold_bps`**<br>equal to 10,000 (100%) or that **`liquidation_incentive_bps`**<br>is greater than or equal|key parameters.<br>Specifically, it does not ensure that<br>**`liquidation_threshold_bps`**<br>equal to 10,000 (100%) or that **`liquidation_incentive_bps`**<br>is greater than or equal|**`liquidation_threshold_bps`**|**`liquidation_threshold_bps`**|**`liquidation_threshold_bps`**|
|key parameters.<br>Specifically, it does not ensure that<br>**`liquidation_threshold_bps`**<br>equal to 10,000 (100%) or that **`liquidation_incentive_bps`**<br>is greater than or equal|**`liquidation_incentive_bps`**|**`liquidation_incentive_bps`**|is greater than or equal|is greater than or equal|



© 2025 Otter Audits LLC. All Rights Reserved. 14 / 33


Echelon Audit 04 - Vulnerabilities


**Remediation**


**Patch**


Fixed in [a6bec7e.](https://github.com/EchelonMarket/echelon-modules/commit/a6bec7ee91e18a23e7ba7e96dc6659f890924145)

|liquidation_incentive_bps|Col2|
|---|---|
|**`liquidation_incentive_bps`**<br><br>|**`BPS_BASE`**|



© 2025 Otter Audits LLC. All Rights Reserved. 15 / 33


Echelon Audit 04 - Vulnerabilities


**Description**


it represents 0 _._ 01%, which is incorrect as 10 basis points equals 0 _._ 10%, not 0 _._ 01%. This mismatch creates

ambiguity regarding the actual fee applied on borrow transactions. If the intended fee is 0 _._ 01%, the value

should be 1, and if the value of 10 is correct, the comment should be updated to state 0 _._ 10%.


_>__ _lending_core/sources/lending.move_ rust

```
  const DEFAULT_ORIGINATION_FEE_BPS: u64 = 10; // 10 bps or 0.01% of the borrowed asset

```

**Remediation**


Ensure the comment and the assigned value are consistent with each other.


**Patch**


Fixed in [a966e7f.](https://github.com/EchelonMarket/echelon-modules/commit/a966e7f61f70119d6d5d527264d85deedc23c358)


© 2025 Otter Audits LLC. All Rights Reserved. 16 / 33


Echelon Audit 04 - Vulnerabilities


**Description**


with lower liquidation incentives. This bypasses the intended safety constraint, enabling borrowers to gain


excessive leverage while reducing rewards for liquidators.


**Remediation**


**Patch**


Fixed in [a966e7f.](https://github.com/EchelonMarket/echelon-modules/commit/a966e7f61f70119d6d5d527264d85deedc23c358)


© 2025 Otter Audits LLC. All Rights Reserved. 17 / 33


Echelon Audit 04 - Vulnerabilities


**Description**


withdrawal will fail, preventing users from claiming their rewards. A similar issue exists within


_>__ _lending_core/sources/lending.move_ rust

```
  public fun claim_reward_fa(account: &signer, asset_metadata: Object<Metadata>,
```

_�→_ `farming_identifier:` `String):` `FungibleAsset` `acquires` `Farming,` `Staker` `{`
```
    let reward_amount = claim_reward_internal(signer::address_of(account),
```

_�→_ `fungible_asset::name(asset_metadata),` `farming_identifier);`
```
    fungible_asset::withdraw(&package::package_signer(),

```


_�→_


_�→_
```
  }

```

**Remediation**


```
primary_fungible_store::primary_store(package::package_address(), asset_metadata),
reward_amount)

```


both non-dispatchable and dispatchable assets.


**Patch**


Fixed in [a6bec7e](https://github.com/EchelonMarket/echelon-modules/commit/a6bec7ee91e18a23e7ba7e96dc6659f890924145) and [809241d.](https://github.com/EchelonMarket/echelon-modules/commit/809241dbed2bddb3b58851214cfbc1b12c6477ab)


© 2025 Otter Audits LLC. All Rights Reserved. 18 / 33


Echelon Audit 04 - Vulnerabilities


**Description**


in permanent lockups. Add a function to unfreeze the store’s proper access control to ensure proper


functionality.


**Remediation**


Implementing a corresponding unfreeze functionality to revert a freeze operation.


**Patch**


Fixed in [a966e7f.](https://github.com/EchelonMarket/echelon-modules/commit/a966e7f61f70119d6d5d527264d85deedc23c358)


© 2025 Otter Audits LLC. All Rights Reserved. 19 / 33


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.


Several liquidation functions mistakenly borrow the wrong asset due to



OS-TEH-SUG-00



incorrect flashloan parameter ordering, resulting in them executing with


zero funds and failing.



OS-TEH-SUG-01 The codebase may be optimized for improved efficiency.


Recommendation for updating the codebase to improve functionality and

OS-TEH-SUG-02

mitigate potential security issues.


There are several instances where proper validation is not performed, re
OS-TEH-SUG-03

sulting in potential security issues.


Modifications to ensure the inclusion of explicit checks to prevent unex


OS-TEH-SUG-04


OS-TEH-SUG-05


OS-TEH-SUG-06



pected aborts or panics, improving the protocol’s robustness and error


handling.


Suggestions regarding inconsistencies in the codebase and ensuring ad

herence to coding best practices.


The codebase contains multiple cases of redundant and unutilized code


that should be removed for better maintainability and clarity.



© 2025 Otter Audits LLC. All Rights Reserved. 20 / 33


Echelon Audit 05 - General Findings


**Failed** **Liquidations** **Due** **to** **Flashloan** **Asset** **Mismatch** OS-TEH-SUG-00


**Description**


and the liquidation proceeds with zero assets, failing with no debt repaid or collateral seized.


_>__ _liquidator/sources/liquidator.move_ rust

```
  public entry fun repay_APT_seize_THL(
    account: &signer,
    vault_address: address,
    repay_amount: u64,
    min_shares_out: u64
  ) {
    let (zero_0, loan, zero_2, zero_3, flashloan) = stable_pool::flashloan<ThalaAPT, AptosCoin,
```

_�→_ `Null,` `Null>(`
```
      repay_amount,
      0,
      0,
      0
    );
    let seized = liquidate<THL, AptosCoin>(account, vault_address, loan, min_shares_out);
    let swapped = weighted_pool::swap_exact_in<THL, AptosCoin, Null, Null, Weight_50, Weight_50,
```

_�→_ `Null,Null,` `THL,` `AptosCoin>(seized);`
```
    repay_amount = repay_amount + math64::mul_div(repay_amount, 1, 10000);
    stable_pool::pay_flashloan(zero_0, coin::extract(&mut swapped, repay_amount), zero_2,
```

_�→_ `zero_3,flashloan);`
```
    aptos_account::deposit_coins<AptosCoin>(signer::address_of(account), swapped);
  }

```

**Remediation**


**Patch**

|l functions in|liquidator|
|---|---|
|**`flashloan`**|calls.|



Acknowledged by Thala team.


© 2025 Otter Audits LLC. All Rights Reserved. 21 / 33


Echelon Audit 05 - General Findings


**Code** **Optimization** OS-TEH-SUG-01


**Description**


**`collateral_factor_bps`** **`<=`** **`liquidation_threshold_bps`** is placed inside the loop even


though these values are constant across the loop. Similarly, in

|set_efficiency_mode_liquidation_threshold_bps|, the|
|---|---|
|**`e_mode.collateral_factor_bps`** **`<=`** **`liquidation_threshold_bps`**|**`e_mode.collateral_factor_bps`** **`<=`** **`liquidation_threshold_bps`**|



the loop. Repeating these assertions for every market is unnecessary. This results in inefficiency


due to redundant computations. Move these two assertions outside their respective loops.


_>__ _lending_core/sources/lending.move_ rust

```
     public entry fun create_efficiency_mode_v2(manager: &signer, markets:

```


_�→_


_�→_


_�→_


```
vector<Object<Market>>, collateral_factor_bps: u64, liquidation_incentive_bps: u64,
liquidation_threshold_bps: u64) acquires Lending, Market,
MarketLiquidationThreshold, MarketLiquidationIncentive, EmodeLiquidationThreshold
{

```


_�→_
```
[...]
vector::for_each(emode_markets, |market_obj| {

```

```
          [...]
          assert!(collateral_factor_bps <=
```

_�→_ `liquidation_threshold_bps,ERR_LENDING_INVALID_LIQUIDATION_THRESHOLD_BPS);`
```
          [...]
       });
     }

```

lize manual signer generation, which duplicates logic. Replacing these with the standardized


which introduces unnecessary complexity. Replace this with a call to


© 2025 Otter Audits LLC. All Rights Reserved. 22 / 33


Echelon Audit 05 - General Findings


_>__ _lending_core/sources/lending.move_ rust

```
     // Reserve is owned by the protocol. The funds can be withdrawn as protocol income.
     public entry fun withdraw_reserve<CoinType>(manager: &signer, market_obj: Object<Market>,
```

_�→_ `recipient:` `address)` `acquires` `Market,` `CoinInfo` `{`
```
       [...]
       market.total_cash = market.total_cash - withdraw_amount;
       let _total_cash = market.total_cash;

       let withdrawn_coins = coin::withdraw<CoinType>(&market_signer(market_obj),
```

_�→_ `withdraw_amount);`
```
       if (signer::address_of(manager) == recipient) {
          coin::register<CoinType>(manager);
       };
       coin::deposit(recipient, withdrawn_coins);
       [...]
     }

```

**Remediation**


Incorporate the above-stated refactors.


© 2025 Otter Audits LLC. All Rights Reserved. 23 / 33


Echelon Audit 05 - General Findings


**Code** **Refactoring** OS-TEH-SUG-02


**Description**


is intended for read-only functions that do not mutate blockchain state. However,

|account_supply_amount|Col2|
|---|---|
|**`accrue_pair_interest`**|,|



decorator to avoid confusion.


_>__ _isolated_lending/sources/isolated_lending.move_ rust

```
     #[view]
     public fun account_supply_amount(account_addr: address, pair_obj: Object<Pair>): u64
```

_�→_ `acquires` `IsolatedLending,` `AccountPositions,` `Pair,` `JumpInterestRateModel` `{`
```
       let shares = account_supply_shares(account_addr, pair_obj);
       if (shares == 0) return 0;

       accrue_pair_interest(pair_obj);
       supply_shares_to_amount(pair_obj, shares)
     }

|e|liquidator|Col3|
|---|---|---|
|**`0.01%`**|**`0.01%`**|).<br>Howe|


```

fee charged by the flashloan provider, especially if the fee structure changes or differs across


assets or platforms. To improve accuracy and adaptability, the repay functions should invoke


3. Entry function wrappers that wrap a deprecated functionality, such as


the utilization of non-functional logic.


unsafe, as names are not unique and may be duplicated across different types. Ensure the reward


is clearly distinguishable. Otherwise, it may result in issues i.e., where new epochs are mistakenly


initiated for different fungible assets that share the same name, potentially resulting in incorrect


transfers.


**Remediation**


Incorporate the above-stated refactors.


© 2025 Otter Audits LLC. All Rights Reserved. 24 / 33


Echelon Audit 05 - General Findings


**Missing** **Validation** **Logic** OS-TEH-SUG-03


**Description**

|Col1|set_market_collateral_factor_bps|Col3|Col4|, it is allowed to be e|
|---|---|---|---|---|
|**`<=`**|**`<=`**|), while in|**`create_market_with_jump_model_internal`**|**`create_market_with_jump_model_internal`**|



This mismatch may allow risky configurations with no liquidation buffer, increasing the chances of


bad debt. The validation logic should be unified across all relevant functions to consistently enforce

**`collateral_factor_bps`** **`<`** **`liquidation_threshold_bps`**, including efficiency mode setters.


_>__ _lending_core/sources/lending.move_ rust

```
     public entry fun set_market_collateral_factor_bps([...]) acquires Market, Lending,
```

_�→_ `MarketLiquidationThreshold` `{`
```
       [...]
       assert!(collateral_factor_bps <=

```


_�→_


_�→_
```
  [...]
}

```

```
borrow_market_liquidation_threshold(market_obj).value_bps,
ERR_LENDING_INVALID_LIQUIDATION_THRESHOLD_BPS);

```

```
     fun create_market_with_jump_model_internal([...]): (signer, Object<Market>) acquires
```

_�→_ `Lending,` `MarketRateLimit,` `Market,` `MarketOriginationFee` `{`
```
       assert!(utilization_kink_bps <= BPS_BASE, ERR_LENDING_INVALID_UTILIZATION_KINK_BPS);
       assert!(collateral_factor_bps < liquidation_threshold_bps,
```

_�→_ `ERR_LENDING_INVALID_COLLATERAL_FACTOR_BPS);`
```
       [...]
     }

|lending_core::create_market_internal|Col2|Col3|
|---|---|---|
|be<br>set<br>equal<br>to|**`BPS_BASE`**|,<br>which<br>is<br>probl|


|collateral_factor_bps < BPS_BASE|Col2|. A|
|---|---|---|
|to verify if|**`collateral_factor_bps`** **`>`** **`0`**|**`collateral_factor_bps`** **`>`** **`0`**|


```

_>__ _lending_core/sources/lending.move_ rust

```
     fun create_market_internal([...]): (signer, Object<Market>) acquires Lending {
       // validate collateral_factor_bps
       let lending = borrow_global_mut<Lending>(package::package_address());
       assert!(collateral_factor_bps <= BPS_BASE, ERR_LENDING_INVALID_COLLATERAL_FACTOR_BPS);
       [...]
     }

```

© 2025 Otter Audits LLC. All Rights Reserved. 25 / 33


Echelon Audit 05 - General Findings


and collateral undermines the collateralization logic, enabling users to borrow against their own


deposits without real risk. An assertion should enforce asset-type distinction during pair creation.


4. The protocol should extend slippage protection to functions beyond liquidation and include checks


to ensure returned shares or amounts are not zero. It should also validate that input amounts passed


to functions are non-zero.


**Remediation**


Include the above-mentioned validations.


© 2025 Otter Audits LLC. All Rights Reserved. 26 / 33


Echelon Audit 05 - General Findings


**Error** **Handling** OS-TEH-SUG-04


**Description**


1. To ensure smooth operation and graceful handling of failures, view-only functions should verify the


which may result in an abort if it is missing.


account has sufficient balance, which may result in abrupt transaction failures. Add checks for


balance to enable more graceful error handling and clearer failure messages.

|burn_fa|Col2|in|echelon_coin|Col5|
|---|---|---|---|---|
|the|**`burn_ref`**|**`burn_ref`**|**`burn_ref`**|. This improv|



_>__ _echelon_coin/sources/echelon_coin.move_ rust

```
     public fun burn_fa(manager: &signer, fa: FungibleAsset) acquires Capabilities {
       assert!(manager::is_manager(manager), ERR_ECHELON_COIN_UNAUTHORIZED);

       let cap = borrow_global<Capabilities>(package::package_address());
       let (burn_ref, burn_ref_receipt) = coin::get_paired_burn_ref(&cap.burn_capability);
       fungible_asset::burn(&burn_ref, fa);
       coin::return_paired_burn_ref(burn_ref, burn_ref_receipt);
     }

```

currently lacks a check to enforce this. Adding a validation to confirm the market type will improve


error handling on encountering incompatible market types.


**Remediation**


Update the codebase with explicit checks to ensure proper error handling.


© 2025 Otter Audits LLC. All Rights Reserved. 27 / 33


Echelon Audit 05 - General Findings


**Code** **Maturity** OS-TEH-SUG-05


**Description**

|proceeding. However,|set_market_liquidation_incentive_bps|Col3|
|---|---|---|
|**`set_market_rate_limit_internal`**|**`set_market_rate_limit_internal`**|**`set_market_rate_limit_internal`**|
|functions verify that the|functions verify that the|**`market_obj`**|



_>__ _isolated_lending/sources/isolated_lending.move_ rust

```
     public entry fun set_pair_liquidation_incentive_bps(manager: &signer, pair_obj:
```

_�→_ `Object<Pair>,` `liquidation_incentive_bps:` `u64)` `acquires` `Pair` `{`
```
       assert!(manager::is_manager(manager), ERR_ISOLATED_LENDING_UNAUTHORIZED);
       assert!(liquidation_incentive_bps >= BPS_BASE && liquidation_incentive_bps <=

```


_�→_


_�→_


```
MAX_LIQUIDATION_INCENTIVE_BPS,
ERR_ISOLATED_LENDING_INVALID_LIQUIDATION_INCENTIVE_BPS);

```

```
       let pair = borrow_mut_pair(pair_obj);
       validate_liquidation_collateral_coverage(pair.collateral_factor_bps,
```

_�→_ `liquidation_incentive_bps);`

```
       // update liquidation_incentive_bps
       pair.liquidation_incentive_bps = liquidation_incentive_bps;
     }

```

2. State-changing functions should emit events to provide transparency and allow off-chain systems


to track protocol changes. Emitting events for important updates, such as changing interest fees,


user awareness on the current protocol state. Events should only be emitted when an actual change


occurs to avoid misleading logs and unnecessary noise.


_>__ _lending_core/sources/lending.move_ rust

```
     public entry fun set_paused(manager: &signer, paused: bool) acquires PauseFlag {
       assert!(manager::is_manager(manager), ERR_LENDING_UNAUTHORIZED);
       assert!(pause_flag_exists(), ERR_LENDING_PAUSE_FLAG_UNINITIALIZED);
       let flag = borrow_global_mut<PauseFlag>(package::package_address());
       flag.paused = paused
     }

```

© 2025 Otter Audits LLC. All Rights Reserved. 28 / 33


Echelon Audit 05 - General Findings


. This improves consistency and aligns with the pattern utilized in other package modules in the


project.


**Remediation**


Implement the above-mentioned suggestions.


© 2025 Otter Audits LLC. All Rights Reserved. 29 / 33


Echelon Audit 05 - General Findings


**Unutilized/Redundant** **Code** OS-TEH-SUG-06


**Description**


unutilized, these functions pose a significant risk if called, as they may perform critical actions like


wiping a user’s collateral without validation or fund transfers. Such functions should be removed.


_>__ _isolated_lending/sources/isolated_lending.move_ rust

```
     #[view]
     fun preview_remove_collateral(account_addr: address, pair_obj: Object<Pair>, amount: u64):

```


_�→_


```
(FixedPoint64, FixedPoint64) acquires AccountPositions, Pair, CoinInfo,

```


_�→_ `FungibleAssetInfo,` `IsolatedLending,` `JumpInterestRateModel` `{`
```
       remove_collateral_internal(account_addr, pair_obj, amount, false);
       account_liquidity(account_addr, pair_obj)
     }

```

prior assertion.


_>__ _lending_core/sources/farming.move_ rust

```
     /// Add a new Reward for a specific farming pool.
     public entry fun init_alloc_point(manager: &signer, reward_name: String,
```

_�→_ `farming_identifier:` `String,` `alloc_point:u64)` `acquires` `Farming` `{`
```
       [...]
       // check Reward has been initialized for Farming
       assert!(simple_map::contains_key(&farming.rewards, &reward_name),
```

_�→_ `ERR_FARMING_REWARD_UNINITIALIZED);`
```
       [...]
       // update Pool
       let pool = simple_map::borrow_mut(&mut farming.pools, &farming_identifier);
       let last_rewards_sec = if (simple_map::contains_key(&farming.rewards, &reward_name)) {
          current_epoch_seconds(simple_map::borrow(&farming.rewards, &reward_name))
       } else {
          0
       };
       [...]
     }

```

© 2025 Otter Audits LLC. All Rights Reserved. 30 / 33


Echelon Audit 05 - General Findings


They should be removed.


5. In the current implementation, repeated borrows in several places across the code introduce avoidable


three times. These borrows may be consolidated in each function to avoid unnecessary storage


reads and associated gas costs. Also, view functions borrow mutably when it is not necessary


is unnecessary and may be removed.


**Remediation**


Remove the redundant and unutilized code instances highlighted above.


© 2025 Otter Audits LLC. All Rights Reserved. 31 / 33


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


© 2025 Otter Audits LLC. All Rights Reserved. 32 / 33


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


© 2025 Otter Audits LLC. All Rights Reserved. 33 / 33


