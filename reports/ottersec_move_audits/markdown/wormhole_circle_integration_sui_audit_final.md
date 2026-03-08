# **Circle Integration Sui**

Security Assessment


December 23rd, 2024 - Prepared by OtterSec


Robert Chen [r@osec.io](mailto:r@osec.io)


Michał Bochnak [embe221ed@osec.io](mailto:embe221ed@osec.io)


Sangsoo Kang [sangsoo@osec.io](mailto:sangsoo@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


Scope 2


**General** **Findings** **3**


OS-CIS-SUG-00 | Code Maturity 4


**Appendices**


**Vulnerability** **Rating** **Scale** **5**


**Procedure** **6**


© 2024 Otter Audits LLC. All Rights Reserved. 1 / 6


**01** **—** **Executive** **Summary**

## Overview


assessment was conducted between December 13th and December 18th, 2024. For more information


on our auditing methodology, refer to Appendix B.

## Key Findings


We produced 1 suggestion throughout this audit engagement.


We made suggestions regarding inconsistencies in the codebase and ensuring adherence to


best development practices (OS-CIS-SUG-00).

## Scope


The source code was delivered to us in a Git repository at [https://github.com/wormholelabs-xyz/wormhole-](https://github.com/wormholelabs-xyz/wormhole-circle-integration-sui)


[circle-integration-sui.](https://github.com/wormholelabs-xyz/wormhole-circle-integration-sui) This audit was performed against [da34eb1.](https://github.com/wormholelabs-xyz/wormhole-circle-integration-sui/commit/da34eb17b00debedadc96829233a34b995427469)


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**


The Wormhole-Circle-Integration-SUI enables cross-chain token

wormhole-circle
transfers combined with custom payloads by leveraging Circle’s CCTP

integration-sui

and Wormhole protocols.


© 2024 Otter Audits LLC. All Rights Reserved. 2 / 6


**02** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.


Suggestions regarding inconsistencies in the codebase and ensuring adherence

OS-CIS-SUG-00

to coding best practices.


© 2024 Otter Audits LLC. All Rights Reserved. 3 / 6


Circle Integration Sui Audit 02 - General Findings


**Code** **Maturity** OS-CIS-SUG-00


**Description**


burning an invalid amount.


_>__ _sui/packages/wormhole_cctp/sources_ _/wormhole_cctp.move_ move

```
     public fun burn<Auth: drop, T: drop>(
       auth: Auth,
       coins: Coin<T>,
       [...]
     ): (DepositForBurnWithCallerTicket<T, Auth>, PublishTicket<Auth>) {
       let publish_ticket = PublishTicket {
          burn_token: token_messenger_minter::token_utils::calculate_token_id<T>(),
          mint_recipient,
          amount: coins.value(),
          destination_domain,
          destination_caller,
          wormhole_nonce,
          payload,
       };
       [...]
     }

```

**Remediation**


Implement the above-mentioned suggestions.


© 2024 Otter Audits LLC. All Rights Reserved. 4 / 6


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


© 2024 Otter Audits LLC. All Rights Reserved. 5 / 6


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


© 2024 Otter Audits LLC. All Rights Reserved. 6 / 6


