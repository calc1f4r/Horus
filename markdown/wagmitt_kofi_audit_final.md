# **Kofi Finance**

Security Assessment


May 10th, 2025 - Prepared by OtterSec


Andreas Mantzoutas [andreas@osec.io](mailto:andreas@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


**Scope** **3**


**Findings** **4**


**Vulnerabilities** **5**


OS-KOF-ADV-00 | Failure to Distribute Staking Rewards 7


OS-KOF-ADV-01 | kAPT Double Minting 8


OS-KOF-ADV-02 | Rounding Error in Delegation Pool 9


OS-KOF-ADV-03 | Abort on Temporary Imbalance During Epoch Transition 10


OS-KOF-ADV-04 | Inconsistent Scaling in Conversion Rate Calculation 11


OS-KOF-ADV-05 | Unnecessary Assertion Causes Protocol Lockup 12


OS-KOF-ADV-06 | Risk of Overpayment 13


OS-KOF-ADV-07 | Protocol Insolvency via Validator Removal 14


OS-KOF-ADV-08 | Buffer Vault Drainage Due to Unaccounted Staking Fees 15


OS-KOF-ADV-09 | Faulty Withdrawal Logic 17


**General** **Findings** **19**


OS-KOF-SUG-00 | Code Maturity 20


**Appendices**


**Vulnerability** **Rating** **Scale** **22**


**Procedure** **23**


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 23


**01** **—** **Executive** **Summary**

## Overview


conducted between April 17th and May 5th, 2025. For more information on our auditing methodology,


refer to Appendix B.

## Key Findings


We produced 11 findings throughout this audit engagement.


In particular, we identified multiple high-risk vulnerabilities affecting staking reward integrity and supply


minting and eventual depegging as the kAPT supply surpasses the actual staked APT (OS-KOF-ADV-01).


Moreover, a medium-severity issue arises from rounding errors in APT-to-share conversions within the


(OS-KOF-ADV-02).


We also recommended codebase modifications to eliminate redundant code, avoid hardcoded values, and


improve overall efficiency, while ensuring adherence to coding best practices (OS-KOF-SUG-00).


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 23


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/wagmitt/kofi-finance-](https://github.com/wagmitt/kofi-finance-contracts)


[contracts.](https://github.com/wagmitt/kofi-finance-contracts) This audit was performed against [75ed16e.](https://github.com/wagmitt/kofi-finance-contracts/commit/75ed16e512fa2c98f47c3d81254d11ec25b49002)


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**



kofi-finance

contracts



A liquid staking protocol for Aptos, allowing users to stake APT tokens


and receive liquid staking derivatives (kAPT and stkAPT).



© 2025 Otter Audits LLC. All Rights Reserved. 3 / 23


**03** **—** **Findings**


Overall, we reported 11 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.



© 2025 Otter Audits LLC. All Rights Reserved. 4 / 23


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


© 2025 Otter Audits LLC. All Rights Reserved. 5 / 23


Kofi Finance Audit 04 - Vulnerabilities



|rewards_manager::update_rewards|Col2|Col3|
|---|---|---|
|date the|**`virtual_balance`**|, causing|


wards to become locked.


not accounting for minting fees, leading to double

may create discrepancies in stake amounts during


delegation and undelegation, resulting in potential


value loss for the pool.


ing operations to fail during temporary imbalances


scaling in its conversion logic, leading to potential

|The|ratio <= RATIO_MAX|Col3|
|---|---|---|
|**`math::ratio`**|**`math::ratio`**|can<br>permanen|



liquidity if the ratio naturally grows beyond the limit.


even if the calculated amount is 0, leading to protocol


overpayment during unstaking.



OS-KOF-ADV-00


OS-KOF-ADV-01


OS-KOF-ADV-02


OS-KOF-ADV-03


OS-KOF-ADV-04


OS-KOF-ADV-05


OS-KOF-ADV-06


OS-KOF-ADV-07


OS-KOF-ADV-08


OS-KOF-ADV-09





Removing validators may result in irretrievable stake,


risking temporary protocol insolvency.


Unaccounted staking fees during delegation cause





the buffer vault to burn more than it mints, gradually


depleting its balance and risking protocol stability.

|delegation_manager::withdraw_stake|Col2|Col3|
|---|---|---|
|sumes that|**`withdrawn_amount`**|is always|



than the minimum threshold, risking unexpected


aborts if this condition is not met.



© 2025 Otter Audits LLC. All Rights Reserved. 6 / 23


Kofi Finance Audit 04 - Vulnerabilities


**Description**









rewards, preventing distribution to stakers.


**Remediation**


**Patch**


Fixed in [e9c9c89.](https://github.com/wagmitt/kofi-finance-contracts/commit/e9c9c8996e7dbec0e4871dc9db41c0b6ee7d6bd7)


© 2025 Otter Audits LLC. All Rights Reserved. 7 / 23


Kofi Finance Audit 04 - Vulnerabilities


**Description**









However, this calculation does not account for minting fees. When stake is added to a delegation pool,


This fee is temporarily subtracted from the delegator’s active stake and is refunded in the next epoch.


The protocol tracks this fee separately and allows the admin to collect it asynchronously. Despite this,


**Remediation**


**Patch**


Fixed in [74d73ff.](https://github.com/wagmitt/kofi-finance-contracts/commit/74d73ffee56ef63b987dee843f18e987946bfbee)


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 23


Kofi Finance Audit 04 - Vulnerabilities


**Description**


unlocking stake (undelegating) from a delegation pool, the amount unlocked may be slightly less than the


calculated number of shares, but due to rounding during the conversion, the actual stake increase may


effectively staked.


It is essential that this rounding error is covered by the user and not the protocol, otherwise, the pool


gradually loses value. Currently, neither delegation nor undelegation accounts for this error. When adding


during undelegation, users withdraw the full requested amount, even if the actual decrease in the pending


inactive stake is less, resulting in the pool losing value. This imbalance may even create a scenario where


the total requested withdrawals exceed the available pending inactive and inactive stake, rendering full


withdrawals impossible for some users.


**Remediation**


operation, and act only based on the actual changes.


**Patch**


Fixed in [eded117](https://github.com/wagmitt/kofi-finance-contracts/commit/eded117bf8ad64aaf639d60dc544b74df29f1300) and [3d2bd6d.](https://github.com/wagmitt/kofi-finance-contracts/commit/3d2bd6d8871b48671b37e4e4b90781be251e7397)


© 2025 Otter Audits LLC. All Rights Reserved. 9 / 23


Kofi Finance Audit 04 - Vulnerabilities


**Description**


. However, this strict check fails to account for a valid edge case involving epoch timing. When the


admin to withdraw. However, the corresponding stake does not become active until the next epoch. If the









**Remediation**


the safe continuation of operations and preventing false failures during temporary imbalances.


**Patch**


Fixed in [246b120.](https://github.com/wagmitt/kofi-finance-contracts/commit/246b12068861c7e4ef1a594315c636c3898f7c2b)


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 23


Kofi Finance Audit 04 - Vulnerabilities


**Description**


prevent overflows, the implementation uses two different branches depending on whether the locked









The issue arises because these branches apply different scaling factors. The _if_ branch scales the amount


rendering the branch distinction unnecessary.


**Remediation**


**Patch**


Fixed in [5f606e6.](https://github.com/wagmitt/kofi-finance-contracts/commit/5f606e61392a16f50d02995d538570c1d5000db8)


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 23


Kofi Finance Audit 04 - Vulnerabilities


**Description**


between the underlying asset and the derivative token naturally increases over time and is not expected


protocol to halt. This failure would prevent any further staking or unstaking operations, effectively locking


all liquidity and breaking the protocol’s functionality indefinitely.









**Remediation**


Remove the assertion.


**Patch**


Fixed in [3cc1271.](https://github.com/wagmitt/kofi-finance-contracts/commit/3cc1271c3dfa15ad260ff2dbcf201afecdaa1cc5)


© 2025 Otter Audits LLC. All Rights Reserved. 12 / 23


Kofi Finance Audit 04 - Vulnerabilities


**Description**


unstaking amount and the current conversion rate. If the computed share amount is 0, while the unstaking


amount is greater than 0, the protocol sets the share amount to 1 to prevent the user from burning tokens


without receiving anything in return. However, this logic introduces an overpayment vulnerability, as the


user receives more value than they originally unstaked.









**Remediation**


Replace the condition with an assertion to prevent users from losing their funds while also avoiding


overpayment during the unstaking process.


**Patch**


Fixed in [63d3a44.](https://github.com/wagmitt/kofi-finance-contracts/commit/63d3a4406fbb2dcce8270018fbaf67bf81e1aad0)


© 2025 Otter Audits LLC. All Rights Reserved. 13 / 23


Kofi Finance Audit 04 - Vulnerabilities


**Description**


their stake allocations. However, it is possible to completely remove certain validators, yet there is no


mechanism to manage their existing stakes or safely unstake the full amount when this occurs. As a result,


re-adding the affected validators.









**Remediation**


to allow only additions or updates, preventing unhandled stakes from becoming irretrievable.


**Patch**


Fixed in [1ff0089.](https://github.com/wagmitt/kofi-finance-contracts/commit/1ff00899f44308ade6631b17556167f0c2c443e2)


© 2025 Otter Audits LLC. All Rights Reserved. 14 / 23


Kofi Finance Audit 04 - Vulnerabilities


**Description**


The protocol introduces a buffer vault that holds initialization funds to ensure validators maintain the


required levels of active and pending inactive stakes, as mandated by protocol parameters. To achieve

this, **`delegation_manager::ensure_minimum_amounts_from_buffer`** enforces that the delegation


pool’s stakes always match the required amounts. For pending inactive stakes, if the balance falls below


levels.


_>__ _delegation_manager.move_ rust

```
  public(friend) fun ensure_minimum_amounts_from_buffer(
    pool_address: address
  ) {
    ...
    if (pending_inactive < min_pending_inactive) {
      ...
      delegation_pool::add_stake(&vault_signer, pool_address, amount_needed);
      let add_stake_fee =
         delegation_pool::get_add_stake_fee(pool_address, amount_needed);

      kAPT_coin::mint(
         signer::address_of(&buffer_signer), amount_needed - add_stake_fee
      );

      delegation_pool::unlock(&vault_signer, pool_address, amount_needed);
      kAPT_coin::burn(&buffer_signer, amount_needed);
      ...
    };
  }

```

amount of APT actually minted to the buffer, while the burned kAPT remains equivalent to the originally


draining its balance. Eventually, this depletion leads to unexpected aborts, which subsequently block


withdrawals from the protocol.


**Remediation**


for one epoch, remove the kAPT minting and burning operations during the buffer adjustment process.


© 2025 Otter Audits LLC. All Rights Reserved. 15 / 23


Kofi Finance Audit 04 - Vulnerabilities


**Patch**


Fixed in [c677934.](https://github.com/wagmitt/kofi-finance-contracts/commit/c677934e59901863bb94e315ff979e39be514951)


© 2025 Otter Audits LLC. All Rights Reserved. 16 / 23


Kofi Finance Audit 04 - Vulnerabilities


**Description**


idators. During this process, the amount unstaked from each validator is split into two parts: the


unlocked vault for user withdrawals.









|mes that|withdraw_amount|Col3|
|---|---|---|
|**`get_min_pending_inactive`**|**`get_min_pending_inactive`**|**`get_min_pending_inactive`**|


to protocol parameter changes or rounding errors during delegation, the subtraction fails, resulting in


unexpected aborts and potentially blocking user withdrawals.


© 2025 Otter Audits LLC. All Rights Reserved. 17 / 23


Kofi Finance Audit 04 - Vulnerabilities


**Remediation**


Include a condition to transfer the full withdrawn amount to the buffer if it is less than


**Patch**


Fixed in [212a282.](https://github.com/wagmitt/kofi-finance-contracts/commit/212a28211e63acb858c4da5cbf6f6ce6c713f8d6)


© 2025 Otter Audits LLC. All Rights Reserved. 18 / 23


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.


Suggestions regarding the removal of redundant and unutilized code and im


OS-KOF-SUG-00



proving the overall efficiency of the codebase, ensuring adherence to coding


best practices.



© 2025 Otter Audits LLC. All Rights Reserved. 19 / 23


Kofi Finance Audit 05 - General Findings


**Code** **Maturity** OS-KOF-SUG-00


**Description**


structure field by field. A direct reference to the global resource is sufficient. Also,


which is redundant and may be removed.


_>__ _config.move_ rust

```
     fun get_global_config(): GlobalConfig acquires GlobalConfig {
       let global_config = borrow_global<GlobalConfig>(@kofi);
       GlobalConfig {
          gateway_config: global_config.gateway_config,
          ...
          package_metadata: global_config.package_metadata
       }
     }

     public fun get_validator_addresses(): vector<address> acquires GlobalConfig {
       *&borrow_global<GlobalConfig>(@kofi).validator_config.addresses
     }

```

during contract initialization, limiting deployment flexibility across environments. Avoid hardcoding


_>__ _config.move_ rust

```
     fun init_module(admin: &signer) {
       // initialize access control
       access_control::initialize_owner(
          admin,
          @0xc0de36135d4eda6ba6cada45fdab868cc5dde0bac1c6ed798af87a631e5a825f
       );
       ...
     }

```

code clarity and eliminate dead code. Similarly, unutilized variables highlighted during compilation


should be removed.


© 2025 Otter Audits LLC. All Rights Reserved. 20 / 23


Kofi Finance Audit 05 - General Findings


_>__ _withdraw_manager.move_ rust

```
     let withdraw_fees = kapt_amount * config::get_withdrawal_fee() / 10000;

```

**Remediation**


Implement the above-mentioned suggestions.


**Patch**


1. Fixed in [35d383b.](https://github.com/wagmitt/kofi-finance-contracts/commit/35d383b1dc66a04bdcdaf4499934b3b45a0b0bba)


2. Fixed in [b3515c2.](https://github.com/wagmitt/kofi-finance-contracts/commit/b3515c28850e1b8ce80b4b6a1da99743d380ee1b)


3. Fixed in [f88f6ef.](https://github.com/wagmitt/kofi-finance-contracts/commit/f88f6ef91d0e7c5a56fa606a7122a89578bbf5c6)


4. Fixed in [7060e40.](https://github.com/wagmitt/kofi-finance-contracts/commit/7060e4000bcac8b7b14e841a6ce75f0e28b806ae)


© 2025 Otter Audits LLC. All Rights Reserved. 21 / 23


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


© 2025 Otter Audits LLC. All Rights Reserved. 22 / 23


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


© 2025 Otter Audits LLC. All Rights Reserved. 23 / 23


