---
# Core Classification
protocol: Tessera
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 12199
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-tessera-versus-contest
source_link: https://code4rena.com/reports/2022-12-tessera
github_link: https://github.com/code-423n4/2022-12-tessera-findings/issues/25

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
  - cross_chain
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - cccz
  - Trust
  - gzeon
---

## Vulnerability Title

[H-05] Attacker can DOS OptimisticListing with very low cost

### Overview


This bug report is about a vulnerability in the code of a protocol called Tessera. The vulnerability allows an attacker to block normal proposal creation by creating a proposal with a lower price but _collateral == 1. This violates the “prevent a user from holding a vault hostage and never letting the piece be reasonably bought” requirement. The vulnerability was found using Foundry, a tool used to find and report bugs. The recommended mitigation step is to require the total value of the new collateral be greater than the previous. This would still, however, allow a Rae holder with a sufficiently large holding to block proposal by creating a new proposal and immediately reject it himself.

### Original Finding Content


The only check on a new proposal is that it is priced lower than the existing proposal. It does not constrain on the `_collateral` supplied (except it will revert in `\_verifyBalance` if set to 0). Anyone can block normal proposal creation by creating a proposal with lower price but `\_collateral == 1`. When a high total supply is used, the price of each Rae is negligible and enables an attacker to DOS the protocol.

This violated the `prevent a user from holding a vault hostage and never letting the piece be reasonably bought` requirement.

### Proof of Concept

For any proposal, an attacker can deny it with `\_collateral = 1` and `\_price = price - 1`.

If he does not want the NFT to be sold, he can reject the proposal himself, resetting the contract state.

<https://github.com/code-423n4/2022-12-tessera/blob/f37a11407da2af844bbfe868e1422e3665a5f8e4/src/seaport/modules/OptimisticListingSeaport.sol#L112-L116>

```solidity
        // Reverts if price per token is not lower than both the proposed and active listings
        if (
            _pricePerToken >= proposedListing.pricePerToken ||
            _pricePerToken >= activeListings[_vault].pricePerToken
        ) revert NotLower();
```

Add this test to OptimisticListingSeaport.t.sol:

        function testProposeRevertLowerTotalValue() public {
            uint256 _collateral = 100;
            uint256 _price = 100;
            // setup
            testPropose(_collateral, _price);
            lowerPrice = pricePerToken - 1;
            // execute
            vm.expectRevert();
            _propose(eve, vault, 1, lowerPrice, offer);
            // expect
            _assertListing(eve, 1, lowerPrice, block.timestamp);
            _assertTokenBalance(eve, token, tokenId, eveTokenBalance - 1);
        }

\[FAIL. Reason: Call did not revert as expected]

### Tools Used

Foundry

### Recommended Mitigation Steps

Require the total value of the new collateral to be greater than the previous.

This however still allows a Rae holder with sufficiently large holding to block proposal by creating a new proposal and immediately reject it himself.

**[stevennevins (Tessera) confirmed](https://github.com/code-423n4/2022-12-tessera-findings/issues/25#issuecomment-1371409906)**

**[HickupHH3 (judge) commented](https://github.com/code-423n4/2022-12-tessera-findings/issues/25#issuecomment-1378890797):**
 > Best report for Foundry POC + the following statement:
> > This violated the `prevent a user from holding a vault hostage and never letting the piece be reasonably bought` requirement.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tessera |
| Report Date | N/A |
| Finders | cccz, Trust, gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tessera
- **GitHub**: https://github.com/code-423n4/2022-12-tessera-findings/issues/25
- **Contest**: https://code4rena.com/contests/2022-12-tessera-versus-contest

### Keywords for Search

`vulnerability`

