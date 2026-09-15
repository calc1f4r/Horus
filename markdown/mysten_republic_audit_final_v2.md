# **Mysten Republic**

Security Assessment


October 28th, 2024 - Prepared by OtterSec


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


OS-RPL-ADV-00 | Repeated Invocation Resulting in Excessive Claims 6


OS-RPL-ADV-01 | Risk of Compromising Snapshot Integrity 7


OS-RPL-ADV-02 | Possible Overflow Due to Exceeding the Type Limit 8


OS-RPL-ADV-03 | Failure to Update Default Group 9


**General** **Findings** **10**


OS-RPL-SUG-00 | Unauthorized Privileges Due to Group ID Reassignment 11


OS-RPL-SUG-01 | Code Refactoring 12


OS-RPL-SUG-02 | Code Maturity 13


**Appendices**


**Vulnerability** **Rating** **Scale** **15**


**Procedure** **16**


© 2024 Otter Audits LLC. All Rights Reserved. 1 / 16


**01** **—** **Executive** **Summary**

## Overview


October 11th and October 21st, 2024. A follow-up review was performed between April 7th and April


13th, 2025. and For more information on our auditing methodology, refer to Appendix B.

## Key Findings


We produced 7 findings throughout this audit engagement.


In particular, we identified a vulnerability in the claim functionality concerning a lack of a check to ensure


that the cumulative amount claimed, including previous claims, does not exceed the total unlocked tokens.


This enables users to repeatedly claim more than the intended unlocked balance (OS-RPL-ADV-00).


Additionally, during the snapshot process, if tokens included in the snapshot are combined with those not


part of it, the integrity of the snapshot is compromised (OS-RPL-ADV-01). Furthermore, we highlighted


the possibility of an overflow in multiplication and division operations if the values exceed the maximum


We also made a recommendation to modify the codebase for enhanced functionality, efficiency, and


maintainability (OS-RPL-SUG-01) and suggested ensuring adherence to coding best practices (OS

RPL-SUG-02).


© 2024 Otter Audits LLC. All Rights Reserved. 2 / 16


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/MystenLabs/security-token.](https://github.com/MystenLabs/security-token)


This audit was performed against [ff7d0a0.](https://github.com/MystenLabs/security-token/commit/ff7d0a083fa9211d4b4d34a454a3558c687ad0b1) A follow-up review was performed against [13e91eb.](https://github.com/MystenLabs/security-token/commit/13e91eb1707e8792565af034d0fe84aba41dc1e8)


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**


A treasury management system that enforces strict access control and
republic

permissions through roles and abilities, within the Sui environment.


© 2024 Otter Audits LLC. All Rights Reserved. 3 / 16


**03** **—** **Findings**


Overall, we reported 7 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.


© 2024 Otter Audits LLC. All Rights Reserved. 4 / 16


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


the cumulative amount claimed, includ


ing previous claims, does not exceed the


total unlocked tokens, allowing users to


repeatedly claim more than the intended


unlocked balance.


During the snapshot process, if tokens in

cluded in the snapshot are combined with


those not part of it, the integrity of the


snapshot is compromised.

|calculate_available_dividends|Col2|Col3|
|---|---|---|
|d|**`calculate_unlocked`**|, the multipli-|



cation and division operations may over

flow if the values exceed the maximum



OS-RPL-ADV-00


OS-RPL-ADV-01


OS-RPL-ADV-02


OS-RPL-ADV-03




|remove_address_from_group|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|the|**`address_info`**|for|**`addr`**|**`addr`**|


|DEFAULT_GROUP<br>it to the, b<br>DEFAULT_GROUP<br>to update the|DEFAULT_GROUP|Col3|Col4|, b|
|---|---|---|---|---|
|it<br>to<br>the<br>**`DEFAULT_GROUP`**<br>,<br>b<br>to update the<br>**`DEFAULT_GROUP`**|**`DEFAULT_GROUP`**|**`DEFAULT_GROUP`**|**`DEFAULT_GROUP`**|**`DEFAULT_GROUP`**|
|**`Group.holders`**|**`Group.holders`**|**`Group.holders`**|.|.|



© 2024 Otter Audits LLC. All Rights Reserved. 5 / 16


Mysten Republic Audit 04 - Vulnerabilities


**Description**


on the unlocked tokens. Without this additional check, a user may exploit the function to repeatedly claim


the maximum allowable unlocked balance, potentially exceeding the actual unlocked amount over multiple


the current timestamp, based on the timelock’s release schedule.


_>__ _treasury_abilities/timelock/timelock.move_ rust

```
  public fun claim<T>(
    self: &mut Timelock<T>,
    amount: Option<u64>,
    clock: &Clock,
    ctx: &mut TxContext,
  ): SplitRequest<T> {
    [...]
    let amount = amount.destroy_or!(unlocked_tokens);
    assert!(amount <= unlocked_tokens, ENotEnoughBalanceUnlocked);
    self.tokens_transferred = self.tokens_transferred + amount;
    let coin = self.left_balance.split(amount).into_coin(ctx);
    let (token, request) = shared_token::from_coin(coin, ctx);
    token.share();
  }

```

However, each call to claim only checks that the currently requested amount is within the currently unlocked


increments by the claimed amount with each call, there is no check to ensure that

|amount + self.tokens_transferred|Col2|
|---|---|
|oversight allows the owner to call|**`claim`**|



maximum unlocked amount each time without accounting for previously claimed tokens.


**Remediation**


Verify that the cumulative amount claimed does not exceed the total unlocked tokens

( **`amount`** **`+`** **`self.tokens_transferred`** **`<=`** **`unlocked_tokens`** ).


**Patch**


Resolved in [fe96359.](https://github.com/MystenLabs/security-token/commit/fe9635990cf67e5c81f0632ec4e41c4bb9042564)


© 2024 Otter Audits LLC. All Rights Reserved. 6 / 16


Mysten Republic Audit 04 - Vulnerabilities


**Description**


The vulnerability concerns the integrity of the snapshot process. A successful snapshot relies on accurately


capturing the total supply of tokens and distinguishing between those that are counted (unlocked) and


the balances and total supply of tokens mid-snapshot. If tokens that are part of the snapshot join with


**Remediation**


**Patch**


Resolved in [f6fa43b.](https://github.com/MystenLabs/security-token/commit/f6fa43b25d87cc2de6d9221860a51d88140cde3b)


© 2024 Otter Audits LLC. All Rights Reserved. 7 / 16


Mysten Republic Audit 04 - Vulnerabilities


**Description**


_>__ _treasury_abilities/pause/dividends.move_ rust

```
  public fun calculate_available_dividends<T, U>(
    self: &Dividends<U>,
    snapshot: &Snapshot<T>,
    addr: address,
  ): u64 {
    [...]
    // prettier-ignore
    let addr_total_dividends =
      (self.total_funds * snapshot.address_balance(addr)) / unlocked_supply_t;
    addr_total_dividends - already_claimed
  }

|shecdule_config::calculate_unlocked|Col2|
|---|---|
|**`u64`**|values, which may result in an overflow|


```

**Remediation**


**Patch**


Resolved in [a393844.](https://github.com/MystenLabs/security-token/commit/a393844f9dd058c52d43d78944c3d571ca9f7bc)


© 2024 Otter Audits LLC. All Rights Reserved. 8 / 16


Mysten Republic Audit 04 - Vulnerabilities


**Description**


intends to reassign the address to the default group.


_>__ _rules/group_holder_config/group_holder_config.move_ rust

```
  /// Will set the address to the DEFAULT_GROUP.
  public fun remove_address_from_group<T>(
    policy: &mut TokenPolicy<T>,
    cap: &TokenPolicyCap<T>,
    addr: address,
  ) {
    [...]
    // Remove address from old group
    let old_group = address_info.group_id;
    let group = &mut config.groups[&old_group];
    group.remove_holder_address(address_info.holder_id, addr);
    // Update addresses Table
    address_info.group_id = DEFAULT_GROUP;
    // If the below assertion fails, it means that the state of the group-holderconfig is
```

_�→_ _`corrupted.`_
```
    let holder_addresses = config.holders[address_info.holder_id];
    assert!(holder_addresses.contains(&addr), EImplementationError);
  }

```

This will result in an inconsistency, as the address will appear to belong to the default group based on

|address_info|,|
|---|---|
|**`config.groups`**|**`config.groups`**|



**Remediation**


**Patch**


Resolved in [f960290.](https://github.com/MystenLabs/security-token/commit/f960290ec7ee2f221854eefc15e6d07c4dcdacf1)


© 2024 Otter Audits LLC. All Rights Reserved. 9 / 16


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.


An admin may arbitrarily set group IDs, allowing for a new group to take the



OS-RPL-SUG-00


OS-RPL-SUG-01


OS-RPL-SUG-02



place of a removed group in an allowed group pair, resulting in access to


unauthorized privileges.


Recommendation for modifying the codebase for improved functionality,


efficiency, and maintainability.


Suggestions regarding inconsistencies in the codebase and ensuring ad

herence to coding best practices.



© 2024 Otter Audits LLC. All Rights Reserved. 10 / 16


Mysten Republic Audit 05 - General Findings


**Unauthorized** **Privileges** **Due** **to** **Group** **ID** **Reassignment** OS-RPL-SUG-00


**Description**


In the current implementation, the management of group IDs is insufficiently controlled, especially regarding


removed, the ID associated with that group becomes available for re-utilization.


_>__ _treasury_abilities/pause/dividends.move_ rust

```
    public fun add_group<T>(
      auth: &Auth<T>,
      policy: &mut TokenPolicy<T>,
      group_id: u64,
      group_name: String,
      max_holders: Option<u64>,
      ctx: &mut TxContext,
    ) {
      assert!(auth.has_ability<T, EditGroupsAbility>(), ENotAllowedToEditGroups);
      policy.add_group(auth.policy_cap(), group_id, group_name, max_holders, ctx);
    }

```

relies on the assumption that group IDs correspond to trusted entities.


By allowing a new group to adopt the ID of a previously removed group, the system undermines its own


trust model. Any operations relying on group pairs may fail to enforce the intended security boundaries.


**Remediation**


Ensure that once a group ID is removed, it is not possible to immediately create another group with a


similar index.


© 2024 Otter Audits LLC. All Rights Reserved. 11 / 16


Mysten Republic Audit 05 - General Findings


**Code** **Refactoring** OS-RPL-SUG-01


**Description**


modules to improve observability.


any specified group, instead of just the default group.


_>__ _sources/rules/group_holder_config/group_holder_config.move_ rust

```
     fun add_holder_address_internal<T>(
       self: &mut Config,
       holder_id: u64,
       addr: address,
       group_id: u64,
     ) {
       event::emit(HolderAddressAdded<T> { holder_id: holder_id, addr });
       self.holders[holder_id].insert(addr);
       self.addresses.add(addr, AddressInfo { holder_id, group_id });
       self.groups[&default_group()].add_holder_address(holder_id, addr);
     }

```

Thus, it would be appropriate to keep only one of them.


**Remediation**


Implement the above-mentioned refactors.


**Patch**


1. Issue #1 resolved in [01504c5.](https://github.com/MystenLabs/security-token/commit/01504c5b203d19310de2d18ff8915d1386ac2422)


2. Issue #2 resolved in [b3a4edf.](https://github.com/MystenLabs/security-token/commit/b3a4edfcef6cc24014aaa9a32db3d42cc751f256)


3. Issue #3 resolved in [f960290.](https://github.com/MystenLabs/security-token/commit/f960290ec7ee2f221854eefc15e6d07c4dcdacf1)


© 2024 Otter Audits LLC. All Rights Reserved. 12 / 16


Mysten Republic Audit 05 - General Findings


**Code** **Maturity** OS-RPL-SUG-02


**Description**


claimed, as most dividend calculations involve proportional distribution, which may result in small


leftover amounts due to rounding.

|In|freeze_rule::add|Col3|Col4|, wh|
|---|---|---|---|---|
|**`TokenPolicy`**|**`TokenPolicy`**|(in the|**`else`**|**`else`**|



point.


_>__ _sources/rules/freeze_rule.move_ rust

```
     public fun add<T>(
       policy: &mut TokenPolicy<T>,
       cap: &TokenPolicyCap<T>,
       action: String,
       frozen_addresses: vector<address>,
       ctx: &mut TxContext,
     ) {
       token::add_rule_for_action<T, FreezeRule>(policy, cap, action, ctx);
       if (policy.has_rule_config_with_type<T, FreezeRule, Config>()) {
          frozen_addresses.do!(|addr| freeze_address(policy, cap, addr, ctx));
       } else {
          token::add_rule_config(
            FreezeRule {},
            policy,
            cap,
            Config { frozen_addresses: vec_set::empty() },
            ctx,
          );
       };
     }

```

users with specific roles may cancel an ongoing snapshot. In particular, since the function resumes


paused treasury and token operations, proper access control is necessary to deter unauthorized


cancellation.


value ranges and ensures safe arithmetic operations.


© 2024 Otter Audits LLC. All Rights Reserved. 13 / 16


Mysten Republic Audit 05 - General Findings


**Remediation**


3. Implement access control to verify if the caller has the required role to cancel the snapshot.


**Patch**


1. Issue #1 resolved in [9980fe5.](https://github.com/MystenLabs/security-token/commit/9980fe5f94335c887c60dc6429b795a68ac9c24e)


2. Issue #2 resolved in [8011e96.](https://github.com/MystenLabs/security-token/commit/8011e969e51d660fa1d713279256b2155c170d74)


3. Issue #3 resolved in [f960290.](https://github.com/MystenLabs/security-token/commit/f960290ec7ee2f221854eefc15e6d07c4dcdacf1)


© 2024 Otter Audits LLC. All Rights Reserved. 14 / 16


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


© 2024 Otter Audits LLC. All Rights Reserved. 15 / 16


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


© 2024 Otter Audits LLC. All Rights Reserved. 16 / 16


