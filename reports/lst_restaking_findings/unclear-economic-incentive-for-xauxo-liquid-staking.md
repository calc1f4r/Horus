---
# Core Classification
protocol: Auxo Governance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60575
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/auxo-governance/6d7dbf90-5898-41c6-a929-3c7a69e9df28/index.html
source_link: https://certificate.quantstamp.com/full/auxo-governance/6d7dbf90-5898-41c6-a929-3c7a69e9df28/index.html
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Ed Zulkoski
  - Ruben Koch
  - Cameron Biniamow
  - Mostafa Yassin
---

## Vulnerability Title

Unclear Economic Incentive for `xAUXO` Liquid Staking

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client.

The client provided the following explanation:

QSP-3 was raised as high severity due to the fact that the xAUXO does not have a withdraw mechanism, and, consequently, there is no guarantee of price parity between AUXO. The comparison was made between staking derivatives between ETH and stETH, where the price is dictated by the ability of the token to be redeemed for ETH at some later date.

xAUXO is easier to compare with other staking derivatives, with significant TVL and application across DeFi, that utilise one-way staking derivatives and no guarantee of price pegging. Examples of such protocols include veCRV/cvxCRV (Curve and ConvexCurve), and Balancer/AURA finance.

The Auxo team feel that, because such protocols have been successful without offering a price peg, this particular issue is incorrectly flagged as high severity when it should be considered 'informational', and communicated clearly to users. Additionally, the DAO has plans to allocate resources to xAUXO buybacks, which, while still to be confirmed, are aiming to give xAUXO holders opportunities to exit their positions.

**File(s) affected:**`xAUXO.sol`, `StakingManager.sol`

**Description:** Typically, liquid staking protocols (e.g., Lido or Coinbase's cbETH) propose liquid staking so that if users do not wish to actively participate in the protocol (e.g., by running an ETH2 validator node), they can still earn a portion of the staking rewards (effectively by delegating stake). In these two example systems, while users hold the Lido `stETH` tokens or Coinbase `cbETH` tokens, they will accrue rewards, which are some fraction of the rewards earned by the underlying validator nodes. The prices of [cbETH](https://coinmarketcap.com/currencies/coinbase-wrapped-staked-eth/) and [stETH](https://coinmarketcap.com/currencies/steth/) typically follow the same trend as ETH (with some deviation due to rewards or general market fluctuations).

However, a key reason for this price parity between `cbETH<>ETH` and `stETH<>ETH` is that **eventually, it will be possible to withdraw ETH from the validator network**. Suppose this were not the case, i.e., users deposited ETH with no chance of ever recovering their tokens. If, for example, the user deposited 1 ETH valued at $2000 at time of stake, then they would need to expect at least $2000 return in rewards, otherwise there would be no economic incentive to stake in the first place.

This possibility of withdrawal does not appear to exist in `xAUXO`, and a comment explicitly states "tokens are [locked in] stakingManager in perpetuity, no coming back". As such, there does not appear to be any reason for price parity between `AUXO<>xAUXO`, making the utility and incentive of the `xAUXO` system unclear.

**Recommendation:** Revise the economic incentive system behind `xAUXO`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Auxo Governance |
| Report Date | N/A |
| Finders | Ed Zulkoski, Ruben Koch, Cameron Biniamow, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/auxo-governance/6d7dbf90-5898-41c6-a929-3c7a69e9df28/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/auxo-governance/6d7dbf90-5898-41c6-a929-3c7a69e9df28/index.html

### Keywords for Search

`vulnerability`

