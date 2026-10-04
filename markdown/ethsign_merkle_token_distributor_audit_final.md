# **Merkle Token Distributor**

Security Assessment


May 8th, 2025 - Prepared by OtterSec


Bartłomiej Wierzbiński [dark@osec.io](mailto:dark@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


**Scope** **3**


**Findings** **4**


**Vulnerabilities** **5**


OS-MTD-ADV-00 | Unrestricted Signer Access 6


OS-MTD-ADV-01 | Failure to Abort on Incorrect Merkle Proof 7


OS-MTD-ADV-02 | DOS via Front-Running Deployment Transaction 8


OS-MTD-ADV-03 | Improper Fee Collection Logic on Max Fee Bips 9


OS-MTD-ADV-04 | Risk of Overflow During Fee Calculation 10


**General** **Findings** **11**


OS-MTD-SUG-00 | Missing Validation Logic 12


OS-MTD-SUG-01 | Error Handling 13


OS-MTD-SUG-02 | Code Refactoring 15


OS-MTD-SUG-03 | Code Maturity 17


OS-MTD-SUG-04 | Code Optimization 19


OS-MTD-SUG-05 | Unutilized/Redundant Code 20


**Appendices**


**Vulnerability** **Rating** **Scale** **23**


**Procedure** **24**


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 24


**01** **—** **Executive** **Summary**

## Overview


conducted between April 1st and April 16th, 2025. For more information on our auditing methodology,


refer to Appendix B.

## Key Findings


We produced 11 findings throughout this audit engagement.


In particular, we identified several critical vulnerabilities, inlcuding one where the functionality for retrieving


the distribution signer is publicly accessible, allowing anyone to reconstruct a signer for any distributor


and withdraw its funds (OS-MTD-ADV-00), and another issue in the verification and claiming logic, which


fails to check the result of Merkle proof verification, allowing anyone to submit invalid proofs and steal


funds (OS-MTD-ADV-01).


Furthermore, the deployment logic is currently susceptible to a front-running attack, enabling an attacker


to preemptively deploy with the same project ID, causing the legitimate deployment to fail (OS-MTD

(OS-MTD-ADV-04).


We also made recommendations for implementing proper validations (OS-MTD-SUG-00) and explicit


checks to improve overall error handling (OS-MTD-SUG-01). We further suggested updating the code

base for improved functionality, efficiency, and overall clarity (OS-MTD-SUG-02). Lastly, we advised


adhering to coding best practices (OS-MTD-SUG-03) and removing redundant or unutilized code in

stances (OS-MTD-SUG-05).


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 24


**02** **—** **Scope**


The source code was delivered to us in a Git repository at [https://github.com/EthSign/merkle-token-](https://github.com/EthSign/merkle-token-distributor-move)


[distributor-move.](https://github.com/EthSign/merkle-token-distributor-move) This audit was performed against commit [8603a29.](https://github.com/EthSign/merkle-token-distributor-move/commit/8603a29a24277c4cb68bd130dba28aa94bde89bc)


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**


A program for secure token airdrops utilizing Merkle proofs, enabling

merkle-token
users to claim tokens by submitting a valid proof that verifies their

distributor

entitlement without storing individual claims on-chain.


© 2025 Otter Audits LLC. All Rights Reserved. 3 / 24


**03** **—** **Findings**


Overall, we reported 11 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.



© 2025 Otter Audits LLC. All Rights Reserved. 4 / 24


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.



OS-MTD-ADV-00


OS-MTD-ADV-01


OS-MTD-ADV-02


OS-MTD-ADV-03


OS-MTD-ADV-04





cessible, allowing anyone to reconstruct a signer


for any distributor and withdraw its funds.


of Merkle proof verification, allowing anyone to


submit invalid proofs and steal funds.


where an attacker may preemptively deploy with


deployment.


a flawed check, allowing distributors to bypass


fee payments.



© 2025 Otter Audits LLC. All Rights Reserved. 5 / 24


Merkle Token Distributor Audit 04 - Vulnerabilities


**Description**


accessible. This allows any external caller to retrieve a signer for any distributor resource account utilizing


on behalf of the distributor. It will be possible for the attacker to call the primary fungible store API and


withdraw funds stored by the distributor. Only modules trusted to act on behalf of distributors should be


allowed to utilize this function.


_>__ _sources/md_create2.move_ rust

```
  public fun get_distribution_signer(
    distribution_addr: address
  ): signer acquires DistributorFactory, ModuleInfo {
    let module_addr = get_module_address();
    let factory = borrow_global<DistributorFactory>(module_addr);
    let signer_cap = table::borrow(&factory.signer_caps, distribution_addr);
    account::create_signer_with_capability(signer_cap)
  }

```

**Remediation**


**Patch**


Resolved in [25238ec.](https://github.com/EthSign/merkle-token-distributor-move/pull/4/commits/25238ecf0eaffde9d431e40c35f51067259b3fcf)


© 2025 Otter Audits LLC. All Rights Reserved. 6 / 24


Merkle Token Distributor Audit 04 - Vulnerabilities


**Description**


but does not check its boolean return value. As a result, invalid Merkle proofs are not rejected, allowing


anyone to submit a fraudulent proof and still claim tokens. This enables malicious users to steal funds by


bypassing the intended verification process.









**Remediation**


aborts if the Merkle verification fails.


**Patch**


Resolved in [3fc010d.](https://github.com/EthSign/merkle-token-distributor-move/pull/4/commits/3fc010dd03efcdb0beccb3df7a673f8bf4650757)


© 2025 Otter Audits LLC. All Rights Reserved. 7 / 24


Merkle Token Distributor Audit 04 - Vulnerabilities


**Description**


will fail. This results in a denial of service for the legitimate deployer, preventing them from creating the


distributor.


_>__ _sources/md_create2.move_ rust

```
  // Deploy a new distributor instance
  public entry fun deploy(
    caller: &signer, project_id: String
  ) acquires DistributorFactory, ModuleInfo {
    [...]
    move_to(&resource_signer, distributor_data);
    table::add(&mut factory.signer_caps, resource_addr, resource_cap);
    table::add(&mut factory.deployments, copy project_id, resource_addr);
    [...]
  }

```

**Remediation**


Update the logic to ensure deployments utilize non-colliding, unique identifiers.


**Patch**


Acknowledged by the EthSign team as an intended design choice so as to align with the Solidity version.


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 24


Merkle Token Distributor Audit 04 - Vulnerabilities


**Description**


There is a flaw in the program’s current implementation of the fee collection logic. In









**Remediation**


is set.


**Patch**


implies zero fees


© 2025 Otter Audits LLC. All Rights Reserved. 9 / 24


Merkle Token Distributor Audit 04 - Vulnerabilities


**Description**


**`(token_transferred`** **`*`** **`fee_bips)`** **`/`** **`BIPS_PRECISION`** . This will overflow, especially if large token


amounts are involved, resulting in a runtime panic.


_>__ _sources/fee_collector.move_ rust

```
  public fun get_fee(
    distributor_address: address, token_transferred: u64
  ): u64 acquires FeeCollectorData, ModuleInfo {
    [...]
    (token_transferred * fee_bips) / BIPS_PRECISION
  }

```

**Remediation**


overflows.


**Patch**


Resolved in [6d988d7.](https://github.com/EthSign/merkle-token-distributor-move/pull/4/commits/6d988d7c7ef643aec9dc33d4f08988b5d76f24f6)


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 24


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.


There are several instances where proper validation is not performed, re
OS-MTD-SUG-00

sulting in potential issues.


Modifications to ensure the inclusion of explicit checks to prevent unex


OS-MTD-SUG-01


OS-MTD-SUG-02


OS-MTD-SUG-03



pected aborts or panics, improving the protocol’s robustness and error


handling.


Recommendation for updating the codebase to improve functionality and


efficiency.


Suggestions regarding inconsistencies in the codebase and ensuring ad

herence to coding best practices.



OS-MTD-SUG-04 Code optimizations for better maintainability and readability.


The codebase contains multiple cases of redundant and unutilized code

OS-MTD-SUG-05

that should be removed.


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 24


Merkle Token Distributor Audit 05 - General Findings


**Missing** **Validation** **Logic** OS-MTD-SUG-00


**Description**


correct length to prevent storing invalid or malformed roots.


_>__ _sources/merkle_distributor.move_ rust

```
     public entry fun update_merkle_root(
       admin: &signer, distributor_address: address, new_root: vector<u8>
     ) acquires ModuleInfo, DistributionData {
       ownable::only_owner(admin, get_module_address());
       let distribution_data = borrow_global_mut<DistributionData>(distributor_address);
       distribution_data.root = new_root;
     }

```

**Remediation**


Include the above validations in the codebase.


**Patch**


1. Issue #2 resolved in [7c85c1c.](https://github.com/EthSign/merkle-token-distributor-move/pull/4/commits/7c85c1c382d7d2d3276d44c2d43c764cdab10ca1)


© 2025 Otter Audits LLC. All Rights Reserved. 12 / 24


Merkle Token Distributor Audit 05 - General Findings


**Error** **Handling** OS-MTD-SUG-01


**Description**


before borrowing.


_>__ _sources/md_create2.move_ rust

```
     public fun get_fee_collector(distribution_addr: address): address acquires DistributorData
```

_�→_ `{`
```
       let distributor_data = borrow_global<DistributorData>(distribution_addr);
       distributor_data.fee_collector
     }

     public fun get_fee_token(distribution_addr: address): address acquires DistributorData {
       let distributor_data = borrow_global<DistributorData>(distribution_addr);
       distributor_data.fee_token
     }

```

claim amount to avoid underflow. Currently, a static fee may exceed the claimed amount, resulting


prevents unexpected failures.


Add an existence check to prevent panics and improve error handling.


_>__ _sources/md_create2.move_ rust

```
     public fun get_distribution_address(
       project_id: String
     ): address acquires DistributorFactory, ModuleInfo {
       let module_addr = get_module_address();
       let factory = borrow_global<DistributorFactory>(module_addr);
       *table::borrow(&factory.deployments, project_id)
     }

```

**Remediation**


Update the codebase with explicit checks listed above to ensure proper error handling.


© 2025 Otter Audits LLC. All Rights Reserved. 13 / 24


Merkle Token Distributor Audit 05 - General Findings


**Patch**


1. Issue #1 was acknowledged by the EthSign team.


2. Issue #2 was partially resolved as the EthSign team mentioned that the fee setting is done manually.


© 2025 Otter Audits LLC. All Rights Reserved. 14 / 24


Merkle Token Distributor Audit 05 - General Findings


**Code** **Refactoring** OS-MTD-SUG-02


**Description**

|fee_collector|prioriti|
|---|---|
|**`distributor_address`**|**`distributor_address`**|



entries. Fixed fees set to 0 are ignored, and bips fees of 0 default to the global fee instead of overriding


tables will accumulate entries over time. Add functionality to remove custom fees and tokens from


defaulting to fallback logic.


maintainability.


_>__ _sources/fee_collector.move_ rust

```
     public entry fun set_custom_fee_fixed(
       caller: &signer, distributor_address: address, fixed_fee: u64
     ) acquires FeeCollectorData, ModuleInfo {
       [...]
       if (table::contains(&fee_data.custom_fees_fixed, distributor_address)) {
          *table::borrow_mut(&mut fee_data.custom_fees_fixed, distributor_address) =
```

_�→_ `fixed_fee;`
```
       } else {
          table::add(&mut fee_data.custom_fees_fixed, distributor_address, fixed_fee);
       };
       event::emit(CustomFeeSetFixed { distributor_address, fixed_fee });
     }

```

resource.

|module_addr<br>by removing the parame<br>@merkle_token_distributor<br>sides at|Col2|Col3|module_addr|parame|
|---|---|---|---|---|
|by removing the<br>**`module_addr`**<br>parame<br>sides at<br>**`@merkle_token_distributor`**|**`@merkle_token_distributor`**|**`@merkle_token_distributor`**|**`@merkle_token_distributor`**|**`@merkle_token_distributor`**|
|**`deployer`**|**`deployer`**|address,<br>and no other addre|address,<br>and no other addre|address,<br>and no other addre|



4. Remove debug comments from all files to clean up the codebase, rendering the code easier to read


and maintain without unnecessary clutter.


the event. This may create confusion and should be corrected.


© 2025 Otter Audits LLC. All Rights Reserved. 15 / 24


Merkle Token Distributor Audit 05 - General Findings


**Remediation**


Incorporate the above-stated refactors.


**Patch**


1. Issue #1 was acknowledged by the Ethsign team, mentioning that the custom fee may be updated


utilizing the setters.


2. Issue #2 resolved in [1f2405a.](https://github.com/EthSign/merkle-token-distributor-move/pull/4/commits/1f2405a6f016aadb47ffa6f3f812b321be437fe9)


3. Issue #3 resolved in [e4bcbba.](https://github.com/EthSign/merkle-token-distributor-move/pull/4/commits/e4bcbba5c04ca77b6aa291eeebcf8fbd41cce1ca)


4. Issue #4 resolved by removing all debug comments.


© 2025 Otter Audits LLC. All Rights Reserved. 16 / 24


Merkle Token Distributor Audit 05 - General Findings


**Code** **Maturity** OS-MTD-SUG-03


**Description**


as an event.


_>__ _sources/md_create2.move_ rust

```
     struct DeployEvent has drop, store {
       project_id: String,
       distribution_address: address,
       deployer: address
     }

```

single call.


_>__ _sources/fee_collector.move_ rust

```
     public fun get_fee(
       distributor_address: address, token_transferred: u64
     ): u64 acquires FeeCollectorData, ModuleInfo {
       let module_addr = get_module_address();
       let fee_data = borrow_global<FeeCollectorData>(module_addr);
       // Check for fixed fee first
       if (table::contains(&fee_data.custom_fees_fixed, distributor_address)) {
          let fixed_fee =
            *table::borrow(&fee_data.custom_fees_fixed, distributor_address);
          if (fixed_fee > 0) {
            return fixed_fee
          }
       };
       [...]
     }

```

locking the module if an incorrect address is inadvertently passed. A two-step process requiring the


new owner to accept ownership will ensure a safer transfer approach.


4. All significant state-changing operations should emit an event, but only when a change has ac

© 2025 Otter Audits LLC. All Rights Reserved. 17 / 24


Merkle Token Distributor Audit 05 - General Findings


Merkle root computation and verification. Align the hashing strategy to prevent bugs and maintain


correctness.


**Remediation**


Implement the above-mentioned suggestions.


© 2025 Otter Audits LLC. All Rights Reserved. 18 / 24


Merkle Token Distributor Audit 05 - General Findings


**Code** **Optimization** OS-MTD-SUG-04


**Description**


below) after asserting that lengths are equal, which is always true and misleading. It should instead


lengths. A check should be added to ensure they are of equal length before proceeding. Further, the


negation reduces readability and should be replaced with clearer logic.


_>__ _sources/merkle_verifier.move_ rust

```
     fun compare_vectors(a: &vector<u8>, b: &vector<u8>): bool {
       let i = 0;
       let len_a = vector::length(a);
       let len_b = vector::length(b);
       assert!(len_a == len_b, EINVALID_LEAF);
       [...]
       len_a <= len_b
     }

```

helper function to reduce code duplication and improve readability and maintainability.


3. The addresses of fee and distribution tokens are utilized solely to convert them into


addresses.


**Remediation**


Include the above recommendations to optimize the logic.


© 2025 Otter Audits LLC. All Rights Reserved. 19 / 24


Merkle Token Distributor Audit 05 - General Findings


**Unutilized/Redundant** **Code** OS-MTD-SUG-05


**Description**

|merkle_distributor::deposit|Col2|
|---|---|
|**`primary_fungible_store::transfer`**|**`primary_fungible_store::transfer`**|
|unnecessary actions by requiring a|**`distributor_address`**|



converting it back to an address. Deposit operations may be handled directly via the public primary


be removed.


_>__ _sources/merkle_distributor.move_ rust

```
     public entry fun deposit<T: key>(
       from: &signer,
       distributor_address: address,
       metadata: Object<T>,
       amount: u64
     ) {
       let distribution_signer =
          md_create2::get_distribution_signer(distributor_address);
       let distribution_addr = signer::address_of(&distribution_signer);
       // Transfer tokens to the distribution
       primary_fungible_store::transfer<T>(from, metadata, distribution_addr, amount);
     }

```

_>__ _sources/fee_collector.move_ rust

```
     struct ModuleInfo has key {
       module_address: address
     }

```

© 2025 Otter Audits LLC. All Rights Reserved. 20 / 24


Merkle Token Distributor Audit 05 - General Findings


checks.









5. Several constants across the codebase are declared but unutilized and may be safely removed.


, this friend declaration is unnecessary and should be removed.


Remove the explicit type definition.









© 2025 Otter Audits LLC. All Rights Reserved. 21 / 24


Merkle Token Distributor Audit 05 - General Findings


**Remediation**


Remove the redundant and unutilized code instances highlighted above.


**Patch**


1. Issue #1 partially resolved in [49eaf58.](https://github.com/EthSign/merkle-token-distributor-move/pull/4/commits/49eaf58fd898161a0dfc108e35f87942d3a1a3d4)


2. Issue #2 partially resolved in [ceded44.](https://github.com/EthSign/merkle-token-distributor-move/pull/4/commits/ceded4434085a70aa8ca4d873ed244ef34e68cb4)


3. Issue #3 partially resolved in [54c11b0.](https://github.com/EthSign/merkle-token-distributor-move/pull/4/commits/54c11b0528f65b620c1b8f3fd6c0b0c32b9f5cd5)


© 2025 Otter Audits LLC. All Rights Reserved. 22 / 24


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


© 2025 Otter Audits LLC. All Rights Reserved. 23 / 24


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


© 2025 Otter Audits LLC. All Rights Reserved. 24 / 24


