# **ThalaSwap V2**

Security Assessment


January 29th, 2025 - Prepared by OtterSec


Andreas Mantzoutas [andreas@osec.io](mailto:andreas@osec.io)


Bartłomiej Wierzbiński [dark@osec.io](mailto:dark@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


**Scope** **3**


**Findings** **4**


**Vulnerabilities** **5**


OS-THL-ADV-00 | Bypassing Funds Repayment via Double Upscaling 6


**General** **Findings** **8**


OS-THL-SUG-00 | Missing Validation Logic 9


OS-THL-SUG-01 | Discrepancies in Event Emissions 11


OS-THL-SUG-02 | Code Maturity 13


**Appendices**


**Vulnerability** **Rating** **Scale** **14**


**Procedure** **15**


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 15


**01** **—** **Executive** **Summary**

## Overview


This assessment was conducted between January 16th and January 24th, 2025. For more information


on our auditing methodology, refer to Appendix B.

## Key Findings


We produced 4 findings throughout this audit engagement.


In particular, we identified a critical loss-of-funds vulnerability concerning the double upscaling of


balances in the metastable pool, which may result in incorrect flashloan repayment calculations, allowing


the avoidance of repaying borrowed funds (OS-THL-ADV-00).


We also made recommendations to incorporate proper validations (OS-THL-SUG-00) and made sugges

tions to ensure adherence to coding best practices (OS-THL-SUG-02). We further advised utilizing the


proper parameters during emission of events for proper logging of data (OS-THL-SUG-01).


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 15


**02** **—** **Scope**


The source code was delivered to us in a Git repository at


[https://github.com/ThalaLabs/thala-modules/thalaswap_v2.](https://github.com/ThalaLabs/thala-modules/thalaswap_v2) This audit was performed against commit


[5700bce.](https://github.com/ThalaLabs/thala-modules/blob/5700bcebda45fd4200dc8789d137d7975f0495ad)


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**


thalaswap-v2 A multi-asset stable pool for stablecoins and weighted pools.


IT provides mathematical utilities for two types of liquidity pools in
thalaswap-math-v2

ThalaSwap, weighted pools and stable swap pools.


© 2025 Otter Audits LLC. All Rights Reserved. 3 / 15


**03** **—** **Findings**


Overall, we reported 4 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.



© 2025 Otter Audits LLC. All Rights Reserved. 4 / 15


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


The double upscaling of balances in the metastable


pool may result in incorrect flashloan repayment cal

culations, allowing the avoidance of repaying bor

rowed funds.


© 2025 Otter Audits LLC. All Rights Reserved. 5 / 15


ThalaSwap V2 Audit 04 - Vulnerabilities


**Description**

|ess in|pay_flashloan|when|
|---|---|---|
|**`balance_after_flashloan`**|**`balance_after_flashloan`**|**`balance_after_flashloan`**|



twice. When handling meta-stable pools the funds are multiplied by their value derived from an oracle.


As a result the post-repayment invariant computation utilizes an incorrectly scaled value.


_>__ _thalaswap_v2/sources/pool.move_ rust

```
  public fun pay_flashloan(assets: vector<FungibleAsset>, loan: Flashloan) acquires PauseFlag,
```

_�→_ `Pool,` `MetaStablePool,` `StablePool,` `ThalaSwap,` `WeightedPool` `{`
```
    [...]
    if (pool_is_metastable(pool_obj)) {
      borrow_amounts = upscale_metastable_amounts(pool_obj, borrow_amounts);
      balances = upscale_metastable_amounts(pool_obj, pool_balances(pool_obj));
    };
    [...]
    while (i < len) {
      let repay_sub_fees = *vector::borrow(&repay_amounts, i) - *vector::borrow(&fee_amounts,
```

_�→_ `i);`
```
      let balance_after_flashloan = *vector::borrow(&balances, i) + repay_sub_fees;
      vector::push_back(&mut balances_after_flashloan, balance_after_flashloan);
      i = i + 1;
    };
    [...]
    if (pool_is_metastable(pool_obj)) {
      balances_after_flashloan = upscale_metastable_amounts(pool_obj,
```

_�→_ `balances_after_flashloan);`
```
    };
    [...]
  }

```

occurred. This incorrect invariant validation allows the flashloan repayment to proceed without properly


verifying the adequacy of the repayment. Thus, the pool may accept a repayment that is less than the


borrowed amount, resulting in loss of funds


**Remediation**


© 2025 Otter Audits LLC. All Rights Reserved. 6 / 15


ThalaSwap V2 Audit 04 - Vulnerabilities


**Patch**


Fixed in [19dc5f1.](https://github.com/ThalaLabs/thala-modules/commit/19dc5f16e9f3067bf165c1eaccf9784358e12228)


© 2025 Otter Audits LLC. All Rights Reserved. 7 / 15


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.


There are several instances where proper validation is not done, resulting in

OS-THL-SUG-00

potential security issues.


OS-THL-SUG-01

emitted resulting in faulty event logs.


Suggestions regarding inconsistencies in the codebase and ensuring adherence

OS-THL-SUG-02

to coding best practices.


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 15


ThalaSwap V2 Audit 05 - General Findings


**Missing** **Validation** **Logic** OS-THL-SUG-00


**Description**


1. There is an absence of validation for asset decimals when creating a metastable pool in


decimal range for assets in Stable pools. This will result in inconsistent handling of token amounts,


as scaling or interacting with the assets within the pool may become inaccurate.


_>__ _thalaswap_v2/sources/pool.move_ rust

```
     fun validate_assets_metadata(metadata: vector<Object<Metadata>>, pool_type: u8): bool {
       [...]
       if (pool_type == POOL_TYPE_STABLE) {
          // Check that pool decimals are within bounds
          let j = 0;
          while (j < num_assets) {
            let x = vector::borrow(&metadata, j);
            let decimals = fungible_asset::decimals(*x);
            if (decimals > MAX_STABLE_DECIMALS_SUPPORTED ||
```

_�→_ `decimals<MIN_STABLE_DECIMALS_SUPPORTED)` `return` `false;`
```
            j = j + 1;
          };
       };
       [...]
     }

```

permits borrowing the entire balance of an asset in the pool. This may result in a temporary drainage


of the entire pool’s liquidity for the duration of the flashloan.


_>__ _thalaswap_v2/sources/pool.move_ rust

```
      public fun flashloan(pool_obj: Object<Pool>, amounts: vector<u64>):
```

_�→_ `(vector<FungibleAsset>,` `Flashloan)` `acquires` `PauseFlag,` `Pool` `{`
```
       [...]
       vector::zip(pool.assets_metadata, amounts, |metadata, amount| assert!(amount <=

```


_�→_


_�→_
```
  [...]
}

```

```
primary_fungible_store::balance(pool_addr, metadata),
ERR_POOL_FLASHLOAN_INVALID_AMOUNT));

```


© 2025 Otter Audits LLC. All Rights Reserved. 9 / 15


ThalaSwap V2 Audit 05 - General Findings


**Remediation**


2. Modify the assert condition to strictly check that the flashloan amount is less than the pool balance


**Patch**


1. Fixed in [19dc5f1.](https://github.com/ThalaLabs/thala-modules/commit/19dc5f16e9f3067bf165c1eaccf9784358e12228)


2. Fixed in [7df3ae8.](https://github.com/ThalaLabs/thala-modules/commit/7df3ae8e0463186bc9753a2f4f7a9090762eed74)


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 15


ThalaSwap V2 Audit 05 - General Findings


**Discrepancies** **in** **Event** **Emissions** OS-THL-SUG-01


**Description**


which is the actual amounts of assets the user deposited into the pool.


_>__ _thalaswap_v2/sources/pool.move_ rust

```
     public fun add_liquidity_weighted(pool_obj: Object<Pool>, assets: vector<FungibleAsset>):
```

_�→_ `(FungibleAsset,` `vector<FungibleAsset>)` `acquires` `PauseFlag,` `Pool` `{`
```
       [...]
       event::emit(AddLiquidityEvent {
          pool_obj,
          metadata,
          amounts,
          minted_lp_token_amount: preview.minted_lp_token_amount,
          pool_balances: pool_balances(pool_obj),
       });
       (lp_token, refunds)
     }

```

_>__ _thalaswap_v2/sources/pool.move_ rust

```
     public fun swap_exact_out_stable([...]) [...] {
       [...]
       event::emit(SwapEvent {
          pool_obj,
          metadata: pool_assets_metadata(pool_obj),
          idx_in: preview.idx_in,
          idx_out: preview.idx_out,
          amount_in,
          amount_out,
          total_fee_amount: preview.total_fee_amount,
          protocol_fee_amount: preview.protocol_fee_amount,
          pool_balances: pool_balances(pool_obj),
       });
       [...]
     }

```

© 2025 Otter Audits LLC. All Rights Reserved. 11 / 15


ThalaSwap V2 Audit 05 - General Findings


**Remediation**


assets deposited into the pool.


**Patch**


1. Fixed in [7df3ae8.](https://github.com/ThalaLabs/thala-modules/commit/7df3ae8e0463186bc9753a2f4f7a9090762eed74)


2. Fixed in [19dc5f1.](https://github.com/ThalaLabs/thala-modules/commit/19dc5f16e9f3067bf165c1eaccf9784358e12228)


© 2025 Otter Audits LLC. All Rights Reserved. 12 / 15


ThalaSwap V2 Audit 05 - General Findings


**Code** **Maturity** OS-THL-SUG-02


**Description**


1. If the flashloan fee is lower than the swap fee, users may exploit this economic imbalance by


repeatedly using flashloans for swaps, effectively bypassing swap fees to achieve the same outcome


at a lower cost. This undermines the protocol’s revenue and reduces rewards for liquidity providers.


To prevent this, the flashloan fee should be set equal to or higher than the swap fee.


2 assets, failing to reflect the diversity of real-world scenarios that the application may encounter.


As a result of this narrow scope, complex conditions and edge cases remain untested.


**Remediation**


Implement the above-mentioned suggestions.


**Patch**


Fixed in [19dc5f1.](https://github.com/ThalaLabs/thala-modules/commit/19dc5f16e9f3067bf165c1eaccf9784358e12228)


© 2025 Otter Audits LLC. All Rights Reserved. 13 / 15


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


© 2025 Otter Audits LLC. All Rights Reserved. 14 / 15


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


© 2025 Otter Audits LLC. All Rights Reserved. 15 / 15


