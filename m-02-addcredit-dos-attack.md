---
# Core Classification
protocol: Particle Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20706
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-particle
source_link: https://code4rena.com/reports/2023-05-particle
github_link: https://github.com/code-423n4/2023-05-particle-findings/issues/16

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

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - d3e4
  - minhquanym
  - bin2chen
---

## Vulnerability Title

[M-02] `addCredit()` DOS Attack

### Overview


A bug has been discovered in the Particle protocol which allows anyone to modify Lien at a small cost, causing the value stored in `liens[lienId]=keccak256(abi.encode(lien))` to change. This bug can be exploited to front-run normal user's transactions, which prevents them from being executed. The methods that can be exploited include `auctionBuyNft()`, `startLoanAuction()`, `stopLoanAuction()` and more.

Recommended mitigation steps include allowing `addCredit()` to be called only by the borrower, adding a modification interval period, and limiting the minimum of `msg.value`. The severity of the bug was first increased to High by the judge, but then decreased to Medium after the sponsor disagreed. Finally, the bug was mitigated with the suggestion to add a borrower only check and add a minimum 0.01 ETH credit limit, as well as enforcing that the borrower is solvent after adding credit.

### Original Finding Content


### Proof of Concept

`addCredit()` can be called by anyone, and the `msg.value` is as small as `1 wei`.

Users can modify Lien at a small cost, causing the value stored in `liens[lienId]=keccak256(abi.encode(lien))` to change. By front-run, the normal user's transaction `validateLien()` fails the check, thus preventing the user's transaction from being executed.

The following methods will be exploited (most methods with `validateLien()` will be affected). For example:

1.  Front-run `auctionBuyNft()` is used to prevent others from bidding.
2.  Front-run  `startLoanAuction()` to prevent the lender from starting the auction.
3.  Front-run  `stopLoanAuction()` is used to stop Lender from closing the auction.
<br>etc.

### Recommended Mitigation Steps

1.  `addCredit()` can execute only by the borrower.
2.  Add the modification interval period.
3.  Limit min of `msg.value`.

### Assessed type

Context

**[hansfriese (judge) increased severity to High and commented](https://github.com/code-423n4/2023-05-particle-findings/issues/16#issuecomment-1578380637):**
 > Concise explanation and reasonable mitigation recommendation. Marked as primary.

**[hansfriese (judge) commented](https://github.com/code-423n4/2023-05-particle-findings/issues/16#issuecomment-1578402043):**
 > Preventing borrowers from repaying NFT by causing DoS for `repayWithNft` is another severe exploit: [#40](https://github.com/code-423n4/2023-05-particle-findings/issues/40)

**[wukong-particle (Particle) confirmed, disagreed with severity and commented](https://github.com/code-423n4/2023-05-particle-findings/issues/16#issuecomment-1579327687):**
 > Should be a Medium risk because no fund or asset can be stolen. `addCredit` incurs non-trivial gas so DOS can't economically happen very often. 
> 
> We agree with the suggestion to add a borrower only check and add a minimum 0.01 ETH credit limit.

**[hansfriese (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2023-05-particle-findings/issues/16#issuecomment-1579990428):**
 > Agree with the sponsor. Downgrading to Medium.

**[d3e4 (warden) commented](https://github.com/code-423n4/2023-05-particle-findings/issues/16#issuecomment-1582615662):**
 > > We agree with the suggestion to add a borrower only check and add a minimum 0.01 ETH credit limit.
> 
> Adding a borrower only check seems good. But I am concerned that 0.01 ETH is not enough. If the max price is 72 ETH, then the auction price will increase 0.01 ETH for every block. It then seems very reasonable that the borrower could still profitably DoS `auctionBuyNft()` so that they can call it when the price is close to max.
> This is, of course, an illegitimate use case of `addCredit()`. A way to avoid having any minimum limit for legitimate use of `addCredit()` is to enforce that the borrower is solvent after adding credit. This way, the hefty minimum limit only applies to adding additional credit, which is what is susceptible to exploits.

**[wukong-particle (Particle) commented](https://github.com/code-423n4/2023-05-particle-findings/issues/16#issuecomment-1584994871):**
 > Mitigated.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Particle Protocol |
| Report Date | N/A |
| Finders | d3e4, minhquanym, bin2chen |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-particle
- **GitHub**: https://github.com/code-423n4/2023-05-particle-findings/issues/16
- **Contest**: https://code4rena.com/reports/2023-05-particle

### Keywords for Search

`vulnerability`

