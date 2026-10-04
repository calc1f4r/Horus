---
# Core Classification
protocol: Visor
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 190
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-05-visor-contest
source_link: https://code4rena.com/reports/2021-05-visorfinance
github_link: https://github.com/code-423n4/2021-05-visorfinance-findings/issues/34

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xRajeev
  - shw
---

## Vulnerability Title

[H-02] NFT transfer approvals are not removed and cannot be revoked thus leading to loss of NFT tokens

### Overview


This bug report is about a vulnerability in the Visor smart contract. This vulnerability allows a delegate to transfer a non-fungible token (NFT) from an owner's vault without requiring a new approval. This means that if the NFT is ever moved back into the owner's vault again, then the delegate can again transfer it to any address of choice without requiring a new approval. Furthermore, if a delegate becomes compromised or untrustworthy after granting approval but before transfer, then the owner will lose their NFT because there is no mechanism to revoke the approval that was granted earlier.

The bug was identified through manual analysis. Two proof of concepts were provided to demonstrate the vulnerability: one where the NFT is moved back into the owner's vault and one where the delegate is compromised before the transfer.

The recommended mitigation step is to add a boolean parameter to approveTransferERC721() and set the nftApprovals to that parameter, which can be true for giving approval and false for removing/revoking approval. If the sender is not the owner, then the approveTransferERC721() should be called with the boolean false to remove approval before making a transfer in transferERC721().

### Original Finding Content

_Submitted by 0xRajeev, also found by shw_

NFT transfer approvals that are set to true in `approveTransferERC721()` are never set to false and there is no way to remove such an nft approval.

**Impact 1**: The approval is not removed (set to false) after a transfer in `transferERC721()`. So if the NFT is ever moved back into the owner's vault again, then the previous/compromised delegate can again transfer it to any address of choice without requiring a new approval.

**Impact 2**: If a delegate becomes compromised/untrustworthy after granting approval but before transfer then the owner will lose its NFT because there is no mechanism to revoke the approval that was granted earlier.

[PoC-1](https://github.com/code-423n4/2021-05-visorfinance/blob/e0f15162a017130aa66910d46c70ee074b64dd40/contracts/contracts/visor/Visor.sol#L477-L487):
* Alice grants Eve approval to transfer a particular NFT out of its vault using `approveTransferERC721()`
* Eve, who has transfer rights to that NFT from Alice’s vault,  transfers that NFT to Bob using `transferERC721()`
* Alice decides to buy back that NFT (e.g. because it is now considered rare and more valuable) from Bob and transfers it back to its vault
* Eve, who continues to have transfer rights to that NFT from Alice’s vault, can steal that NFT and transfer to anyone

[PoC-2](https://github.com/code-423n4/2021-05-visorfinance/blob/e0f15162a017130aa66910d46c70ee074b64dd40/contracts/contracts/visor/Visor.sol#L489-L522):
* Alice grants Eve approval to transfer a particular NFT out of its vault using `approveTransferERC721()`
* Alice learns that Eve’s keys are compromises or that Eve is malicious and wants to revoke the approval but there is no mechanism to do so
* Eve (or whoever stole her credentials) has transfer rights to that NFT from Alice’s vault and can steal that NFT and transfer to anyone

Recommend adding a boolean parameter to `approveTransferERC721()` and set the `nftApprovals`  to that parameter which can be true for giving approval and false for removing/revoking approval
If ```msg.sender != _getOwner()```, call `approveTransferERC721()` with the boolean false to remove approval before making a transfer in `transferERC721()` on L515.

**[xyz-ctrl (Visor) commented](https://github.com/code-423n4/2021-05-visorfinance-findings/issues/34#issuecomment-862438325):**
> duplicate
> https://github.com/code-423n4/2021-05-visorfinance-findings/issues/35

**[ghoul-sol (Judge) commented](https://github.com/code-423n4/2021-05-visorfinance-findings/issues/34#issuecomment-873475636):**
> #35 is about token being stuck in the vault. This issue is about not being able to revoke approval. Marking this as separate.

**[ztcrypto (Visor) patched](https://github.com/code-423n4/2021-05-visorfinance-findings/issues/34#issuecomment-889187960):**
 > patch [link](https://github.com/VisorFinance/visor-core/commit/71797204108fee8375bfb99a435c0e379bbcbd84#diff-b094db7ce2f99cbcbde7ec178a6754bac666e2192f076807acbd70d49ddd0559)



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Visor |
| Report Date | N/A |
| Finders | 0xRajeev, shw |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-visorfinance
- **GitHub**: https://github.com/code-423n4/2021-05-visorfinance-findings/issues/34
- **Contest**: https://code4rena.com/contests/2021-05-visor-contest

### Keywords for Search

`vulnerability`

