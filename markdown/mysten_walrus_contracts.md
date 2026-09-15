# **Mysten Walrus**

Security Assessment


March 3rd, 2025 - Prepared by OtterSec


Sangsoo Kang [sangsoo@osec.io](mailto:sangsoo@osec.io)


Michał Bochnak [embe221ed@osec.io](mailto:embe221ed@osec.io)


Nicholas R. Putra [nicholas@osec.io](mailto:nicholas@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **3**


Overview 3


Key Findings 3


**Scope** **4**


**Findings** **5**


**Vulnerabilities** **6**


OS-MSW-ADV-00 | Missing Activation Epoch Check in Join 8


OS-MSW-ADV-01 | Inconsistencies Due to Zero Share Amount Value 9


OS-MSW-ADV-02 | Abort via Large Node Capacity Value 10


OS-MSW-ADV-03 | Epoch Mismatch in Storage Reclamation 11


OS-MSW-ADV-04 | Division by Zero in Committee Selection 12


OS-MSW-ADV-05 | Exceeding Object Size Limit 13


OS-MSW-ADV-06 | Missing Commission Rate Check 14


OS-MSW-ADV-07 | Missing Check for Sequence Number 15


OS-MSW-ADV-08 | Utilization of Incorrect Commission Rate 16


OS-MSW-ADV-09 | Bypassing Stake Threshold Check 17


**General** **Findings** **18**


OS-MSW-SUG-00| Failure to Replace Inactive Node 19


OS-MSW-SUG-01| Missing Validation Logic 20


OS-MSW-SUG-02| Code Refactoring 22


OS-MSW-SUG-03| Code Maturity 23


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 26


Mysten Walrus Audit


**Appendices**



TABLE OF CONTENTS



**Vulnerability** **Rating** **Scale** **25**


**Procedure** **26**


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 26


**01** **—** **Executive** **Summary**

## Overview


conducted between January 21st and February 25th, 2025. For more information on our auditing


methodology, refer to Appendix B.

## Key Findings


We produced 14 findings during this audit engagement, all of which were successfully remediated in


accordance with our recommendations.


In particular, we identified several vulnerabilities. One involves the lack of an activation epoch check


when joining the StakedWal, which allows users to inflate their rewards(OS-MSW-ADV-00). Another


vulnerability occurs when the share amount is manipulated to be zero in the exchange rate, preventing


epoch changes and blocking StakedWal withdrawals(OS-MSW-ADV-01). Additionally, we discovered


multiple vulnerabilities that can disrupt epoch advancement, including division by zero, overflow, and


object size limits.


We also provided suggestions to address inconsistencies in the codebase and ensure adherence to


coding best practices (OS-MSW-SUG-03) and made recommendations regarding modifications to the


codebase for improved functionality, efficiency, and robustness (OS-MSW-SUG-02). Moreover, we


advised including additional safety checks within the codebase to improve security (OS-MSW-SUG-01).


© 2025 Otter Audits LLC. All Rights Reserved. 3 / 26


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/MystenLabs/walrus.](https://github.com/MystenLabs/walrus) This


audit was performed against commit [a45e012.](https://github.com/MystenLabs/walrus/commit/a45e0124f3c2ee5ae9b2934cae06bce2a9c0f3db )


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**


Walrus uses Sui smart contracts to manage storage, payments, and


governance, storing only metadata on-chain while keeping blob data


off-chain. Users purchase storage, assign a blob ID, and obtain avail


walrus-contracts



ability certificates, allowing storage nodes to handle and extend storage


as needed. At each storage epoch, storage nodes verify performance


and distribute payments, ensuring efficient and reliable decentralized


storage.



© 2025 Otter Audits LLC. All Rights Reserved. 4 / 26


**03** **—** **Findings**


Overall, we reported 14 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.



© 2025 Otter Audits LLC. All Rights Reserved. 5 / 26


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


Missing the activation epoch check when joining



incorrect reward calculations.


It is possible to manipulate the pool’s share

allows zero-share withdrawals currently, and


a denial of service scenario may occur due to


is share amount is zero.


A malicious user may inflate the node’s ca

pacity by setting an excessively large value for


and potentially resulting in epoch advancement


failures.


Splitting storage by epoch creates a new stor

age object, but the accounting system may in

correctly decrease storage reclamation for the


wrong epoch.


risks division by zero when calculating

|capacity_vote|Col2|
|---|---|
|count<br>(|**`weight`**|



stake.



OS-MSW-ADV-00


OS-MSW-ADV-01


OS-MSW-ADV-02


OS-MSW-ADV-03


OS-MSW-ADV-04





© 2025 Otter Audits LLC. All Rights Reserved. 6 / 26


Mysten Walrus Audit 04 - Vulnerabilities


Excessive length in



and blocking staker withdrawals by restricting


Failing to check whether the commission


rate is within the valid range can cause an


disrupt the epoch change.


The lack of validation for

|ending_checkpoint_sequence_num|Col2|
|---|---|
|**`certify_event_blob`**|can<br>caus|



matches between node-processed event blobs


and on-chain tracking.


dated commission rate for the current epoch


instead of the previous one.


allowing users to stake above the threshold to


enter the active set and then withdraw early to


reduce their stake below the minimum require

ment while still remaining in the set.



OS-MSW-ADV-05


OS-MSW-ADV-06


OS-MSW-ADV-07


OS-MSW-ADV-08


OS-MSW-ADV-09





© 2025 Otter Audits LLC. All Rights Reserved. 7 / 26


Mysten Walrus Audit 04 - Vulnerabilities


**Description**


activation epoch check is missing. Since the share amount is calculated based on the activation epoch,


this omission results in incorrect reward calculations, allowing an attacker to gain additional benefits.


_>__ _sources/staking/staked_wal.move_ rust

```
  public fun join(sw: &mut StakedWal, other: StakedWal) {
    assert!(sw.node_id == other.node_id, EMetadataMismatch);
    [...]

    // Withdrawing scenario - we no longer check that the activation epoch is
    // the same, as the staked WAL is in the process of withdrawing. Instead,
    // we make sure that the withdraw epoch is the same.
    assert!(sw.is_withdrawing() && other.is_withdrawing(), EMetadataMismatch);
    assert!(sw.withdraw_epoch() == other.withdraw_epoch(), EMetadataMismatch);

    let StakedWal { id, principal, .. } = other;
    sw.principal.join(principal);
    id.delete();
  }

```

**Remediation**


**Patch**


Fixed in [3396941.](https://github.com/MystenLabs/walrus/commit/33969413ce559f1aaa2c0666ccc18181117cb915)


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 26


Mysten Walrus Audit 04 - Vulnerabilities


**Description**

|staking_inner::request_withdraw_stake|Col2|Col3|
|---|---|---|
|a|**`share_amount`**|of zero.<br>This oversight may|



share-to-asset ratio by withdrawing a small principal or leaving it.

|exchange_rate::convert_to_wal_amount|Col2|Col3|Col4|,|
|---|---|---|---|---|
|division by|**`share_amount`**|to compute the|**`WAL`**|**`WAL`**|



and stake withdrawals.


_>__ _sources/staking/exchange_rate.move_ rust

```
  public(package) fun convert_to_wal_amount(exchange_rate: &PoolExchangeRate, amount: u64): u64 {
    match (exchange_rate) {
      PoolExchangeRate::Flat => amount,
      PoolExchangeRate::Variable { wal_amount, share_amount } => {
         let amount = (amount as u128);
         let res = (amount * *wal_amount) / *share_amount;
         res as u64
      },
    }
  }

```

**Remediation**


**Patch**


Fixed in [cc4aaaa.](https://github.com/MystenLabs/walrus/commit/cc4aaaae20c5d5e085d0dc9b72f05bf89d31d52a)


© 2025 Otter Audits LLC. All Rights Reserved. 9 / 26


Mysten Walrus Audit 04 - Vulnerabilities


**Description**


There is a potential flaw in how the vote calculations are handled in


_>__ _sources/staking/staking_inner.move_ rust

```
  /// Selects the committee for the next epoch.
  public(package) fun select_committee_and_calculate_votes(self: &mut StakingInnerV1) {
    [...]
    // Iterate over the next committee to do the following:
    // - store the next epoch public keys for the nodes
    // - calculate the votes for the next epoch parameters
    node_ids.length().do!(|idx| {
      [...]
      // Perform calculation of the votes.
      write_prices.insert(pool.write_price(), weight);
      storage_prices.insert(pool.storage_price(), weight);
      let capacity_vote = (pool.node_capacity() * (self.n_shards as u64)) / weight;
      capacity_votes.insert(capacity_vote, weight);
    });
    [...]
  }

```

**Remediation**


**Patch**


Fixed in [cc4aaaa.](https://github.com/MystenLabs/walrus/commit/cc4aaaae20c5d5e085d0dc9b72f05bf89d31d52a)


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 26


Mysten Walrus Audit 04 - Vulnerabilities


**Description**


mechanism for storage reclamation does not properly adjust to this split, resulting in inconsistencies when


wrong epoch.


**Remediation**


**Patch**


Fixed in [f9a7865.](https://github.comMystenLabs/walrus/commit/f9a786562c30587e579712e2048421b959be8d05)


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 26


Mysten Walrus Audit 04 - Vulnerabilities


**Description**

|staking_inner::select_committee_and_calculate_votes|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|lculating|**`capacity_vote`**|if|**`weight`**|is zero, as the calculatio|



of shards assigned to a node in the next epoch. If a node’s staked amount is too low, it may not receive


the voting mechanism from progressing.


_>__ _sources/staking/staking_inner.move_ rust

```
  /// Selects the committee for the next epoch.
  public(package) fun select_committee_and_calculate_votes(self: &mut StakingInnerV1) {
    [...]
    node_ids.length().do!(|idx| {
      [...]
      // perform calculation of the votes
      write_prices.insert(pool.write_price(), weight);
      storage_prices.insert(pool.storage_price(), weight);
      let capacity_vote = (pool.node_capacity() * (self.n_shards as u64)) / weight;
      capacity_votes.insert(capacity_vote, weight);
    });
    [,,,]
    self.next_epoch_params = option::some(epoch_params);
  }

```

**Remediation**


**Patch**


Fixed in [a1e81c6.](https://github.com/MystenLabs/walrus/commit/a1e81c6f8803307d33ba8762eb61dcd03ef43559)


© 2025 Otter Audits LLC. All Rights Reserved. 12 / 26


Mysten Walrus Audit 04 - Vulnerabilities


**Description**


to an excessively long value by the node owner, it may contribute significantly to the total size of the


thereby blocking stakers from making withdrawals.


**Remediation**


**Patch**


Fixed in [a1e81c6.](https://github.com/MystenLabs/walrus/commit/a1e81c6f8803307d33ba8762eb61dcd03ef43559)


© 2025 Otter Audits LLC. All Rights Reserved. 13 / 26


Mysten Walrus Audit 04 - Vulnerabilities


**Description**


set. However, since there is no check to ensure that the commission rate is less than or equal to 10000,


of the committee. As a result, a single node can disrupt the epoch change.









**Remediation**


Ensure that a commission rate doesn’t exceed 10000 in creating a node.


**Patch**


Fixed in [a1e81c6.](https://github.com/MystenLabs/walrus/commit/a1e81c6f8803307d33ba8762eb61dcd03ef43559)


© 2025 Otter Audits LLC. All Rights Reserved. 14 / 26


Mysten Walrus Audit 04 - Vulnerabilities


**Description**


of the event blob being recorded. While there is validation for the blob ID, there is no validation for the


ending checkpoint sequence number. As a result, the value provided by a quorum-reaching node gets


recorded in the state. If an incorrect number is entered, it causes a mismatch between the event blob


being processed by the node and the on-chain tracking.


**Remediation**


Track both the blob ID and ending checkpoint sequence number when recording the event blob certification


state.


**Patch**


Fixed in [c873816.](https://github.com/MystenLabs/walrus/commit/c8738169d9383d6f8f865ac5225fd425e9b1ecc3)


© 2025 Otter Audits LLC. All Rights Reserved. 15 / 26


Mysten Walrus Audit 04 - Vulnerabilities


**Description**


a pending commission rate for the current epoch. If there is one, it updates the pool’s commission rate


to the new value. The function then splits the rewards between the pool’s rewards and the operator’s


commission. This is done by utilizing the updated commission rate.


However, the updated commission rate is intended for future epochs and not for the current epoch. Thus,


it will result in an incorrect calculation of the operator’s commission.


**Remediation**


Ensure that the commission calculation utilizes the old commission rate for the current epoch.


**Patch**


Fixed in [cc4aaaa.](https://github.com/MystenLabs/walrus/commit/cc4aaaae20c5d5e085d0dc9b72f05bf89d31d52a)


© 2025 Otter Audits LLC. All Rights Reserved. 16 / 26


Mysten Walrus Audit 04 - Vulnerabilities


**Description**


active set below the required threshold.


_>__ _sources/staking/active_set.move_ rust

```
  /// Updates the staked amount of the storage node with the given `node_id` in
  /// the active set. Returns true if the node is in the set.
  public(package) fun update(set: &mut ActiveSet, node_id: ID, staked_amount: u64): bool {
    let index = set.nodes.find_index!(|entry| entry.node_id == node_id);
    if (index.is_none()) {
      return false
    };
    index.do!(|idx| {
      set.total_stake = set.total_stake + staked_amount - set.nodes[idx].staked_amount;
      set.nodes[idx].staked_amount = staked_amount;
    });
    true
  }

```

stake is removed to accommodate the new entry. After successfully inserting, the user immediately calls


secures a place in the active set without the required stake amount.


**Remediation**


**Patch**


Fixed in [134fee8.](https://github.com/MystenLabs/walrus/commit/134fee8bb1004938d3f42d0e770bf2674673dcb7)


© 2025 Otter Audits LLC. All Rights Reserved. 17 / 26


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.



OS-MSW-SUG-00


OS-MSW-SUG-01


OS-MSW-SUG-02


OS-MSW-SUG-03



action occurs. If a node leaves and another node qualifies but does not


trigger a stake change, that node will not be added to the active set.


There are several instances where proper validation is not performed, re

sulting in potential underflow issues.


Recommendation for modifying the codebase for improved functionality,


efficiency, and robustness.


Suggestions regarding inconsistencies in the codebase and ensuring ad

herence to coding best practices.



© 2025 Otter Audits LLC. All Rights Reserved. 18 / 26


Mysten Walrus Audit 05 - General Findings


**Failure** **to** **Replace** **Inactive** **Node** OS-MSW-SUG-00


**Description**


_>__ _sources/staking/active_set.move_ rust

```
  public(package) fun insert_or_update(set: &mut ActiveSet, node_id: ID, staked_amount: u64): bool
```

_�→_ `{`
```
    if (set.update(node_id, staked_amount)) {
      return true
    };
    set.insert(node_id, staked_amount)
  }

```

properly handle the return value.

|tion,|insert_or_update|Col3|
|---|---|---|
|**`staked_amount`**|**`staked_amount`**|is invali|



_>__ _sources/staking/active_set.move_ rust

```
  public(package) fun insert_or_update(set: &mut ActiveSet, node_id: ID, staked_amount: u64): bool
```

_�→_ `{`
```
    // Currently, the `threshold_stake` is set to `0`, so we need to account for that.
    if (staked_amount == 0 || staked_amount < set.threshold_stake) {
      set.remove(node_id);
      return false
    };
    if (set.update(node_id, staked_amount)) true
    else set.insert(node_id, staked_amount)
  }

```

**Remediation**


Add a method that lets nodes proactively attempt to join when an opening exists.


**Patch**


Fixed in [bb9e9e6.](https://github.com/MystenLabs/walrus/commit/bb9e9e67219ead709bb50c8e031e98d21e069ab2)


© 2025 Otter Audits LLC. All Rights Reserved. 19 / 26


Mysten Walrus Audit 05 - General Findings


**Missing** **Validation** **Logic** OS-MSW-SUG-01


**Description**

|previous epoch ( old_epoch_u old_epoch_u old_epoch_used_capacity old_epoch_used_capacity|used_capacity used_capacity ). Ho|
|---|---|
|**`old_epoch_used_capacity`**|, it will result in an ov|
|**`old_epoch_used_capacity`** **`>`** **`deny_list_size`**|**`old_epoch_used_capacity`** **`>`** **`deny_list_size`**|


|system_state_inner::advance_epoch|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|rent|**`node_id`**|, the|**`deny_list_size`**|i|



_>__ _sources/system/system_state_inner.move_ rust

```
     public(package) fun advance_epoch([...]): VecMap<ID, Balance<WAL>> {
       [...]
       node_ids.zip_do!(weights, |node_id, weight| {
          let deny_list_size = deny_list_sizes.try_get(&node_id).destroy_or!(0);
          let stored = (weight as u128) * ((old_epoch_used_capacity - deny_list_size) as
```

_�→_ `u128);`
```
          total_stored = total_stored + stored;
          stored_vec.push_back(stored);
       });
       [...]
     }

```

for the given epoch to prevent an underflow.


_>__ _sources/staking/pending_values.move_ rust

```
     public(package) fun reduce(self: &mut PendingValues, epoch: u32, value: u64) {
       let map = &mut self.0;
       if (!map.contains(&epoch)) {
          abort EMissingEpochValue
       } else {
          let curr = map[&epoch];
          *&mut map[&epoch] = curr - value;
       };
     }

```

**Remediation**


Add the underflow checks as stated above.


© 2025 Otter Audits LLC. All Rights Reserved. 20 / 26


Mysten Walrus Audit 05 - General Findings


**Patch**


1. Issue #1 fixed in [cc4aaaa.](https://github.com/MystenLabs/walrus/commit/cc4aaaae20c5d5e085d0dc9b72f05bf89d31d52a)


2. Issue #2 fixed in [cc4aaaa.](https://github.com/MystenLabs/walrus/commit/cc4aaaae20c5d5e085d0dc9b72f05bf89d31d52a)


© 2025 Otter Audits LLC. All Rights Reserved. 21 / 26


Mysten Walrus Audit 05 - General Findings


**Code** **Refactoring** OS-MSW-SUG-02


**Description**

|pool.is_empty()|Col2|, a|
|---|---|---|
|for|**`pending_stakes`**|**`pending_stakes`**|



_>__ _sources/system/staking_pool.move_ rust

```
     /// Destroy the pool if it is empty.
     public(package) fun destroy_empty(pool: StakingPool) {
       assert!(pool.is_empty(), EPoolNotEmpty);
       [...]
       let (_epochs, pending_stakes) = pending_stake.unwrap().into_keys_values();
       pending_stakes.do!(|stake| assert!(stake == 0));
     }

```

+3 to allow all users to react.


**Remediation**


Incorporate the above refactors into the codebase.


**Patch**


1. Issue #1 fixed in [cc4aaaa.](https://github.com/MystenLabs/walrus/commit/cc4aaaae20c5d5e085d0dc9b72f05bf89d31d52a)


2. Issue #2 fixed in [cc4aaaa.](https://github.com/MystenLabs/walrus/commit/cc4aaaae20c5d5e085d0dc9b72f05bf89d31d52a)


© 2025 Otter Audits LLC. All Rights Reserved. 22 / 26


Mysten Walrus Audit 05 - General Findings


**Code** **Maturity** OS-MSW-SUG-03


**Description**


returns an address, whereas it actually returns an object. Update the comment to: _Returns_ _the_


_‘Authorized‘_ _as_ _an_ _object._


_>__ _sources/staking/active_set.move_ rust

```
     /// Returns the `Authorized` as an address.
     public fun authorized_object(id: ID): Authorized {
       Authorized::ObjectID(id)
     }

|The current implementation of|take_threshold_value|
|---|---|
|**`staking_inner::quorum_below`**|**`staking_inner::quorum_below`**|


```

whether a slightly lower value may also have been supported by the quorum. If strictly following the

|quorum_below|Col2|should find th|
|---|---|---|
|d in|**`take_threshold_value`**|**`take_threshold_value`**|



_>__ _sources/staking/staking_inner.move_ rust

```
     /// Take the lowest value, s.t. a quorum (2f + 1) voted for a value lower or equal to
```

_�→_ _`this.`_
```
     fun quorum_below(vote_queue: &mut PriorityQueue<u64>, n_shards: u16): u64 {
       let threshold_weight = ((n_shards - 1) / 3 + 1) as u64;
       take_threshold_value(vote_queue, threshold_weight)
     }

     fun take_threshold_value(vote_queue: &mut PriorityQueue<u64>, threshold_weight: u64): u64
```

_�→_ `{`
```
       let mut sum_weight = 0;
       // The loop will always succeed if `threshold_weight` is smaller than the total
```

_�→_ _`weight.`_
```
       loop {
          let (value, weight) = vote_queue.pop_max();
          sum_weight = sum_weight + weight;
          if (sum_weight >= threshold_weight) {
            return value
          };
       }
     }

```

© 2025 Otter Audits LLC. All Rights Reserved. 23 / 26


Mysten Walrus Audit 05 - General Findings


occurred exactly at the epoch transition boundary.


**Remediation**


Implement the above-mentioned suggestions.


**Patch**


1. Issue #1 fixed in [422f76d.](https://github.com/MystenLabs/walrus/commit/422f76deb1474f058033062faea99ce6a4a58f87)


2. Issue #2 fixed in [a1e81c6.](https://github.com/MystenLabs/walrus/commit/a1e81c6f8803307d33ba8762eb61dcd03ef43559)


3. Issue #3 fixed in [a1e81c6.](https://github.com/MystenLabs/walrus/commit/a1e81c6f8803307d33ba8762eb61dcd03ef43559)


© 2025 Otter Audits LLC. All Rights Reserved. 24 / 26


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


© 2025 Otter Audits LLC. All Rights Reserved. 25 / 26


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


© 2025 Otter Audits LLC. All Rights Reserved. 26 / 26


