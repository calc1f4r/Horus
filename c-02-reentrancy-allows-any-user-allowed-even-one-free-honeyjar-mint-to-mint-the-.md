---
# Core Classification
protocol: Bearcave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20530
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-03-01-BearCave.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[C-02] Reentrancy allows any user allowed even one free `HoneyJar` mint to mint the max supply for himself for free

### Overview


This bug report describes a vulnerability in the `HoneyBox` contract that allows a user to claim all `HoneyJar` NFTs without paying anything. This vulnerability is caused by the `claim` method in the `HoneyBox` contract, which calls `honeyJar::batchMint`, which uses `safeMint`, which does an unsafe external call to the mint recipient. This call can reenter the `claim` method while the `claimed` accounting was still not done and actually claim all of the `HoneyJar` NFTs until `mintConfig.maxHoneyJar` is hit. The likelihood of this attack is high as reentrancy is a very common attack vector and easily exploitable.

To address this vulnerability, it is recommended to make sure the `claim` method is following the Checks-Effects-Interactions pattern or add a `nonReentrant` modifier to it. This would ensure that the `claimed` accounting is done before any external calls are made and prevent the attack.

### Original Finding Content

**Impact:**
High, as the user will steal all `HoneyJar` NFTs, paying nothing

**Likelihood:**
High, as reentrancy is a very common attack vector and easily exploitable

**Description**

The `claim` method in `HoneyBox` (from its NatSpec) "Allows a player to claim free HoneyJar based on eligibility". Let's look at this part of its code:

```solidity
_canMintHoneyJar(bundleId_, numClaim); // Validating here because numClaims can change

// If for some reason this fails, GG no honeyJar for you
_mintHoneyJarForBear(msg.sender, bundleId_, numClaim);

claimed[bundleId_] += numClaim;
// Can be combined with "claim" call above, but keeping separate to separate view + modification on gatekeeper
gatekeeper.addClaimed(bundleId_, gateId, numClaim, proof);
```

Where you update the `claimed` mapping and account for the claim in the `Gatekeeper` contract after you actually do the minting itself. The problem is that the `_mintHoneyJarForBear` method calls `honeyJar::batchMint`, that uses `safeMint`, which does an unsafe external call to the mint recipient. This call can reenter the `claim` method while the `claimed` accounting was still not done and actually claim all of the `HoneyJar` NFTs until `mintConfig.maxHoneyJar` is hit, which will most likely make him the winner of the game so he will get all of the NFTs in it as well, paying nothing.

What makes it worse as well is that even though the `claim` method has protection because it accepts a `gateId` argument, and the gates themselves have a `maxClaimable` property, this is also broken since the `gatekeeper::addClaimed` call is also done after the unsafe external call, so multiple invariants can be broken here.

**Recommendations**

Make sure the `claim` method is following the Checks-Effects-Interactions pattern or add a `nonReentrant` modifier to it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Bearcave |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-03-01-BearCave.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

