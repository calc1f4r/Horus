---
# Core Classification
protocol: Sperax - USDs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59841
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html
source_link: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html
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
finders_count: 3
finders:
  - Shih-Hung Wang
  - Pavel Shabarkin
  - Ibrahim Abouzied
---

## Vulnerability Title

External Risks that May Affect Protocol Security

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> Given that USDs is built to act as a Yield-Automator for its holders. It will always be dependent on external protocols for generating the yield. At this point of time we can only focus on strengthening our process of integrating with other protocols like:
> 
> 
> 1.   Assessing the credibility, security and risks involved while selecting a strategy for a collateral.
> 2.   Strategies are to be linked only via governance proposals.
> 3.   Ensuring diversification in the USDs strategy portfolio.
> 4.   Actively monitoring the changes in the other protocols / depeg events impacting USDs.

**File(s) affected:**`oracle/SPAOracle.sol`, `oracle/USDsOracle.sol`, `strategies/aave/AaveStrategy.sol`, `strategies/compound/CompoundStrategy.sol`, `strategies/stargate/StargateStrategy.sol`, `vault/VaultCore.sol`

**Description:** The protocol extensively relies on several external applications, especially protocols that generate yields for USDs holders. Therefore, handling the failures of these external applications and controlling the damage is critical to the protocol. This issue highlights the possible failures of external applications and the potential impact:

**1. Implementation Changes in External Protocols**

The implementation of the strategy contracts highly depends on the behavior of the external protocols and their current configurations. For example, the`checkRewardEarned()`function of the`CompoundStrategy`contract assumes that the reward tokens are the same across all invested markets, which is not guaranteed to hold in the future. Also, the`_convertToCollateral()`function in the`StargateStrategy`contract assumes the conversion formula between LP and underlying tokens, which depends on Stargate implementation details. Therefore, a change in the external contracts in the future could possibly cause inconsistencies. Moreover, the protocol maintains the assumption that LP token and deposited collateral has same precision. For current strategies in review the implementation of the assumption is correct, however it is important to keep track of when adding new strategies to the protocol.

**2. Security Incidents of External Protocols and Depeg Events**

An attack on these protocols may cause the deposited collateral tokens to be lost. If the loss is significant and makes the USDs tokens not fully backed, USDs holders may likely choose to withdraw from the other unaffected strategies to avoid fund losses. After most or all the funds from the other strategies are withdrawn, the remaining holders withdrawing from the affected strategy will bear the loss for the others.

Similarly, if a stablecoin collateral depegs with a significant price fall, some USDs holders might redeem USDs for other unaffected collateral, further exacerbating the USDs unbacked situation.

**3. TWAP Oracle Manipulation**

Uniswap V3 pools with low liquidity are more vulnerable to manipulation since attackers require less capital to manipulate the prices. Also, the design of concentrated liquidity can make TWAP manipulations more cost-efficient, especially for the USDs/USDC pair, where most of the liquidity is likely to be concentrated around the center tick. A manipulated TWAP may affect the price evaluation in the`SPABuyback`and`YieldReserve`contracts, which may, for example, allow an attacker to buy USDs at a manipulated low price.

**Recommendation:**

1.   Consider keeping track of the latest status of the external protocols and ensuring that the assumptions still hold if new changes are introduced.

2.   Consider implementing on-chain monitoring systems and reacting promptly to security incidents on any external applications or potential TWAP manipulation activities, such as pausing the protocol operations to reduce the damage.

3.   Increase the TWAP window to the time window that is sufficient enough to reduce the described risk, and consider adding more liquidity to the Uniswap pool in the central and around central liquidity ticks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Sperax - USDs |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Pavel Shabarkin, Ibrahim Abouzied |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/sperax-us-ds/0612feed-ab51-4cb5-a2b2-32ed244dc385/index.html

### Keywords for Search

`vulnerability`

