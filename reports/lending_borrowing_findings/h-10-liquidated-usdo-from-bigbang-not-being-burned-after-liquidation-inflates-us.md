---
# Core Classification
protocol: Tapioca DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27500
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-tapioca
source_link: https://code4rena.com/reports/2023-07-tapioca
github_link: https://github.com/code-423n4/2023-07-tapioca-findings/issues/1355

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - peakbolt
  - 0xnev
  - 0xRobocop
  - unsafesol
  - rvierdiiev
---

## Vulnerability Title

[H-10] Liquidated USDO from BigBang not being burned after liquidation inflates USDO supply and can threaten peg permanently

### Overview


A bug report has been filed for Tapioca's BigBang market which results in an overcollaterization of USDO. This occurs when a user liquidates their collateral and no USDO is burned. This is due to the lack of proper USDO burn after liquidation in the BigBang market. As a result, an excessive amount of USDO is being minted without any collateral or backing, leading to the USDO peg being threatened and yieldBox strategies failing.

To mitigate this issue, the USDO acquired through liquidation should be burned after extracting fees for appropriate parties. This has been confirmed by 0xRektora (Tapioca).

### Original Finding Content


Absence of proper USDO burn after liquidation in the BigBang market results in a redundant amount of USDO being minted without any collateral or backing. Thus, the overcollaterization of USDO achieved through BigBang will be eventually lost and the value of USDO in supply (1USDO = 1&#36;) will exceed the amount of collateral locked in BigBang. This has multiple repercussions- the USDO peg will be threatened and yieldBox will have USDO which has virtually no value, resulting in all the BigBang strategies failing.

### Proof of Concept

According to the Tapioca documentation, the BigBang market mints USDO when a user deposits sufficient collateral and borrows tokens. When a user repays the borrowed USDO, the market burns the borrowed USDO and unlocks the appropriate amount of collateral. This is essential to the peg of USDO, since USDO tokens need a valid collateral backing.

While liquidating a user as well, the same procedure should be followed- after swapping the user’s collateral for USDO, the repaid USDO (with liquidation) must be burned so as to sustain the USDO peg. However, this is not being done.
As we can see here: <https://github.com/Tapioca-DAO/tapioca-bar-audit/blob/2286f80f928f41c8bc189d0657d74ba83286c668/contracts/markets/bigBang/BigBang.sol#L618-L637>, the collateral is swapped for USDO, and fee is extracted and transferred to the appropriate parties, but nothing is done for the remaining USDO which was repaid. At the same time, this was done correctly done in BigBang#\_repay for repayment here: <https://github.com/Tapioca-DAO/tapioca-bar-audit/blob/2286f80f928f41c8bc189d0657d74ba83286c668/contracts/markets/bigBang/BigBang.sol#L734-L736>.

This has the following effects:

1.  The BigBang market now has redundant yieldBox USDO shares which have no backing.
2.  The redundant USDO is now performing in yieldBox strategies of tapioca.
3.  The USDO eventually becomes overinflated and exceeds the value of underlying collateral.
4.  The strategies start not performing since they have unbacked USDO, and the USDO peg is lost as well since there is no appropriate amount of underlying collateral.

### Recommended Mitigation Steps

Burn the USDO acquired through liquidation after extracting fees for appropriate parties.

**[0xRektora (Tapioca) confirmed](https://github.com/code-423n4/2023-07-tapioca-findings/issues/1355#issuecomment-1703046614)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tapioca DAO |
| Report Date | N/A |
| Finders | peakbolt, 0xnev, 0xRobocop, unsafesol, rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-tapioca
- **GitHub**: https://github.com/code-423n4/2023-07-tapioca-findings/issues/1355
- **Contest**: https://code4rena.com/reports/2023-07-tapioca

### Keywords for Search

`vulnerability`

