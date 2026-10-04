# **Lombard Finance**

Security Assessment


December 6th, 2024 - Prepared by OtterSec


Michał Bochnak [embe221ed@osec.io](mailto:embe221ed@osec.io)


Sangsoo Kang [sangsoo@osec.io](mailto:sangsoo@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


**Scope** **3**


**Findings** **4**


**Vulnerabilities** **5**


OS-LBF-ADV-00 | Improper Mint Limit Reset 6


OS-LBF-ADV-01 | Lack of Configurable Delay Setting in Timelock 7


**General** **Findings** **8**


OS-LBF-SUG-00 | Missing Validation Logic 9


**Appendices**


**Vulnerability** **Rating** **Scale** **10**


**Procedure** **11**


© 2024 Otter Audits LLC. All Rights Reserved. 1 / 11


**01** **—** **Executive** **Summary**

## Overview


conducted between December 2nd and December 5th, 2024. For more information on our auditing


methodology, refer to Appendix B

## Key Findings


We produced 3 findings throughout this audit engagement.


In particular, we identified a critical vulnerability, where the minting function incorrectly resets the remaining


mint limit during a new epoch, as it assigns the limit value directly instead of referencing (OS-LBF-ADV

00), and another issue concerning upgrade authorization function, which utilizes a hardcoded delay of


24 hours instead of the configurable delay, limiting its flexibility and disregarding custom delay settings


(OS-LBF-ADV-01).


We also made recommendations for modifying the codebase to improve functionality and prevent unex

pected outcomes (OS-LBF-SUG-00).


© 2024 Otter Audits LLC. All Rights Reserved. 2 / 11


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/lombard-finance/sui-](https://github.com/lombard-finance/sui-contracts)


[contracts.](https://github.com/lombard-finance/sui-contracts) This audit was performed against commit [45400c0.](https://github.com/lombard-finance/sui-contracts/commit/45400c0b8a8da0f29438990887dc215f2f172fbe)


**A** **brief** **description** **of** **the** **programs** **is** **as** **follows:**


The Sui contracts of the Lombard Finance Protocol bridge Bitcoin into



sui-contracts



DeFi through LBTC, a regulated, yield-bearing token backed 1:1 by


BTC.



© 2024 Otter Audits LLC. All Rights Reserved. 3 / 11


**03** **—** **Findings**


Overall, we reported 3 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.









© 2024 Otter Audits LLC. All Rights Reserved. 4 / 11


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


The minting function incorrectly resets the remaining





regarding custom delay settings.



© 2024 Otter Audits LLC. All Rights Reserved. 5 / 11


Lombard Finance Audit 04 - Vulnerabilities


**Description**

|ury::mint_and_transfer ury::mint_and_transfer, the line left left get_cap_mut(treasury, ctx.sender()) get_cap_mut(treasury, ctx.sender())|Col2|Col3|
|---|---|---|
|**`get_cap_mut(treasury,`** **`ctx.sender())`**|**`get_cap_mut(treasury,`** **`ctx.sender())`**|**`get_cap_mut(treasury,`** **`ctx.sender())`**|
|ociated with the sender. This implies|**`left`**|i|



_>__ _lbtc/sources/treasury.move_ move

```
  public fun mint_and_transfer<T>(
   [...]
  ) {
    [...]
    // Get the MinterCap and check the limit; if a new epoch - reset it
    let MinterCap { limit, epoch, mut left } = get_cap_mut(treasury, ctx.sender());
    // Reset the limit if this is a new epoch
    if (ctx.epoch() > *epoch) {
      left = limit;
      *epoch = ctx.epoch();
    };

    // Check that the amount is within the mint limit; update the limit
    assert!(amount <= *left, EMintLimitExceeded);
    *left = *left - amount;
    [...]
  }

```

**Remediation**


**Patch**


Fixed in [ecf55e3.](https://github.com/lombard-finance/sui-contracts/commit/ecf55e33e268bed8d1980bffd8cfca4e36dc6892)


© 2024 Otter Audits LLC. All Rights Reserved. 6 / 11


Lombard Finance Audit 04 - Vulnerabilities


**Description**


enforce the time restriction on upgrades, rather than referencing the configurable delay stored in


delay feature.









**Remediation**


**Patch**


Fixed in [d2e3a5d.](https://github.com/lombard-finance/sui-contracts/commit/d2e3a5d9748fc91a490666c7746791bb8cd11f3a)


© 2024 Otter Audits LLC. All Rights Reserved. 7 / 11


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.


There are several instances where proper validation is not done, resulting in

OS-LBF-SUG-00

potential security issues.


© 2024 Otter Audits LLC. All Rights Reserved. 8 / 11


Lombard Finance Audit 05 - General Findings


**Missing** **Validation** **Logic** OS-LBF-SUG-00


**Description**

|e assertion:|assert!(delay_ms == MS_24_HOURS || delay_ms == MS_48_HOURS)|Col3|Col4|Col5|
|---|---|---|---|---|
|**`EInvalidDelayValue`**|**`EInvalidDelayValue`**|error, in|**`new_timelock`**|to validate that the provided delay value|



is one of the allowed options (24 hours or 48 hours).


_>__ _timelock_policy/sources/timelock_upgrade.move_ move

```
     /// Creates a new TimelockCap with the specified delay.
     public fun new_timelock(
       upgrade_cap: UpgradeCap,
       delay_ms: u64,
       ctx: &mut TxContext,
     ): TimelockCap {
       TimelockCap {
          id: object::new(ctx),
          upgrade_cap,
          last_authorized_time: 0,
          delay_ms,
       }
     }

```

a valid public key before it is utilized in the multisig address validation.


zero, which impacts the correctness of these operations. Allowing zero-value minting or burning


is unnecessary, wastes computational resources, and adds noise to event logs. Add validation to


**Remediation**


Incorporate the above-mentioned validations into the codebase.


**Patch**


1. Issue #1 fixed in [d2e3a5d.](https://github.com/lombard-finance/sui-contracts/commit/d2e3a5d9748fc91a490666c7746791bb8cd11f3a)


2. Issue #2 fixed in [00d1dfc.](https://github.com/lombard-finance/sui-contracts/commit/00d1dfc934693095b81dce092d2cf9b73c728521)


3. Issue #3 fixed in [0f00717.](https://github.com/lombard-finance/sui-contracts/commit/0f00717904b405f3736dd689af3e8e27042e3231)


© 2024 Otter Audits LLC. All Rights Reserved. 9 / 11


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


© 2024 Otter Audits LLC. All Rights Reserved. 10 / 11


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


© 2024 Otter Audits LLC. All Rights Reserved. 11 / 11


