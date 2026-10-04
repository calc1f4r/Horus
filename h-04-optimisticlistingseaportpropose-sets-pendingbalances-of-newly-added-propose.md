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
solodit_id: 12198
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-tessera-versus-contest
source_link: https://code4rena.com/reports/2022-12-tessera
github_link: https://github.com/code-423n4/2022-12-tessera-findings/issues/12

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
finders_count: 2
finders:
  - Lambda
  - Trust
---

## Vulnerability Title

[H-04] OptimisticListingSeaport.propose sets pendingBalances of newly added proposer instead of previous one

### Overview


This report describes a bug found in the code of a specific GitHub repository. The bug allows the proposer of a previous proposal to lose their collateral, while the new proposer can make proposals for free. The bug is demonstrated in a proof of concept code snippet, which fails and shows that the proposed collateral is not set to the old proposer, but to the new one. The recommended mitigation step for this bug is to run the proposed collateral line of code before the _setListing call. This way, the bug will no longer work.

### Original Finding Content


In `OptimisticListingSeaport.propose`, `pendingBalances` is set to the collateral. The purpose of this is that the proposer of a previous proposal can withdraw his collateral afterwards. However, this is done on the storage variable `proposedListing` after the new listing is already set:

```solidity
_setListing(proposedListing, msg.sender, _collateral, _pricePerToken, block.timestamp);

// Sets collateral amount to pending balances for withdrawal
pendingBalances[_vault][proposedListing.proposer] += proposedListing.collateral;
```

Because of that, it will actually set `pendingBalances` of the new proposer. Therefore, the old proposer loses his collateral and the new one can make proposals for free.

### Proof Of Concept

```diff
--- a/test/seaport/OptimisticListingSeaport.t.sol
+++ b/test/seaport/OptimisticListingSeaport.t.sol
@@ -379,8 +379,11 @@ contract OptimisticListingSeaportTest is SeaportTestUtil {
     /// ===== LIST =====
     /// ================
     function testList(uint256 _collateral, uint256 _price) public {
         // setup
         testPropose(_collateral, _price);
+        assertEq(optimistic.pendingBalances(vault, bob), 0);
         _increaseTime(PROPOSAL_PERIOD);
         _collateral = _boundCollateral(_collateral, bobTokenBalance);
         _price = _boundPrice(_price);
```

This test fails and `optimistic.pendingBalances(vault, bob)` is equal to `_collateral`.

### Recommended Mitigation Steps

Run `pendingBalances[_vault][proposedListing.proposer] += proposedListing.collateral;` before the `_setListing` call, in which case the above PoC no longer works.

**[HickupHH3 (judge) commented](https://github.com/code-423n4/2022-12-tessera-findings/issues/12#issuecomment-1358744847):**
 > > Because of that, it will actually set pendingBalances of the new proposer. Therefore, the old proposer loses his collateral and the new one can make proposals for free.
> 
> Seems like intended behaviour to me (actually set pendingBalances of the new proposer). The old proposer wouldn't be losing his collateral because his pendingBalances would've been set when he called `propose()`.

**[mehtaculous (Tessera) confirmed and commented](https://github.com/code-423n4/2022-12-tessera-findings/issues/12#issuecomment-1371507827):**
 > Agree with severity. The suggested solution makes sense.

**[stevennevins (Tessera) mitigated](https://github.com/code-423n4/2022-12-tessera-findings/issues/12#issuecomment-1404411097):**
 > https://github.com/fractional-company/modular-fractional/pull/202
>
 **Status:** Mitigation confirmed by [gzeon](https://github.com/code-423n4/2023-01-tessera-mitigation-findings/issues/42), [IllIllI](https://github.com/code-423n4/2023-01-tessera-mitigation-findings/issues/23), and [Lambda](https://github.com/code-423n4/2023-01-tessera-mitigation-findings/issues/5).

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
| Finders | Lambda, Trust |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tessera
- **GitHub**: https://github.com/code-423n4/2022-12-tessera-findings/issues/12
- **Contest**: https://code4rena.com/contests/2022-12-tessera-versus-contest

### Keywords for Search

`vulnerability`

