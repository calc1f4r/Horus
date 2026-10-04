---
# Core Classification
protocol: Slock.it Incubed3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13971
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2019/09/slock.it-incubed3/
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Martin Ortner
  - Shayan Eskandari
---

## Vulnerability Title

NodeRegistry.registerNodeFor() no replay protection and expiration  Won't Fix

### Overview


This bug report is about an issue related to node-owner and signer. The owner can register a node with the signer not being the owner by calling `registerNodeFor`. The owner submits a message signed for the owner including the properties of the node including the url. This signed data does not include the `registryID` nor the `NodeRegistry`’s address and can therefore be used by the owner to submit the same node to multiple registries or chains without the signer's consent. The signed data does not expire and can be re-used by the owner indefinitely to submit the same node again to future contracts or the same contract after the node has been removed. Furthermore, arguments are not validated in the external function.

To address this issue, the statement suggests that the owner should always know the privateKey of the signer, and that a replay-protection would be useless because the owner could always sign the necessary message. It also suggests that the reason for separating the signer from the owner was to enable the possibility of owning an in3-node as with a multisig-account, as due to the nature of the exposal of the signer-key the possibility of it being leaked somehow is given.

The recommendation is to include `registryID` and an expiration timestamp that is checked in the contract with the signed data, as well as to validate function arguments.

### Original Finding Content

#### Resolution



This issue was addressed with the following statement:



> 
> In our understanding of the relationship between node-owner and signer the owner both are controlled by the very same entity, thus the owner should always know the privateKey of the signer. With this in mind a replay-protection would be useless, as the owner could always sign the necessary message.
> The reason why we separated the signer from the owner was to enable the possibility of owning an in3-node as with a multisig-account, as due to the nature of the exposal of the signer-key the possibility of it being leaked somehow is given (e.g. someone “hacks” the server), making the signer-key more unsecure.
> In addition, even though it’s possible to replay the register as an owner it would unfeasable, as the owner would have to pay for the deposit anyway thus rendering the attack useless as there would be no benefit for an owner to do it.
> 
> 
> 




#### Description


An owner can register a node with the signer not being the owner by calling `registerNodeFor`. The owner submits a message signed for the owner including the properties of the node including the url.


* The signed data does not include the `registryID` nor the `NodeRegistry`’s address and can therefore be used by the owner to submit the same node to multiple registries or chains without the signers consent.
* The signed data does not expire and can be re-used by the owner indefinitely to submit the same node again to future contracts or the same contract after the node has been removed.
* Arguments are not validated in the external function (also see [issue 6.17](#registries---incomplete-input-validation-and-inconsistent-order-of-validations))


**code/in3-contracts/contracts/NodeRegistry.sol:L215-L223**



```
bytes32 tempHash = keccak256(
    abi.encodePacked(
        \_url,
        \_props,
        \_timeout,
        \_weight,
        msg.sender
    )
);

```
#### Recommendation


Include `registryID` and an expiration timestamp that is checked in the contract with the signed data. Validate function arguments.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Slock.it Incubed3 |
| Report Date | N/A |
| Finders | Martin Ortner, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2019/09/slock.it-incubed3/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

