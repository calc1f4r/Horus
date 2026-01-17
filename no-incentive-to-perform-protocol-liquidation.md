---
# Core Classification
protocol: Ion Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32720
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/ion-protocol-audit
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

No Incentive to Perform Protocol Liquidation

### Overview


The `Liquidation` contract has a function called `liquidate` that is used to liquidate a vault when it does not have enough collateral to meet the `TARGET_HEALTH` ratio. However, when the vault does have enough collateral, the caller pays off the debt and receives the discounted collateral. This does not incentivize anyone to perform a liquidation when there is not enough collateral, which could cause delays. The Ion Protocol team has acknowledged this issue but does not consider it a vulnerability as there is a fallback option for protocol liquidations where the bad debt is transferred to the protocol's balance sheet. They see this as an extra utility for governance and not a vulnerability.

### Original Finding Content

The [`liquidate` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/Liquidation.sol#L162) of the `Liquidation` contract performs a "protocol" liquidation when there is insufficient collateral to bring the health ratio of a vault up to the `TARGET_HEALTH` ratio. In this type of liquidation, the `PROTOCOL` address receives the collateral from the underwater vault and is responsible for repaying the bad debt. During a liquidation in which the vault does have enough collateral to bring its health ratio back to `TARGET_HEALTH`, the caller pays off the debt of the vault by transferring WETH to the contract, and the keeper (specified by the caller) receives the vault's collateral at a discount such that liquidating the vault is profitable to the caller. Since a protocol liquidation does not transfer discounted collateral to the caller, there is no incentive for anyone to perform a protocol liquidation.


Consider providing an incentive to users to perform protocol liquidations to ensure they are done in a timely manner.


***Update:** Acknowledged, not resolved. Ion Protocol team stated:*



> *This is known and by design. We would not consider this a vulnerability. The option for protocol liquidation exists as a fallback path where the liquidator pays the gas fees for transferring the vault's bad debt to the protocol balance sheet. Vaults that are already in bad debt do not need to be liquidated by searchers and therefore doesn't require incentives.*
> 
> 
> *In more detail:*
> 
> 
> *Protocol liquidations are liquidations where there is not enough collateral to be sold at the discounted price to reach the target health ratio. If there’s bad debt in the position (debt that can’t be paid off with collateral), there is also no profitable path for the liquidator, and we do not expect a searcher to call an unprofitable trade.*
> 
> 
> *The protocol liquidation logical path only exists such that if for some reason a searcher tries to liquidate a position that is in bad debt, it will simply automatically transfer this bad debt to the badDebt variable in IonPool such that the unprofitable searcher pays for the gas cost of transferring badDebt instead of governance having to manually call the transaction.*
> 
> 
> *The alternative option is to simply not do anything about this when bad debt forms, but we decided to add this fallback to automatically transfer bad debt to the balance sheet without paying for gas.*
> 
> 
> *We see this as extra utility for the governance and therefore not a vulnerability.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Ion Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/ion-protocol-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

