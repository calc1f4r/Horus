# **Magna**

Security Assessment


March 19th, 2025 - Prepared by OtterSec


Bartłomiej Wierzbiński [dark@osec.io](mailto:dark@osec.io)


Robert Chen [notdeghost@osec.io](mailto:notdeghost@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **3**


Overview 3


Key Findings 3


**Scope** **4**


**Findings** **5**


**Vulnerabilities** **6**


OS-MGN-ADV-00 | Frontrunning Vesting Creation 7


OS-MGN-ADV-01 | Incorrect Rejections of Cancellation Requests 9


OS-MGN-ADV-02 | Failure to Check Schedules Funding Status 11


OS-MGN-ADV-03 | Improper Termination Handling in Withdrawals 12


**General** **Findings** **13**


OS-MGN-SUG-00 | Unverifiable Merkle Proof due to Length Mismatch 15


OS-MGN-SUG-01 | Missing Validation Logic 17


OS-MGN-SUG-02 | Additional Safety Checks 19


OS-MGN-SUG-03 | Error Handling 21


OS-MGN-SUG-04 | Utilization of incorrect Comparison operators 22


OS-MGN-SUG-05 | Code Maturity 24


OS-MGN-SUG-06 | Code Redundancy 26


OS-MGN-SUG-07 | Unutilized Code 28


OS-MGN-SUG-08 | Unnecessary Assert Check 30


OS-MGN-SUG-09 | Potential Overflow Scenarios 32


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 34


Magna Audit


**Appendices**



TABLE OF CONTENTS



**Vulnerability** **Rating** **Scale** **33**


**Procedure** **34**


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 34


**01** **—** **Executive** **Summary**

## Overview


between February 28th and March 17th, 2025. For more information on our auditing methodology, refer


to Appendix B.

## Key Findings


We produced 14 findings throughout this audit engagement.


We identified several vulnerabilities in the vesting creation and management process. The vesting creation


mechanism is susceptible to frontrunning attacks, allowing attackers to preemptively create a vesting


contract with the same seed ID or register an account for the target vesting address, resulting in legitimate


creation attempts to fail (OS-MGN-ADV-00). Additionally, the cancellation of interval-based vesting


schedules incorrectly determines full unlock status by disregarding the cliff timestamp. If the cliff timestamp


is set after the last period, the function may abort, preventing valid cancellations (OS-MGN-ADV-01).


that funding is possible when it is not (OS-MGN-ADV-02).


We also made suggestions regarding the need to ensure adherence to coding best practices and code


optimization (OS-MGN-SUG-05), and suggested removing redundant and unutilized code instances


(OS-MGN-SUG-06, OS-MGN-SUG-07). Moreover, we advised including additional safety checks within


the codebase to improve security (OS-MGN-SUG-01,OS-MGN-SUG-03). Lastly, when generating a


Merkle proof, the program inserts an empty vector instead of duplicating the last node for odd-length


levels, resulting in unverifiable proofs due to length mismatches (OS-MGN-SUG-00).


© 2025 Otter Audits LLC. All Rights Reserved. 3 / 34


**02** **—** **Scope**


The source code was delivered to us in a Git repository at


[https://github.com/magna-eng/protocol/tree/main/move.](https://github.com/magna-eng/protocol/tree/main/move) This audit was performed against commit


[679af5e0.](https://github.com/magna-eng/protocol/commit/679af5e025b6f9ead3ee84e2840bb74113680a92)


**A** **brief** **description** **of** **the** **programs** **is** **as** **follows:**


A rewrite of the Airlock V2 Solidity contracts in Aptos Move, includ


airlock-aptos



ing the porting of all unit tests to verify the correctness of the new


implementation.



© 2025 Otter Audits LLC. All Rights Reserved. 4 / 34


**03** **—** **Findings**


Overall, we reported 14 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.



© 2025 Otter Audits LLC. All Rights Reserved. 5 / 34


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


**ID** **Severity** **Status** **Description**


attacks. Attackers may preemptively create a



target vesting address, resulting in legitimate


attempts to create a vesting contract to fail.


rectly determine full unlock status by ignoring


set after the last period, the function may pre

maturely abort, preventing valid cancellations.


already fully funded and may falsely claim that


funding is possible when it is not.


withdrawals after revocation, resulting in an

|n addition,|can_withdraw_calendar|Col3|
|---|---|---|
|**`can_withdraw_interval`**|**`can_withdraw_interval`**|throw<br>an|



error on revocation instead of returning true or


false.



OS-MGN-ADV-00


OS-MGN-ADV-01


OS-MGN-ADV-02


OS-MGN-ADV-03





© 2025 Otter Audits LLC. All Rights Reserved. 6 / 34


Magna Audit 04 - Vulnerabilities


**Description**


to frontrun the creation of a vesting contract in multiple ways. The first vulnerability occurs due to the use of


. The logic in these functions contains an assertion that checks if a vesting contract already exists for a


from continuing.


_>__ _move/airlock_vesting/sources/vesting.move_ rust

```
  fun create_vesting<CoinType, PaymentCoinType>(seed_id: vector<u8>,[...]): Object<Vesting>
```

_�→_ `acquires` `Airlock` `{`
```
    [...]
    assert!(!vesting_exists(seed_id), ERR_VESTING_EXISTS);
    [...]
    aptos_account::create_account(vesting_addr);
  }

```

abort the original user’s vesting creation.

|ntract with any|seed_id|Col3|
|---|---|---|
|**`create_vesting`**|**`create_vesting`**|utilizi|



_>__ _move/airlock_vesting/sources/vesting_merkle.move_ rust

```
  public fun create_vesting_internal<CoinType, PaymentCoinType>(seed_id: vector<u8>,[...]):
```

_�→_ `Object<Vesting>` `acquires` `Airlock` `{`
```
    [...]
    assert!(!vesting_exists(seed_id), ERR_VESTING_EXISTS);
    [...]
    aptos_account::create_account(vesting_addr);
  }

|vesting::create_vesting|Col2|an|
|---|---|---|
|s account via|**`create_account`**|**`create_account`**|


|vesting_merkle::create_vesting_internal|Col2|
|---|---|
|**`create_account`**|may be called by anyone with|


```

any address and will abort if the account already exists. Consequently, an attacker may frontrun the


© 2025 Otter Audits LLC. All Rights Reserved. 7 / 34


Magna Audit 04 - Vulnerabilities


**Remediation**


should skip account creation if the account already exists.


**Patch**


This issue was acknowledged by the client and the risk was accepted.


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 34


Magna Audit 04 - Vulnerabilities


**Description**


be canceled. One of its key checks ensures that the schedule is not already fully unlocked before allowing


the fully unlocked status. This omission may result in a logic error where valid schedules may be incorrectly


considered fully unlocked and thus non-cancelable.

|hout considering the|cliff_timestamp|Col3|
|---|---|---|
|**`unlocked_at_start`**|**`unlocked_at_start`**|may be accessed.|



_>__ _move/airlock_vesting/sources/vesting.move_ rust

```
  public entry fun cancel_schedule_interval([...]) acquires Interval, Schedule, Vesting {
    [...]
    let fully_unlocked_timestamp =
      interval.unlock_timestamp
         + (interval.number_of_periods * interval.period_length);
    let now_seconds = timestamp::now_seconds();
    assert!(now_seconds <= fully_unlocked_timestamp, ERR_ALREADY_FULLY_UNLOCKED);
    [...]
    event::emit(ScheduleCanceledEvent { schedule_addr });
  }

```

cancellation of the vesting schedule will be restricted even though the majority of the funds are still locked


**Remediation**


© 2025 Otter Audits LLC. All Rights Reserved. 9 / 34


Magna Audit 04 - Vulnerabilities


**Patch**


Resolved in [ac03e9e.](https://github.com/magna-eng/protocol/commit/ac03e9ec801819b3e62cc12383f0ced18bef3dfb)


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 34


Magna Audit 04 - Vulnerabilities


**Description**


even if the vesting schedule is already fully funded and no more funding is allowed, as the function does


not check if the schedule is already fully funded.


_>__ _move/airlock_vesting/sources/vesting.move_ rust

```
  #[view]
  public fun can_fund(schedule_obj: Object<Schedule>, amount: u64): bool acquires Schedule {
    let schedule_addr = object::object_address(&schedule_obj);
    if (!exists<Schedule>(schedule_addr)) {
      return false
    };
    let schedule = borrow_global<Schedule>(schedule_addr);
    schedule.terminated_timestamp == 0 && amount != 0
  }

```

**Remediation**


any additional funding should be prevented.


**Patch**


Resolved in [e300c3b.](https://github.com/magna-eng/protocol/commit/e300c3b3959863759babf5fedeb30be55ba3e5c3)


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 34


Magna Audit 04 - Vulnerabilities


**Description**


a vulnerability where the withdrawn amount may exceed the vested amount under certain conditions.


in case of termination. This will lead to mathematical underflow errors.


return true or false based on whether any vested amount remains at the time of termination, instead of


throwing an error and disrupting transaction execution.


**Remediation**


Ensure the case of withdrawal after revoke is be explicitly checked and handled separately in


errors.


**Patch**


Resolved in [e300c3b.](https://github.com/magna-eng/protocol/commit/e300c3b3959863759babf5fedeb30be55ba3e5c3)


© 2025 Otter Audits LLC. All Rights Reserved. 12 / 34


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.



OS-MGN-SUG-00


OS-MGN-SUG-01


OS-MGN-SUG-02


OS-MGN-SUG-03


OS-MGN-SUG-04


OS-MGN-SUG-05


OS-MGN-SUG-06


OS-MGN-SUG-07



There are several instances where proper validation is not performed, re

sulting in potential security issues.


Additional safety checks may be incorporated within the codebase to make


it more robust and secure.


The error handling may be improved to avoid unexpected failures during


code execution.


cancellation of vesting schedules even after the schedule is already fully


unlocked and there is nothing to cancel.


Suggestions regarding inconsistencies in the codebase and ensuring ad

herence to coding best practices.


The codebase contains multiple cases of redundancy that should be re

moved for better maintainability and clarity.


The codebase contains multiple cases of unnecessary or unutilized code


that should be removed.



© 2025 Otter Audits LLC. All Rights Reserved. 13 / 34


Magna Audit 05 - General Findings



OS-MGN-SUG-08


OS-MGN-SUG-09



fail in the current implementation.


There are multiple areas within the codebase where an overflow may occur


if the administrator were to set extremely large values.



© 2025 Otter Audits LLC. All Rights Reserved. 14 / 34


Magna Audit 05 - General Findings


**Unverifiable** **Merkle** **Proof** **due** **to** **Length** **Mismatch** OS-MGN-SUG-00


**Description**


However, if the node is the last element in an odd-length list, it incorrectly inserts an empty vector (


due to a length mismatch.









implying the _alone_ node is hashed with itself during root calculation. To ensure a correct proof step in


such cases, the proof element must match the hashed element. Therefore, the proof should include the


node itself rather than an all-zero vector.









© 2025 Otter Audits LLC. All Rights Reserved. 15 / 34


Magna Audit 05 - General Findings


**Remediation**


mentioned by Magna.


© 2025 Otter Audits LLC. All Rights Reserved. 16 / 34


Magna Audit 05 - General Findings


**Missing** **Validation** **Logic** OS-MGN-SUG-01


**Description**


improve error handling. This ensures that the contract does not attempt to borrow data for the wrong


type of vesting schedule, thereby preventing unexpected errors during execution.


_>__ _move/airlock_vesting/sources/vesting.move_ rust

```
     public entry fun withdraw_interval<CoinType, PaymentCoinType>(
       fee_payer: &signer, schedule_obj: Object<Schedule>
     ) acquires Schedule, Interval, Vesting {
       [...]
       let interval = borrow_global<Interval>(schedule_addr);
       [...]
     }

     public entry fun withdraw_calendar<CoinType, PaymentCoinType>(
       fee_payer: &signer, schedule_obj: Object<Schedule>
     ) acquires Schedule, Calendar, Vesting {
       [...]
       let calendar = borrow_global<Calendar>(schedule_addr);
       [...]
     }

```

validate if the borrowed object exists before borrowing, to avoid runtime errors. For example,


vector and that the sum of the amounts is not 0. However, it does not check if individual values are


greater than zero.


total amount to be vested over the intervals.


© 2025 Otter Audits LLC. All Rights Reserved. 17 / 34


Magna Audit 05 - General Findings


**Remediation**


Add the missing validations mentioned above.


© 2025 Otter Audits LLC. All Rights Reserved. 18 / 34


Magna Audit 05 - General Findings


**Additional** **Safety** **Checks** OS-MGN-SUG-02


**Description**

|tion in|vesting::can_withdraw_terminated_funds|Col3|Col4|to ex|
|---|---|---|---|---|
|**`terminated_amount`**|**`terminated_amount`**|keeps the total below|**`funded_amount`**|**`funded_amount`**|



_>__ _move/airlock_vesting/sources/vesting.move_ rust

```
     #[view]
     public fun can_withdraw_terminated_funds(
       schedule_obj: Object<Schedule>
     ): bool acquires Schedule {
       let schedule_addr = object::object_address(&schedule_obj);
       if (!exists<Schedule>(schedule_addr)) {
          return false
       };

       let schedule = borrow_global<Schedule>(schedule_addr);
       schedule.terminated_amount != 0
          && schedule.terminated_withdrawn != schedule.terminated_amount
          && schedule.withdrawn + schedule.terminated_withdrawn
            <= schedule.funded_amount
     }

```

timestamps are in increasing order, but fail to check if they are in the future. Allowing past timestamps


will render the vesting logic ineffective as the funds may be withdrawn immediately unlocked upon


creation.

|vesting::create_schedule_interval|Col2|Col3|should|
|---|---|---|---|
|**`amount_to_fund`** **`!=`** **`0`**|.<br>If|**`amount_to_fund`**|**`amount_to_fund`**|


|In|create_schedule_interval|Col3|
|---|---|---|
|**`cliff_timestamp`**|**`cliff_timestamp`**|is zero, as the|



actual cliff timestamp.


© 2025 Otter Audits LLC. All Rights Reserved. 19 / 34


Magna Audit 05 - General Findings


**Remediation**


Ensure the above checks are included in the codebase.


© 2025 Otter Audits LLC. All Rights Reserved. 20 / 34


Magna Audit 05 - General Findings


**Error** **Handling** OS-MGN-SUG-03


**Description**


the transfer to improve error handling. If the benefactor does not have enough funds, the transfer


has enough coin to funds, to handle the potential errors if there is not enough cash to transfer


before the transfer, to handle the potential error gracefully.


_>__ _move/airlock_vesting/sources/vesting.move_ rust

```
     /// @notice Handle paying claim fees.
     /// @param fee_payer The payer of the fee.
     /// @param vesting The vesting object.
     fun handle_claim_fee<PaymentCoinType>(
       fee_payer: &signer, vesting: &Vesting
     ) {
       if (vesting.claim_fee != 0) {
          assert!(vesting.fee_collector != @0x0, ERR_INVALID_FEE_COLLECTOR);
          aptos_account::transfer_coins<PaymentCoinType>(
            fee_payer, vesting.fee_collector, vesting.claim_fee
          );
       }
     }

```

to withdraw before proceeding with the token transfer to gracefully handle potential errors related to


insufficient balance.


attempt to access an invalid index, resulting in an abort. Ensure the functions first check whether


**Remediation**


Modify the code to ensure proper error handling is implemented.


© 2025 Otter Audits LLC. All Rights Reserved. 21 / 34


Magna Audit 05 - General Findings


**Utilization** **of** **incorrect** **Comparison** **operators** OS-MGN-SUG-04


**Description**


celable even after it has reached the fully unlocked state where there is nothing left to cancel.


_>__ _move/airlock_vesting/sources/vesting.move_ rust

```
  public entry fun cancel_schedule_calendar([...]) acquires Calendar, Schedule, Vesting {
    [...]
    let now_seconds = timestamp::now_seconds();
    assert!(
       now_seconds
         <= *vector::borrow(
           &calendar.unlock_timestamps,
           vector::length(&calendar.unlock_timestamps) - 1
         ),
       ERR_ALREADY_FULLY_UNLOCKED
    );[...]
  }

```

”unlocked.” If the schedule has already reached the final unlock timestamp, it indicates that there are


consistency between the logic for canceling and the calculation of vested amounts.









© 2025 Otter Audits LLC. All Rights Reserved. 22 / 34


Magna Audit 05 - General Findings


where the schedule is considered cancelable even after it has reached the fully unlocked state where


there is nothing left to cancel.


**Remediation**


schedules that are already fully unlocked.


© 2025 Otter Audits LLC. All Rights Reserved. 23 / 34


Magna Audit 05 - General Findings


**Code** **Maturity** OS-MGN-SUG-05


**Description**

|Functions such as|vesting_merkle::withdraw_interval|Col3|
|---|---|---|
|**`vesting::transfer_beneficiary_address`**|**`vesting::transfer_beneficiary_address`**|,<br>which<br>modi|



proper logging of state modifications and for providing better integration with off-chain services and


user interfaces.


improve the clarity and precision of the error messages when the withdrawal fails to meaningfully


describe the point of failure.


_>__ _move/airlock_vesting/sources/vesting.move_ rust

```
     public entry fun withdraw_terminated_funds<CoinType>(
       benefactor: &signer, schedule_obj: Object<Schedule>
     ) acquires Schedule, Vesting {
       [...]
       let schedule = borrow_global_mut<Schedule>(schedule_addr);
       assert!(schedule.terminated_amount != 0, ERR_NOT_FUNDED);
       assert!(
          schedule.terminated_withdrawn != schedule.terminated_amount, ERR_NOT_FUNDED
       );
       [...]
     }

|vesting::create_schedule_interval|Col2|
|---|---|
|**`vesting_addr`**|value instead of recomput|


```

_>__ _move/airlock_vesting/sources/vesting.move_ rust

```
     public fun create_schedule_interval<CoinType>([...]): Object<Interval> acquires Vesting {
       [...]
       event::emit(
          ScheduleCreatedEvent {
            schedule_addr,
            vesting_addr: object::object_address(&vesting_obj),
            [...]
          }
       );
       [...]
     }

```

service attacks on vector operations.


© 2025 Otter Audits LLC. All Rights Reserved. 24 / 34


Magna Audit 05 - General Findings


_>__ _move/airlock_vesting/sources/vesting.move_ rust

```
     #[view]
     public fun all_vestings(): vector<Object<Vesting>> acquires Airlock {
       let airlock = borrow_global<Airlock>(package::resource_account_address());
       smart_vector::to_vector(&airlock.vestings)
     }

```

be implemented to ensure its existence, allowing it to be borrowed within the main function flow.


**Remediation**


Implement the above-mentioned suggestions.


© 2025 Otter Audits LLC. All Rights Reserved. 25 / 34


Magna Audit 05 - General Findings


**Code** **Redundancy** OS-MGN-SUG-06


**Description**

|mplicitly guarantees that|unlocked_at_start + cliff_amount|Col3|Col4|Col5|
|---|---|---|---|---|
|**`unlocked_at_start`** **`+`** **`cliff_amount`**|**`unlocked_at_start`** **`+`** **`cliff_amount`**|is more than|**`amount`**|,|



anyway, rendering this check unnecessary.


_>__ _move/airlock_vesting/sources/vesting.move_ rust

```
     public fun create_schedule_interval<CoinType>([...]): Object<Interval> acquires Vesting {
       [...]
       assert!(
          unlocked_at_start + cliff_amount <= amount,
          ERR_INVALID_AMOUNT
       );
       [...]
       let total_amount =
          get_total_amount_for_interval(
            unlocked_at_start,
            cliff_amount,
            number_of_periods,
            tokens_per_period
          );
       assert!(total_amount == amount, ERR_INVALID_AMOUNT);
       [...]
     }

|vesting vesting, Vesting Vesting|both c c|
|---|---|
|**`Vesting`**|objec|
|**`borrow_global`**|**`borrow_global`**|


```

© 2025 Otter Audits LLC. All Rights Reserved. 26 / 34


Magna Audit 05 - General Findings


the same throughout execution and may be acquired only once.


_>__ _move/airlock_vesting/sources/vesting.move_ rust

```
     public entry fun withdraw_terminated_funds<CoinType>(
       benefactor: &signer, schedule_obj: Object<Schedule>
     ) acquires Schedule, Vesting {
       [...]
       assert_is_benefactor(vesting.benefactors, signer::address_of(benefactor));
       [...]
       withdraw_terminated_to_benefactor<CoinType>(
          &vesting_signer,
          schedule,
          signer::address_of(benefactor),
          amount_to_terminate
       );
     }

```

**Remediation**


Remove the redundant code instances.


© 2025 Otter Audits LLC. All Rights Reserved. 27 / 34


Magna Audit 05 - General Findings


**Unutilized** **Code** OS-MGN-SUG-07


**Description**


recorded as one or the current timestamp.


_>__ _move/airlock_vesting/sources/vesting.move_ rust

```
     fun calc_vested_amount_interval([...]): u64 {
       let timestamp = timestamp::now_seconds();
       let final_timestamp =
          if (terminated_timestamp == 0) timestamp
          else math64::min(terminated_timestamp, timestamp);
       [...]
     }

```

based on the constraints of the different scenarios within the function.


may be removed.


© 2025 Otter Audits LLC. All Rights Reserved. 28 / 34


Magna Audit 05 - General Findings


**Remediation**


Remove any unutilized code.


© 2025 Otter Audits LLC. All Rights Reserved. 29 / 34


Magna Audit 05 - General Findings


**Unnecessary** **Assert** **Check** OS-MGN-SUG-08


**Description**

|withdraw_calendar|Col2|Col3|and|withdraw_interval|Col6|Col7|the assert check is|
|---|---|---|---|---|---|---|---|
|**`withdrawn`**|+|**`terminated_withdrawn`**|**`terminated_withdrawn`**|**`terminated_withdrawn`**|+|**`withdrawable_amount`**|**`withdrawable_amount`**|



outcomes of this assert are:


always true.


previous assumption.

|In|withdraw_terminated_funds|
|---|---|
|**`terminated_amount`**|**`terminated_amount`**|
|**`schedule.terminated_withdrawn`** **`!=`** **`schedule.terminated_amount`**|**`schedule.terminated_withdrawn`** **`!=`** **`schedule.terminated_amount`**|
|**`terminated_withdrawn`** <br>|**`terminated_withdrawn`** <br>|



© 2025 Otter Audits LLC. All Rights Reserved. 30 / 34


Magna Audit 05 - General Findings


is always true because the withdraws are limited to vested amounts (or funded if less than vested).


**Remediation**


© 2025 Otter Audits LLC. All Rights Reserved. 31 / 34


Magna Audit 05 - General Findings


**Potential** **Overflow** **Scenarios** OS-MGN-SUG-09


**Description**


In the current codebase, overflows may occur in multiple areas of the code. However, they require an


administrator to set extremely large values. It is assumed that the administrator is not malicious and is


knowledgeable about the protocol, ensuring reasonable parameter settings that prevent such cases.


Below are examples where an overflow may occur:


is greater than max u64.


) is more than max u64.

|vesting_merkle::calc_vested_piece_amount|Col2|Col3|Col4|
|---|---|---|---|
|**`piece.amount`**|*|**`fully_vested_periods`**|is mo|



more than max u64.


**Remediation**


Add overflow checks and upscaling in potential overflow areas.


© 2025 Otter Audits LLC. All Rights Reserved. 32 / 34


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


© 2025 Otter Audits LLC. All Rights Reserved. 33 / 34


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


© 2025 Otter Audits LLC. All Rights Reserved. 34 / 34


