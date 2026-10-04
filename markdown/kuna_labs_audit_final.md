# **Kuna Labs**

Security Assessment


September 3rd, 2025 - Prepared by OtterSec


Michał Bochnak [embe221ed@osec.io](mailto:embe221ed@osec.io)


Sangsoo Kang [sangsoo@osec.io](mailto:sangsoo@osec.io)


alpha toure [shxdow@osec.io](mailto:shxdow@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


**Scope** **3**


**Findings** **4**


**Vulnerabilities** **5**


OS-KUL-ADV-00 | Unfair Rewards via Incorrect Supply Pool Instance 6


OS-KUL-ADV-01 | Precision Loss in Calculation of Token X Amount 8


**General** **Findings** **9**


OS-KUL-SUG-00 | Unbacked Equity Share Minting 10


OS-KUL-SUG-01 | Missing Share Type Validation 11


OS-KUL-SUG-02 | Absence of Pool-Position Validation 12


OS-KUL-SUG-03 | Risk of Debt Share Dilution 13


OS-KUL-SUG-04 | Missing Validation Logic 14


OS-KUL-SUG-05 | Code Refactoring 15


OS-KUL-SUG-06 | Code Maturity 16


**Appendices**


**Vulnerability** **Rating** **Scale** **17**


**Procedure** **18**


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 18


**01** **—** **Executive** **Summary**

## Overview


assessment was conducted between May 29th and June 20th, 2025. For more information on our auditing


methodology, refer to Appendix B.

## Key Findings


We produced 9 findings throughout this audit engagement.


In particular, we identified a vulnerability the position core does not verify that the correct Supply Pool


object is utilized during liquidation, allowing a liquidator to exploit mismatched share types and receive


rewards without repaying debt (OS-KUL-ADV-00). Furthermore, we highlighted an instance of precision


loss due to division before multiplication when computing the amount of token X locked in the LP position


for a given price and liquidity (OS-KUL-ADV-01).


We also made recommendations regarding modifications to the codebase for improved functionality and


reduced redundancy (OS-KUL-SUG-05) and suggested the need to ensure adherence to coding best


practices (OS-KUL-SUG-06). Moreover, we advised adding share type assertions to prevent incorrect


dept repayments (OS-KUL-SUG-01), and incorporating additional safety checks within the codebase to


mitigate potential security issues (OS-KUL-SUG-04).


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 18


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/kunalabs-io/sui-smart-](https://github.com/kunalabs-io/sui-smart-contracts)


[contracts.](https://github.com/kunalabs-io/sui-smart-contracts) This audit was performed against [8eb311b.](https://github.com/kunalabs-io/sui-smart-contracts/commit/8eb311b1189cdc8cc1a79a22c5874c40d210bea5)


**Brief** **descriptions** **of** **the** **programs** **are** **as** **follows:**



access-management





Enables users to create and manage leveraged concentrated liquidity
leverage

positions in CLMM protocols such as Cetus and Bluefin.


© 2025 Otter Audits LLC. All Rights Reserved. 3 / 18


**03** **—** **Findings**


Overall, we reported 9 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.



© 2025 Otter Audits LLC. All Rights Reserved. 4 / 18


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


**ID** **Severity** **Status** **Description**



uidation, allowing a liquidator to exploit mis

matched share types and receive rewards with

out repaying debt.


fore multiplication, which may result in precision


uidity.



OS-KUL-ADV-00


OS-KUL-ADV-01





© 2025 Otter Audits LLC. All Rights Reserved. 5 / 18


Kuna Labs Audit 04 - Vulnerabilities


**Description**


|SupplyPool<X, SX0>|Col2|
|---|---|
|**`SupplyPool`**|instance|









|SupplyPool<X, SX1>|to|Col3|liquidate_col_y|
|---|---|---|---|
|ttempting to repay with|ttempting to repay with|**`SX1`**|results in no repay|


function still proceeds to grant rewards. This results in the liquidator receiving collateral without reducing


any debt.


© 2025 Otter Audits LLC. All Rights Reserved. 6 / 18


Kuna Labs Audit 04 - Vulnerabilities


**Remediation**


**Patch**


Resolved in [6116084](https://github.com/kunalabs-io/sui-smart-contracts/commit/61160843b666ee3b011f05bb040471fdffee7cf9) and [02b13e0.](https://github.com/kunalabs-io/sui-smart-contracts/commit/02b13e026966f03e1b52f4c3205a4f792207edb7)


© 2025 Otter Audits LLC. All Rights Reserved. 7 / 18


Kuna Labs Audit 04 - Vulnerabilities


**Description**


liquidation logic.









**Remediation**


merical accuracy.


**Patch**


Resolved in [ad08f8c.](https://github.com/kunalabs-io/sui-smart-contracts/commit/ad08f8c2141e1344aafa4642817c08b20465f8ef)


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 18


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.



OS-KUL-SUG-00



shares if the registry is reset to zero, enabling a malicious user to drain real



OS-KUL-SUG-01 Certain functions lack share type checks, risking incorrect debt repayments.


OS-KUL-SUG-02

the LP in the position.



OS-KUL-SUG-03


OS-KUL-SUG-04


OS-KUL-SUG-05


OS-KUL-SUG-06



resulting in the loss of existing debt share value.


There are several instances where proper validation checks may be incor

porated within the codebase to make it more robust and secure.


Recommendation for updating the codebase to improve functionality and


reducing redundancy.


Suggestions regarding inconsistencies in the codebase and ensuring ad

herence to coding best practices.



© 2025 Otter Audits LLC. All Rights Reserved. 9 / 18


Kuna Labs Audit 05 - General Findings


**Unbacked** **Equity** **Share** **Minting** OS-KUL-SUG-00


**Description**

|decrease_value_x64|Col2|Col3|
|---|---|---|
|with|**`value_x64`**|pass|



_>__ _kai/leverage/core/sources/primitives/equity.move_ rust

```
  public fun increase_value_and_issue_x64<T>(
    registry: &mut EquityRegistry<T>,
    value_x64: u128,
  ): EquityShareBalance<T> {
    if (registry.underlying_value_x64 == 0) {
      registry.underlying_value_x64 = value_x64;
      registry.supply_x64 = value_x64;
      return EquityShareBalance { value_x64 }
    };
    [...]
  }

```

**Remediation**

|Add a guard in|increase_value_and_issue_x64|Col3|
|---|---|---|
|**`registry.underlying_value_x64`** **`==`** **`0`**|**`registry.underlying_value_x64`** **`==`** **`0`**|.|



**Patch**


Resolved in [76b2dc7.](https://github.com/kunalabs-io/sui-smart-contracts/commit/76b2dc75dfb6b2e9633cf83d189b60f1f434797e)


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 18


Kuna Labs Audit 05 - General Findings


**Missing** **Share** **Type** **Validation** OS-KUL-SUG-01


**Description**


include these safety assertions to enforce share type correctness. To maintain protocol integrity, the


same type checks should be added to the deleveraging functions and extended to all functions interacting


**Remediation**


**Patch**


Resolved in [d5e3404.](https://github.com/kunalabs-io/sui-smart-contracts/commit/d5e3404b5a912b645522ffca9ffe65e85bfbc515)


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 18


Kuna Labs Audit 05 - General Findings


**Absence** **of** **Pool-Position** **Validation** OS-KUL-SUG-02


**Description**


or empty pools, resulting in incorrect fee accounting.


**Remediation**


**Patch**


Resolved in [3d7cb98.](https://github.com/kunalabs-io/sui-smart-contracts/commit/3d7cb982f7c116031db2790892a56380aedfc9d8)


© 2025 Otter Audits LLC. All Rights Reserved. 12 / 18


Kuna Labs Audit 05 - General Findings


**Risk** **of** **Debt** **Share** **Dilution** OS-KUL-SUG-03


**Description**

|avior. However,|Col2|increase_liability_and_issue_x64|
|---|---|---|
|**`liability_value_x64`** **`==`** **`0`**|**`liability_value_x64`** **`==`** **`0`**|**`liability_value_x64`** **`==`** **`0`**|
|s in|**`DebtRegistry<T>`**|**`DebtRegistry<T>`**|



As a result, users holding valid shares may lose their value.


_>__ _kai/leverage/core/sources/primitives/debt.move_ rust

```
  public fun increase_liability_and_issue_x64<T>(
    registry: &mut DebtRegistry<T>,
    value_x64: u128,
  ): DebtShareBalance<T> {
    if (registry.liability_value_x64 == 0) {
      registry.liability_value_x64 = value_x64;
      registry.supply_x64 = value_x64;
      return DebtShareBalance { value_x64 }
    };
    [...]
  }

```

**Remediation**


**Patch**


The Kuna Labs team acknowledged this issue.


© 2025 Otter Audits LLC. All Rights Reserved. 13 / 18


Kuna Labs Audit 05 - General Findings


**Missing** **Validation** **Logic** OS-KUL-SUG-04


**Description**


aligns with the expected debt share type to prevent misconfigurations.


3. In the current implementation, it is possible for a single pool to have multiple configs. As a result,


Restrict a pool to a single config.


**Remediation**


Update the codebase with the above checks.


**Patch**


1. Issue #1 resolved in [d5e3404.](https://github.com/kunalabs-io/sui-smart-contracts/commit/d5e3404b5a912b645522ffca9ffe65e85bfbc515)


2. Issue #2 resolved in [be2918c.](https://github.com/kunalabs-io/sui-smart-contracts/commit/be2918c3a30c61ba62ebe737ceff3b08d2ac8aba)


© 2025 Otter Audits LLC. All Rights Reserved. 14 / 18


Kuna Labs Audit 05 - General Findings


**Code** **Refactoring** OS-KUL-SUG-05


**Description**


looping and interpolation.


reduce accuracy. Downstream logic will benefit from retaining full millisecond precision.


_>__ _kai/leverage/core/sources/util.move_ rust

```
     /// Get current clock timestamp in seconds.
     public fun timestamp_sec(clock: &Clock): u64 {
       clock::timestamp_ms(clock) / 1000
     }

```

**Remediation**


Incorporate the above refactors.


© 2025 Otter Audits LLC. All Rights Reserved. 15 / 18


Kuna Labs Audit 05 - General Findings


**Code** **Maturity** OS-KUL-SUG-06


**Description**


_>__ _kai/leverage/core/sources/util.move_ rust

```
     public fun divide_and_round_up_u128(a: u128, b: u128): u128 {
       (a + b - 1) / b
     }

     public fun divide_and_round_up_u256(a: u256, b: u256): u256 {
       (a + b - 1) / b
     }

```

2. Several setter functions lack input validation, which may result in unsafe or illogical configuration


values. Add sanity checks to ensure values remain within acceptable bounds.


**Remediation**


Implement the above-mentioned suggestions.


**Patch**


1. Issue #1 resolved in [0a779eb.](https://github.com/kunalabs-io/sui-smart-contracts/commit/0a779ebec7d8bfe62602241a19feb93dd566e78d)


© 2025 Otter Audits LLC. All Rights Reserved. 16 / 18


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


© 2025 Otter Audits LLC. All Rights Reserved. 17 / 18


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


© 2025 Otter Audits LLC. All Rights Reserved. 18 / 18


