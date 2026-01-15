---
# Core Classification
protocol: Sentiment Update
chain: everychain
category: oracle
vulnerability_type: l2_sequencer

# Attack Vector Details
attack_type: l2_sequencer
affected_component: oracle

# Source Information
source: solodit
solodit_id: 3545
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/17
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-sentiment-judging/issues/3

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - l2_sequencer
  - chainlink
  - arbitrum

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - obront
  - pashov
---

## Vulnerability Title

M-4: No check for active Arbitrum Sequencer in WSTETH Oracle

### Overview


This bug report is about the WSTETH Oracle, which is a part of the Sentiment protocol. The bug is that the WSTETH Oracle does not have a check to make sure that the Arbitrum Sequencer is active before trusting the data returned by the oracle. This means that if the Arbitrum Sequencer goes down, then the data returned by the oracle will become stale, and users will be able to continue to interact with the protocol directly through the L1 optimistic rollup contract. This could lead to users being able to borrow more than they should be able to, as the protocol would be relying on stale data. 

The bug was found by pashov and obront, and was confirmed by zobront. The code snippet and recommendation are included in the report. The recommended fix is to add the same check to WSTETHOracle.sol that exists in ArbiChainlinkOracle.sol, which is a check to ensure that the Sequencer Uptime Feed is live before trusting the data returned by the oracle. A fix PR has also been provided.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-sentiment-judging/issues/3 

## Found by 
pashov, obront

## Summary

Chainlink recommends that all Optimistic L2 oracles consult the Sequencer Uptime Feed to ensure that the sequencer is live before trusting the data returned by the oracle. This check is implemented in ArbiChainlinkOracle.sol, but is skipped in WSTETHOracle.sol.

## Vulnerability Detail

If the Arbitrum Sequencer goes down, oracle data will not be kept up to date, and thus could become stale. However, users are able to continue to interact with the protocol directly through the L1 optimistic rollup contract. You can review Chainlink docs on [L2 Sequencer Uptime Feeds](https://docs.chain.link/docs/data-feeds/l2-sequencer-feeds/) for more details on this.

As a result, users may be able to use the protocol while oracle feeds are stale. This could cause many problems, but as a simple example:
- A user has an account with 100 tokens, valued at 1 ETH each, and no borrows
- The Arbitrum sequencer goes down temporarily
- While it's down, the price of the token falls to 0.5 ETH each
- The current value of the user's account is 50 ETH, so they should be able to borrow a maximum of 200 ETH to keep account healthy (`(200 + 50) / 200 = 1.2`)
- Because of the stale price, the protocol lets them borrow 400 ETH (`(400 + 100) / 400 = 1.2`)

## Impact

If the Arbitrum sequencer goes down, the protocol will allow users to continue to operate at the previous (stale) rates.

## Code Snippet

https://github.com/sherlock-audit/2022-11-sentiment/blob/main/oracle-merged/src/wsteth/WSTETHOracle.sol#L45-L57

## Tool used

Manual Review

## Recommendation

Add the same check to WSTETHOracle.sol that exists in ArbiChainlinkOracle.sol:

```solidity
function getPrice(address token) external view override returns (uint) {
    if (!isSequencerActive()) revert Errors.L2SequencerUnavailable();
    ...
}
```

```solidity
function isSequencerActive() internal view returns (bool) {
    (, int256 answer, uint256 startedAt,,) = sequencer.latestRoundData();
    if (block.timestamp - startedAt <= GRACE_PERIOD_TIME || answer == 1)
        return false;
    return true;
}
```

## Discussion

**r0ohafza**

Fix PR: https://github.com/sentimentxyz/oracle/pull/46

**zobront**

PR confirmed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Sentiment Update |
| Report Date | N/A |
| Finders | obront, pashov |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-sentiment-judging/issues/3
- **Contest**: https://app.sherlock.xyz/audits/contests/17

### Keywords for Search

`L2 Sequencer, Chainlink, Arbitrum`

