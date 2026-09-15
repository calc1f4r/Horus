---
# Core Classification
protocol: Malt Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42390
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-11-malt
source_link: https://code4rena.com/reports/2021-11-malt
github_link: https://github.com/code-423n4/2021-11-malt-findings/issues/372

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
  - yield
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-25] AMM pool can be drained using a flashloan and calling `stabilize`

### Overview


The bug report highlights a vulnerability in the `StabilizerNode` contract, where an attacker can manipulate the price of Malt, a cryptocurrency, to steal a small amount of money from the protocol. This can also cause confusion and damage to the protocol. The recommended solution is to use a different method for calculating the trade size to prevent this exploit. The severity of the bug has been downgraded to medium, as there is not a clear incentive for an attacker to perform this exploit.

### Original Finding Content

_Submitted by stonesandtrees_

All of the `rewardToken` in a given AMM pool can be removed from the AMM pool and distributed as LP rewards.

#### Proof of Concept

In the `stabilize` method in the `StabilizerNode` the initial check to see if the Malt price needs to be stabilized it uses a short period TWAP:
<https://github.com/code-423n4/2021-11-malt/blob/main/src/contracts/StabilizerNode.sol#L156>

However, if the price is above the threshold for stabilization then the trade size required to stabilize looks at the AMM pool directly which is vulnerable to flashloan manipulation.

<https://github.com/code-423n4/2021-11-malt/blob/main/src/contracts/DexHandlers/UniswapHandler.sol#L250-L275>

Attack:

1.  Wait for TWAP to rise above the stabilization threshold
2.  Flashloan remove all but a tiny amount of Malt from the pool.
3.  Call `stabilize`. This will pass the TWAP check and execute `_distributeSupply` which in turn ultimately calls `_calculateTradeSize` in the `UniswapHandler`. This calculation will determine that almost all of the `rewardToken` needs to be removed from the pool to return the price to peg.
4.  Malt will mint enough Malt to remove a lot of the `rewardToken` from the pool.
5.  The protocol will now distribute that received `rewardToken` as rewards. 0.3% of which goes directly to the attacker and the rest goes to LP rewards, swing trader and the treasury.

The amount of money that can be directly stolen by a malicious actor is small but it can cause a lot of pain for the protocol as the pool will be destroyed and confusion around rewards will be created.

#### Recommended Mitigation Steps

Use a short TWAP to calculate the trade size instead of reading directly from the pool.

**[0xScotch (sponsor) confirmed](https://github.com/code-423n4/2021-11-malt-findings/issues/372)** 

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2021-11-malt-findings/issues/372#issuecomment-1020734907):**
 > I believe the warden has identified a valid grief and potential exploit
> 
> I'm not convinced on the simplicity of:
> `2. Flashloan remove all but a tiny amount of Malt from the pool.`
> 
> You'd have to buy that liquidity in order to be able to remove the malt, which effectively makes the operation not as straightforward (if not unprofitable for the attacker).
> 
> I do believe the grief can be performed but in lack of a clear incentive for the attacker, am going to downgrade to Medium Severity.
> Can be done, but not clear on the incentives





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Malt Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-malt
- **GitHub**: https://github.com/code-423n4/2021-11-malt-findings/issues/372
- **Contest**: https://code4rena.com/reports/2021-11-malt

### Keywords for Search

`vulnerability`

