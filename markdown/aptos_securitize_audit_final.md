# **Aptos Securitize**

Security Assessment


November 5th, 2024 - Prepared by OtterSec


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


OS-ASC-ADV-00 | Logic Flaw in Time Check 9


OS-ASC-ADV-01 | Absence of State Variable Update on Wallet Removal 10


OS-ASC-ADV-02 | Incorrect Issuance Value Recording 12


OS-ASC-ADV-03 | Incorrect Lock Removal Logic 13


OS-ASC-ADV-04 | Artificial Reduction of Investor Counts 14


OS-ASC-ADV-05 | Disabling Withdrawals by Withdrawing Zero-Value FA 16


OS-ASC-ADV-06 | Flaw in Full Transfer Checks 17


OS-ASC-ADV-07 | Discrepancies in Updating Investor Count 18


OS-ASC-ADV-08 | Utilization of Proper Assertions for Wallet Creation 19


OS-ASC-ADV-09 | Abort Due to Underflow in Difference Calculation 21


OS-ASC-ADV-10 | Wallet Balance Misverification 22


OS-ASC-ADV-11 | Missing Bound Check on Lock Removal 24


OS-ASC-ADV-12 | Failure to Clear Investor Attributes After Removal 25


OS-ASC-ADV-13 | Investor Limit Calculation Error 26


OS-ASC-ADV-14 | Incongruities in Role Management Checks 27


OS-ASC-ADV-15 | Utilization of Empty Investor ID 28


© 2024 Otter Audits LLC. All Rights Reserved. 1 / 37


Aptos Securitize Audit


TABLE OF CONTENTS


OS-ASC-ADV-16 | Missing Last Modifier Update 29


**General** **Findings** **30**


OS-ASC-SUG-00 | Missing Approval Removal Function 31


OS-ASC-SUG-01 | Missing Validation Logic 32


OS-ASC-SUG-02 | Additional Safety Checks 33


OS-ASC-SUG-03 | Code Refactoring 34


**Appendices**


**Vulnerability** **Rating** **Scale** **36**


**Procedure** **37**


© 2024 Otter Audits LLC. All Rights Reserved. 2 / 37


**01** **—** **Executive** **Summary**

## Overview


October 14th and October 29th, 2024. For more information on our auditing methodology, refer to


Appendix B.

## Key Findings


We produced 21 findings throughout this audit engagement.


In particular, we identified several vulnerabilities related to the utilization of zero-amount fungible assets,


including the possibility of users with zero balances repeatedly depositing and withdrawing zero-value


assets, artificially decreasing the total investor count, preventing the proper removal of inactive investors


(OS-ASC-ADV-04), and causing the withdrawal count to be in a state that blocks further withdrawals


when zero-value fungible assets are withdrawn and destroyed without depositing (OS-ASC-ADV-05).


We also highlighted several inconsistencies in the locking logic, concerning the incorrect deletion of the


last lock record, resulting in inaccuracies in tracking transferable tokens (OS-ASC-ADV-03), and the


lack of proper validation and failure to fully remove lock records, allowing the same lock to be removed


multiple times (OS-ASC-ADV-11).


Furthermore, removing an investor does not clear the attributes associated with the investor when they


are removed from the registry (OS-ASC-ADV-12), and a flaw in the full transfer checks incorrectly blocks


all transfers from the US region to the platform wallet (OS-ASC-ADV-06).


Additionally, we identified numerous discrepancies in the role management verifications, which are


flawed in multiple functions, resulting in improper access control and inconsistency between the actual


implementation and the documentation (OS-ASC-ADV-14). There are also multiple instances where the


investor count is not correctly updated, particularly during burn events and when adjusting for a change


in an investor’s country (OS-ASC-ADV-07).


We also recommended adding a function to revoke any given spender’s permission by deleting their


entry from the allowances list altogether (OS-ASC-SUG-00) and advised incorporating additional checks


within the codebase for improved robustness and security (OS-ASC-SUG-01). We further suggested


modifying the codebase for improved functionality, efficiency, and maintainability (OS-ASC-SUG-03).


© 2024 Otter Audits LLC. All Rights Reserved. 3 / 37


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/aptos-labs/aptos-securitize.](https://github.com/aptos-labs/aptos-securitize)


This audit was performed against commit [bd5269f.](https://github.com/aptos-labs/aptos-securitize/commit/bd5269f94c35d45c9296f744ac638d9c7af6bce2)


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**


It consists of a set of smart contracts to manage regulated digital sesecuritize

curities.


© 2024 Otter Audits LLC. All Rights Reserved. 4 / 37


**03** **—** **Findings**


Overall, we reported 21 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.





© 2024 Otter Audits LLC. All Rights Reserved. 5 / 37


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.



a logic flaw where it always returns true if


ing any subsequent checks against the current


timestamp.

|remove_wallet|Col2|
|---|---|
|**`investor.wallets`**|**`investor.wallets`**|



resulting in inaccurate balance calculations in


sets issuance values to zero instead of


correctly deletes the last lock record instead


of the specified lock, resulting in inaccuracies


in tracking transferable tokens.


Users with zero balances may repeatedly de

posit and withdraw zero-value assets, artifi

cially decreasing the total investor count, and


preventing proper removal of inactive investors.


When zero-value FAs are withdrawn and


destroyed without being deposited, the


blocks further withdrawals by violating the



OS-ASC-ADV-00


OS-ASC-ADV-01


OS-ASC-ADV-02


OS-ASC-ADV-03


OS-ASC-ADV-04


OS-ASC-ADV-05





© 2024 Otter Audits LLC. All Rights Reserved. 6 / 37


Aptos Securitize Audit 04 - Vulnerabilities


A flaw in the full transfer checks incorrectly


blocks all transfers from the US region to the



is set, without verifying whether the transfer


amount matches the investor’s balance.


There are multiple instances where the investor


count is not correctly updated, particularly dur

ing burn events and when adjusting for a change


in an investor’s country.


It is possible to prevent registration of


wallet addresses due to the utilization

|create_primary_store<br>of ins<br>ensure_primary_store_exists<br>of|Col2|create_primary_store|Col4|ins|
|---|---|---|---|---|
|of<br>**`create_primary_store`**<br>ins<br>of<br>**`ensure_primary_store_exists`**|**`ensure_primary_store_exists`**|**`ensure_primary_store_exists`**|**`ensure_primary_store_exists`**|**`ensure_primary_store_exists`**|
|**`add_wallet`**|**`add_wallet`**|**`add_wallet`**|.|.|



A potential underflow scenario exists if


fies wallet balances based on investor balances,


allowing the addition of zero-balance wallets to


the system.


The lock removal process lacks proper vali

dation and does not fully remove lock records,


allowing the same lock to be removed multiple


times and resulting in inaccurate lock informa

tion.


tributes associated with an investor when they


are removed from the registry.


sidered when calculating the limit for U.S. in

vestors, resulting in potential inaccuracies.



OS-ASC-ADV-06


OS-ASC-ADV-07


OS-ASC-ADV-08


OS-ASC-ADV-09


OS-ASC-ADV-10


OS-ASC-ADV-11


OS-ASC-ADV-12


OS-ASC-ADV-13





© 2024 Otter Audits LLC. All Rights Reserved. 7 / 37


Aptos Securitize Audit 04 - Vulnerabilities


The role management verifications are flawed in



multiple functions, resulting in improper access


control and inconsistencies between the actual


implementation and the documentation.


empty string IDs, which may result in significant


logical errors in the contract.


record, which may result in outdated tracking of


who last modified the investor’s attributes.



OS-ASC-ADV-14


OS-ASC-ADV-15


OS-ASC-ADV-16





© 2024 Otter Audits LLC. All Rights Reserved. 8 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**

|is_block_flowback_end_time_ok|Col2|
|---|---|
|**`block_flowback_end_time`**|is zero|



evaluates to false, and the function will never abort, as the second condition


_>__ _move/sources/compliance_service.move_ rust

```
  /// Checks if the block flowback end time has been reached.
  fun is_block_flowback_end_time_ok(block_flowback_end_time: u256): bool {
    block_flowback_end_time != 0
      || (timestamp::now_seconds() as u256) < block_flowback_end_time
  }

```

always return true, resulting in the function aborting. As a result, it will not check the

**`timestamp::now_seconds()`** **`as`** **`u256)`** **`<`** **`block_flowback_end_time`** condition.


**Remediation**

|Return true when|block_flowback_end_time|Col3|
|---|---|---|
|**`block_flowback_end_time`**|**`block_flowback_end_time`**|is greater than ze|



the flowback end time. If it is, it indicates the flowback period is still active, and the function should return


true. If not, return false, indicating that the flowback period has ended.


**Patch**


Resolved in [4e2290c.](https://github.com/aptos-labs/aptos-securitize/commit/4e2290c2)


© 2024 Otter Audits LLC. All Rights Reserved. 9 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**


_>__ _move/sources/registry_service.move_ rust

```
  public entry fun remove_wallet(
    authorizer: &signer, wallet_addr: address, id: String
  ) acquires InvestorInfo {
    [...]
    let investor_wallets_mut = &mut investor_info_mut().investors_wallets;
    smart_table::remove(investor_wallets_mut, wallet_addr);
    let investor = smart_table::borrow_mut(&mut investor_info_mut().investors, id);
    investor.wallet_count = investor.wallet_count - 1;
    event::emit(
      DSRegistryServiceWalletRemoved {
         wallet: wallet_addr,
         investorId: id,
         sender: authorizer_address
      }
    );
  }

```

reduced, the iteration may stop prematurely.


_>__ _move/sources/registry_service.move_ rust

```
  public fun investor_wallet_balance_total(investor_id: String): u64 acquires InvestorInfo {
    [...]
    for (i in 0..investor.wallet_count) {
      let wallet = *vector::borrow(&investor.wallets, i);
      let pfs = primary_fungible_store::primary_store_inlined(wallet, asset);
      balance = balance + fungible_asset::balance(pfs);
    };
    balance
  }

```

© 2024 Otter Audits LLC. All Rights Reserved. 10 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Remediation**


**Patch**


Resolved in [06538b8](https://github.com/aptos-labs/aptos-securitize/commit/06538b82) and [689014d.](https://github.com/aptos-labs/aptos-securitize/commit/689014dc053ae67f8b8fdc6f76cbf935d24de74a)


© 2024 Otter Audits LLC. All Rights Reserved. 11 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**


instead of the actual issuance amount. Because every issuance is recorded with a value of zero, the


_>__ _move/sources/compliance_service.move_ rust

```
  fun create_issuance_information(
    investor: String, _value: u256, issuance_time: u256
  ): bool acquires ComplianceData {
    [...]
    // Update the issuances value with respect to the investor and current issuancescount.
    let issuances_values = &mut compliance_data_mut.issuances_values;
    let value = 0;
    [...]
  }

```

**Remediation**


passed to the function.


**Patch**


Resolved in [9f5d9b2.](https://github.com/aptos-labs/aptos-securitize/commit/9f5d9b28)


© 2024 Otter Audits LLC. All Rights Reserved. 12 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**


_>__ _move/sources/lock_manager.move_ rust

```
  public entry fun remove_lock_record_for_investor(
    authorizer: &signer, investor: String, lock_index: u64
  ) acquires LockInfo {
    let lock_info = lock_info_mut();
    let investor_locks = &lock_info.investor_locks;
    assert!(smart_table::contains(investor_locks, investor), EINVESTOR_NOT_LOCKED);
    let investor_locks_inner = smart_table::borrow(investor_locks, investor);
    assert!(
      smart_table::contains(investor_locks_inner, lock_index), EINVESTOR_NOT_LOCKED
    );
    let lock = smart_table::borrow(investor_locks_inner, lock_index);
    [...]
    smart_table::upsert(investor_locks_count, investor, last_lock_number);
    set_lock_info_impl(
      investor,
      lock_index,
      lock.value,
      lock.reason_code,
      lock.reason_string,
      lock.release_time,
      investor_locks_mut
    );
  }

```

**Remediation**


**Patch**


Resolved in [06538b8.](https://github.com/aptos-labs/aptos-securitize/commit/06538b82)


© 2024 Otter Audits LLC. All Rights Reserved. 13 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**


There is an inconsistency in the way the system allows users to create zero-value fungible assets (FA)


. A user with a zero FA balance may withdraw a zero-value FA and then deposit it, setting


_>__ _aptos-move/framework/aptos-framework/sources/fungible_asset.move_ rust

```
  /// Create a fungible asset with zero amount.
  /// This can be useful when starting a series of computations where the initial value is 0.
  public fun zero<T: key>(metadata: Object<T>): FungibleAsset {
    FungibleAsset {
      metadata: object::convert(metadata),
      amount: 0,
    }
  }

```

of investors in the system.

|fungible_asset::zero|Col2|) an|
|---|---|---|
|hich calls|**`record_transfer`**|**`record_transfer`**|



_>__ _move/sources/compliance_ __service.move_ rust

```
  /// Records the transfer between two investors.
  /// Adjusts the total investors count based on balances.
  fun record_transfer(
    from: address,
    to: address,
    value: u256,
  ): bool acquires ComplianceData {
    if (compare_investor_balance(to, value, 0)) {
      adjust_total_investors_counts(to, true);
    };
    if (balance_of_investor(from) == 0) {
      adjust_total_investors_counts(from, false);
    };
    true
  }

```

© 2024 Otter Audits LLC. All Rights Reserved. 14 / 37


Aptos Securitize Audit 04 - Vulnerabilities


This logic assumes that a zero balance indicates that the investor no longer holds any assets in the system;


thus, they should no longer be considered active investors. Consequently, it is possible to artificially


reduce the investor count, which may prevent the proper removal of investors.


**Remediation**


Ensure that the investor is not depositing a zero amount.


**Patch**


Resolved in [9f5d9b2.](https://github.com/aptos-labs/aptos-securitize/commit/9f5d9b283c84389b69c8d3ab2e625c733fbd3f2e)


© 2024 Otter Audits LLC. All Rights Reserved. 15 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**


(FA). Since this FA has a value of zero, it does not represent any meaningful asset transfer. Still, the









Thus, the system will now believe that a withdrawal is still in progress, even though the zero-value FA was


check.


**Remediation**


Ensure that the investor is not withdrawing a zero amount.


**Patch**


Resolved in [06538b8.](https://github.com/aptos-labs/aptos-securitize/commit/06538b825da127fa06312d0ab2e69b75798b95c1)


© 2024 Otter Audits LLC. All Rights Reserved. 16 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**


dition checks if full transfers are enforced when the transfer originates from the US. If this condition


platform wallet is rejected, regardless of whether the transfer satisfies the required full transfer conditions.


As a result, valid transactions may be blocked.


_>__ _move/sources/compliance_service.move_ rust

```
  fun pre_deposit_check_regulated(
    withdraw_from: &mut WithdrawFrom,
    to: address,
    value: u256,
    paused: bool,
  ): (u256, u64) acquires ComplianceData, ComplianceConfig, TransferRestrictions,TokenLimits,
```

_�→_ `TimeConstraints` `{`
```
    [...]
    if (is_platform_wallet) {
      if ((get_force_full_transfer()
         && from_region == US)
         || (
           get_world_wide_force_full_transfer()
              && (from_investor_balance as u256) > value
         )) {
         abort EONLY_FULL_TRANSFER
      };
      return (0, VALID)
    };
    [...]
  }

```

**Remediation**


**Patch**


Resolved in [#61.](https://github.com/aptos-labs/aptos-securitize/pull/61/)

|ced by confirming if|get_force_full_transfer|Col3|
|---|---|---|
|**`get_world_wide_force_full_transfer`**|**`get_world_wide_force_full_transfer`**|is set.|



© 2024 Otter Audits LLC. All Rights Reserved. 17 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**


decrease the total investor count incorrectly, even though the investor was already inactive (with a zero


balance) and should not have been counted.


_>__ _move/sources/compliance_service.move_ rust

```
  fun record_burn(who: address, value: u256): bool acquires ComplianceData {
    let balance_who = balance_of_investor(who);
    if (balance_who == (value as u64)) {
      adjust_total_investors_counts(who, false);
    };
    true
  }

```

Additionally, **`registry_service::adjust_investor_counts_after_country_change`** currently


only increases the investor count for the new country but does not decrease it for the previous country. If


an investor changes their country, compliance counts for the old country need to be updated to reflect


that the investor no longer belongs to it.


**Remediation**


**Patch**


Resolved in [9f5d9b2.](https://github.com/aptos-labs/aptos-securitize/commit/9f5d9b28)


© 2024 Otter Audits LLC. All Rights Reserved. 18 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**


permissionless.


|::add_wallet ::add_wallet wallet_addr wallet_addr|Col2|
|---|---|
|**`wallet_addr`**|**`wallet_addr`**|
||**`add_wallet`**|









is a special wallet, unintentionally allowing only special wallets to be added. This behavior may expose


the system to risks. The intended functionality, however, is to prevent the registration of special wallets.


_>__ _move/sources/registry_service.move_ rust

```
  /// Allows an investor to add a wallet to their own account.
  public entry fun add_wallet_by_investor(
    authorizer: &signer, wallet_addr: address
  ) acquires InvestorInfo, WalletTypesRegistry {
    assert!(is_special_wallet(wallet_addr), EWALLET_SPECIAL);
    [...]
  }

```

© 2024 Otter Audits LLC. All Rights Reserved. 19 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Remediation**


**Patch**


Resolved in [06538b8](https://github.com/aptos-labs/aptos-securitize/commit/06538b82) and [8932cf1.](https://github.com/aptos-labs/aptos-securitize/commit/8932cf16)


© 2024 Otter Audits LLC. All Rights Reserved. 20 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**

|get_compliance_transferable_tokens_deposit|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|ithin|**`compliance_service`**|,|**`difference`**|is calculate|



_>__ _move/sources/compliance_service.move_ rust

```
  fun get_compliance_transferable_tokens_deposit(
    who: address,
    time: u64,
    lock_time: u64,
    from_balance: u64
  ): u64 acquires ComplianceData {
    assert!(time > 0, EINVALID_TIME);
    [...]
    let total_tokens_locked = 0;
    for (i in 0..investor_issuances_count) {
      let issuances_timestamps = &compliance_data.issuances_timestamps;
      let issuances_timestamps_inner =
         smart_table::borrow(issuances_timestamps, investor);
      let issuance_time =
         *smart_table::borrow_with_default(issuances_timestamps_inner, i, &0);
      let difference = time - lock_time;
      if (lock_time > time || issuance_time > (difference as u256)) {
         let issuances_values = &mut compliance_data.issuances_values;
         let issuances_values_inner =
           smart_table::borrow_mut(issuances_values, investor);
         total_tokens_locked = total_tokens_locked
           + *smart_table::borrow_mut_with_default(issuances_values_inner, i, 0);
      }
    };
    [...]
  }

```

**Remediation**


**Patch**


Resolved in [9f5d9b2.](https://github.com/aptos-labs/aptos-securitize/commit/9f5d9b28)


© 2024 Otter Audits LLC. All Rights Reserved. 21 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**


balance in each individual wallet. This implies that even if a wallet holds zero tokens, it will still be added to


the active wallet list if the investor’s total balance is non-zero. This discrepancy may allow an investor to


balance), initiating a token transfer to each of these wallets with a value of zero.


_>__ _move/sources/ds_token.move_ rust

```
  /// Check wallets for list.
  /// This function is called after every transfer, burn, mint, and seize operation.
  fun check_wallets_for_list(from: address, to: address) acquires WalletData {
    let from_balance =
       registry_service::investor_wallet_balance_total(
         registry_service::get_investor(from)
       );
    let to_balance =
       registry_service::investor_wallet_balance_total(
         registry_service::get_investor(to)
       );
    if (from_balance == 0) {
       remove_wallet_from_list(from)
    };
    if (to_balance > 0) {
       add_wallet_to_list(to)
    };
  }

|wallet_list|Col2|and|wallet_indexes|Col5|
|---|---|---|---|---|
|and|**`wallet_indexes`**|**`wallet_indexes`**|**`wallet_indexes`**|, the transfer fu|


```

some wallets may result in a hash-denial-of service scenario. However, executing this attack is costly,


and there is no direct monetary reward to benefit from. Furthermore, it is a regulated environment where


all wallets have to undergo a KYC procedure.


This function maintains a registry of active wallets, updating it to add wallets with positive balances and


remove those with zero balances. However, this process does not account for transfers processed through


© 2024 Otter Audits LLC. All Rights Reserved. 22 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Remediation**


wallet registry accurately after every deposit action regardless of the transfer method.


**Patch**


Resolved in [438f61f.](https://github.com/aptos-labs/aptos-securitize/commit/438f61f0)


© 2024 Otter Audits LLC. All Rights Reserved. 23 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**


renders the data accessible in the system even after it is supposedly removed. Since locks are not fully


result, the same lock may be removed multiple times repeatedly, each time decreasing the lock count.


**Remediation**


function.


**Patch**


Resolved in [06538b8.](https://github.com/aptos-labs/aptos-securitize/commit/06538b82)


© 2024 Otter Audits LLC. All Rights Reserved. 24 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**


investors table is deleted. Any associated data, such as compliance attributes, remains in the attributes


table. If a new investor is later registered with the same ID as the removed investor, the system will


inadvertently link the new investor to the old attributes, potentially allowing unintended access to privileges


based on deleted investor’s attributes.


_>__ _move/sources/registry_service.move_ rust

```
  public entry fun remove_investor(authorizer: &signer, id: String) acquires InvestorInfo {
    [...]
    let investors = &mut investor_info_mut().investors;
    smart_table::remove(investors, id);
    event::emit(
      DSRegistryServiceInvestorRemoved {
         investorId: id,
         sender: signer::address_of(authorizer)
      }
    );
  }

```

**Remediation**


Remove the investor’s attributes from the attributes table when the investor record is deleted.


**Patch**


Resolved in [06538b8.](https://github.com/aptos-labs/aptos-securitize/commit/06538b82)


© 2024 Otter Audits LLC. All Rights Reserved. 25 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**


investors’ limit is intended to restrict the percentage of U.S. investors relative to the total number of


investors may exceed the intended compliance threshold.


**Remediation**


Calculate the limit as shown below:




       Actual Limit = min



max_us_investors_percentage _×_ total_investors            us_investors_limit _,_

100



**Patch**


Resolved in [#61.](https://github.com/aptos-labs/aptos-securitize/pull/61/)


© 2024 Otter Audits LLC. All Rights Reserved. 26 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**


limiting it to issuers, transfer agents, or higher authority roles. However, the requirement is that these


above two functions.


_>__ _move/sources/registry_service.move_ rust

```
  public entry fun register_investor(
    authorizer: &signer, id: String, collision_hash: String
  ) acquires InvestorInfo {
    trust_service::assert_only_issuer_or_transfer_agent_or_above(authorizer);
    assert!(!is_investor(id), EINVESTOR_ALREADY_EXISTS);
    [...]
  }

```

**Remediation**


Address the above discrepancies in role management.


**Patch**


Resolved in [06538b8.](https://github.com/aptos-labs/aptos-securitize/commit/06538b82)


© 2024 Otter Audits LLC. All Rights Reserved. 27 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**


other valid IDs. An empty string ID has a special meaning in the contract and will break many parts of

|Col1|is_wallet|Col3|
|---|---|---|
|**`""`**|**`""`**|. This will|



contract’s logic, where functions that check for investor existence may incorrectly identify an empty ID as


a valid investor.


_>__ _move/sources/registry_service.move_ rust

```
  /// Registers a new investor with the given ID and collision hash. Only callable by issuer or
```

_�→_ _`transfer`_ _`agent`_ _`or`_ _`above.`_
```
  public entry fun register_investor(
    authorizer: &signer, id: String, collision_hash: String
  ) acquires InvestorInfo {
    trust_service::assert_only_issuer_or_transfer_agent_or_above(authorizer);
    assert!(!is_investor(id), EINVESTOR_ALREADY_EXISTS);
    let investor = Investor {
      id,
      collision_hash,
      creator: signer::address_of(authorizer),
      last_updated_by: signer::address_of(authorizer),
      country: string::utf8(b""),
      wallet_count: 0,
      wallets: vector::empty()
    };
    [...]
  }

```

**Remediation**


**Patch**


Resolved in [06538b8.](https://github.com/aptos-labs/aptos-securitize/commit/06538b82)


© 2024 Otter Audits LLC. All Rights Reserved. 28 / 37


Aptos Securitize Audit 04 - Vulnerabilities


**Description**


modification to an investor’s attributes.


**Remediation**


**Patch**


Resolved in [06538b8.](https://github.com/aptos-labs/aptos-securitize/commit/06538b82)


© 2024 Otter Audits LLC. All Rights Reserved. 29 / 37


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.


OS-ASC-SUG-00

another address, but lacks a way to completely remove this approval.


There are several instances where proper validation is not done, resulting

OS-ASC-SUG-01

in potential security issues.


Additional safety checks may be incorporated within the codebase to make

OS-ASC-SUG-02

it more robust and secure.


Recommendation for modifying the codebase for improved functionality,

OS-ASC-SUG-03

efficiency, and maintainability.


© 2024 Otter Audits LLC. All Rights Reserved. 30 / 37


Aptos Securitize Audit 05 - General Findings


**Missing** **Approval** **Removal** **Function** OS-ASC-SUG-00


**Description**


However, there is no direct way to withdraw or remove this approval from the allowances list. Instead, the


only option is to reset the approval amount to zero.


**Remediation**


list altogether.


**Patch**


Resolved in [06538b8.](https://github.com/aptos-labs/aptos-securitize/commit/06538b82)


© 2024 Otter Audits LLC. All Rights Reserved. 31 / 37


Aptos Securitize Audit 05 - General Findings


**Missing** **Validation** **Logic** OS-ASC-SUG-01


**Description**

|init_module<br>tion, functions d<br>ds_protocol<br>ddress stored in|init_module|Col3|Col4|functions d|
|---|---|---|---|---|
|tion, **`init_module`**<br>functions d<br>ddress stored in **`ds_protocol`**|**`init_module`**|**`ds_protocol`**|**`ds_protocol`**|**`ds_protocol`**|
|**`dstoken_address`**|**`dstoken_address`**|**`dstoken_address`**|rely on this|rely on this|



_>__ _move/sources/token_issuer.move_ rust

```
     public entry fun issue_tokens(
       [...]
     ) {
       [...]
       if (registry_service::is_wallet(to)) {
          assert!(registry_service::get_investor(to) != string::utf8(b""), 0);
       }[...]
     }

```

that the wallet address does not already exist for the specified investor before adding it.


actually exists.


**Remediation**


1. Verify that the deployer’s address aligns with the stored one.


ensure that tokens are issued to the correct investor.


**Patch**


1. Issue #1 resolved in [06538b8.](https://github.com/aptos-labs/aptos-securitize/commit/06538b82)


2. Issue #2 resolved in [06538b8.](https://github.com/aptos-labs/aptos-securitize/commit/06538b82)


3. Issue #3 resolved in [06538b8.](https://github.com/aptos-labs/aptos-securitize/commit/06538b82)


© 2024 Otter Audits LLC. All Rights Reserved. 32 / 37


Aptos Securitize Audit 05 - General Findings


**Additional** **Safety** **Checks** OS-ASC-SUG-02


**Description**


is within the allowed range.

|compliance_service::validate_issuance_time|Col2|Col3|
|---|---|---|
|es not verify whether the provided|**`issuance_time`**|i|



equal to the current timestamp.


_>__ _move/sources/compliance_service.move_ rust

```
     fun validate_issuance_time(issuance_time: u256): u256 acquires Miscellaneous {
       if (!get_disallow_back_dating()) {
          return issuance_time
       };
       return (timestamp::now_seconds() as u256)
     }

```

**Remediation**


2. Add a check to ensure that the issuance time is not in the future.


© 2024 Otter Audits LLC. All Rights Reserved. 33 / 37


Aptos Securitize Audit 05 - General Findings


**Code** **Refactoring** OS-ASC-SUG-03


**Description**


_>__ _move/sources/registry_service.move_ rust

```
     public entry fun add_wallet_by_investor(
       authorizer: &signer, wallet_addr: address
     ) acquires InvestorInfo, WalletTypesRegistry {
       [...]
       smart_table::add(
          investor_wallets,
          wallet_addr,
          Wallet { owner, creator: wallet_addr, last_updated_by: wallet_addr }
       );
       [...]
       event::emit(
          DSRegistryServiceWalletAdded {
            wallet: wallet_addr,
            investorId: owner,
            sender: wallet_addr
          }
       );
     }

|Abort|lock_manager::remove_lock_record|Col3|
|---|---|---|
|**`lock_index`**|**`lock_index`**|does not exist to improve code rel|


```

result in ambiguity, as the caller may not be aware that the intended operation did not succeed.


modules for consistency.


© 2024 Otter Audits LLC. All Rights Reserved. 34 / 37


Aptos Securitize Audit 05 - General Findings


**Remediation**


Implement the above-mentioned suggestions.


**Patch**


1. Issue #1 resolved in [06538b8.](https://github.com/aptos-labs/aptos-securitize/commit/06538b82)


2. Issue #2 resolved in [06538b8.](https://github.com/aptos-labs/aptos-securitize/commit/06538b82)


© 2024 Otter Audits LLC. All Rights Reserved. 35 / 37


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


© 2024 Otter Audits LLC. All Rights Reserved. 36 / 37


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


© 2024 Otter Audits LLC. All Rights Reserved. 37 / 37


