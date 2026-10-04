---
# Core Classification
protocol: Y2k Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5775
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-09-y2k-finance-contest
source_link: https://code4rena.com/reports/2022-09-y2k-finance
github_link: https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/283

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
  - services
  - liquidity_manager
  - insurance

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - PwnPatrol
---

## Vulnerability Title

[H-03] A design flaw in the case of using 2 oracles (aka PegOracle)

### Overview


A design flaw has been discovered in the case of using two oracles, known as PegOracle, when it comes to providing price feeds denominated in ETH or USD. This flaw comes from the fact that PegOracle treats both assets symmetrically, even when one of the assets behaves as expected. This can create an issue in the case of a market on renBTC depegging from BTC value, as the depeg event can be triggered when WBTC significantly depreciates or appreciates against BTC value, even if renBTC perfectly maintains its value to BTC. The same is true for ETH pairs like stETH/aETH and stablecoin pairs like FRAX/MIM. To avoid this, it is recommended to only support markets for assets that have access to an oracle with price against canonical value x/ETH or x/USD.

### Original Finding Content


A design flaw in the case of using 2 oracles (aka PegOracle).

### Proof of Concept

Chainlink provides price feeds denominated either in ETH or USD. But some assets don't have canonical value accessed on-chain. An example would be BTC and it's many on-chain forms like renBTC, hitBTC, WBTC, aBTC etc... For example in the case of a market on renBTC depegging from BTC value, probably a pair like renBTC/WBTC would be used (leveraging PegOracle). But even if renBTC perfectly maintains it's value to BTC, the depeg event can be triggered when WBTC significantly depreciates or appreciates against BTC value. This depeg event will be theoretically unsound since renBTC behaved as expected. The flaw comes from PegOracle because it treats both assets symmetrically.

This is also true for ETH pairs like stETH/aETH etc.. or stablecoin pairs like FRAX/MIM etc..
Of course, it should never be used like this because Chainlink provides price feeds with respect to true ETH and USD values but we have found that test files include PegOracle for stablecoin pairs.

### Recommended Mitigation Steps

Support markets only for assets that have access to an oracle with price against canonical value x/ETH or x/USD.

**[MiguelBits (Y2K Finance) disputed](https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/283)** 


**[HickupHH3 (judge) commented](https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/283#issuecomment-1281801755):**
 > From what I understand, the warden is arguing that if the underlying asset is itself a pegged asset, then it wouldn't be a very good measure against the "canonical price". 
> 
> Eg. `MIM` (pegged) -> `USDC` (underlying), and USDC de-pegs, even though MIM is close to `$1`, the protocol would recognise this as a de-peg event.
> 
> I agree with the issue, but disagree with the severity. The choice of the underlying token is quite obviously important; I think the sponsor can attest to this.
> 
> @3xHarry thoughts? Perhaps low severity is more appropriate because it isn't a technical vulnerability per-se, more of the choice of underlying to be used.

**[HickupHH3 (judge) commented](https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/283#issuecomment-1281879652):**
 > Keeping high severity even though there are a couple of prerequisites:
> - the protocol uses a poor underlying token (Eg. USDT that has de-pegged to `$0.97` before)
> - underlying token de-pegs substantially to inaccurately trigger (or not trigger) a de-peg event
> 
> I classify this as indirect loss of assets from a valid attack path that does not have hand-wavy hypotheticals
> > 3 — High: Assets can be stolen/lost/compromised directly (or indirectly if there is a valid attack path that does not have hand-wavy hypotheticals).
> 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Y2k Finance |
| Report Date | N/A |
| Finders | PwnPatrol |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-y2k-finance
- **GitHub**: https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/283
- **Contest**: https://code4rena.com/contests/2022-09-y2k-finance-contest

### Keywords for Search

`vulnerability`

