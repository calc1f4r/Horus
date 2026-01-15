---
# Core Classification
protocol: Zer0 - zNS
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13411
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/05/zer0-zns/
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
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - David Oz Kashi
  - Martin Ortner
---

## Vulnerability Title

zNS - anyone can front-run fulfillDomainBid to lock the domain setting or set different metadata ✓ Fixed

### Overview


This bug report is about a vulnerability in the code of the StakingController.sol contract. Anyone observing a call to `fulfillDomainBid` can front-run this call for the original bidder, provide different metadata/royalty amount, or lock the metadata, as these parameters are not part of the bidder’s signature. This can have an impact on the domain owner after creation, as both metadata, royalty amount, and lock state can be changed.

The resolution of this bug was addressed with a commit to the GitHub repository. The commit restricts the method to only be callable by the requester.

The recommendation is to consider adding `metadata`, `royaltyAmount`, and `lockOnCreation` to the message signed by the bidder if the parent should have some control over metadata and lockstatus and restrict access to this function to `msg.sender==recoveredbidder`.

### Original Finding Content

#### Resolution



Addressed with [zer0-os/[email protected]`ab7d62a`](https://github.com/zer0-os/ZNS/commit/ab7d62a7b8d51b04abea895e241245674a640fc1) by restricting the method to only be callable by the requester.


#### Description


Anyone observing a call to `fulfillDomainBid` can front-run this call for the original bidder, provide different metadata/royalty amount, or lock the metadata, as these parameters are not part of the bidder’s signature.
The impact is limited as both metadata, royalty amount, and lock state can be changed by the domain owner after creation.


#### Examples


**zNS/contracts/StakingController.sol:L120-L143**



```
  function fulfillDomainBid(
  uint256 parentId,
  uint256 bidAmount,
  uint256 royaltyAmount,
  string memory bidIPFSHash,
  string memory name,
  string memory metadata,
  bytes memory signature,
  bool lockOnCreation,
  address recipient
) external {
  bytes32 recoveredBidHash = createBid(parentId, bidAmount, bidIPFSHash, name);
  address recoveredBidder = recover(recoveredBidHash, signature);
  require(recipient == recoveredBidder, "ZNS: bid info doesnt match/exist");
  bytes32 hashOfSig = keccak256(abi.encode(signature));
  require(approvedBids[hashOfSig] == true, "ZNS: has been fullfilled");
  infinity.safeTransferFrom(recoveredBidder, controller, bidAmount);
  uint256 id = registrar.registerDomain(parentId, name, controller, recoveredBidder);
  registrar.setDomainMetadataUri(id, metadata);
  registrar.setDomainRoyaltyAmount(id, royaltyAmount);
  registrar.transferFrom(controller, recoveredBidder, id);
  if (lockOnCreation) {
    registrar.lockDomainMetadataForOwner(id);
  }

```
#### Recommendation


Consider adding `metadata`, `royaltyAmount`, and `lockOnCreation` to the message signed by the bidder if the parent should have some control over metadata and lockstatus and restrict access to this function to `msg.sender==recoveredbidder`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Zer0 - zNS |
| Report Date | N/A |
| Finders | David Oz Kashi, Martin Ortner |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/05/zer0-zns/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

