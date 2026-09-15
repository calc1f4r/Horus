---
# Core Classification
protocol: Notional
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24663
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-notional
source_link: https://code4rena.com/reports/2022-01-notional
github_link: https://github.com/code-423n4/2022-01-notional-findings/issues/165

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
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-06] `getVotingPower` Is Not Equipped To Handle On-Chain Voting

### Overview


Notional is a decentralized governance platform that uses a token called `NOTE` to vote on governance issues. The `NOTE` token is staked in a contract called `sNOTE` to earn rewards. It is important for Notional's governance to correctly handle on-chain voting by tracking the relative voting power of `sNOTE` holders in terms of their equivalent `NOTE` amount. 

The `getVotingPower` function is used to track the relative voting power of a staker, however, it does not utilise any checkpointing mechanism to ensure the user's voting power is a snapshot of a specific block number. This makes it possible to manipulate a user's voting power by casting a vote on-chain and then have them transfer their `sNOTE` to another account to then vote again.

A proof of concept was provided which demonstrated how this manipulation could be done. To mitigate this issue, it is recommended to implement a `getPriorVotingPower` function which takes in a `blockNumber` argument and returns the correct balance at that specific block. This would also make the system more resilient to manipulation, such as using flashloans. This recommendation was confirmed by Notional and commented on by a judge.

### Original Finding Content

_Submitted by leastwood_

As `NOTE` continues to be staked in the `sNOTE` contract, it is important that Notional's governance is able to correctly handle on-chain voting by calculating the relative power `sNOTE` has in terms of its equivalent `NOTE` amount.

`getVotingPower` is a useful function in tracking the relative voting power a staker has, however, it does not utilise any checkpointing mechanism to ensure the user's voting power is a snapshot of a specific block number. As a result, it would be possible to manipulate a user's voting power by casting a vote on-chain and then have them transfer their `sNOTE` to another account to then vote again.

#### Proof of Concept

<https://github.com/code-423n4/2022-01-notional/blob/main/contracts/sNOTE.sol#L271-L293>
```solidity
function getVotingPower(uint256 sNOTEAmount) public view returns (uint256) {
    // Gets the BPT token price (in ETH)
    uint256 bptPrice = IPriceOracle(address(BALANCER_POOL_TOKEN)).getLatest(IPriceOracle.Variable.BPT_PRICE);
    // Gets the NOTE token price (in ETH)
    uint256 notePrice = IPriceOracle(address(BALANCER_POOL_TOKEN)).getLatest(IPriceOracle.Variable.PAIR_PRICE);
    
    // Since both bptPrice and notePrice are denominated in ETH, we can use
    // this formula to calculate noteAmount
    // bptBalance * bptPrice = notePrice * noteAmount
    // noteAmount = bptPrice/notePrice * bptBalance
    uint256 priceRatio = bptPrice * 1e18 / notePrice;
    uint256 bptBalance = BALANCER_POOL_TOKEN.balanceOf(address(this));

    // Amount_note = Price_NOTE_per_BPT * BPT_supply * 80% (80/20 pool)
    uint256 noteAmount = priceRatio * bptBalance * 80 / 100;

    // Reduce precision down to 1e8 (NOTE token)
    // priceRatio and bptBalance are both 1e18 (1e36 total)
    // we divide by 1e28 to get to 1e8
    noteAmount /= 1e28;

    return (noteAmount * sNOTEAmount) / totalSupply();
}
```

#### Recommended Mitigation Steps

Consider implementing a `getPriorVotingPower` function which takes in a `blockNumber` argument and returns the correct balance at that specific block.

**[jeffywu (Notional) confirmed](https://github.com/code-423n4/2022-01-notional-findings/issues/165)**


**[pauliax (judge) commented](https://github.com/code-423n4/2022-01-notional-findings/issues/165#issuecomment-1041539604):**
 > Great find, voting power snapshots would also make the system more resilient to manipulation, e.g. by using flashloans.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Notional |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-notional
- **GitHub**: https://github.com/code-423n4/2022-01-notional-findings/issues/165
- **Contest**: https://code4rena.com/reports/2022-01-notional

### Keywords for Search

`vulnerability`

