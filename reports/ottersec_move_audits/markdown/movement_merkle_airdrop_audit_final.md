# **Movedrop L2**

Security Assessment


May 23rd, 2025 - Prepared by OtterSec


Andreas Mantzoutas [andreas@osec.io](mailto:andreas@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


**Scope** **3**


**Findings** **4**


**Vulnerabilities** **5**


OS-MVD-ADV-00 | Merkle Proof Replay 6


OS-MVD-ADV-01 | Flawed Merkle Proof Verification Logic 7


OS-MVD-ADV-02 | Missing Admin Validation Locks Funds Permanently 8


OS-MVD-ADV-03 | Event Spoofing via Resource Index Collision 9


**General** **Findings** **10**


OS-MVD-SUG-00 | Inefficient Claim Tracking Mechanism 11


OS-MVD-SUG-01 | Lack of Domain Separation 12


**Appendices**


**Vulnerability** **Rating** **Scale** **13**


**Procedure** **14**


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 14


**01** **—** **Executive** **Summary**

## Overview


between May 6th and May 7th, 2025. For more information on our auditing methodology, refer to


Appendix B.

## Key Findings


We produced 6 findings throughout this audit engagement.


In particular, we identified a critical vulnerability where the same Merkle proof can be reused multiple


times by providing different leaf indices, leading to multiple claims and extracting more than the intended


allocation (OS-MVD-ADV-00). Additionally, we highlighted an inconsistency between the result expected


(OS-MVD-ADV-01).


We also made recommendations to improve the codebase’s efficiency and security hardening. Specifically,


we advised against using a vector to track claims, as each claim requires full deserialization, resulting


in increased transaction costs (OS-MVD-SUG-00). Lastly, we proposed the incorporation of domain


separators to mitigate second preimage attacks against the Merkle tree, particularly if future changes


allow leaf nodes to reach 64 bytes in length (OS-MVD-SUG-01).


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 14


**02** **—** **Scope**


The source code was delivered to us in a git repository at [https://github.com/movementlabsxyz/movedrop-](https://github.com/movementlabsxyz/movedrop-l2)


[l2.](https://github.com/movementlabsxyz/movedrop-l2) This audit was performed against commit [d6b1a1d.](https://github.com/movementlabsxyz/movedrop-l2/blob/d6b1a1da23ae925368729f09ff03a2acf198dc85)


**A** **brief** **description** **of** **the** **programs** **is** **as** **follows:**


The movedrop-l2 module enables token distributions via resource ac

counts managed by an admin. The direct airdrop supports batch trans


movedrop-l2



fers to explicit recipient lists, while the Merkle airdrop allows users to


claim tokens by proving inclusion in a Merkle tree, optimizing for gas


efficiency.



© 2025 Otter Audits LLC. All Rights Reserved. 3 / 14


**03** **—** **Findings**


Overall, we reported 6 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.









© 2025 Otter Audits LLC. All Rights Reserved. 4 / 14


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities identified during our audit. These vulnerabilities


have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


Flawed comparison logic leads to incorrect proof ver




loss.


it vulnerable to event spoofing.



© 2025 Otter Audits LLC. All Rights Reserved. 5 / 14


Movedrop L2 Audit 04 - Vulnerabilities


**Description**


along with the proof and the leaf index of their node. The function then constructs the leaf’s hash using


the caller’s address and the amount, validates the proof, and, if successful, transfers the amount to the


user while marking the corresponding leaf index as claimed to prevent double claims.


_>__ _sources/merkle_airdrop.move_ rust

```
  public entry fun claim(
    recipient: &signer,
    amount: u64,
    proof: vector<vector<u8>>,
    leaf_index: u64
  ) acquires AirdropData {
    ...
    let leaf = hash_leaf(recipient_addr, amount);

    // Verify the Merkle proof
    assert!(verify_proof(leaf, proof, airdrop_data.merkle_root),
      error::invalid_argument(EINVALID_PROOF));
    ...
    aptos_account::transfer(&resource_signer, recipient_addr, amount);
    ...
    }

```

However, the issue arises because the leaf index is neither validated against the provided leaf node nor


included in the hash or proof verification. This oversight allows the same valid Merkle proof to be reused


with different leaf indices, enabling multiple unauthorized claims from a single valid proof.


**Remediation**


Include the leaf index as part of the node’s hash during its construction.


**Patch**


Fixed in [78782bd.](https://github.com/movementlabsxyz/movedrop-l2/commit/78782bd319e2f153faf236df0087cf4f7cfbedda)


© 2025 Otter Audits LLC. All Rights Reserved. 6 / 14


Movedrop L2 Audit 04 - Vulnerabilities


**Description**


whether the first byte sequence is less than, equal to, or greater than the second, returning 0, 1, or 2,


to validate that the computed hash matches the expected Merkle root.









computation. Additionally, the function mistakenly returns true when the computed hash is merely less


than the Merkle root (i.e., when the comparison yields 0), rather than strictly equal. This flaw completely


disrupts the verification logic, enabling unauthorized claims while potentially invalidating legitimate ones.


**Remediation**


Update the conditions to properly validate the ordering logic and the final hash comparison


**Patch**


Fixed in [78782bd.](https://github.com/movementlabsxyz/movedrop-l2/commit/78782bd319e2f153faf236df0087cf4f7cfbedda)


© 2025 Otter Audits LLC. All Rights Reserved. 7 / 14


Movedrop L2 Audit 04 - Vulnerabilities


**Description**


derived from the signer’s address and a fixed seed, then stores the airdrop’s resources and locks the


specified amount within that account.









However, subsequent functions attempt to access the airdrop’s resources using a specific resource


This mismatch causes all operations to interact with the pre-determined resource account, ignoring any


user-specific instances. Consequently, if a user initializes an airdrop for their own address, the resources


are effectively locked and inaccessible, resulting in a permanent loss of funds.


**Remediation**


airdrops.


**Patch**


Fixed in [78782bd.](https://github.com/movementlabsxyz/movedrop-l2/commit/78782bd319e2f153faf236df0087cf4f7cfbedda)


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 14


Movedrop L2 Audit 04 - Vulnerabilities


**Description**


_>__ _sources/merkle_airdrop.move_ rust

```
  #[event]
  struct AirdropEvent has drop, store {
    resource_index: u64,
    num_recipients: u64,
    total_amount: u64,
    timestamp: u64
  }

|resource_index|Col2|is no|
|---|---|---|
|sults in|**`AirdropEvent`**|**`AirdropEvent`**|


```

actors to mimic the event details of legitimate airdrops, causing confusion in off-chain indexers and


analytics platforms.


**Remediation**


**Patch**


Fixed in [5fdd39c.](https://github.com/movementlabsxyz/movedrop-l2/commit/5fdd39c52661ecd3e553ec48eeff3847712c9527)


© 2025 Otter Audits LLC. All Rights Reserved. 9 / 14


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.


The bitmap-based claim tracking mechanism requires full deserialization on

OS-MVD-SUG-00

every claim, making large-scale airdrops inefficient and costly.


The lack of domain separation could make the Merkle tree susceptible to second

OS-MVD-SUG-01

preimage attacks.


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 14


Movedrop L2 Audit 05 - General Findings


**Inefficient** **Claim** **Tracking** **Mechanism** OS-MVD-SUG-00


**Description**


The current implementation tracks claims using a bitmap to prevent double-claiming. This bitmap is





While this design is space-efficient for on-chain storage, it introduces significant performance bottlenecks.


bit. As a result, gas costs scale linearly with the size of the airdrop, making large-scale distributions


increasingly inefficient and costly.


**Remediation**


enables sparse storage.


**Patch**


Fixed in [78782bd.](https://github.com/movementlabsxyz/movedrop-l2/commit/78782bd319e2f153faf236df0087cf4f7cfbedda)


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 14


Movedrop L2 Audit 05 - General Findings


**Lack** **of** **Domain** **Separation** OS-MVD-SUG-01


**Description**


The current implementation of the Merkle tree lacks domain separation and uses the same hashing


algorithm for both leaf and intermediate nodes. This design flaw allows leaf nodes and internal nodes to


be indistinguishable during hash computation. If the leaf nodes are exactly 64 bytes—the output size of


typical hash functions—the structure becomes vulnerable to second preimage attacks.


A second preimage attack occurs when an attacker is able to craft a different input that produces the same


hash as an existing one. In this context, an attacker could create a 64-byte leaf that hashes identically to


an internal node, potentially forging valid Merkle proofs and bypassing verification checks.


**Remediation**


Introduce domain separation by adding unique prefixes for leaf and intermediate nodes to prevent second


preimage collisions.


**Patch**


Fixed in [78782bd.](https://github.com/movementlabsxyz/movedrop-l2/commit/78782bd319e2f153faf236df0087cf4f7cfbedda)


© 2025 Otter Audits LLC. All Rights Reserved. 12 / 14


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


© 2025 Otter Audits LLC. All Rights Reserved. 13 / 14


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


© 2025 Otter Audits LLC. All Rights Reserved. 14 / 14


