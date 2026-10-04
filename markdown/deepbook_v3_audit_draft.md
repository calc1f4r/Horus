# **Mysten Deepbook V3**

Security Assessment


April 15th, 2025 - Prepared by OtterSec


Sangsoo Kang [sangsoo@osec.io](mailto:sangsoo@osec.io)


Michał Bochnak [embe221ed@osec.io](mailto:embe221ed@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


**Scope** **3**


**Findings** **4**


**Vulnerabilities** **5**


OS-MDV-ADV-00 | Fee Accounting Inconsistency 6


OS-MDV-ADV-01 | Lack of Revoke Function 7


**General** **Findings** **8**


OS-MDV-SUG-00 | Inaccurate Swap Output Estimation 9


OS-MDV-SUG-01 | Rounding Error in Quote Calculation 10


OS-MDV-SUG-02 | Code Maturity 11


**Appendices**


**Vulnerability** **Rating** **Scale** **12**


**Procedure** **13**


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 13


**01** **—** **Executive** **Summary**

## Overview


between March 12th and April 11th, 2025. For more information on our auditing methodology, refer to


Appendix B.

## Key Findings


We produced 5 findings throughout this audit engagement.


In particular, we identified several vulnerabilities in the fee computation logic where, when paying fees in


DEEP, a zero deep quantity causes the fee to be incorrectly calculated as base or quote (OS-MDV-ADV

00), and a lack of revoke functions for caps of balance manager (OS-MDV-ADV-01).


We also made recommendations for modifying the codebase to improve functionality and ensure adherence


to coding best practices (OS-MDV-SUG-02), and highlighted the possibility of inaccurate results for


(OS-MDV-SUG-00). Furthermore, setting a very small lot size may create rounding errors, reducing price


granularity and resulting in inaccurate or unfair trade valuations (OS-MDV-SUG-01).


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 13


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/MystenLabs/deepbookv3.](https://github.com/MystenLabs/deepbookv3)


This audit was performed against commit [2c04083.](https://github.com/MystenLabs/deepbookv3/commit/2c0408375e933497f5c0a155fda38bc178b38d7a)


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**


A decentralized central limit order book (CLOB) built on the Sui


blockchain, designed for high-performance, low-latency trading. It



deepbookV3



introduces features such as flashloans, governance, and improved ac

count abstraction, leveraging Sui’s parallel execution to enable efficient


on-chain order matching.



© 2025 Otter Audits LLC. All Rights Reserved. 3 / 13


**03** **—** **Findings**


Overall, we reported 5 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.



© 2025 Otter Audits LLC. All Rights Reserved. 4 / 13


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.



OS-MDV-ADV-00


OS-MDV-ADV-01





then the fee is calculated using either the base or the


quote instead of DEEP.


function ineffective.



© 2025 Otter Audits LLC. All Rights Reserved. 5 / 13


Mysten Deepbook V3 Audit 04 - Vulnerabilities


**Description**


instead, resulting in the fee being paid in a way that does not match the user’s intention.


_>__ _deepbook/sources/vault/deep_price.move_ rust

```
  public(package) fun fee_quantity([...]): Balances {
   [...]
    if (deep_quantity > 0) {
      balances::new(0, 0, deep_quantity)
    } else if (is_bid) {
      balances::new(
         0,
         math::mul(
           quote_quantity,
           constants::fee_penalty_multiplier(),
         ),
         0,
      )
    } [...]
  }

```

**Remediation**


**Patch**


Fixed in [PR#357.](https://github.com/MystenLabs/deepbookv3/pull/357)


© 2025 Otter Audits LLC. All Rights Reserved. 6 / 13


Mysten Deepbook V3 Audit 04 - Vulnerabilities


**Description**


list. As a result, it’s not possible to remove the cap using the existing revoke function.


_>__ _deepbook/sources/balance_manager.move_ rust

```
  public(package) fun generate_proof_as_depositor(
    balance_manager: &BalanceManager,
    deposit_cap: &DepositCap,
    ctx: &TxContext,
  ): TradeProof {
    assert!(
      balance_manager.id() == deposit_cap.balance_manager_id,
      EDepositCapBalanceManagerMismatch,
    );

    TradeProof {
      balance_manager_id: object::id(balance_manager),
      trader: ctx.sender(),
    }
  }

```

**Remediation**


Add the depositor and withdrawer to the allowed list in creation, and check that they’re on the list during


verification.


**Patch**


Fixed in [PR#348.](https://github.com/MystenLabs/deepbookv3/pull/348)


© 2025 Otter Audits LLC. All Rights Reserved. 7 / 13


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.



OS-MDV-SUG-00


OS-MDV-SUG-01


OS-MDV-SUG-02



and actual execution.


granularity and resulting in inaccurate or unfair trade valuations.


Recommendations to improve functionality and ensure adherence to coding


best practices.



© 2025 Otter Audits LLC. All Rights Reserved. 8 / 13


Mysten Deepbook V3 Audit 05 - General Findings


**Inaccurate** **Swap** **Output** **Estimation** OS-MDV-SUG-00


**Description**


result in discrepancies between simulation and actual execution, especially for large trades.


**Remediation**


**Patch**


Fixed in [0606ed9.](https://github.com/MystenLabs/deepbookv3/commits/0606ed92e0941bf82b71d3d01c7c913d5668a129)


© 2025 Otter Audits LLC. All Rights Reserved. 9 / 13


Mysten Deepbook V3 Audit 05 - General Findings


**Rounding** **Error** **in** **Quote** **Calculation** OS-MDV-SUG-01


**Description**


is set too small, it can introduce rounding errors in quote calculations, especially with large order sizes.


is 1000, both 1000 and 1999 units of base asset may map to the same quote value, creating pricing


inaccuracies.


**Remediation**


Monitor the configuration of the permissionless pool.


**Patch**


Fixed in [PR#349.](https://github.com/MystenLabs/deepbookv3/pull/349)


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 13


Mysten Deepbook V3 Audit 05 - General Findings


**Code** **Maturity** OS-MDV-SUG-02


**Description**

|Col1|fee_quantity|
|---|---|
|**`if`** **`(!fill.expired())`**|**`if`** **`(!fill.expired())`**|



no meaningful actions related to fees. This renders the conditional check useless and may thus be


removed.


_>__ _deepbook/sources/state/state.move_ rust

```
     fun process_fills(self: &mut State, fills: &mut vector<Fill>, ctx: &TxContext) {
       let mut i = 0;
       let num_fills = fills.length();
       while (i < num_fills) {
          [...]
          if (!fill.expired()) {
            fill.set_fill_maker_fee(&fee_quantity);
            self.history.add_volume(base_volume, account.active_stake());
            self.history.add_total_fees_collected(fee_quantity);
          } else {
            account.add_settled_balances(fee_quantity);
          };

          i = i + 1;
       };
     }

```

clarity and semantics.


**Remediation**


Implement the above mentioned suggestions.


**Patch**


Issue #1 and #2 resolved in [PR#342.](https://github.com/MystenLabs/deepbookv3/pull/342)


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 13


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


© 2025 Otter Audits LLC. All Rights Reserved. 12 / 13


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


© 2025 Otter Audits LLC. All Rights Reserved. 13 / 13


