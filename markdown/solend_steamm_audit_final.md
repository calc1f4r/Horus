# **Solend Steamm**

Security Assessment


February 4th, 2025 - Prepared by OtterSec


Sangsoo Kang [sangsoo@osec.io](mailto:sangsoo@osec.io)


Michał Bochnak [embe221ed@osec.io](mailto:embe221ed@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


**Scope** **3**


**Findings** **4**


**Vulnerabilities** **5**


OS-SAM-ADV-00 | Lack of Minimum Liquidity Constraint 6


OS-SAM-ADV-01 | Assertion Failure Due to Rounding 7


OS-SAM-ADV-02 | Overestimation of Tokens Resulting in Oversupply 8


OS-SAM-ADV-03 | Risk of Excess Recall Amount 9


OS-SAM-ADV-04 | Lack of Synchronization Between Bank and LendingMarket 10


OS-SAM-ADV-05 | Division by Zero Error 11


**General** **Findings** **12**


OS-SAM-SUG-00 | Minimum Pool Liquidity 13


OS-SAM-SUG-01 | Missing Validation Logic 14


OS-SAM-SUG-02 | Additional Safety Checks 16


OS-SAM-SUG-03 | Code Refactoring 18


OS-SAM-SUG-04 | Code Maturity 20


OS-SAM-SUG-05 | Code Clarity 22


**Appendices**


**Vulnerability** **Rating** **Scale** **24**


**Procedure** **25**


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 25


**01** **—** **Executive** **Summary**

## Overview


January 18th and January 31st, 2025. For more information on our auditing methodology, refer to


Appendix B.

## Key Findings


We produced 12 findings throughout this audit engagement.


In particular, we identified a vulnerability in which inadequate minimum liquidity may result in inflation


attacks in the bank module (OS-SAM-ADV-00). Additionally, the assertion check for the CToken ratio


may fail due to the presence of roundings during cToken-to-underlying token conversions in the recall


functionality, resulting in frequent aborts (OS-SAM-ADV-01). Furthermore, the current tokens-to-deposit


logic allows users to over-supply tokens due to insufficient checks, which may disrupt the pool’s balance


(OS-SAM-ADV-02).


We also made suggestions regarding inconsistencies in the codebase and ensuring adherence to coding


best practices (OS-SAM-SUG-04), and advised introducing a minimum liquidity reserve to prevent


the pool from becoming entirely empty (OS-SAM-SUG-00). We further recommended implementing


validation logic in several areas within the codebase to mitigate potential security issues (OS-SAM-SUG

01).


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 25


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/solendprotocol/steamm.](https://github.com/solendprotocol/steamm)


This audit was performed against commit [ecfdf45.](https://github.com/solendprotocol/steamm/commit/ecfdf457242d33dc73b11a6f05ee8b086d67a4ae) We further reviewed [PR#81.](https://github.com/solendprotocol/steamm/pull/81)


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**


Steamm is an AMM with embedded money market integration, designed


to maximize capital efficiency. It improves liquidity utilization by de
steamm

positing idle funds into Suilend’s lending markets, generating extra yield


for liquidity providers.


© 2025 Otter Audits LLC. All Rights Reserved. 3 / 25


**03** **—** **Findings**


Overall, we reported 12 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.







© 2025 Otter Audits LLC. All Rights Reserved. 4 / 25


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


Inadequate minimum liquidity may result in in


fail due to the presence of roundings during


users to oversupply tokens due to insufficient


checks, which may disrupt the pool’s balance.


the available reserves due to the utilization of


insufficient liquidity for the recall process.


fications to the obligation’s state and potential


If one reserve is fully drained, functions

|such as|tokens_to_deposit|Col3|
|---|---|---|
|**`lp_tokens_to_mint`**|**`lp_tokens_to_mint`**|will<br>fail<br>d|



division by zero error.



OS-SAM-ADV-00


OS-SAM-ADV-01


OS-SAM-ADV-02


OS-SAM-ADV-03


OS-SAM-ADV-04


OS-SAM-ADV-05





© 2025 Otter Audits LLC. All Rights Reserved. 5 / 25


Solend Steamm Audit 04 - Vulnerabilities


**Description**


present at all times. Insufficient minimum liquidity may expose it to inflation attacks, enabling malicious


burning bToken and increasing the amount of the underlying token can trigger zero mint when a user


deposits, causing a loss for the user.


**Remediation**


**Patch**


Resolved in [6e17d4f.](https://github.com/solendprotocol/steamm/commit/6e17d4fc8be77557e51b45bcb3c308d3423d0d0d)


© 2025 Otter Audits LLC. All Rights Reserved. 6 / 25


Solend Steamm Audit 04 - Vulnerabilities


**Description**



_bank.funds_ _ _deployed_



_ _deployed_

_<_ = _[recalled]_ [_] _[amount]_
_lending.ctokens_ _ctoken_ _ _amount_



_ctoken_ _ _amount_



_>__ _steamm/sources/bank/bank.move_ rust

```
  fun recall<P, T, BToken>(
    bank: &mut Bank<P, T, BToken>,
    lending_market: &mut LendingMarket<P>,
    amount_to_recall: u64,
    clock: &Clock,
    ctx: &mut TxContext,
  ) {
    [...]
     assert!(
      ctoken_amount * bank.funds_deployed(lending_market, clock).floor() <= lending.ctokens *
```

_�→_ `recalled_amount,`
```
      EInvalidCTokenRatio,
    );
    [...]
  }

```

**Remediation**


Remove the assertion since the inequality isn’t always guaranteed to hold.


**Patch**


Resolved in [38c5317.](https://github.com/solendprotocol/steamm/commit/38c53173e5d6efa65924bbf4754aeaa57a2b1d9c)


© 2025 Otter Audits LLC. All Rights Reserved. 7 / 25


Solend Steamm Audit 04 - Vulnerabilities


**Description**

|b_star|Col2|
|---|---|
|**`b_star`** <br>|~~**`max_a`**~~|



under certain conditions.


_>__ _steamm/sources/pool/pool_math.move_ rust

```
  fun tokens_to_deposit(reserve_a: u64, reserve_b: u64, max_a: u64, max_b: u64): (u64, u64) {
    assert!(max_a > 0, EDepositMaxAParamCantBeZero);
    if (reserve_a == 0 && reserve_b == 0) {
      (max_a, max_b)
    } else {
      let b_star = safe_mul_div_up(max_a, reserve_b, reserve_a);
      if (b_star <= max_b) { (max_a, b_star) } else {
         let a_star = safe_mul_div_up(max_b, reserve_a, reserve_b);
         assert!(a_star > 0, EDepositRatioLeadsToZeroA);
         assert!(a_star <= max_a, EDepositRatioInvalid);
         (a_star, max_b)
      }
    }
  }

```

may include a dust amount. This implies that users may inadvertently attempt to supply more tokens than


necessary to maintain the correct reserve balance.


**Remediation**


**Patch**


Acknlowedged by the Solend development team.


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 25


Solend Steamm Audit 04 - Vulnerabilities


**Description**


the recall amount to the minimum block size. The issue occurs if the available funds (the reserves in the


**Remediation**


**Patch**


Acknowledged by the Solend development team.


© 2025 Otter Audits LLC. All Rights Reserved. 9 / 25


Solend Steamm Audit 04 - Vulnerabilities


04


**Description**


implies that a new obligation may be created without requiring interaction with the Bank module, which


changes in its tracking system.


**Remediation**


Ensure that the bank and lending market are operated by a trustworthy entity.


**Patch**


Acknowledged by the developers.


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 25


Solend Steamm Audit 04 - Vulnerabilities


**Description**


In the current implementation, it is possible for the pool to have one of the reserves fully drained. In


should deposit based on the current ratio between the reserves of token A and token B. The function utilizes


_>__ _steamm/sources/pool/pool_math.move_ rust

```
  fun tokens_to_deposit(reserve_a: u64, reserve_b: u64, max_a: u64, max_b: u64): (u64, u64) {
    assert!(max_a > 0, EDepositMaxAParamCantBeZero);
    if (reserve_a == 0 && reserve_b == 0) {
      (max_a, max_b)
    } else {
      let b_star = safe_mul_div_up(max_a, reserve_b, reserve_a);
      if (b_star <= max_b) { (max_a, b_star) } else {
         let a_star = safe_mul_div_up(max_b, reserve_a, reserve_b);
         assert!(a_star > 0, EDepositRatioLeadsToZeroA);
         assert!(a_star <= max_a, EDepositRatioInvalid);
         (a_star, max_b)
      }
    }
  }

```

**Remediation**


**Patch**


Acknowledged by the developers.


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 25


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.



OS-SAM-SUG-00


OS-SAM-SUG-01


OS-SAM-SUG-02


OS-SAM-SUG-03


OS-SAM-SUG-04


OS-SAM-SUG-05



a non-zero reserve, allowing for full withdrawals.


There are several instances where proper validation is not performed, resulting


in potential security issues.


Additional safety checks may be incorporated within the codebase to make it


more robust and secure.


Recommendation for modifying the codebase for improved functionality, effi

ciency, and mitigate potential security issues.


Suggestions regarding inconsistencies in the codebase and ensuring adherence


to coding best practices.


Highlighting inconsistencies that affecting the overall functionality and clarity of


the codebase.



© 2025 Otter Audits LLC. All Rights Reserved. 12 / 25


Solend Steamm Audit 05 - General Findings


**Minimum** **Pool** **Liquidity** OS-SAM-SUG-00


**Description**


in the calculation of the utilization ratio formula will result in a division-by-zero error. However, this


creates a problem during full withdrawals.


_>__ _steamm/sources/bank/bank_math.move_ rust

```
  public(package) fun compute_utilisation_bps(funds_available: u64, funds_deployed: u64): u64 {
    assert!(funds_available + funds_deployed > 0, EEmptyBank);
    (funds_deployed * 10_000) / (funds_available + funds_deployed)
  }

```

and preventing the last withdrawal.


**Remediation**


becoming entirely empty.


**Patch**


Resolved in [6e17d4f.](https://github.com/solendprotocol/steamm/commit/6e17d4fc8be77557e51b45bcb3c308d3423d0d0d)


© 2025 Otter Audits LLC. All Rights Reserved. 13 / 25


Solend Steamm Audit 05 - General Findings


**Missing** **Validation** **Logic** OS-SAM-SUG-01


**Description**


1. Include a check to ensure that the two tokens involved in the creation of the pool are of different


types.

|pool::redeem_liquidity|Col2|includes a ch|
|---|---|---|
|via|**`assert_lp_supply_reserve_ratio`**|**`assert_lp_supply_reserve_ratio`**|



well.


operations. Allowing zero-value minting, burning, deposit, and withdrawing is unnecessary, wastes


for such cases.

|s. Ensure|coin_in|Col3|
|---|---|---|
|**`amount_in`**|**`amount_in`**|is great|



_>__ _steamm/sources/quoters/quoter_math.move_ rust

```
     public(package) fun swap([...]): u64 {
       [...]
       // `z` is defined as �out / ReserveOut. Therefore depending on the
       // direction of the trade we pick the corresponding ouput reserve
       let delta_out = if (x2y) {
          z.mul(r_y).to_u128_down() as u64
       } else {
          z.mul(r_x).to_u128_down() as u64
       };
       [...]
     }

```

© 2025 Otter Audits LLC. All Rights Reserved. 14 / 25


Solend Steamm Audit 05 - General Findings


6. Ensure that when a pool is created, the token type is correctly linked to the corresponding oracle


index to prevent mismatches. Additionally, prevent modification of the oracle reference to another


feed post-deployment, as this may compromise price accuracy and protocol security.


**Remediation**


Incorporate the above-mentioned validations into the codebase.


**Patch**


1. Issue #1 resolved in [344e81b.](https://github.com/solendprotocol/steamm/commit/344e81b2dc4330502412bce26d22f85d68a3dd43)


2. Issue #2 resolved in [ab76c55.](https://github.com/solendprotocol/steamm/commit/ab76c550412d811b2f8e66dc26728d4ce6ebc58e)


3. Issue #3 resolved in [a8c5738.](https://github.com/solendprotocol/steamm/commit/a8c57388f22dd9f1a50bcd21169bbeeae1c67277)


© 2025 Otter Audits LLC. All Rights Reserved. 15 / 25


Solend Steamm Audit 05 - General Findings


**Additional** **Safety** **Checks** OS-SAM-SUG-02


**Description**


ensures that when the first deposit is made, enough LP tokens exist for the minimum lock.


_>__ _steamm/sources/pool/pool.move_ rust

```
     public fun deposit_liquidity<A, B, Quoter: store, LpType: drop>([...]): (Coin<LpType>,
```

_�→_ `DepositResult)` `{`
```
       pool.version.assert_version_and_upgrade(CURRENT_VERSION);
       assert!(!(coin_a.value() == 0 && coin_b.value() == 0), EEmptyCoins);
       // Compute token deposits and delta lp tokens
       let quote = quote_deposit_(
          pool,
          max_a,
          max_b,
       );
       let initial_lp_supply = pool.lp_supply.supply_value();
       let (initial_total_funds_a, initial_total_funds_b) = pool.balance_amounts();
       let balance_a = coin_a.balance_mut().split(quote.deposit_a());
       let balance_b = coin_b.balance_mut().split(quote.deposit_b());
     }

```

errors if incorrect values are provided. Implementing proper validation is recommended to ensure


robustness.

|Validate the subtractions in both|bank_math::compute_amount_to_deploy|Col3|
|---|---|---|
|**`bank_math::compute_amount_to_recall`**|**`bank_math::compute_amount_to_recall`**|**`bank_math::compute_amount_to_recall`**|
|the subtraction operations, especially if the|the subtraction operations, especially if the|**`target_utilisation`**|



to appropriately address the scenario when the bank’s liquidity falls below a minimum threshold


required to maintain stable operations.


utilization of invalid or zero prices within the protocol.


**Remediation**


Add the checks stated above.


© 2025 Otter Audits LLC. All Rights Reserved. 16 / 25


Solend Steamm Audit 05 - General Findings


**Patch**


1. Issue #1 resolved in [0a27ee9.](https://github.com/solendprotocol/steamm/commit/0a27ee911655f6fbc09be69065444769c2beac3d)


2. Issue #2 resolved in [0aa893f.](https://github.com/solendprotocol/steamm/commit/0aa893f54f7da139da3c5e3347a9a17538537f65)


© 2025 Otter Audits LLC. All Rights Reserved. 17 / 25


Solend Steamm Audit 05 - General Findings


**Code** **Refactoring** OS-SAM-SUG-03


**Description**


system remains within its desired liquidity utilization range.

|The early return in|bank::deploy|Col3|
|---|---|---|
|**`min_token_block_size`**|**`min_token_block_size`**|. However|



rate, preventing it from staying within the target utilization range.


_>__ _steamm/sources/bank/bank.move_ rust

```
     fun deploy<P, T, BToken>(
       bank: &mut Bank<P, T, BToken>,
       lending_market: &mut LendingMarket<P>,
       amount_to_deploy: u64,
       clock: &Clock,
       ctx: &mut TxContext,
     ) {
       let lending = bank.lending.borrow();
       if (amount_to_deploy < bank.min_token_block_size) {
          return
       };
       let balance_to_lend = bank.funds_available.split(amount_to_deploy);
       [...]
     }

```

mediate values, which may result in precision loss. Dividing first and then multiplying ensures higher


precision.









© 2025 Otter Audits LLC. All Rights Reserved. 18 / 25


Solend Steamm Audit 05 - General Findings


that the values will wrap around rather than panic on overflow.


**Remediation**


Update the codebase with the above refactors.


**Patch**


1. Issue #3 resolved in [96f13c5.](https://github.com/solendprotocol/steamm/commit/96f13c5b80437b9fd75506fe258df0cae4efbf30)


© 2025 Otter Audits LLC. All Rights Reserved. 19 / 25


Solend Steamm Audit 05 - General Findings


**Code** **Maturity** OS-SAM-SUG-04


**Description**


fields always reflect the actual fees collected.

|amounts from|quote.fees|Col3|Col4|in|
|---|---|---|---|---|
|**`balance_a_value`**|**`balance_a_value`**|) and|**`coin_b`**|**`coin_b`**|



_>__ _contracts/steamm/sources/pool/pool.move_ rust

```
     public fun redeem_liquidity<A, B, Quoter: store, LpType: drop>(
       pool: &mut Pool<A, B, Quoter, LpType>,
       lp_tokens: Coin<LpType>,
       min_a: u64,
       min_b: u64,
       ctx: &mut TxContext,
     ): (Coin<A>, Coin<B>, RedeemResult) {
       [...]
       // Update redemption fee data
       pool.trading_data.redemption_fees_a = pool.trading_data.redemption_fees_a +
```

_�→_ `quote.fees_a();`
```
       pool.trading_data.redemption_fees_b = pool.trading_data.redemption_fees_b +
```

_�→_ `quote.fees_b();`
```
       [...]
     }

```

rounds up, favoring the pool and liquidity providers rather than the users.


reflection to validate type relationships. However, this method is not a reliable approach for type


verification and should be utilized cautiously. That said, its current implementation does not pose a


direct security risk.


_>__ _sources/bank/bank.move_ rust

```
     public(package) fun assert_btoken_type<T, BToken>() {
       let type_reflection_t = get_type_reflection<T>();
       let type_reflection_btoken = get_type_reflection<BToken>();

       let mut expected_btoken_type = string::utf8(b"B_");
       string::append(&mut expected_btoken_type, type_reflection_t);
       assert!(type_reflection_btoken == expected_btoken_type, EBTokenTypeInvalid);
     }

```

© 2025 Otter Audits LLC. All Rights Reserved. 20 / 25


Solend Steamm Audit 05 - General Findings


true to correctly interpret Switchboard prices as fixed-point decimals.


**Remediation**


Implement the above-mentioned suggestions.


**Patch**


1. Issue #1 resolved in [2b99003.](https://github.com/solendprotocol/steamm/commit/2b99003dd1955f6fa584e1a1d0e85c7758cf4b89)


2. Issue #2 resolved in [5325116.](https://github.com/solendprotocol/steamm/commit/53251167b86166093bb80c09e1e2b5b85b542c9d)


3. Issue #4 resolved in [71c2aed.](https://github.com/solendprotocol/steamm/commit/71c2aed242105ad49e2fd4ef1b2ffb45d5aa8239)


© 2025 Otter Audits LLC. All Rights Reserved. 21 / 25


Solend Steamm Audit 05 - General Findings


**Code** **Clarity** OS-SAM-SUG-05


**Description**


_>__ _steamm/sources/quote.move_ rust

```
     public fun output_fee_rate(swap_quote: &SwapQuote): Decimal {
       let total_fees = decimal::from(
          swap_quote.output_fees().pool_fees() + swap_quote.output_fees().protocol_fees(),
       );
       total_fees.div(decimal::from(swap_quote.amount_out()))
     }

```

the utilization rate is below 100%, however, the actual error is about indicating when the utilization


range is below zero. Utilize the correct error.


data, it is a greater than or equal to function, and not a compare function.


_>__ _steamm/sources/math.move_ rust

```
     public(package) fun safe_compare_mul_u64(a1: u64, b1: u64, a2: u64, b2: u64): bool {
       let left = (a1 as u128) * (b1 as u128);
       let right = (a2 as u128) * (b2 as u128);
       left >= right
     }

```

**Remediation**


© 2025 Otter Audits LLC. All Rights Reserved. 22 / 25


Solend Steamm Audit 05 - General Findings


**Patch**


1. Issue #2 resolved in [0aa893f.](https://github.com/solendprotocol/steamm/commit/0aa893f54f7da139da3c5e3347a9a17538537f65)


2. Issue #3 resolved in [cc20935.](https://github.com/solendprotocol/steamm/commit/cc20935223a73b3603545f5d7c07846b7622cf7b)


3. Issue #4 resolved in [1a36800.](https://github.com/solendprotocol/steamm/commit/1a3680001a7cb2b5e08b3153a715f02459ae5f2f)


© 2025 Otter Audits LLC. All Rights Reserved. 23 / 25


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


undue risk.


Examples:


        - Oracle manipulation with large capital requirements and multiple transactions.


Examples:


        - Explicit assertion of critical internal invariants.


        - Improved input validation.


© 2025 Otter Audits LLC. All Rights Reserved. 24 / 25


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


© 2025 Otter Audits LLC. All Rights Reserved. 25 / 25


