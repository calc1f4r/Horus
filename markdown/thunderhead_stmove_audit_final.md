# **Thunderhead Labs**

Security Assessment


December 4th, 2024 - Prepared by OtterSec


Nicholas R. Putra [nicholas@osec.io](mailto:nicholas@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


**Scope** **3**


**Findings** **4**


**General** **Findings** **5**


OS-THL-SUG-00 | Code Refactoring 6


OS-THL-SUG-01 | Code Maturity 7


**Appendices**


**Vulnerability** **Rating** **Scale** **8**


**Procedure** **9**


© 2024 Otter Audits LLC. All Rights Reserved. 1 / 9


**01** **—** **Executive** **Summary**

## Overview


was conducted between November 27th and November 28th, 2024. For more information on our auditing


methodology, refer to Appendix B.

## Key Findings


We produced 2 findings throughout this audit engagement.


We recommended modifying the codebase to mitigate potential security issues and improve functionality


(OS-THL-SUG-00) and made suggestions regarding inconsistencies in the codebase to ensure adherence


to best development practices (OS-THL-SUG-01).


© 2024 Otter Audits LLC. All Rights Reserved. 2 / 9


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/thunderhead-labs/stmove-](https://github.com/thunderhead-labs/stmove-contracts-eth)


[contracts-eth.](https://github.com/thunderhead-labs/stmove-contracts-eth) This audit was performed against commit [4a28edf.](https://github.com/thunderhead-labs/stmove-contracts-eth/commit/4a28edf9ab9480f350cbf4397aa3175382adb9a3)


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**


The system employs a non-transferable, rebasing token mechanism


to simulate APY growth by periodically increasing user balances. It



stmove-contracts

eth



as a placeholder to represent future staking rewards or allocations.



© 2024 Otter Audits LLC. All Rights Reserved. 3 / 9


**03** **—** **Findings**


Overall, we reported 2 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.



© 2024 Otter Audits LLC. All Rights Reserved. 4 / 9


**04** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.


Recommendations for modifying the codebase to mitigate potential security

OS-THL-SUG-00

issues and improve functionality.


Suggestions regarding inconsistencies in the codebase and ensuring adherence

OS-THL-SUG-01

to coding best practices.


© 2024 Otter Audits LLC. All Rights Reserved. 5 / 9


Thunderhead Labs Audit 04 - General Findings


**Code** **Refactoring** OS-THL-SUG-00


**Description**


rate. However, this may not accurately reflect the current state of the share rate, as it is dynamic and





these conditions are not met, the function should revert with an error.


**Remediation**


Incorporate the above-stated refactors.


© 2024 Otter Audits LLC. All Rights Reserved. 6 / 9


Thunderhead Labs Audit 04 - General Findings


**Code** **Maturity** OS-THL-SUG-01


**Description**


improve clarity.


_>__ _src/Lock.sol_ solidity

```
     function redesignate(bytes32 moveAddress) public {
       if (frozen) {
          revert LockPeriodEnded();
       }
       emit Redesignation(designated[msg.sender], moveAddress);
       designated[msg.sender] = moveAddress;
     }

```

and is not meant to be in production code.


**Remediation**


Implement the above-mentioned suggestions.


© 2024 Otter Audits LLC. All Rights Reserved. 7 / 9


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


© 2024 Otter Audits LLC. All Rights Reserved. 8 / 9


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


© 2024 Otter Audits LLC. All Rights Reserved. 9 / 9


