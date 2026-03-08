# **Aftermath Market Making**

Security Assessment


January 25th, 2025 - Prepared by OtterSec


Sangsoo Kang [sangsoo@osec.io](mailto:sangsoo@osec.io)


Michał Bochnak [embe221ed@osec.io](mailto:embe221ed@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **3**


Overview 3


Key Findings 3


**Scope** **4**


**Findings** **5**


**Vulnerabilities** **6**


OS-AMM-ADV-00 | Lack of Access Control 8


OS-AMM-ADV-01 | Tolerance Check Bypass on Forced Withdrawal 9


OS-AMM-ADV-02 | Fund Loss Due to Unchecked Conversion 10


OS-AMM-ADV-03 | Fee Manipulation via Improper LP Coin Split 11


OS-AMM-ADV-04 | Miscalculation Due to Negative Withdrawal Amount 13


OS-AMM-ADV-05 | DoS Due to Surpassing of Event Limit 14


OS-AMM-ADV-06 | Risk of Negative Margin Calculation 15


OS-AMM-ADV-07 | Improper Zero Mint Check 16


OS-AMM-ADV-08 | Inability to Withdraw Owner Fees 17


OS-AMM-ADV-09 | Misalignment of Token Metadata 18


OS-AMM-ADV-10 | Failure to Update Last Used Timestamp of Vault Cap 19


**General** **Findings** **20**


OS-AMM-SUG-00| Utilization of Incorrect Relational Operator 21


OS-AMM-SUG-01| Misleading Event Emission 23


OS-AMM-SUG-02| Missing Validation Logic 24


OS-AMM-SUG-03| Code Maturity 25


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 28


Aftermath Market Making Audit


TABLE OF CONTENTS


OS-AMM-SUG-04| Code Refactoring 26


**Appendices**


**Vulnerability** **Rating** **Scale** **27**


**Procedure** **28**


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 28


**01** **—** **Executive** **Summary**

## Overview


between January 6th and January 20th, 2025. For more information on our auditing methodology, refer


to Appendix B.

## Key Findings


We produced 16 findings throughout this audit engagement.


In particular, we identified a critical vulnerability involving the exploitation of a high minimum expected


balance output amount to trigger the force withdrawal mechanism, which bypasses margin tolerance


checks when closing all positions with market orders, thereby exposing the system to significant slippage


risks (OS-AMM-ADV-01). We also identified another issue wherein if the accumulated slippage exceeds


the withdrawal balance, it creates a negative value that is then converted to an absolute amount, allowing


attackers to gain unexpected profits at the vault’s expense (OS-AMM-ADV-02).


We further highlighted the lack of any functionality for withdrawing accumulated owner fees, leaving col

lected fees inaccessible and potentially locking significant funds (OS-AMM-ADV-08), and the possibility


of unauthorized interactions with perpetuities, as the account allows direct access to the trading account


(OS-AMM-ADV-00). Additionally, if a short position incurs losses larger than amount to withdraw, the


subsequent calculation produces a negative value, resulting in miscalculations (OS-AMM-ADV-04).


Furthermore, the vault owner may accumulate excessive pending orders across multiple clearing houses,


surpassing the maximum event emission limit and blocking the force withdrawal process. Similarly, an


attacker may flood the order book with numerous small orders, also exceeding the event emission limit


(OS-AMM-ADV-05).


We also made suggestions regarding inconsistencies in the codebase and ensuring adherence to coding


best practices (OS-AMM-SUG-03) and advised to avoid emission of misleading events (OS-AMM-SUG

01). We further recommended implementing validation to verify the new version is strictly greater than


the current version, and enforcing checks to ensure stop order tickets do not interact with the clearing


house during active deposit or withdraw sessions (OS-AMM-SUG-02).


© 2025 Otter Audits LLC. All Rights Reserved. 3 / 28


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/AftermathFinance/market-](https://github.com/AftermathFinance/market-making-v2)


[making-v2.](https://github.com/AftermathFinance/market-making-v2) This audit was performed against commit [f1c5aa9](https://github.com/AftermathFinance/market-making-v2/commit/f1c5aa9a1e9cef101b850456b9d154ad7dc99839) and [16dc86e.](https://github.com/AftermathFinance/market-making-v2/commit/16dc86eb285d8f9d885cf7228ec5ccb22835d597)


**A** **brief** **description** **of** **the** **programs** **is** **as** **follows:**


The market making module interacts with Aftermath Perpetual contracts,



market-making-v2



enabling vault operators to manage liquidity provided by participants.


Profits and losses are shared based on the liquidity contributed.



© 2025 Otter Audits LLC. All Rights Reserved. 4 / 28


**03** **—** **Findings**


Overall, we reported 16 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.



© 2025 Otter Audits LLC. All Rights Reserved. 5 / 28


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


**ID** **Severity** **Status** **Description**



trading account, enabling unauthorized inter

actions with a perpetual.


A user may exploit high


trigger the force withdrawal mechanism, which


bypasses margin tolerance checks when


closing all positions utilizing market orders,


exposing the system to significant slippage


risks.


If accumulated slippage exceeds the withdrawal


balance, it creates a negative value that is con

verted to an absolute amount, allowing attack

ers to gain unexpected profits at the vault’s ex

pense.


tially manipulating fee calculations during with

If a short position incurs losses larger than


lation to produce a negative value, resulting in


miscalculations.



OS-AMM-ADV-00


OS-AMM-ADV-01


OS-AMM-ADV-02


OS-AMM-ADV-03


OS-AMM-ADV-04





© 2025 Otter Audits LLC. All Rights Reserved. 6 / 28


Aftermath Market Making Audit 04 - Vulnerabilities


The vault owner may accumulate excessive


pending orders across multiple clearing houses,


surpassing the maximum event emission limit



and blocking the force withdrawal process.


Similarly, an attacker could flood the order book


with numerous small orders, also exceeding the


event emission limit.


negative margin during deposit and withdrawal


sessions, resulting in incorrect margin calcu

lations and unsafe liquidity conditions for the


vault.

|The|lp_to_mint != 0|Col3|
|---|---|---|
|**`end_deposit_session`**|**`end_deposit_session`**|do|



rately prevent minting zero tokens, as the


The vault lacks a function for withdrawing ac

cumulated owner fees, leaving collected fees


inaccessible and potentially locking significant


funds.

|create_vault_cap|Col2|Col3|Col4|
|---|---|---|---|
|~~**`name`**~~|and|**`symbol`**|p|



metadata assignment.


The failure to update


fying the fee rate, lock period, or force withdraw


delay allows the cool-down period to be


bypassed, enabling potential abuse by vault


owners through repeated updates in quick


succession.



OS-AMM-ADV-05


OS-AMM-ADV-06


OS-AMM-ADV-07


OS-AMM-ADV-08


OS-AMM-ADV-09


OS-AMM-ADV-10





© 2025 Otter Audits LLC. All Rights Reserved. 7 / 28


Aftermath Market Making Audit 04 - Vulnerabilities


**Description**


positions or collateral balances, possibly leading to a loss of funds.


_>__ _market-making-vault/sources/vault.move_ rust

```
  /// Retrieves a reference to the trading account associated with the given Vault.
  ///
  /// Parameters:
  /// - `vault`: Reference to the `Vault` from which the trading account is being accessed.
  ///
  /// Returns:
  /// - `&Account<C>`: A reference to the `Account` associated with the specified Vault.
  public fun account<L, C>(
    vault: &Vault<L, C>
  ): &Account<C> {
    // Borrow a reference to the trading account associated with the vault.
    dof::borrow(&vault.id, keys::account_key())
  }

```

**Remediation**


**Patch**


Resolved in [a6316ee.](https://github.com/AftermathFinance/market-making-v2/commit/a6316ee58e221806b90cf9882106dbc6aa185683)


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 28


Aftermath Market Making Audit 04 - Vulnerabilities


**Description**


bypassing tolerance checks by closing positions with market orders. Closing all bases allows the tolerance


check on the margin ratio to be skipped. The skipped tolerance check


the account margin ratios within a safe range. By bypassing this, the function potentially exposes the


account to greater losses due to slippage. Market orders execute trades immediately at the current best


available prices. These orders do not control for slippage.


With the margin tolerance check bypassed when the base position is closed, losses are exacerbated


since the position may not satisfy the safety thresholds for acceptable collateral allocation. This issue is


unrealistically high value that the vault will not be able to satisfy. This effectively locks the withdrawal


session. Consequently, the user may trigger a forced withdrawal, bypassing the default constraints on


withdrawal processing, resulting in losses to the vault.


**Remediation**


**Patch**


Resolved in [25bcdcb.](https://github.com/AftermathFinance/market-making-v2/commit/25bcdcb1e1ae1bcaabf8acbe9e8eeef6b9bdcef5)


© 2025 Otter Audits LLC. All Rights Reserved. 9 / 28


Aftermath Market Making Audit 04 - Vulnerabilities


**Description**


processes accumulated slippage, and converts this value into a withdrawable balance. Specifically, when


value. Thus, an attacker may receive unexpected profit while causing a loss of funds for the vault.


_>__ _market-making-vault/sources/vault.move_ rust

```
  public(package) fun end_withdraw_session<L, C>(
    withdraw_session: WithdrawSession<L, C>,
    ctx: &mut TxContext
  ) {
    [...]
    let mut balance_to_withdraw = multiply_by_rational_ifixed(
      ifixed::from_balance(lp_balance.value(), constants::b9_scaling()),
      total_vault_balance,
      ifixed::from_balance(vault.lp_supply_value(), constants::b9_scaling()),
    );
    balance_to_withdraw = ifixed::add(balance_to_withdraw, accumulated_slippage);
    let lp_balance_value = lp_balance.value();
    burn_lp_balance(&mut vault, lp_balance);
    let mut withdrawn_balance = vault.remove_collateral_from_vault(
      ifixed::to_balance(
         ifixed::div(balance_to_withdraw, collateral_price),
         scaling_factor
         )
    );
    [...]
  }

```

**Remediation**


**Patch**


Resolved in [66e5dfd.](https://github.com/AftermathFinance/market-making-v2/commit/66e5dfdcc6364351c3f97b94d07c83d5713bd2d8)


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 28


Aftermath Market Making Audit 04 - Vulnerabilities


**Description**

|provided_value_usd|will be calculated as|provided_value_usd - new_provided_value_usd|Col4|Col5|Col6|
|---|---|---|---|---|---|
|is results in a reduced|**`provided_value_usd`**|**`provided_value_usd`**|for the original coin and a new|**`UserLpCoin`**|with|



_>__ _market-making-vault/sources/vault.move_ rust

```
  public(package) fun split_user_lp_coin<L>([...]): UserLpCoin<L> {
    // Calculate the split ratio to adjust the initial provided usd value
    let split_ratio = ifixed::div(
      ifixed::from_balance(amount, constants::b9_scaling()),
      ifixed::from_balance(user_lp_coin.lp_balance.value(), constants::b9_scaling())
    );
    let new_provided_value_usd = ifixed::mul(user_lp_coin.provided_value_usd,split_ratio);
    user_lp_coin.provided_value_usd = user_lp_coin.provided_value_usd -new_provided_value_usd;
    // Split balance and create new UserLpCoin
    UserLpCoin {
      id: object::new(ctx),
      lp_balance: user_lp_coin.lp_balance.split(amount),
      start_timestamp_ms: user_lp_coin.start_timestamp_ms,
      provided_value_usd: new_provided_value_usd
    }
  }

```

amounts.

|provided_value_usd|Col2|
|---|---|
|**`provided_value_usd`**|**`provided_value_usd`**|



withdrawal of funds based on its LP balance. This withdrawal bypasses the fee calculation mechanism,


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 28


Aftermath Market Making Audit 04 - Vulnerabilities


**Remediation**


**Patch**


Resolved in [ffaff4b.](https://github.com/AftermathFinance/market-making-v2/commit/ffaff4b5cd2a7f13459cf50712362eb26f216543)


© 2025 Otter Audits LLC. All Rights Reserved. 12 / 28


Aftermath Market Making Audit 04 - Vulnerabilities


**Description**


potential vulnerability that arises from an edge case where short positions incur a large loss. If the loss


the user and the vault.


_>__ _market-making-vault/sources/vault.move_ rust

```
  public(package) fun process_clearing_house_for_force_withdraw<L, C>(
    [...]
  ) {
    [...]
    // Close the required part of the position. Apply slippage and fees to the amount
    // to withdraw for this force withdrawal
    if (base_amount != 0) {
      [...]
      let pnl = if (position_is_ask) {
         ifixed::sub(expected_quote_asset_delta, quote_asset_delta)
      } else {
         ifixed::sub(quote_asset_delta, expected_quote_asset_delta)
      };
      let fees = ifixed::mul(quote_asset_delta, taker_fee);
      withdraw_session.accumulated_slippage = ifixed::add(
         withdraw_session.accumulated_slippage,
         ifixed::sub(pnl, fees)
      );
      amount_to_withdraw = ifixed::add(amount_to_withdraw, ifixed::sub(pnl, fees));
    };
    [...]
  }

```

**Remediation**


**Patch**


Resolved in [a53cf8e.](https://github.com/AftermathFinance/market-making-v2/commit/a53cf8efe9436fccd3c10ebb9787254e9ba83b79)


© 2025 Otter Audits LLC. All Rights Reserved. 13 / 28


Aftermath Market Making Audit 04 - Vulnerabilities


**Description**


may intentionally place multiple pending orders across various clearing houses, thereby accumulating a


large number of events to be processed. If the number of events exceeds 1024, it will block the force


withdrawal process.


**Remediation**


Enforce tighter validation or limits on the number of pending orders a vault owner may place.


**Patch**


Resolved in [d41ff62.](https://github.com/AftermathFinance/market-making-v2/commit/d41ff62e4d3514ec87f2e34ca8ae77354ae3c73e)


© 2025 Otter Audits LLC. All Rights Reserved. 14 / 28


Aftermath Market Making Audit 04 - Vulnerabilities


**Description**


_>__ _market-making-vault/sources/vault.move_ rust

```
      // Calculate the amount of lp_coin to mint for the user
      let lp_to_mint = multiply_by_rational_ifixed(
         provided_balance_value,
         ifixed::from_balance(vault.lp_supply_value(), constants::b9_scaling()),
         vault_balance_value
      );
      assert!(lp_to_mint != 0, errors::user_lp_calculation_zero());

      // Mint the lp_coin and check for slippage
      let lp_balance = mint_lp_balance(
         &mut vault,
         ifixed::to_balance(lp_to_mint, constants::b9_scaling())
      );

```

**Remediation**


**Patch**


Resolved in [b041a2e.](https://github.com/AftermathFinance/market-making-v2/commit/b041a2ee638b05f563351c8372703410301e1536)


© 2025 Otter Audits LLC. All Rights Reserved. 15 / 28


Aftermath Market Making Audit 04 - Vulnerabilities


**Description**


conversion.


_>__ _market-making-vault/sources/vault.move_ rust

```
  public(package) fun end_deposit_session<L, C>(
    deposit_session: DepositSession<L, C>,
    min_expected_lp_coin_out: u64,
    ctx: &mut TxContext
  ) {
    [...]
    assert!(lp_to_mint != 0, errors::user_lp_calculation_zero());

    // Mint the lp_coin and check for slippage
    let lp_balance = mint_lp_balance(
      &mut vault,
      ifixed::to_balance(lp_to_mint, constants::b9_scaling())
    );
    [...]
  }

```

**Remediation**


Perform a validation after the conversion to ensure the minted LP balance is valid and non-zero.


**Patch**


Resolved in [25bcdcb.](https://github.com/AftermathFinance/market-making-v2/commit/25bcdcb1e1ae1bcaabf8acbe9e8eeef6b9bdcef5)


© 2025 Otter Audits LLC. All Rights Reserved. 16 / 28


Aftermath Market Making Audit 04 - Vulnerabilities


**Description**


The vault allows for the collection of owner fees, however, it currently lacks a function to withdraw these


accumulated fees, introducing operational inefficiencies. Without a withdrawal function, owner fees


remain inaccessible, causing substantial funds to be locked in the contract over time as they accumulate,


which negatively impacts the protocol’s revenue model.


**Remediation**


Implement a function that enables the vault owner to withdraw the accumulated fees.


**Patch**


Resolved in [415146d.](https://github.com/AftermathFinance/market-making-v2/commit/415146d274c9731ca697addb9171d2d086c6dd77)


© 2025 Otter Audits LLC. All Rights Reserved. 17 / 28


Aftermath Market Making Audit 04 - Vulnerabilities


**Description**


_>__ _market-making-vault/sources/vault.move_ rust

```
  public(package) fun create_vault_cap<L: drop>(
    [...]
  ) {
    let (treasury_cap, mut coin_metadata) = coin::create_currency<L>(
      witness,
      decimals,
      name,
      symbol,
      description,
      option::none(),
      ctx
    );
    [...]
  }

```

expected token metadata will create confusion among users and external programs interacting with the


token affecting the operational integrity of the program.


**Remediation**


**Patch**


Resolved in [25bcdcb.](https://github.com/AftermathFinance/market-making-v2/commit/25bcdcb1e1ae1bcaabf8acbe9e8eeef6b9bdcef5)


© 2025 Otter Audits LLC. All Rights Reserved. 18 / 28


Aftermath Market Making Audit 04 - Vulnerabilities


**Description**


additional updates to bypass the cool-down check. As a result, it will be possible to continuously update


these parameters to extremely low or high values, destabilizing the system.


**Remediation**


respective parameter.


**Patch**


Resolved in [db6c2f1.](https://github.com/AftermathFinance/market-making-v2/commit/db6c2f19178b9b7a58a3c83e528bbcb1bac5e93f)


© 2025 Otter Audits LLC. All Rights Reserved. 19 / 28


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.


Preventing the addition of extra elements beyond predefined limits by en


OS-AMM-SUG-00


OS-AMM-SUG-01


OS-AMM-SUG-02


OS-AMM-SUG-03


OS-AMM-SUG-04



drawal sessions via misleading event emissions by processing standard


withdrawals while emitting force withdrawal events.


against the target vault and fails to ensure new version is strictly greater


than the current version.


Suggestions regarding inconsistencies in the codebase and ensuring ad

herence to coding best practices.


Recommendations for modifying the codebase to mitigate potential security


issues and improve functionality.



© 2025 Otter Audits LLC. All Rights Reserved. 20 / 28


Aftermath Market Making Audit 05 - General Findings


**Utilization** **of** **Incorrect** **Relational** **Operator** OS-AMM-SUG-00


**Description**


verifying pending orders and clearing house IDs, which is inconsistent with the subsequent login in these

|deposit_into_perpetuals<br>s. The assertion in verif<br>max_markets_in_vault<br>is equal to or fewer than its<br>max_markets_in_vault<br>clearing house IDs. Howeve|deposit_into_perpetuals|Col3|verif|
|---|---|---|---|
|s. The assertion in **`deposit_into_perpetuals`**<br>verif<br> is equal to or fewer than its **`max_markets_in_vault`**<br> **`max_markets_in_vault`**<br>clearing house IDs. Howeve|**`deposit_into_perpetuals`**|**`max_markets_in_vault`**|**`max_markets_in_vault`**|
|**`max_markets_in_vault`**|**`max_markets_in_vault`**|**`max_markets_in_vault`**|**`max_markets_in_vault`**|



subsequently, potentially causing this limit to be exceeded.


_>__ _market-making-vault/sources/perpetuals_api.move_ rust

```
  public(package) fun deposit_into_perpetuals<L, C>([...]) {
    [...]
    let clearing_house_id = object::id(clearing_house);
    if(!vector::contains(&vault.ch_ids(), &clearing_house_id)) {
      assert!(vector::length(&vault.ch_ids()) <=
```

_�→_ `vault.max_markets_in_vault(),errors::max_markets_exceeded());`
```
      vector::push_back(vault.ch_ids_mut(), clearing_house_id);
      let vault_account = vault.account_mut();
      let account_id = vault_account.get_account_id();
      if (!clearing_house.exists_position(account_id)) {
         perpetuals::create_market_position(clearing_house, vault_account);
      }
    };
    [...]
  }

|Similarly, in|place_limit_order|Col3|asserts|Col5|
|---|---|---|---|---|
|**`get_pending_orders_counter(position)`** **`<=`** **`vault.max_pending_orders_per_position`**|**`get_pending_orders_counter(position)`** **`<=`** **`vault.max_pending_orders_per_position`**|**`get_pending_orders_counter(position)`** **`<=`** **`vault.max_pending_orders_per_position`**|**`get_pending_orders_counter(position)`** **`<=`** **`vault.max_pending_orders_per_position`**|**`get_pending_orders_counter(position)`** **`<=`** **`vault.max_pending_orders_per_position`**|
|if there are already|if there are already|**`max_pending_orders_per_position`**|**`max_pending_orders_per_position`**|orders pending, placing a new limit|


```

will exceed the allowed limit.


_>__ _market-making-vault/sources/perpetuals_api.move_ rust

```
  public(package) fun place_limit_order<L, C>([...]) {
    [...]
    assert!(position::get_pending_orders_counter(position)
```

_�→_ `<=vault.max_pending_orders_per_position(),` `errors::max_pending_orders_exceeded());`
```
    [...]
    // i. Start a new session and place the limit order.
    let mut session = perpetuals::start_session(
      clearing_house,
      vault.account_mut(),

```

© 2025 Otter Audits LLC. All Rights Reserved. 21 / 28


Aftermath Market Making Audit 05 - General Findings

```
      base_oracle,
      collateral_oracle,
      clock,
    );
    perpetuals::place_limit_order(&mut session, side, size, price, order_type);
    [...]
  }

```

**Remediation**


that the operations will proceed only if adding the next element will not exceed the maximum allowed limit.


**Patch**


Resolved in [d41ff62.](https://github.com/AftermathFinance/market-making-v2/commit/d41ff62e4d3514ec87f2e34ca8ae77354ae3c73e)


© 2025 Otter Audits LLC. All Rights Reserved. 22 / 28


Aftermath Market Making Audit 05 - General Findings


**Misleading** **Event** **Emission** OS-AMM-SUG-01


**Description**


event, even though the withdrawal was not processed as a forced one.


**Remediation**


requirements.


**Patch**


Resolved in [6d78b43.](https://github.com/AftermathFinance/market-making-v2/commit/6d78b4312d37db2c538f4af3ddd4068cbe5f73b2)


© 2025 Otter Audits LLC. All Rights Reserved. 23 / 28


Aftermath Market Making Audit 05 - General Findings


**Missing** **Validation** **Logic** OS-AMM-SUG-02


**Description**


ter but does not validate its connection to the specified vault. Either ensure that the provided


to trigger the version update without ownership verification. Furthermore, validate whether the new


version is greater than the previous version to maintain consistency, security, and versioning integrity


within the system.


_>__ _market-making-vault/sources/vault.move_ rust

```
     public(package) fun update_vault_version<L, C>(
       _vault_owner_cap: &VaultOwnerCap,
       vault: &mut Vault<L, C>
     ) {
       // Update the vault's version to the latest version specified in the constants module.
       vault.version = constants::version();
       events::emit_update_vault_version(
          vault.id(),
          constants::version(),
       );
     }

```

check if the new limit is below the number of markets already registered in the vault.


**Patch**


1. Issue #1 resolved in [dbd0db8.](https://github.com/AftermathFinance/market-making-v2/commit/dbd0db8bb707d4c40e93ff375c4be76c5f348598)


**Remediation**


Add the above validations.


© 2025 Otter Audits LLC. All Rights Reserved. 24 / 28


Aftermath Market Making Audit 05 - General Findings


**Code** **Maturity** OS-AMM-SUG-03


**Description**


convention.

|coin::create_currency|Col2|
|---|---|
|**`coin::update_icon_url`**<br><br>|**`coin::update_icon_url`**<br><br>|
|**`effective_icon_url`**|in a|



_>__ _market-making-vault/sources/vault.move_ rust

```
     public(package) fun create_vault_cap<L: drop>(
       [...]
     ) {
       let (treasury_cap, mut coin_metadata) = coin::create_currency<L>(
          [...]
       );
       let effective_icon_url = if (!vector::is_empty(&icon_url)) {
          icon_url
       } else {
          constants::default_lp_coin_image()
       };
       coin::update_icon_url(&treasury_cap, &mut coin_metadata,
```

_�→_ `ascii::string(effective_icon_url));`
```
       [...]
     }

```

docstrings are updated.


**Remediation**


Implement the above-mentioned suggestions.


© 2025 Otter Audits LLC. All Rights Reserved. 25 / 28


Aftermath Market Making Audit 05 - General Findings


**Code** **Refactoring** OS-AMM-SUG-04


**Description**


emit events similar to other update functions to ensure proper logging of state changes.


**Remediation**


Incorporate the above refactors.


**Patch**


1. Issue #1 resolved in [d4b52ef.](https://github.com/AftermathFinance/market-making-v2/commit/d4b52ef7cfafdcdf87ab5197cbe8f48d07752c09)


© 2025 Otter Audits LLC. All Rights Reserved. 26 / 28


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


© 2025 Otter Audits LLC. All Rights Reserved. 27 / 28


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


© 2025 Otter Audits LLC. All Rights Reserved. 28 / 28


