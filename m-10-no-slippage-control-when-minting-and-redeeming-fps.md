---
# Core Classification
protocol: Frankencoin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20031
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-frankencoin
source_link: https://code4rena.com/reports/2023-04-frankencoin
github_link: https://github.com/code-423n4/2023-04-frankencoin-findings/issues/396

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

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - ToonVH
  - santipu\_
  - DishWasher
  - cccz
  - joestakey
---

## Vulnerability Title

[M-10] No slippage control when minting and redeeming FPS

### Overview


This bug report is about the lack of slippage control when minting and redeeming FPS in Equity. Slippage control helps protect users from sandwich attacks, which occur when the price of FPS changes with the zchf reserve in the contract. To demonstrate this, the report outlines a scenario in which Alice and Bob use 4000 zchf and 400 FPS, respectively. Without slippage control, Alice would receive 710 FPS and Bob would receive 4258 zchf in profit. Proof of concept and recommended mitigation steps are also provided. The recommended mitigation step is to set minFPSout and minZCHFout parameters to allow slippage control when minting and redeeming FPS. This bug has been confirmed by luziusmeisser (Frankencoin).

### Original Finding Content


When minting and redeeming FPS in Equity, there is no slippage control. Since the price of FPS will change with the zchf reserve in the contract, users may suffer from sandwich attacks.

Consider the current contract has a zchf reserve of 1000 and a total supply of 1000.

Alice considers using 4000 zchf to mint FPS. Under normal circumstances, the contract reserve will rise to 5000 zchf, and the total supply will rise to (5000/1000)&ast;&ast;(1/3)&ast;1000 = 1710, that is, alice will get 1710 - 1000 = 710 FPS.

Bob holds 400 FPS, and bob observes alice's transaction in MemPool, bob uses MEV to preemptively use 4000 zchf to mint 710 FPS.

When alice's transaction is executed, the contract reserve will increase from 5000 to 9000 zchf, and the total supply will increase from 1710 to (9000/5000)&ast;&ast;(1/3)&ast;1710 = 2080, that is, alice gets 2080-1710 = 370FPS.

Then bob will redeem 400 FPS, the total supply will drop from 2080 to 1680, and the contract reserve will drop from 9000 to (1689/2080)&ast;&ast;3&ast;9000 = 4742, that is, bob gets 9000-4742 = 4258 zchf.

Bob's total profit is 310 FPS and 258 zchf.

### Proof of Concept

<https://github.com/code-423n4/2023-04-frankencoin/blob/1022cb106919fba963a89205d3b90bf62543f68f/contracts/Equity.sol#L241-L255> <br><https://github.com/code-423n4/2023-04-frankencoin/blob/1022cb106919fba963a89205d3b90bf62543f68f/contracts/Equity.sol#L266-L270> <br><https://github.com/code-423n4/2023-04-frankencoin/blob/1022cb106919fba963a89205d3b90bf62543f68f/contracts/Equity.sol#L275-L282> <br><https://github.com/code-423n4/2023-04-frankencoin/blob/1022cb106919fba963a89205d3b90bf62543f68f/contracts/Equity.sol#L290-L297>

### Recommended Mitigation Steps

Consider setting minFPSout and minZCHFout parameters to allow slippage control when minting and redeeming FPS

**[luziusmeisser (Frankencoin) confirmed](https://github.com/code-423n4/2023-04-frankencoin-findings/issues/396#issuecomment-1532494762):**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Frankencoin |
| Report Date | N/A |
| Finders | ToonVH, santipu\_, DishWasher, cccz, joestakey, KIntern\_NA, giovannidisiena, SolidityATL |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-frankencoin
- **GitHub**: https://github.com/code-423n4/2023-04-frankencoin-findings/issues/396
- **Contest**: https://code4rena.com/reports/2023-04-frankencoin

### Keywords for Search

`vulnerability`

