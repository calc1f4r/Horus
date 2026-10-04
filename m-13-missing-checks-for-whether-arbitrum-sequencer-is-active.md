---
# Core Classification
protocol: Blueberry Update
chain: everychain
category: oracle
vulnerability_type: l2_sequencer

# Attack Vector Details
attack_type: l2_sequencer
affected_component: oracle

# Source Information
source: solodit
solodit_id: 18507
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/69
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/142

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
  - l2_sequencer
  - arbitrum
  - stale_price
  - oracle
  - missing-logic

protocol_categories:
  - lending
  - leveraged_farming
  - options_vault

# Audit Details
report_date: unknown
finders_count: 9
finders:
  - Bauer
  - J4de
  - tallo
  - tsvetanovv
  - deadrxsezzz
---

## Vulnerability Title

M-13: Missing checks for whether Arbitrum Sequencer is active

### Overview


This bug report is about the missing checks for whether the Arbitrum Sequencer is active. It was found by 0xepley, Bauchibred, Bauer, Brenzee, J4de, ctf\_sec, deadrxsezzz, tallo, and tsvetanovv. The protocol intends to deploy to Arbtrium, and Chainlink recommends that users using price oracles check whether the Arbitrum sequencer is active. If the sequencer goes down, the index oracles may have stale prices which can result in false liquidation or over-borrowing. The code snippet for this issue can be found at the given link. The tool used was Manual Review. The recommendation is to use sequencer oracle to determine whether the sequencer is offline or not, and not to allow orders to be executed while the sequencer is offline.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/142 

## Found by 
0xepley, Bauchibred, Bauer, Brenzee, J4de, ctf\_sec, deadrxsezzz, tallo, tsvetanovv
## Summary

Missing checks for whether Arbitrum Sequencer is active

## Vulnerability Detail

the onchain deployment context is changed, in prev contest the protocol only attemps to deploy the code to ethereum while in the current contest

the protocol intends to deploy to arbtrium as well!

Chainlink recommends that users using price oracles, check whether the Arbitrum sequencer is active

https://docs.chain.link/data-feeds#l2-sequencer-uptime-feeds

If the sequencer goes down, the index oracles may have stale prices, since L2-submitted transactions (i.e. by the aggregating oracles) will not be processed.

## Impact

Stale prices, e.g. if USDC were to de-peg while the sequencer is offline, stale price is used and can result in false liquidation or over-borrowing.

## Code Snippet

https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/oracle/ChainlinkAdapterOracle.sol#L76-L98

## Tool used

Manual Review

## Recommendation

Use sequencer oracle to determine whether the sequencer is offline or not, and don't allow orders to be executed while the sequencer is offline.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update |
| Report Date | N/A |
| Finders | Bauer, J4de, tallo, tsvetanovv, deadrxsezzz, Brenzee, Bauchibred, 0xepley, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/142
- **Contest**: https://app.sherlock.xyz/audits/contests/69

### Keywords for Search

`L2 Sequencer, Arbitrum, Stale Price, Oracle, Missing-Logic`

