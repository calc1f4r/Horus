---
# Core Classification
protocol: Cryptex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40216
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c146b746-c0ce-4310-933c-d2e5e3ec934a
source_link: https://cdn.cantina.xyz/reports/cantina_cryptex_sep2024.pdf
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
finders_count: 2
finders:
  - cccz
  - Patrick Drotleff
---

## Vulnerability Title

Harden Chainlink Price Feed integration 

### Overview

See description below for full details.

### Original Finding Content

## AggregatedChainlinkOracle Analysis

## Context
**File:** AggregatedChainlinkOracle.sol#L18-L21

## Description
The `AggregatedChainlinkOracle` currently lacks validation of the returned data, aside from a simple sanity check ensuring the price is non-zero.

```solidity
function latestPrice() public view virtual override returns (uint256) {
    (, int256 answer,,,) = feed.latestRoundData();
    // @audit in case of a stale oracle do not revert because it would prevent users from withdrawing
    assert(answer > 0);
    // @audit feed decimals cannot exceed 18
    uint256 adjustedDecimalsAnswer = uint256(answer) * 10 ** (18 - feedDecimals);
    return adjustedDecimalsAnswer;
}
```

The Cryptex Team aims to allow users to withdraw any free funds at any time and prefers to keep functions that enhance protocol health—such as debt burning and liquidations—available at all times. Introducing checks for the freshness of price information may obstruct these objectives by causing these actions to revert.

Officially, Chainlink "encourages" users to verify whether the received data is current by inspecting `updatedAt` (or `answeredInRound`, which has been deprecated). In practice, many protocols completely disregard such checks, as seen here. Others implement a diverse range of staleness threshold checks based on `updatedAt`, using constant thresholds like:

- 5m
- 90m
- 4h
- 24h

Some protocols allow these thresholds to be configured via storage.

There is no clear consensus on whether and how to check for the "freshness" of feed prices. Additionally, various sanity checks are commonly implemented in projects similar to `assert(answer > 0)`:

- `assert(roundId > 0)`
- `assert(updatedAt > 0)`
- `assert(updatedAt <= block.timestamp)`

It can be verified that ignoring `startedAt` and `answeredInRound` is safe by examining Chainlink's contracts, which simply return the values for `updatedAt` and `roundId` respectively. 

While implementing these sanity checks might pose little harm, threshold checks on `updatedAt` or price need to be determined based on the project's nature and associated risks.

## Risk Analysis
As TCAP is a synthetic asset, there seems to be little immediate risk from its oracle price being outdated—it remains pegged to the target price. However, outdated collateral prices could lead to arbitrage opportunities. For example, if the collateral is ETH and the oracle price remains high while the market value has significantly decreased, actions could lead to profitability:

> Buying ETH from an AMM, depositing it into a Vault, minting TCAP, and selling for ETH again—repeatedly.

The older Cryptex proposal CIP-14 exemplifies such exploitation.

In addition to risks from stale prices, there are concerns regarding prices that are updated after being stale. A stale oracle target price for TCAP may be harmless, but sudden increases in TCAP price upon re-updating the total market cap oracle could catch many borrowers off guard, possibly leading to sudden liquidations. Conversely, borrowers monitoring market price movements might leverage the period before price feeds are updated to exit positions, while less informed borrowers may suffer.

On Layer 2 solutions, these circumstances can be particularly problematic. For instance, many Layer 2s, including the protocol's target chain Arbitrum, permit transaction submissions even when the sequencer is down. It is reasonable to assume that liquidators are often more technically adept than the average borrower and might exploit this when borrowers cannot access the protocol to maintain sufficient collateral. Some protocols, such as Aave, have implemented "borrower grace periods" to prevent liquidations or further borrowing until borrowers can secure their positions after sequencer downtime.

## Recommendations
- Add the aforementioned sanity checks.
- Implement monitoring for Chainlink price feeds and Arbitrum sequencer to track irregularities.
- Set up monitoring to identify "arbitrage opportunities" and inform the team about significant market price discrepancies.
- Consider implementing grace periods for borrowers following a sequencer outage.
- Encourage borrowers to subscribe to notifications about potential risks to their positions from oracle or sequencer outages.
- Document and publish guidelines for the governance community to respond to such incidents.
- Consider implementing circuit breakers for extreme cases of price staleness or deviations. In rare instances where circuit breakers engage, a governance proposal may deploy adjusted oracle contracts with updated parameters based on the situation.
- Instead of entirely pausing the protocol with circuit breakers, consider "speed bumps" that prevent flash loans during price staleness, de-pegging conditions, or market volatility. Such methods can mitigate arbitrage opportunities relying on flash loans by ensuring a time gap between deposit and mint actions.
- If price checks will be limited to specific interactions with the protocol, it is advised to incorporate them into the mint function, preventing the creation of new debt during risky periods. Disallowing liquidations may favor the protocol, but it might lead to unfair liquidation of borrowers, especially if only one oracle (collateral or TCAP target price) becomes stale. Allowing withdrawals of "free" collateral while oracles are outdated could enable the protocol to bear temporary bad debt once oracles are functional again. Given the Cryptex Team's intention to allow withdrawals anytime for users’ benefit, governance should consider establishing emergency funds to manage any resultant bad debt that could negatively affect the TCAP price peg.

## Action Taken
- **Cryptex:** Fixed in commit `3209c762`.
- **Cantina Managed:** Fixed. The Cryptex Team addressed this finding by adding a staleness check executed only when minting TCAP (i.e., when creating new debt).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Cryptex |
| Report Date | N/A |
| Finders | cccz, Patrick Drotleff |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_cryptex_sep2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c146b746-c0ce-4310-933c-d2e5e3ec934a

### Keywords for Search

`vulnerability`

