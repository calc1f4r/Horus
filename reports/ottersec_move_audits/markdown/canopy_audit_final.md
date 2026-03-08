# **Canopy**

Security Assessment


March 11th, 2025 - Prepared by OtterSec


Bartłomiej Wierzbiński [dark@osec.io](mailto:dark@osec.io)


Fineas Silaghi [fedex@osec.io](mailto:fedex@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **3**


Overview 3


Key Findings 3


**Scope** **4**


**Findings** **5**


**Vulnerabilities** **6**


OS-CPY-ADV-00 | Ambiguous Handling of Asset Contributions 8


OS-CPY-ADV-01 | Improper Transfer via Shared Resource Account 10


OS-CPY-ADV-02 | Incorrect Claim Calculations 11


OS-CPY-ADV-03 | Message Validation Bypass 13


OS-CPY-ADV-04 | Inconsistency in Emergency Withdrawal Procedure 14


OS-CPY-ADV-05 | Unrestricted Cross-Chain Messaging 15


OS-CPY-ADV-06 | Signature Replay in Claim Functionality 16


**General** **Findings** **17**


OS-CPY-SUG-00 | Pause State Transition Inconsistency 19


OS-CPY-SUG-01 | Ambiguous Dumped Amount Reporting 20


OS-CPY-SUG-02 | Unnecessary Boolean Checks in Claim Tracking 21


OS-CPY-SUG-03 | Code Optimization 22


OS-CPY-SUG-04 | Modifying Mapping Update Logic 23


OS-CPY-SUG-05 | Missing Validation Logic 24


OS-CPY-SUG-06 | Code Refactoring 25


OS-CPY-SUG-07 | Code Maturity 27


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 38


Canopy Audit


TABLE OF CONTENTS


OS-CPY-SUG-08 | Code Clarity 28


OS-CPY-SUG-09 | Documentation Enhancement 30


OS-CPY-SUG-10 | Code Redundancy 32


OS-CPY-SUG-11 | Unutilized Code 35


**Appendices**


**Vulnerability** **Rating** **Scale** **37**


**Procedure** **38**


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 38


**01** **—** **Executive** **Summary**

## Overview


between January 10th and March 10th, 2025. We also conducted a follow-up audit from April 18th to


April 19th, 2025. For more information on our auditing methodology, refer to Appendix B.

## Key Findings


We produced 19 findings throughout this audit engagement.


In particular, we identified several critical vulnerabilities, including one concerning the protocol’s am

biguous handling of asset contributions based on the resource account’s balances, which may result


in incorrect asset processing, creating a denial of service or loss of funds due to misinterpretation of


incoming contributions (OS-CPY-ADV-01), and a lack of validation for incoming messages, allowing


attackers to exploit griefing and funds-stealing vulnerabilities by sending malformed or empty messages


to misappropriate or dump funds (OS-CPY-ADV-03).


Additionally, the creator of the single asset base deployer may directly withdraw funds from the primary


fungible store via the FA API, bypassing the emergency withdrawal restrictions (OS-CPY-ADV-05).


We also made recommendations regarding modifications to the codebase for improved functionality,


efficiency, and robustness (OS-CPY-SUG-06) and suggested removing redundant and unutilized code


instances (OS-CPY-SUG-10, OS-CPY-SUG-11). Moreover, we advised adhering to coding best prac

tices (OS-CPY-SUG-07) and including additional safety checks within the codebase to improve security


(OS-CPY-SUG-05).


Furthermore, we highlighted certain modifications to rectify informational and typographical errors in


the comments to implement proper error handling and emit events to log state changes for improved


transparency and debugging (OS-CPY-SUG-08).


© 2025 Otter Audits LLC. All Rights Reserved. 3 / 38


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/Canopyxyz/cornucopia-](https://github.com/Canopyxyz/cornucopia-move)


[move.](https://github.com/Canopyxyz/cornucopia-move) This audit was performed against commit [fcca73b.](https://github.com/Canopyxyz/cornucopia-move/commit/fcca73b4aef9f8a349f4f9c2245180322c914a48) We further reviewed [PR#30.](https://github.com/Canopyxyz/cornucopia-move/pull/30)


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**


A cross-chain liquidity deployment and rewards management system


that bridges assets from Ethereum to the Move blockchain using Lay
cornucopia-move

erZero. It manages user deposits, investments in underlying protocols,


and reward distributions.


© 2025 Otter Audits LLC. All Rights Reserved. 4 / 38


**03** **—** **Findings**


Overall, we reported 19 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.





© 2025 Otter Audits LLC. All Rights Reserved. 5 / 38


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


**ID** **Severity** **Status** **Description**


The protocol’s ambiguous handling of asset contribu

tions based on the resource account’s balances may



result in incorrect asset processing, creating a denial


of service or a loss of funds due to misinterpretation


of incoming contributions.


the global resource account to the deployer’s primary


fungible store. This approach may result in interfer

objects sharing the same asset.


the lockup phase fail to account for withdrawals and


deployments, resulting in incorrect share and unde

ployed base asset distribution.


There is a lack of validation for incoming messages in


attackers to exploit griefing and funds-stealing vul

nerabilities by sending malformed or empty messages


to misappropriate or dump funds.


directly withdraw funds from the primary fungible


store via the fungible asset API, bypassing the emer

gency withdrawal restrictions.


arbitrary cross-chain messages, resulting in unau

thorized interactions or exploits.



OS-CPY-ADV-00


OS-CPY-ADV-01


OS-CPY-ADV-02


OS-CPY-ADV-03


OS-CPY-ADV-04


OS-CPY-ADV-05





© 2025 Otter Audits LLC. All Rights Reserved. 6 / 38


Canopy Audit 04 - Vulnerabilities



attacks, allowing the possibility of retransmitting valid


claim requests within the deadline window.



OS-CPY-ADV-06





© 2025 Otter Audits LLC. All Rights Reserved. 7 / 38


Canopy Audit 04 - Vulnerabilities


**Description**


The vulnerability in the dual asset module relates to the ambiguity in deciding which asset contribution to


process based on the primary fungible store balances of the resource account. The contributions in dual


asset are made for one asset at a time. Thus, the protocol must make two separate contributions - for


both assets. The protocol chooses which asset to proceed with based on the balance of assets in the


primary fungible store of the resource account. This ambiguity may result in denial of service or loss of


funds scenarios.


This may be exploited in two ways as illustrated below:


**Proof** **of** **Concept**


Below scenario takes into account the presence of an attacker:


the resource account, and the protocol waits for the compose trigger.


The following example illustrates the case where there is no attacker:


**Remediation**


The protocol should process the assets based on the message source, not the asset balances.


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 38


Canopy Audit 04 - Vulnerabilities


**Patch**


Resolved in [5abad86](https://github.com/Canopyxyz/cornucopia-move/commit/5abad868724d1680221460b5a149e25ca9e5f2b5) and [6bac9d0.](https://github.com/Canopyxyz/cornucopia-move/commit/6bac9d00e5f7e389ca8253bbc175d0e5cf26ec92)


© 2025 Otter Audits LLC. All Rights Reserved. 9 / 38


Canopy Audit 04 - Vulnerabilities


**Description**


information about bridged assets. It records individual contributor amounts for funds that were directly


account to the deployer’s primary fungible store without distinguishing between different deployers.


_>__ _deployers/single-asset/sources/base/single_asset_base_deployer.move_ rust

```
  public(friend) fun notify_funds(
    base_deployer_obj_address_bytes: vector<u8>,
    eth_contributors: vector<vector<u8>>,
    contribution_amounts: vector<u64>
  ): (u64, u64) acquires GlobalConfig, SingleAssetBaseDeployer {
    [...]
    // Transfer any asset from resource account to deployer
    let resource_balance = primary_fungible_store::balance(resource_account_addr, base_asset);
    if (resource_balance > 0) {
      let funds = primary_fungible_store::withdraw(&resource_signer, base_asset,
```

_�→_ `resource_balance);`
```
      primary_fungible_store::deposit(deployer_addr, funds);
    };
    [...]
  }

```

Transferring all available assets from the global resource account to the deployer’s primary fungible store


without proper segregation may result in assets intended for one deployer to be allocated to another.


Additionally, if one deployer consumes all available assets, others may be unable to function properly.


**Remediation**


**Patch**


Resolved in [5abad86.](https://github.com/Canopyxyz/cornucopia-move/commit/5abad86)


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 38


Canopy Audit 04 - Vulnerabilities


**Description**


base assets and shares when contributors claim their funds. Specifically, when a claim occurs during the


lockup phase and is followed by another deployment, the subsequent claims may become inconsistent,


resulting in incorrect share allocations and undeployed base distributions. The function does not correctly


account for changes in total shares and base assets caused by partial claims and subsequent deployments.


**Proof** **of** **Concept**


2. When the first deployment occurs, 8000 base assets are deployed to receive 8000 shares. Now


is 2000.


3. One contributor claims their funds during the lockup phase. They claim 200 undeployed base assets


8000, the primary fungible store actually holds only 7200 because 800 shares were withdrawn.


4. A second deployment occurs, and another 1000 base assets are deployed to exchange 1000 more

|last_base_balance|Col2|is now 800, and|Col4|total_shares_received|
|---|---|---|---|---|
|ion updates|**`total_shares_received`**|**`total_shares_received`**|to equal the balance of the p|to equal the balance of the p|



for share assets.


5. After the lockup phase ends, the remaining 9 contributors try to claim their funds. The undeployed


base asset calculation distributes 100 base per contributor


6. Thus, it will not be possible for the last claimant to claim their 100 base assets since only 800


remain. Also, the primary fungible store is left with 1640 unclaimed shares, breaking the expected


fair distribution of funds.


**Remediation**


Ensure that the formula utilized to calculate shares and undeployed amounts accounts for changes resulting


from withdrawals and deployments, reflecting these changes in the total shares and base asset.


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 38


Canopy Audit 04 - Vulnerabilities


**Patch**


Resolved in [e461d18.](https://github.com/Canopyxyz/cornucopia-move/commit/e461d1875e13a7319dfc69e4d947c83c7c00a9d6)


© 2025 Otter Audits LLC. All Rights Reserved. 12 / 38


Canopy Audit 04 - Vulnerabilities


**Description**

|Col1|r may deploy a et et that matches the victim’s he SingleAssetBaseDepl SingleAssetBaseDepl resource_account_addr resource_account_addr|
|---|---|
||**`resource_account_addr`**|
|**`timelocked_asset_dump`**|**`timelocked_asset_dump`**|



_>__ _deployers/single-asset/sources/base/single_asset_base_deployer.move_ rust

```
  public(friend) fun notify_funds(
    base_deployer_obj_address_bytes: vector<u8>,
    eth_contributors: vector<vector<u8>>,
    contribution_amounts: vector<u64>
  ): (u64, u64) acquires GlobalConfig, SingleAssetBaseDeployer {
    [...]
    if (vector::length(&eth_contributors) != vector::length(&contribution_amounts)) {
      dump_unnotified_balances(deployer_ref, global_config, unnotified_balance);
      return (TRACE_MISMATCHED_VECTORS, 0)
    };
    [...]
  }

```

Furthermore, an attacker may exploit unprocessed contributions (such as when bridged fungible assets


are minted to the store, but the original contribution message has not been processed yet) to steal funds.


message would be discarded.


**Remediation**


succeeding without the necessary checks.


**Patch**


Resolved in [03bb14d.](https://github.com/Canopyxyz/cornucopia-move/commit/03bb14d)


© 2025 Otter Audits LLC. All Rights Reserved. 13 / 38


Canopy Audit 04 - Vulnerabilities


**Description**


The protocol’s emergency withdraw procedure may be initiated and completed without the ability for the


ability to bypass protocol restrictions, including emergency withdrawals. Due to the way in which the


to directly interact with its primary fungible store via the fungible asset API.


**Remediation**


the creator.


**Patch**


Resolved in [8b29ad3.](https://github.com/Canopyxyz/cornucopia-move/commit/8b29ad3)


© 2025 Otter Audits LLC. All Rights Reserved. 14 / 38


Canopy Audit 04 - Vulnerabilities


**Description**


configured peers without any access control or authorization checks. Since it does not verify the caller’s


authorization, any user may send messages from this OApp. The impact of this issue depends on who


receives the message and how the message contents are processed on the receiving end.


**Remediation**


Remove this feature or have its access restricted.


**Patch**


Resolved in [5549c0f.](https://github.com/Canopyxyz/cornucopia-move/commit/5549c0f)


© 2025 Otter Audits LLC. All Rights Reserved. 15 / 38


Canopy Audit 04 - Vulnerabilities


**Description**


withdraw funds on behalf of the user during the deadline window. Moreover, if the phase transitions to


the lockup phase in the meantime, the user will incur additional penalties for withdrawing during lockup.


**Remediation**


Restrict the use of the signature-style claim and document it clearly, or remove it entirely. Currently,


high-level overview documentation only references the address mapping claim style.


**Patch**


Resolved in [b08b177.](https://github.com/Canopyxyz/cornucopia-move/commit/b08b177)


© 2025 Otter Audits LLC. All Rights Reserved. 16 / 38


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.


A pause state change may be initiated before deployment and completed



OS-CPY-SUG-00


OS-CPY-SUG-01


OS-CPY-SUG-02


OS-CPY-SUG-03


OS-CPY-SUG-04


OS-CPY-SUG-05


OS-CPY-SUG-06


OS-CPY-SUG-07



afterward, potentially creating inconsistencies, while other timelocked


changes will not be executed or canceled if conditions are not met.


inconsistently, as it refers to different asset types in various parts of the


The utilization of boolean values in the claimed lockup tables is unnecessary,


as checking the existence of the address is sufficient.


The overall code may be streamlined further to reduce complexity and


improve efficiency.

|gic in|configure_move_claim_address|Col3|
|---|---|---|
|**`table::upsert`**|**`table::upsert`**|, which handles both the|



insertion and updating of key-value pairs.


There are several instances where proper validation is not performed, re

sulting in potential issues.


Recommendation for modifying the codebase for improved efficiency, func

tionality, and robustness.


Suggestions regarding inconsistencies in the codebase and ensuring ad

herence to coding best practices.



© 2025 Otter Audits LLC. All Rights Reserved. 17 / 38


Canopy Audit 05 - General Findings


Modifications to the codebase to improve transparency through proper

OS-CPY-SUG-08

event emission and error handling.


The natspec comments and documentation may be updated to accurately

OS-CPY-SUG-09

reflect the current functionality and ensure consistency.


There are multiple instances of redundant code that should be removed for

OS-CPY-SUG-10

better maintainability and clarity.


The codebase contains multiple cases of unnecessary or unutilized code

OS-CPY-SUG-11

that should be removed.


© 2025 Otter Audits LLC. All Rights Reserved. 18 / 38


Canopy Audit 05 - General Findings


**Pause** **State** **Transition** **Inconsistency** OS-CPY-SUG-00


**Description**


deployment, but this change may be finalized after the deployment. The


function proceeds with the update only during the first phase. However, in order to execute the change,


checked during change initiation and not at execution.


_>__ _deployers/single-asset/sources/base/single_asset_base_deployer.move_ rust

```
  public entry fun manage_timelocked_pause_state([...]) acquires SingleAssetBaseDeployer {
    let deployer_ref =
```

_�→_ `borrow_global_mut<SingleAssetBaseDeployer(object::object_address(&deployer_obj));`
```
    assert_signer_is_deployer_owner(deployer_obj, account);
    if (option::is_some(&new_pause_state)) {
      assert!(
         deployer_ref.first_deployment_timestamp == 0,
         E_CANNOT_MODIFY_PAUSE_AFTER_DEPLOYMENT
      );
    };
    timelocked::manage_timelocked_update(&mut deployer_ref.timelocked_pause,
```

_�→_ `new_pause_state,new_delay);`
```
  }

```

of any future changes to the pause state, which effectively locks it. This is an admin-controlled function.


In other functions that manage timelocked values, if a change request is made but the change conditions


are no longer fulfillable, the system does not allow the change to be executed or canceled.


**Remediation**


Enforce stricter checks to ensure that any pause state change may only be initiated and completed within


a valid pre-deployment phase.


© 2025 Otter Audits LLC. All Rights Reserved. 19 / 38


Canopy Audit 05 - General Findings


**Ambiguous** **Dumped** **Amount** **Reporting** OS-CPY-SUG-01


**Description**


deposited into a dump account. However, in the last call (after successfully notifying the deployer),


types of asset dumps.


**Remediation**


fungible asset amount, as implemented in the dual asset module.


© 2025 Otter Audits LLC. All Rights Reserved. 20 / 38


Canopy Audit 05 - General Findings


**Unnecessary** **Boolean** **Checks** **in** **Claim** **Tracking** OS-CPY-SUG-02


**Description**


has claimed rewards during each respective phase.


_>__ _deployers/single-asset/sources/base/single_asset_base_deployer.move_ rust

```
  struct SingleAssetBaseDeployer has key {
    [...]
    /// Maps ethereum addresses to whether they claimed during lockup phase, disqualifying them
```

_�→_ _`from`_ _`MOVE`_ _`rewards`_
```
    claimed_during_lockup: Table<vector<u8>, bool>,
    /// Mapping of ethereum address and whether the user has claimed post lockup and hence is
```

_�→_ _`unable`_ _`to`_ _`call`_ _`claim_relevant_assets`_ _`again`_
```
    claimed_post_lockup: Table<vector<u8>, bool>,
    [...]
  }

```

Although the code frequently checks the value of these entries to determine if an address has claimed


of an entry is sufficient to confirm that the address has claimed rewards during the corresponding phase.


Therefore, checking the value of these entries is unnecessary.


**Remediation**


and value.


© 2025 Otter Audits LLC. All Rights Reserved. 21 / 38


Canopy Audit 05 - General Findings


**Code** **Optimization** OS-CPY-SUG-03


**Description**


if it does not, eliminating the need for an explicit if-else statement.









loop. Additionally, there are redundant vector length checks during decoding that may be optimized.

|There are multiple instances of|primary_fungible_store::withdraw|
|---|---|
|**`primary_fungible_store::deposit`**|**`primary_fungible_store::deposit`**|



**Remediation**


Update the codebase with the above-listed optimizations.


© 2025 Otter Audits LLC. All Rights Reserved. 22 / 38


Canopy Audit 05 - General Findings


**Modifying** **Mapping** **Update** **Logic** OS-CPY-SUG-04


**Description**


associating an Ethereum address with a corresponding Movement address. The code that checks if the


_>__ _deployers/single-asset/sources/base/single_asset_base_deployer.move_ rust

```
  public(friend) fun configure_move_claim_address(eth_address: vector<u8>, move_claim_address:
```

_�→_ `vector<u8>)` `acquires` `GlobalConfig` `{`
```
    [...]
    // Try to update the mapping safely
    if (table::contains(&global_config.claim_addresses, eth_address)) {
      let stored_move_addr = table::borrow_mut(&mut
```

_�→_ `global_config.claim_addresses,eth_address);`
```
      *stored_move_addr = move_claim_address;
    } else {
      table::add(&mut global_config.claim_addresses, eth_address, move_claim_address);
    };
  }

```

**Remediation**


operation in a single function call.


© 2025 Otter Audits LLC. All Rights Reserved. 23 / 38


Canopy Audit 05 - General Findings


**Missing** **Validation** **Logic** OS-CPY-SUG-05


**Description**


should check if a proposal actually exists before attempting to clear the emergency withdrawal


proposal.


bytes, not just 204 bytes. This ensures the minimum size is met, even if there are no contributors or


amounts. Sizes must still be included in the message, even when set to 0.


limits. It is recommended to add restrictions for minimum values to ensure validation across the


entire acceptable range.

|execute_emergency_withdraw|doe|
|---|---|
|**`execute_sweep_resource_account`**|**`execute_sweep_resource_account`**|



5. Claims should only be allowed after the corresponding fungible assets have been transferred. If


contributions are notified and claims are enabled before the deployer’s fungible asset store receives


the funds, users may encounter errors, receive zero share and base assets, and lose their contribution


entry.


**Remediation**


Add the validations stated above.


© 2025 Otter Audits LLC. All Rights Reserved. 24 / 38


Canopy Audit 05 - General Findings


**Code** **Refactoring** OS-CPY-SUG-06


**Description**


1. Utilize an already retrieved signer address during an ownership check in


issues. Ensure that trace codes are distinct.


_>__ _deployers/dual-asset/sources/base/dual_asset_base_deployer.move_ rust

```
     module cornucopia_dual_deployers::dual_asset_base_deployer {
       [...]
       /// Deployer is paused
       const TRACE_DEPLOYER_PAUSED: u64 = 203;
       /// Vector lengths mismatched
       const TRACE_MISMATCHED_VECTORS: u64 = 203;
     }

```

should be updated with the actual deployed amounts derived from balance deltas, which may differ


from the function’s input parameters. Currently, this is only a suggestion, as the field is not utilized


in any calculations.


_>__ _deployers/dual-asset/sources/base/dual_asset_base_deployer.move_ rust

```
     fun assert_valid_lock_duration(lock_duration: u64) {
       assert!(lock_duration < MAX_LOCK_DURATION, E_EXCEEDS_MAX_LOCK_DURATION);
     }

```

**`current_shares_balance`** **`>=`** **`pre_deploy_shares_balance`** . This slippage check is critical


and should fail if no new shares are obtained during a deployment. The check may be refactored to


account for fake deployments while preserving its integrity in real deployments.


© 2025 Otter Audits LLC. All Rights Reserved. 25 / 38


Canopy Audit 05 - General Findings


fields should be updated to preserve their role in maintaining protocol visibility.


**Remediation**


Incorporate the above refactors.


© 2025 Otter Audits LLC. All Rights Reserved. 26 / 38


Canopy Audit 05 - General Findings


**Code** **Maturity** OS-CPY-SUG-07


**Description**

|The existing implementation of|safe_decode_type_2_message|Col3|Col4|in|
|---|---|---|---|---|
|**`cornucopia_std::message_decoding`**|**`cornucopia_std::message_decoding`**|returns a boolean|~~**`success`**~~|~~**`success`**~~|



the decoding was successful, which provides limited insight into the nature of any failure. Instead,


returning specific error codes will significantly improve the error handling and debugging process.





|cts eth_contributors eth_contributors and c c MAX_CONTRIBUTORS_LENGTH MAX_CONTRIBUTORS_LENGTH|Col2|Col3|
|---|---|---|
|**`MAX_CONTRIBUTORS_LENGTH`**|**`MAX_CONTRIBUTORS_LENGTH`**|**`MAX_CONTRIBUTORS_LENGTH`**|
|g in the previous|**`notify`**|flow|


decoding and should explicitly assert these conditions to prevent potential errors.


to paused states or mismatched vectors, the function returns zero as the second value (the dumped


4. The resource account sweep should include a defined mechanism to cancel the sweep proposal if


needed.


**Remediation**


Implement the above-mentioned suggestions.


© 2025 Otter Audits LLC. All Rights Reserved. 27 / 38


Canopy Audit 05 - General Findings


**Code** **Clarity** OS-CPY-SUG-08


**Description**

|satay_deployer::create_internal|Col2|Col3|
|---|---|---|
|internally by|**`create`**|.|



_>__ _deployers/single-asset/sources/concrete/satay_deployer.move_ rust

```
     public fun create_internal(creator: &signer, vault_address: address):
```

_�→_ `Object<SingleAssetBaseDeployer>` `{`
```
          [...]
     }

```

an Ethereum address, which is conventionally 20 bytes long. However, in this function, the parameter


actually holds a 32-byte deployer address. To improve clarity, change the parameter name to clearly


reflect its purpose.


_>__ _deployers/single-asset/sources/base/single_asset_base_deployer.move_ rust

```
     /// Looks up a deployer object by its 32-byte address
     /// @return Option<Object<SingleAssetBaseDeployer>> - The deployer object if found
     public fun get_deployer_from_32_bytes(eth_bytes: vector<u8>):
```

_�→_ `Option<Object<SingleAssetBaseDeployer>>` `acquires` `GlobalConfig` `{`
```
       let global_config = borrow_global<GlobalConfig>(@cornucopia_single_deployers);
       if (table::contains(&global_config.deployer_map, eth_bytes)) {
          option::some(*table::borrow(&global_config.deployer_map, eth_bytes))
       } else {
          option::none()
       }
     }

|The way|configure_move_claim_address|and|
|---|---|---|
|**`configure_move_claim_address_for_deployer`**|**`configure_move_claim_address_for_deployer`**|**`configure_move_claim_address_for_deployer`**|


```

indistinguishable from failure, as they silently return when specific conditions are not met. This may


result in unnoticed failures and unexpected behaviors. Explicit error returns should be implemented


to enhance transparency and facilitate debugging.


© 2025 Otter Audits LLC. All Rights Reserved. 28 / 38


Canopy Audit 05 - General Findings


To ensure proper logging of global state changes, all significant state-changing operations should


emit events.


**Remediation**


Ensure proper error handling and emit events to log state changes for improved transparency and facilitate


debugging.


© 2025 Otter Audits LLC. All Rights Reserved. 29 / 38


Canopy Audit 05 - General Findings


**Documentation** **Enhancement** OS-CPY-SUG-09


**Description**


_proposal”_, however, the function has no ability to overwrite an existing proposal. Similarly, for


_claim_ _method_ _that_ _allows_ _a_ _Movement_ _address_ _that_ _was_ _configured_ _via_ _LayerZero”_, but there is no


first method anymore. Rectify the natspec to reflect the correct information.


_>__ _deployers/single-asset/sources/concrete/satay_deployer.move_ rust

```
     /// Proposes an emergency withdrawal of funds
     /// @param owner - Signer proving caller is the owner
     /// @param deployer_obj - The deployer object
     /// @param asset - Asset to withdraw
     /// @param recipient - Address to receive the withdrawn funds
     /// @param amount - Amount to withdraw (None means withdraw all available)
     ///
     /// @notice Creates or overwrites existing proposal
     public entry fun propose_emergency_withdraw([...]) acquires SingleAssetBaseDeployer
```

_�→_ `{[...]}`

|t for|single_asset_base_deployer::notify_funds|
|---|---|
|**`skip_balance_check`**|**`skip_balance_check`**|



and maintainability.


_>__ _deployers/single-asset/sources/base/single_asset_base_deployer.move_ rust

```
     /// @param base_deployer_obj_address_bytes - 32-byte representation of deployer object
```

_�→_ _`address`_
```
     /// @param eth_contributors - Vector of contributor Ethereum addresses as vector<u8>
     /// @param contribution_amounts - Vector of contribution amounts corresponding to
```

_�→_ _`eth_addresses`_
```
     [...]
     /// @dev The message payload is encoded on Ethereum using solidity abi.encode with format:
     /// (bytes32 base_deployer_obj_address, address[] eth_contributors, uint64[]
```

_�→_ _`contribution_amounts)`_
```
     public(friend) fun notify_funds(
       base_deployer_obj_address_bytes: vector<u8>,
       eth_contributors: vector<vector<u8>>,
       contribution_amounts: vector<u64>,
       skip_balance_check: bool
     ): u64 acquires GlobalConfig, SingleAssetBaseDeployer {[...]}

```

© 2025 Otter Audits LLC. All Rights Reserved. 30 / 38


Canopy Audit 05 - General Findings


3. [PR#30](https://github.com/Canopyxyz/cornucopia-move/pull/30) does not include the updated default timelock durations outlined in the scoping docu

ment. These changes should be implemented to ensure integrity between the codebase and the


documentation.


**Remediation**


ensure consistency between the codebase.


© 2025 Otter Audits LLC. All Rights Reserved. 31 / 38


Canopy Audit 05 - General Findings


**Code** **Redundancy** OS-CPY-SUG-10


**Description**


1. Across the codebase, there are repeated assertion checks to verify whether the deployment has


repeated checks clutter the code and thus, extracting this logic into a separate helper function will


reduce code duplication.


_>__ _deployers/single-asset/sources/base/single_asset_base_deployer.move_ rust

```
     public entry fun manage_timelocked_lock_duration([...]) acquires SingleAssetBaseDeployer {
       [...]
       if (deployer_ref.first_deployment_timestamp != 0) { // only check if deployment has
```

_�→_ _`started`_
```
          assert!(
            current_time < deployer_ref.first_deployment_timestamp +
```

_�→_ `timelocked::get_value(&deployer_ref.timelocked_lock_duration),`
```
            E_LOCK_DURATION_PASSED
          );
       };
       [...]
     }

```

twice for different values, once to check if it is less than 204 and again to check if it is less than


140. Remove the redundant checks and ensure proper validation of message length with the correct


value.


_>__ _packages/std/sources/libs/message_decoding.move_ rust

```
     public fun safe_decode_type_2_message(message: &vector<u8>): (bool, vector<u8>,
```

_�→_ `vector<vector<u8>>,` `vector<u64>)` `{`
```
       // Check minimum length for LayerZero metadata (76 bytes) + fixed fields (32 + 32 + 32
```

_�→_ _`+`_ _`32`_ _`=`_ _`128`_ _`bytes)`_
```
       if (vector::length(message) < 204) {
          return (false, vector::empty(), vector::empty(), vector::empty())
       };

       // Extract base_deployer_bytes using slice (76 + 32 = 108 for start, 76 + 64 = 140 for
```

_�→_ _`end)`_
```
       if (140 > vector::length(message)) {
          return (false, vector::empty(), vector::empty(), vector::empty())
       };
       [...]
     }

```

© 2025 Otter Audits LLC. All Rights Reserved. 32 / 38


Canopy Audit 05 - General Findings

|unnotified_balance_1|), it is|
|---|---|
|**`dual_asset_base_deployer`**|**`dual_asset_base_deployer`**|



_>__ _deployers/dual-asset/sources/base/dual_asset_base_deployer.move_ rust

```
     fun dump_unnotified_balances(
       [...]
       unnotified_balance_0: u64,
       unnotified_balance_1: u64
     ): (u64, u64) {
       let dumped_amount_0 = 0u64;
       let dumped_amount_1 = 0u64;
       if (unnotified_balance_0 > 0) {
            dump_funds_to_asset_dump(deployer_ref, global_config,
```

_�→_ `deployer_ref.asset_0,unnotified_balance_0);`
```
          dumped_amount_0 = unnotified_balance_0;
       };
       if (unnotified_balance_1 > 0) {
            dump_funds_to_asset_dump(deployer_ref, global_config,
```

_�→_ `deployer_ref.asset_1,unnotified_balance_1);`
```
          dumped_amount_1 = unnotified_balance_1;
       };
       (dumped_amount_0, dumped_amount_1)
     }

```

4. In **`deploy_funds_fa::test_production_deployer_deploy_none`**, the first assertion in the


deployer’s final state verification is redundant and can be removed, as the subsequent assertion


performs an equivalent check.


_>__ _single-asset/tests/integration/satay/entry_functions/deploy_funds_fa.move_ rust

```
     #[test(aptos_framework = @aptos_framework, governance = @satay, account = @DEV_ADDR)]
     fun test_production_deployer_deploy_none(account: &signer) {
       satay_deployer_helpers::setup();
       [...]
       // Verify deployer's final state
       assert!(single_asset_base_deployer::last_base_balance(deployer) == 0, 0); // All base
```

_�→_ _`claimed`_
```
       assert!(primary_fungible_store::balance(deployer_addr, base_asset) == 0, 0);
       [...]
     }

```

© 2025 Otter Audits LLC. All Rights Reserved. 33 / 38


Canopy Audit 05 - General Findings


**Remediation**


Remove the redundant code instances.


© 2025 Otter Audits LLC. All Rights Reserved. 34 / 38


Canopy Audit 05 - General Findings


**Unutilized** **Code** OS-CPY-SUG-11


**Description**

|In|process_claim|Col3|
|---|---|---|
|**`table::upsert`**|**`table::upsert`**|is|



_>__ _deployers/dual-asset/sources/base/dual_asset_base_deployer.move_ rust

```
     /// View struct for claimable amounts including vesting details
     struct ClaimableAmounts has copy, drop {
       [...]
       next_vest_amount: u64,
       next_vest_timestamp: u64,
       [...]
     }

|d86, both|dump_unnotified_balances|Col3|
|---|---|---|
|**`dual_asset_base_deployer`**|**`dual_asset_base_deployer`**|and may b|


```

unutilized, and many functions in the extensions packages are non-functional, as their referenced


6. The codebase contains several unutilized error codes and wrong or outdated comments that obscure


the code, hindering maintenance and development efficiency. Remove such dead code to streamline


the codebase and ensure comments are accurate.


© 2025 Otter Audits LLC. All Rights Reserved. 35 / 38


Canopy Audit 05 - General Findings


**Remediation**


Remove any unutilized code.


© 2025 Otter Audits LLC. All Rights Reserved. 36 / 38


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


© 2025 Otter Audits LLC. All Rights Reserved. 37 / 38


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


© 2025 Otter Audits LLC. All Rights Reserved. 38 / 38


