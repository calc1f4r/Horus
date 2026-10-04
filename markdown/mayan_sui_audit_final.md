# **Mayan Sui**

Security Assessment


March 4th, 2025 - Prepared by OtterSec


Akash Gurugunti [sud0u53r.ak@osec.io](mailto:sud0u53r.ak@osec.io)


Ajay Shankar Kunapareddy [d1r3wolf@osec.io](mailto:d1r3wolf@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


**Scope** **3**


**Findings** **4**


**Vulnerabilities** **5**


OS-MSI-ADV-00 | Permissionless Order Fulfillment Before Penalty Period 6


OS-MSI-ADV-01 | Loss of Funds Due to Invalid Gas Recipient 7


OS-MSI-ADV-02 | Missing Version Checks in Admin Functions 8


**General** **Findings** **9**


OS-MSI-SUG-00 | Validation and Consistency Checks 10


OS-MSI-SUG-01 | Missing Validation Logic 11


OS-MSI-SUG-02 | Code Maturity 12


OS-MSI-SUG-03 | Redundant/Unutilized Code 14


**Appendices**


**Vulnerability** **Rating** **Scale** **15**


**Procedure** **16**


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 16


**01** **—** **Executive** **Summary**

## Overview


between January 10th, 2024 and February 14th, 2025. For more information on our auditing methodology,


refer to Appendix B.

## Key Findings


We produced 7 findings throughout this audit engagement.


In particular, we identified a vulnerability concerning improper access control in the order fulfillment


functionality, where the driver check on the sender is only enforced during the penalty period, allowing


anyone to fulfill the order before the penalty period begins (OS-MSI-ADV-00). Additionally, there is a


lack of version checks in the admin functions, allowing the utilization of outdated package versions and


enabling the bypassing of restrictions and security measures in newer implementations (OS-MSI-ADV

02). Furthermore, we highlighted a potential loss of funds issue, where sending gas to the destination


address in the case of a custom payload results in irretrievable funds, as object IDs are unable to receive


coins (OS-MSI-ADV-01).


We also made recommendations regarding the need for improved validation and consistency checks


(OS-MSI-SUG-01), and suggested removing unnecessary and redundant instances (OS-MSI-SUG-03).


Moreover, we advised adherence to coding best practices (OS-MSI-SUG-02).


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 16


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/mayan-finance/mayan_swift_sui.](https://github.com/mayan-finance/mayan_swift_sui)


This audit was performed against commit [f0d914a.](https://github.com/mayan-finance/mayan_swift_sui/commit/f0d914a74a5a7a26680ca7016e0d346cedf9ba3ad)


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**


A cross-chain token transfer and order fulfillment protocol implemented
swift-sui

on Sui that uses Wormhole for secure messaging between blockchains.


© 2025 Otter Audits LLC. All Rights Reserved. 3 / 16


**03** **—** **Findings**


Overall, we reported 7 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.



© 2025 Otter Audits LLC. All Rights Reserved. 4 / 16


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


**ID** **Severity** **Status** **Description**



enforced only during the penalty period, allow

ing anyone to fulfill the order before the penalty


period begins.


not a user address. Sending gas to it results in


irretrievable funds, as object IDs will not be able


to receive coins.


Lack of version checks in admin functions allows


the utilization of outdated package versions, en

abling the bypassing of restrictions and security


measures in newer implementations.



OS-MSI-ADV-00


OS-MSI-ADV-01


OS-MSI-ADV-02





© 2025 Otter Audits LLC. All Rights Reserved. 5 / 16


Mayan Sui Audit 04 - Vulnerabilities


**Description**


penalty period, which is defined as the time window between


_>__ _mayan_swift/sources/fulfill.move_ rust

```
  public fun prepare_fulfill_winner([...]): FulfillTicket {
    [...]
    let clock_now_s = clock.timestamp_ms() / 1000;
    assert!(order_item.deadline() > clock_now_s, EDeadlineIsPassed);

    if (clock_now_s >= order_item.deadline() - (order_item.penalty_period() as u64)) {
      assert!(msg_driver == ctx.sender(), EInvalidDriver);
    };

    [...]
  }

```

Before the penalty period, there is no restriction on who may call the function. Anyone may prepare the


fulfillment before the penalty period, regardless of whether they are the legitimate auction winner


**Remediation**


Enforce the driver check before the penalty period condition to ensure that only the legitimate auction


winner may prepare the fulfillment before the penalty period.


**Patch**


Resolved in [ac8a875.](https://github.com/mayan-finance/mayan_swift_sui/commit/ac8a875eb962f21581c68263b8caa4f594a7bd24)


© 2025 Otter Audits LLC. All Rights Reserved. 6 / 16


Mayan Sui Audit 04 - Vulnerabilities


**Description**


receive funds.


_>__ _mayan_swift_sui/packages/mayan_swift/sources/state.move_ rust

```
  public(package) fun fulfill_dest_order<CoinType>(
     state: &mut State,
     fund: Coin<CoinType>,
     gas: Coin<SUI>,
     addr_dest: address,
     [...]
     payload_type: u8,
     custom_payload: address,
     ctx: &mut TxContext,
  ): (u8, u64, Option<ID>) {
    if (gas.value() > 0) {
      transfer::public_transfer(gas, addr_dest);
    } else {
      gas.destroy_zero();
    };
    [...]
  }

```

**Remediation**


**Patch**


Resolved in [95ce7b8.](https://github.com/mayan-finance/mayan_swift_sui/commit/95ce7b8403ea449929075bd5dd0b60b1322c686c)


© 2025 Otter Audits LLC. All Rights Reserved. 7 / 16


Mayan Sui Audit 04 - Vulnerabilities


**Description**


do not include any version checks, which implies that an administrator may utilize an older version of


the contract to bypass restrictions that are enforced in newer versions. Similarly, version checks are not


**Remediation**


Ensure to update admin functions with checks to verify the utilized object is the supported version.


**Patch**


Resolved in [ac8a875.](https://github.com/mayan-finance/mayan_swift_sui/commit/ac8a875eb962f21581c68263b8caa4f594a7bd24)


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 16


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.



OS-MSI-SUG-00


OS-MSI-SUG-01


OS-MSI-SUG-02


OS-MSI-SUG-03



inconsistent state management.


There are several instances where proper validation is not performed, re

sulting in potential security issues.


Suggestions regarding inconsistencies in the codebase and ensuring ad

herence to coding best practices.


The codebase contains multiple cases of redundant and unnecessary code


that should be removed for better maintainability and clarity.



© 2025 Otter Audits LLC. All Rights Reserved. 9 / 16


Mayan Sui Audit 05 - General Findings


**Validation** **and** **Consistency** **Checks** OS-MSI-SUG-00


**Description**


with the intended cross-chain behavior.


Also, it is possible for an order to have zero input funds, which does not make sense for a swap operation.


**Remediation**

|Refactor|initialize_order|Col3|
|---|---|---|
|**`input_funds.value()`** **`>`** **`0`**|**`input_funds.value()`** **`>`** **`0`**|, a|



**Patch**


Resolved in [ac8a875.](https://github.com/mayan-finance/mayan_swift_sui/commit/ac8a875eb962f21581c68263b8caa4f594a7bd24)


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 16


Mayan Sui Audit 05 - General Findings


**Missing** **Validation** **Logic** OS-MSI-SUG-01


**Description**


cancellations. Standardize this logic across chains, ideally utilizing an inclusive check for clarity and


consistency.


2. Add a check in the following functions to ensure that the current version is valid and not outdated or


deprecated:


**Remediation**


Incorporate the above valuations into the codebase.


**Patch**


Issue #1 resolved in [95ce7b8.](https://github.com/mayan-finance/mayan_swift_sui/commit/95ce7b8403ea449929075bd5dd0b60b1322c686c)


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 16


Mayan Sui Audit 05 - General Findings


**Code** **Maturity** OS-MSI-SUG-02


**Description**


_>__ _sources/state.move_ rust

```
     fun max_compatible_state_version(state: &State): u64 {
       let keys = state.version_set.keys();
       let len = vector::length(keys);
       assert!(len > 0, 1); // Ensure the VecSet is not empty
       let mut max_value = *vector::borrow(keys, 0); // Initialize with the first element
       let mut i = 1;
       while (i < len) {
          let current = *vector::borrow(keys, i);
          if (current > max_value) {
            max_value = current;
          };
          i = i + 1;
       };
       max_value
     }

|compact|Col2|field is hard|
|---|---|---|
|meter to|**`post_batch`**|**`post_batch`**|


```

parameter rather than emitting a hardcoded value.


_>__ _sources/batch_post.move_ rust

```
     public fun post_batch(
       state: &mut State,
       orders: vector<address>,
       compact: bool,
     ): MessageTicket {
       [...]
       sui::event::emit(BatchUnlockPosted {
          compact: false,
          orders,
       });
       message_ticket
     }

```

© 2025 Otter Audits LLC. All Rights Reserved. 12 / 16


Mayan Sui Audit 05 - General Findings


locking calls, into a shared function to improve code re-usability, maintainability, and efficiency.


**Remediation**


Implement the above-mentioned suggestions.


**Patch**


Issue #2 resolved in [95ce7b8.](https://github.com/mayan-finance/mayan_swift_sui/commit/95ce7b8403ea449929075bd5dd0b60b1322c686c)


© 2025 Otter Audits LLC. All Rights Reserved. 13 / 16


Mayan Sui Audit 05 - General Findings


**Redundant/Unutilized** **Code** OS-MSI-SUG-03


**Description**


check.





may be removed.


**Remediation**


Remove the redundant/unnecessary code instances listed above.


**Patch**


Issue #1 resolved in [ac8a875.](https://github.com/mayan-finance/mayan_swift_sui/commit/ac8a875eb962f21581c68263b8caa4f594a7bd24)


© 2025 Otter Audits LLC. All Rights Reserved. 14 / 16


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


© 2025 Otter Audits LLC. All Rights Reserved. 15 / 16


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


© 2025 Otter Audits LLC. All Rights Reserved. 16 / 16


