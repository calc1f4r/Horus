# **Echelon Staked LPT**

Security Assessment


April 18th, 2025 - Prepared by OtterSec


Andreas Mantzoutas [andreas@osec.io](mailto:andreas@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


Scope 2


**Findings** **3**


**Vulnerabilities** **4**


OS-ESL-ADV-00 | Risk of Borrowing Undervalued Collateral 5


**Appendices**


**Vulnerability** **Rating** **Scale** **6**


**Procedure** **7**


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 7


**01** **—** **Executive** **Summary**

## Overview


conducted between April 6th and April 10th, 2025. For more information on our auditing methodology,


refer to Appendix B.

## Key Findings


We produced 1 finding throughout this audit engagement.


is currently allowed due to oracle mispricing. While safe as collateral, this poses a risk if such assets are


borrowed at below-market value (OS-ESL-ADV-00).

## Scope


The source code was delivered to us in a Git repository at


[https://github.com/EchelonMarket/echelon-modules.](https://github.com/EchelonMarket/echelon-modules) This audit was performed against [PR#271.](https://github.com/EchelonMarket/echelon-modules/pull/271)


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**



echelon-staked-lpt


(PR#271)



The PR adds support for adding Thala staked LPTs (xLPTs) as collateral


in Echelon pools.



© 2025 Otter Audits LLC. All Rights Reserved. 2 / 7


**02** **—** **Findings**


Overall, we reported 1 finding.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.


© 2025 Otter Audits LLC. All Rights Reserved. 3 / 7


**03** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


**ID** **Severity** **Status** **Description**



is currently allowed due to oracle mispricing. While


safe as collateral, this poses a risk if such assets are


borrowed at below-market value.



OS-ESL-ADV-00





© 2025 Otter Audits LLC. All Rights Reserved. 4 / 7


Echelon Staked LPT Audit 03 - Vulnerabilities


**Description**


does not impact their utilization as collateral—effectively acting as a reduced collateral factor—it is critical


to prevent borrowing of these undervalued assets. An undervalued oracle price only limits borrowing


power, which is acceptable as long as borrowing is not permitted against such assets.


**Remediation**


**Patch**


Fixed in [332854e.](https://github.com/EchelonMarket/echelon-modules/commit/332854e40071772659b605246056b2e3be109fbf)


© 2025 Otter Audits LLC. All Rights Reserved. 5 / 7


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


© 2025 Otter Audits LLC. All Rights Reserved. 6 / 7


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


© 2025 Otter Audits LLC. All Rights Reserved. 7 / 7


