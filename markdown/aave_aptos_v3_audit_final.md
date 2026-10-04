# **Aave Aptos V3**

Security Assessment


August 8th, 2025 - Prepared by OtterSec


Bartłomiej Wierzbiński [dark@osec.io](mailto:dark@osec.io)


Andreas Mantzoutas [andreas@osec.io](mailto:andreas@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **3**


Overview 3


Key Findings 3


**Scope** **4**


**Findings** **5**


**Vulnerabilities** **6**


OS-AAV-ADV-00 | Denial of Service Due to Unbounded Rewards Map 7


OS-AAV-ADV-01 | Failure to Check for Stale Oracle Price 8


OS-AAV-ADV-02 | Allocation of Excessive Privileges to Listing Admin 9


OS-AAV-ADV-03 | Denial of Service via Hash Collision 10


OS-AAV-ADV-04 | Improper Event Emission Due to Variable Shadowing 11


**General** **Findings** **12**


OS-AAV-SUG-00 | Incorrect Liquidation Bonus Configuration 14


OS-AAV-SUG-01 | Inconsistency in Role Check Logic 15


OS-AAV-SUG-02 | State Handling Discrepancies 16


OS-AAV-SUG-03 | Standardization of Asset Operations 17


OS-AAV-SUG-04 | Code Maturity 18


OS-AAV-SUG-05 | Missing Validation Logic 19


OS-AAV-SUG-06 | Event Emission Inconsistencies 21


OS-AAV-SUG-07 | Error Handling 22


OS-AAV-SUG-08 | Code Optimization 24


OS-AAV-SUG-09 | Code Refactoring 26


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 30


Aave Aptos V3 Audit


TABLE OF CONTENTS


OS-AAV-SUG-10 | Unutilized Code 28


**Appendices**


**Vulnerability** **Rating** **Scale** **29**


**Procedure** **30**


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 30


**01** **—** **Executive** **Summary**

## Overview


between June 24th and July 24th, 2025. For more information on our auditing methodology, refer to


Appendix B.

## Key Findings


We produced 16 findings throughout this audit engagement.


In particular, we identified a vulnerability where the function responsible for retrieving the asset price


fails to check if the Chainlink price data is stale, risking the utilization of outdated asset prices (OS-AAV

ADV-01). Additionally, it is possible for the asset listing admin to arbitrarily modify reserve configurations,


effectively bypassing role separation and increasing governance risk (OS-AAV-ADV-02).


Furthermore, the rewards controller utilizes a vector-backed structure to track user data, which grows


unbounded as users interact with the system, resulting in out-of-gas errors during critical operations


such as minting or liquidation, creating a denial-of-service and potential protocol insolvency (OS-AAV

ADV-00).


We also recommended codebase modifications to enhance functionality and align with coding best


practices (OS-AAV-SUG-09, OS-AAV-SUG-04), and suggested incorporating additional checks and


assertions to mitigate potential security issues and improve error handling (OS-AAV-SUG-05, OS-AAV

SUG-07).


We further advised emitting events only on meaningful state changes, and ensuring that functions log


events when necessary (OS-AAV-SUG-06). Lastly, we highlighted the necessity of removing multiple


instances of repetitive and unutilized code for improved gas optimization, clarity, and maintainability


(OS-AAV-SUG-08, OS-AAV-SUG-10).


© 2025 Otter Audits LLC. All Rights Reserved. 3 / 30


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/aave/aptos-v3.](https://github.com/aave/aptos-v3) This audit


was performed against commit [a8f9c40.](https://github.com/aave/aptos-v3/commit/a8f9c40983c6009bb859d8673ed2ea1d0ab7e3f0)


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**


A Move-based implementation of the Aave V3.3 lending protocol,


enabling decentralized borrowing and lending with enhanced secu


aave-aptos-v3



rity, composability, and performance. It leverages Aptos’s resource

oriented design, strict module boundaries, and formal verification to


ensure safe and efficient asset management.



© 2025 Otter Audits LLC. All Rights Reserved. 4 / 30


**03** **—** **Findings**


Overall, we reported 16 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.



© 2025 Otter Audits LLC. All Rights Reserved. 5 / 30


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


**ID** **Severity** **Status** **Description**


The rewards controller utilizes a vector-backed


structure to track user data, which grows un

bounded as users interact with the system, re


sulting in out-of-gas errors during critical op

erations such as minting or liquidation, creating


a denial-of-service and potential protocol in

solvency.


if the Chainlink price data is stale, risking the


utilization of outdated asset prices.


The asset listing admin may arbitrar

ily modify reserve configurations via


, effectively bypassing role separation and


increasing governance risk.


denial-of-service attack, where malicious users


may overload a specific bucket, creating aborts


and denying access to legitimate users with col

liding keys.


event always reporting a zero value instead of



OS-AAV-ADV-00


OS-AAV-ADV-01


OS-AAV-ADV-02


OS-AAV-ADV-03


OS-AAV-ADV-04





© 2025 Otter Audits LLC. All Rights Reserved. 6 / 30


Aave Aptos V3 Audit 04 - Vulnerabilities


**Description**


insertion or lookup requires linear-time scanning of the vector. As this structure grows, its performance


degrades, and operations that iterate over it may run out of gas. Specifically, in this case, every user is


expected to maintain an entry in the map. As a result, the map is expected to grow indefinitely.





Since this is permissionless, a malicious actor may create many such entries by interacting with the pool


This behavior may have severe implications. For instance, an attacker may fill the vector with numerous


positions, bloating the map until liquidation becomes impossible due to gas exhaustion, and then open a


position where they borrow a significant amount of funds near the liquidation threshold. Subsequently,


even if the position becomes eligible for liquidation, it may remain unliquidatable, potentially creating bad


debt for the protocol.


**Remediation**


Avoid utilizing vector-backed structures for permissionless or unbounded data storage to prevent un

bounded growth and potential denial-of-service risks.


**Patch**


Aave acknowledged this issue.


© 2025 Otter Audits LLC. All Rights Reserved. 7 / 30


Aave Aptos V3 Audit 04 - Vulnerabilities


**Description**


entries by not updating the price if **`feed.observation_timestamp`** **`≥observation_timestamp`**, it


does not prevent the oracle from returning stale prices if the feed stops updating. This creates a risk


where outdated prices could be used in core protocol logic.


**Remediation**


Enforce a maximum timestamp age check to reject stale data explicitly while retrieving the asset price.


**Patch**


Resolved in [PR#445.](https://github.com/aave/aptos-v3/pull/445)


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 30


Aave Aptos V3 Audit 04 - Vulnerabilities


**Description**


The current design of AAVE’s governance framework delegates admin responsibilities across multiple


roles, helping reduce centralization risks by distributing authority across different addresses. Specifically,


the asset listing admin is responsible for adding new reserves by setting their configurations to default


values and configuring oracles, while the pool admin manages critical parameters of active reserves.


_>__ _aave-core/sources/aave-pool/pool.move_ rust

```
  /// @notice Sets the reserve configuration with guard
  /// @param account The account signer of the caller
  /// @param asset The address of the underlying asset of the reserve
  /// @param reserve_config_map The new configuration bitmap
  public fun set_reserve_configuration_with_guard(
    account: &signer, asset: address, reserve_config_map: ReserveConfigurationMap
  ) acquires Reserves, ReserveData {
    assert!(
      acl_manage::is_asset_listing_admin(signer::address_of(account))
         || acl_manage::is_pool_admin(signer::address_of(account)),
      error_config::get_ecaller_not_asset_listing_or_pool_admin()
    );
    set_reserve_configuration(asset, reserve_config_map);
  }

```

listing admin to update any reserve’s configuration. While this is intended for the pool admin, the listing


admins should not be allowed to arbitrarily overwrite the configuration of any reserve. This goes beyond


their intended scope and grants them unrestricted control over reserve parameters. As a result, the listing


admin effectively gains elevated super-admin privileges. This undermines the intended role hierarchy


and significantly increases the protocol’s governance and security risks.


**Remediation**


configurations beyond their intended permissions.


**Patch**


Aave acknowledged this issue.


© 2025 Otter Audits LLC. All Rights Reserved. 9 / 30


Aave Aptos V3 Audit 04 - Vulnerabilities


**Description**


attacker who controls the keys to insert multiple entries that hash to the same bucket, temporarily blocking


further insertions into that bucket. This vulnerability affects multiple instances across the codebase, with


user addresses to configuration data.


_>__ _aave-core/sources/aave-pool/pool.move_ rust

```
  /// @notice Map of users address and their configuration data (user_address =>
```

_�→_ _`UserConfigurationMap)`_
```
  struct UsersConfig has key {
    value: SmartTable<address, UserConfigurationMap>
  }

```

Since keys (addresses) are controlled by users, an attacker may generate multiple addresses that delib

erately hash to the same bucket. Each of these attacker-controlled accounts may open small positions,


10,000 entries, any new user whose address hashes to that same bucket will be unable to interact with


the protocol, resulting in an unexpected abort. This effectively blocks legitimate users from participating,


creating a denial-of-service for that bucket.


**Remediation**


**Patch**


The Avve team acknowledged the issue but stated they do not plan to address it immediately, as the mainnet


stabilize, they intend to migrate to them due to their improved concurrency support and performance


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 30


Aave Aptos V3 Audit 04 - Vulnerabilities


**Description**


_>__ _aave-core/sources/aave-pool/pool_configurator.move_ rust

```
  public entry fun set_reserve_freeze(
    account: &signer, asset: address, freeze: bool
  ) acquires InternalData {
    [...]
    let pending_ltv_set = 0;
    let ltv_set = 0;
    if (freeze) {
      let pending_ltv_set = reserve_config::get_ltv(&reserve_config_map);
      smart_table::upsert(&mut internal_data.pending_ltv, asset, pending_ltv_set);
      reserve_config::set_ltv(&mut reserve_config_map, 0);
    } else {[...]};

    event::emit(PendingLtvChanged { asset, pending_ltv_set });
    [...]
  }

```

**Remediation**


**Patch**


Resolved in [PR#457.](https://github.com/aave/aptos-v3/pull/457)


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 30


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.



OS-AAV-SUG-00


OS-AAV-SUG-01



|Currently, the|liquidation_bonus|Col3|
|---|---|---|
|**`PERCENTAGE_FACTOR`**|**`PERCENTAGE_FACTOR`**|, implying that no r|


gency admins being skipped during setup.



OS-AAV-SUG-02

may silently alter or preserve the liquidation grace period.



OS-AAV-SUG-03


OS-AAV-SUG-04


OS-AAV-SUG-05


OS-AAV-SUG-06


OS-AAV-SUG-07


OS-AAV-SUG-08



cleaner code and proper handling of store initialization and dispatchable


assets.


Certain parts of the codebase can be updated to maintain consistency and


ensure alignment with coding best practices.


There are several instances where proper validation is not performed, re

sulting in potential security issues.


Multiple functions emit events even when no state-change has occurred


and others fail to log events when required.


The codebase will benefit from additional assertions to improve general


error handling and traceability of potential runtime errors.


There are several redundant and repetitive code instances that may be


removed to save gas.



© 2025 Otter Audits LLC. All Rights Reserved. 12 / 30


Aave Aptos V3 Audit 05 - General Findings


Recommendation for updating the codebase to improve overall clarity and

OS-AAV-SUG-09

functionality and mitigate potential security issues.


The codebase contains multiple cases of redundant and unutilized code

OS-AAV-SUG-10

that should be removed for better maintainability and clarity.


© 2025 Otter Audits LLC. All Rights Reserved. 13 / 30


Aave Aptos V3 Audit 05 - General Findings


**Incorrect** **Liquidation** **Bonus** **Configuration** OS-AAV-SUG-00


**Description**


value. This misconfiguration fails to provide the intended bonus and removes the financial incentive for


result, undercollateralized positions may remain unliquidated, increasing protocol insolvency risk. The


issue is especially critical since it’s already deployed on mainnet.









**Remediation**


Correct the liquidation bonus and adjust it to the correct value in the setters.


© 2025 Otter Audits LLC. All Rights Reserved. 14 / 30


Aave Aptos V3 Audit 05 - General Findings


**Inconsistency** **in** **Role** **Check** **Logic** OS-AAV-SUG-01


**Description**


results in the script skipping adding emission privileges for addresses that are already emergency admins.


**Remediation**


Ensure that the check correctly evaluates whether the emission role is already assigned.


**Patch**


Resolved in [PR#453.](https://github.com/aave/aptos-v3/pull/453)


© 2025 Otter Audits LLC. All Rights Reserved. 15 / 30


Aave Aptos V3 Audit 05 - General Findings


**State** **Handling** **Discrepancies** OS-AAV-SUG-02


**Description**


pausing an already paused reserve or unpausing one that is already active. This will result in unnecessary


silently updates the grace period, even if it is already unpaused. Additionally, failing to set the grace


period in case of 0 may introduce confusing edge cases. For example, if a reserve was paused, then


unpaused with a grace period, then paused again, and then unpaused again without a grace period, the


grace period from the first unpause may still be in effect.


**Remediation**


or unpause one that is not paused.


**Patch**


who are trusted in nature.


© 2025 Otter Audits LLC. All Rights Reserved. 16 / 30


Aave Aptos V3 Audit 05 - General Findings


**Standardization** **of** **Asset** **Operations** OS-AAV-SUG-03


**Description**


asset transfers, deposits, and balance operations. However, they require repetitive boilerplate code and


they fail to gracefully handle cases where a store does not yet exist. It is more appropriate to utilize


does not exist, supports dispatchable assets as expected by the framework, and reduces boilerplate code.


**Remediation**


**Patch**

|fungible_store<br>Aave acknowledged the utilization of<br>primary_fungible_store<br>stores, rendering unsuit<br>primary_fungible_store<br>has been utilized wherever p|fungible_store|
|---|---|
|**`primary_fungible_store`**|**`primary_fungible_store`**|



for their design and architecture.


© 2025 Otter Audits LLC. All Rights Reserved. 17 / 30


Aave Aptos V3 Audit 05 - General Findings


**Code** **Maturity** OS-AAV-SUG-04


**Description**


_>__ _aave-core/sources/aave-tokens/token_base.move_ rust

```
     /// @notice Drops the token data from the token map
     /// @dev Only callable by the a_token_factory and variable_debt_token_factory module
     /// @param metadata_address The address of the token
     public(friend) fun drop_token(metadata_address: address) acquires ManagedFungibleAsset {
       assert_token_exists(metadata_address);
       assert_managed_fa_exists(metadata_address);
       // detach the managed fungibel asset from the metadata address
       move_from<ManagedFungibleAsset>(metadata_address);
     }

```

direction is mentioned at the beginning and in every function’s description. This inconsistency


introduces ambiguity and may result in incorrect assumptions about numerical precision.


return may optimize performance and reduce resource usage.


**Remediation**


Implement all the listed suggestions.


**Patch**


1. Resolved in [PR#44.](https://github.com/aave/aptos-v3/pull/44)


© 2025 Otter Audits LLC. All Rights Reserved. 18 / 30


Aave Aptos V3 Audit 05 - General Findings


**Missing** **Validation** **Logic** OS-AAV-SUG-05


**Description**


1. The oracle module currently permits either the asset listing admin or the pool admin to set a custom


of the custom price exceeds the asset’s configured price cap. It fails to verify whether a price cap


is defined for the asset. As a result, even if a high custom price (above the limit) is set, the oracle


may still return the capped price, creating inconsistencies between the set custom price and the


effective price utilized by the system.


_>__ _aave-core/aave-oracle/sources/oracle.move_ rust

```
     /// @notice Sets a custom price for an asset
     /// @param account Admin account that sets the price
     /// @param asset Address of the asset
     /// @param custom_price Custom price value
     public entry fun set_asset_custom_price(
       account: &signer, asset: address, custom_price: u256
     ) acquires PriceOracleData {
       only_asset_listing_or_pool_admin(account);
       assert!(custom_price > 0, error_config::get_ezero_asset_custom_price());
       update_asset_custom_price(asset, custom_price);
     }

```

This may result in loss of administrative control over the protocol. A safeguard should be added to


ensure that at least one admin is always present.


expired, resulting in wasted state updates and unnecessary emissions.


**Remediation**


exceeding the defined price cap, if one exists.


3. Add a check to ensure that each distribution period remains valid.


© 2025 Otter Audits LLC. All Rights Reserved. 19 / 30


Aave Aptos V3 Audit 05 - General Findings


**Patch**


1. Resolved in [PR#45.](https://github.com/aave/aptos-v3/pull/45)


2. Aave acknowledged this issue, stating that it reflects the original logic inherited from Aave v3 (Solidity)


and is therefore by design, with no plans for change.


3. Aave acknowledged this issue, attributing it to an operational oversight, as not all participants may


© 2025 Otter Audits LLC. All Rights Reserved. 20 / 30


Aave Aptos V3 Audit 05 - General Findings


**Event** **Emission** **Inconsistencies** OS-AAV-SUG-06


**Description**


the current one, which may mislead observers and clutter event logs. Avoid emitting the event unless


event even if the asset is already configured as borrowable in isolation. To prevent confusion, avoid


emitting events when no actual change occurs.


**Remediation**


Ensure functions emit events only when a meaningful state change occurs, as emitting events without


changes may create confusion. For key state transitions, event emission is essential to enhance protocol


transparency and traceability.


**Patch**


implementation, where the event is emitted regardless of whether the configuration is updated or not.


© 2025 Otter Audits LLC. All Rights Reserved. 21 / 30


Aave Aptos V3 Audit 05 - General Findings


**Error** **Handling** OS-AAV-SUG-07


**Description**


transferring. Without this, transfers may fail with unclear errors if the balance is insufficient. Adding


or pool admin, returns an incorrect error code meant for an incorrect asset listing or pool admin

|get_ecaller_not_asset_listing_or_pool_admin|Col2|). This ambiguity will create c|
|---|---|---|
|ring failures.<br>Replace it with the correct|**`get_ecaller_not_risk_or_pool_admin`**|**`get_ecaller_not_risk_or_pool_admin`**|



clarity and accuracy.


_>__ _aave-core/aave-scripts/sources/6_configure_price_feeds.move_ rust

```
     fun main(account: &signer, network: String) {
       // Verify the caller has appropriate permissions
       assert!(
          acl_manage::is_risk_admin(signer::address_of(account))
            || acl_manage::is_pool_admin(signer::address_of(account)),
          error_config::get_ecaller_not_asset_listing_or_pool_admin()
       );
       [...]
     }

|virtual_balance - (amount as u128)|Col2|) if there is insufficient|
|---|---|---|
|sult in unexpected runtime aborts.|**`validate_flashloan_simple`**|**`validate_flashloan_simple`**|


```

balance to ensure sufficient liquidity. Similar issue is present in the borrowing mechanism.


amounts. Attempting to send more than the sender’s balance results in a subtraction underflow,


aborting the transaction. Explicitly check that the sender has enough balance to satisfy the transfer


amount.


**Remediation**


Incorporate the error handling checks mentioned above.


© 2025 Otter Audits LLC. All Rights Reserved. 22 / 30


Aave Aptos V3 Audit 05 - General Findings


**Patch**


Resolved in [PR#451.](https://github.com/aave/aptos-v3/pull/451)


© 2025 Otter Audits LLC. All Rights Reserved. 23 / 30


Aave Aptos V3 Audit 05 - General Findings


**Code** **Optimization** OS-AAV-SUG-08


**Description**

|fee_manager::get_apt_fee|should utilize|borrow_with_default|
|---|---|---|
|returning the configured fee or **`DEFAULT_APT_FEE`**<br>if the asset is not f<br>for a separate **`contains`**<br>check.|returning the configured fee or **`DEFAULT_APT_FEE`**<br>if the asset is not f<br>for a separate **`contains`**<br>check.|returning the configured fee or **`DEFAULT_APT_FEE`**<br>if the asset is not f<br>for a separate **`contains`**<br>check.|



unnecessary code duplication. Extract this logic into a helper function to improve readability and


reduce redundancy.


|signer::address_of(account)<br>ute just once and r<br>fee_manager::init_module<br>(as highlighted below) in<br>Object<Metadata><br>should only be retrieved once.|signer::address_of(account)|Col3|just once and r|
|---|---|---|---|
|ute **`signer::address_of(account)`**<br>just once and r<br> (as highlighted below) in **`fee_manager::init_module`** <br> **`Object<Metadata>`**<br>should only be retrieved once.|**`signer::address_of(account)`**|**`fee_manager::init_module`**|**`fee_manager::init_module`**|
|**`Object<Metadata>`**|**`Object<Metadata>`**|**`Object<Metadata>`**|**`Object<Metadata>`**|









current one to save gas and prevent unnecessary state changes.


match the signer’s address. This may be simplified by removing the user argument and directly


_>__ _aave-core/aave-acl/sources/acl_manage.move_ rust

```
     public entry fun renounce_role(admin: &signer, role: String, user: address) acquires Roles
```

_�→_ `{`
```
       assert!(signer::address_of(admin) == user,
```

_�→_ `error_config::get_erole_can_only_renounce_self());`
```
       revoke_role_internal(admin, role, user);
     }

```

© 2025 Otter Audits LLC. All Rights Reserved. 24 / 30


Aave Aptos V3 Audit 05 - General Findings


This may be optimized by calling it once and storing the result in a local variable. Similarly,


_>__ _aave-core/sources/aave-periphery/emission_manager.move_ rust

```
     public entry fun set_pull_rewards_transfer_strategy([...]) acquires EmissionManagerData {
       [...]
       assert!(
          transfer_strategy::pull_rewards_transfer_strategy_get_incentives_controller(
            pull_rewards_transfer_strategy
          ) == get_rewards_controller_ensure_defined(),
          error_config::get_eincentives_controller_mismatch()
       );

       rewards_controller::set_pull_rewards_transfer_strategy(
          reward,
          object::object_address(&pull_rewards_transfer_strategy),
          get_rewards_controller_ensure_defined()
       );
     }

```

the repetitive declaration of these variables.


**Remediation**


Optimize the code as stated above.


**Patch**


Resolved in [PR#451.](https://github.com/aave/aptos-v3/pull/451)


© 2025 Otter Audits LLC. All Rights Reserved. 25 / 30


Aave Aptos V3 Audit 05 - General Findings


**Code** **Refactoring** OS-AAV-SUG-09


**Description**


inaccurate. There is no _virtual_ _accounting_ bit at position 252, nor any corresponding mask. Update


the comment to accurately reflect the structure.


address to the current, correct oracle feed.


_>__ _aave-core/aave-data/sources/v1_values.move_ rust

```
     public fun build_price_feeds_mainnet(): SmartTable<String, vector<u8>> {
       let price_feeds_mainnet = smart_table::new<string::String, vector<u8>>();
       [...]
       smart_table::add(
          &mut price_feeds_mainnet,
          string::utf8(SUSDE_ASSET),
          x"01532c3a7e000332000000000000000000000000000000000000000000000000"
       );
       price_feeds_mainnet
     }

|fee_manager::withdraw_apt_fee|Col2|Col3|
|---|---|---|
|funds if the|**`to`**|address (for exam|


```

of handling fungible assets only. Thus, for smart contracts that only support the fungible asset


into a fungible asset before withdrawal.


**Remediation**


Modify the code to include the refactors.


© 2025 Otter Audits LLC. All Rights Reserved. 26 / 30


Aave Aptos V3 Audit 05 - General Findings


**Patch**


1. Resolved in [PR#451.](https://github.com/aave/aptos-v3/pull/451)


2. Resolved in [7163a7e.](https://github.com/aave/aptos-v3/commit/7163a7e039cad6437e0d8b68a62de0f69e443a59#diff-bffbdf87315ffb0aebfa3c62092b41f6758d19b89cbe99fa5a6e174395311f25)


pool admin must ensure the recipient has a coin store to receive the transfer. An account with the


though an API exists for conversion if needed.


© 2025 Otter Audits LLC. All Rights Reserved. 27 / 30


Aave Aptos V3 Audit 05 - General Findings


**Unutilized** **Code** OS-AAV-SUG-10


**Description**


1. Several unutilized constants are defined across the codebase and may be removed, such as


variable is unutilized and may be removed.


, as this field is unutilized and it is not possible for flash loans to be executed on behalf of another


user.


unutilized as it is never populated.


removed.


**Remediation**


Remove all instances of unutilized code.


**Patch**


Resolved in [PR#42.](https://github.com/aave/aptos-aave-v3/pull/42)


© 2025 Otter Audits LLC. All Rights Reserved. 28 / 30


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


© 2025 Otter Audits LLC. All Rights Reserved. 29 / 30


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


© 2025 Otter Audits LLC. All Rights Reserved. 30 / 30


