---
# Core Classification
protocol: Advanced Blockchain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17713
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ42021.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ42021.pdf
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Jim Miller
  - Sam Moelius
  - Natalie Chin
---

## Vulnerability Title

Slash amount is signiﬁcantly lower than the minimum stake amount

### Overview


This bug report concerns the runtime/picasso/src/lib.rs file of a Parachain network. The issue is that the value of PICA is set at 1,000,000,000,000, but the minimum stake required for a node to stake in the network is 1,000 PICA tokens and the slash amount is only 5. This means that a malicious node can still retain a significant portion of their stake after being slashed.

The short-term recommendation is to increase the slash amount to a significant portion of the minimum stake amount, incentivizing honest behavior. In the long-term, the arbitrary and template constants in the Composable Finance runtime should be reviewed and adjusted accordingly.

References to Staking and Slashing on the Polkadot Network and Slashing Incentives on Proof of Stake Blockchains are included.

### Original Finding Content

## Type: Undefined Behavior
## Target: runtime/picasso/src/lib.rs

### Difficulty: Low

### Description
Parachain nodes are not properly incentivized to behave honestly, as the `SlashAmount` is significantly lower than the `MinStake` amount. The value of PICA is defined in the runtime library as follows:

```rust
pub const PICA: Balance = 1_000_000_000_000;
```
_Figure 17.1: runtime/common/src/lib.rs#L73_

The minimum stake required for a node to stake in the network is 1,000 PICA tokens, but the slash amount is only 5.

```rust
//TODO set
parameter_types! {
    pub const StakeLock: BlockNumber = 50;
    pub const StalePrice: BlockNumber = 5;
    /// TODO: discuss with omar/cosmin
    pub const MinStake: Balance = 1000 * PICA;
    pub const RequestCost: Balance = PICA;
    pub const RewardAmount: Balance = 5 * PICA;
    // Shouldn't this be a ratio based on locked amount?
    pub const SlashAmount: Balance = 5;
    pub const MaxAnswerBound: u32 = 25;
    pub const MaxAssetsCount: u32 = 100_000;
}
```
_Figure 17.2: runtime/picasso/src/lib.rs#L369-L383_

### Exploit Scenario
Eve’s node has staked the minimum amount. Eve behaves maliciously, and her stake is slashed, but only by five PICA tokens. She therefore retains a significant portion of her stake.

### Recommendations
- **Short term**: Increase the slash amount such that it is a significant portion of the minimum stake amount. This will ensure that nodes are properly incentivized to behave honestly.
- **Long term**: Review the arbitrary and template constants defined in the Composable Finance runtime and adjust them to better suit this runtime.

### References
- Staking and Slashing on the Polkadot Network
- Slashing incentives on Proof of Stake Blockchains

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Advanced Blockchain |
| Report Date | N/A |
| Finders | Jim Miller, Sam Moelius, Natalie Chin |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ42021.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchainQ42021.pdf

### Keywords for Search

`vulnerability`

