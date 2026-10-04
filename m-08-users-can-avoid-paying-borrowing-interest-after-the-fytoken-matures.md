---
# Core Classification
protocol: Yield
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4087
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-05-yield-contest
source_link: https://code4rena.com/reports/2021-05-yield
github_link: https://github.com/code-423n4/2021-05-yield-findings/issues/71

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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-08] Users can avoid paying borrowing interest after the fyToken matures

### Overview


This bug report describes a vulnerability in the protocol design of a system which allows users to avoid paying borrowing interest when repaying the debt with underlying tokens after maturity. This could make users less incentivized to repay the debt before maturity and hold the underlying tokens until liquidation. 

The bug is demonstrated with a Proof of Concept (POC). A user creates a new vault and opens a borrowing position as usual. Then, the maturity date passes. If the user wants to close the position using underlying tokens, he has to pay a borrowing interest. To avoid paying the borrowing interest, the user gives his vault to `Witch` and then calls the function `buy` of `Witch` with the corresponding `vaultId` to buy all his collateral using underlying tokens. This is possible because the `elapsed` time is equal to the current timestamp since the vault is never grabbed by `Witch` before, and thus the auction time of the vault, `cauldron.auctions(vaultId)`, is 0.

The recommended mitigation steps to fix this vulnerability are to not allow users to `give` vaults to `Witch` and to require `vaultOwners[vaultId]` and `cauldron.auctions(vaultId)` to be non-zero at the beginning of function `buy`.

### Original Finding Content


According to the protocol design, users have to pay borrowing interest when repaying the debt with underlying tokens after maturity. However, a user can give his vault to `Witch` and then buy all his collateral using underlying tokens to avoid paying the interest. Besides, this bug could make users less incentivized to repay the debt before maturity and hold the underlying tokens until liquidation.

1. A user creates a new vault and opens a borrowing position as usual.
2. The maturity date passed. If the user wants to close the position using underlying tokens, he has to pay a borrowing interest (line 350 in `Ladle`), which is his debt multiplied by the rate accrual (line 373).
3. Now, the user wants to avoid paying the borrowing interest. He gives his vault to `Witch` by calling the function `batch` of `Ladle` with the operation `GIVE`.
4. He then calls the function `buy` of `Witch` with the corresponding `vaultId` to buy all his collateral using underlying tokens.

In the last step, the `elapsed` time (line 61) is equal to the current timestamp since the vault is never grabbed by `Witch` before, and thus the auction time of the vault, `cauldron.auctions(vaultId)`, is 0 (the default mapping value). Therefore, the collateral is sold at a price of `balances_.art/balances_.ink` (line 74). The user can buy `balances_.ink` amount of collateral using `balances_.art` but not paying for borrowing fees.

Recommend not allowing users to `give` vaults to `Witch`. And to be more careful, requiring `vaultOwners[vaultId]` and `cauldron.auctions(vaultId)` to be non-zero at the beginning of function `buy`.

**[albertocuestacanada (Yield) confirmed](https://github.com/code-423n4/2021-05-yield-findings/issues/71#issuecomment-856589289):**
 > That's a good catch. The mitigation steps are right to avoid this being exploited by malicious users, but it would be better to fix the underlying issue.
>
> The problem is that the Witch always applies a 1:1 exchange rate between underlying and fyToken, which is not true after maturity. As long as this is not fixed, the protocol will lose money after maturity liquidations.

**[albertocuestacanada (Yield) commented](https://github.com/code-423n4/2021-05-yield-findings/issues/71#issuecomment-856599112):**
 > More specifically, `_debtInBase` should be a Cauldron public function, and return (debtInFYToken, debtInBase). The Ladle would save a bit in deployment gas; the Witch would use it to determine the underlying / fyToken exchange rate.

**[albertocuestacanada (Yield) commented](https://github.com/code-423n4/2021-05-yield-findings/issues/71#issuecomment-856614042):**
 > However, since `grab` wouldn't be called on the Witch, the vault owner wouldn't be registered. With the liquidation being a Dutch auction, the vault owner would only get a portion of his collateral back after paying all the debt. The vault with the remaining collateral would be given to address(0).
>
> There is a small protocol loss from miscalculated vault debt on vaults liquidated after maturity, but no user funds would be at risk.
>
> I would propose a severity of 2, given there are monetary losses, however slight, to the protocol. The attack described can't happen, but it revealed a real issue.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yield |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-yield
- **GitHub**: https://github.com/code-423n4/2021-05-yield-findings/issues/71
- **Contest**: https://code4rena.com/contests/2021-05-yield-contest

### Keywords for Search

`vulnerability`

