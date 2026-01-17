---
# Core Classification
protocol: Elixir Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41638
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf
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
  - Damilola Edwards
  - Emilio López
  - Bo Henderson
  - Artur Cygan
---

## Vulnerability Title

Attackers can cause slashing to become economically infeasible

### Overview

See description below for full details.

### Original Finding Content

## Type: Timing

## Difficulty: Low

## Description
The slash function takes a single address as a parameter, alongside the amount to be slashed. When a significant number of users needs to be slashed, the slash function must be called for each address individually. This approach becomes infeasible if there is a large number of small delegations.

```solidity
/// @notice Slashes a staker
/// @param staker Staker to be slashed
/// @param amount Amount to be slashed
function slash(address staker, uint256 amount) external onlyCore {
    // Reduces staked balance.
    stakedBalance[staker] -= amount;
    // Reduced delegated balance.
    _moveDelegates(delegates[staker], address(0), amount);
    // Transfers the tokens.
    elixirToken.safeTransfer(msg.sender, amount);
    emit Slashed(staker, amount, stakedBalance[staker]);
}
```
*Figure 11.1: The slash method (StakeManager.sol#L271-L285)*

Based on the current design of the protocol, when a validator is jailed, all delegators who staked with that jailed validator will have their stakes locked and potentially slashed. However, in the event of slashing, each affected delegator needs to be slashed individually. The cost of performing slashing on the entire set of affected delegators increases proportionally with the number of delegators involved. In cases where the number of affected delegators is significantly large, the high cost may discourage the execution of slashing, allowing delegators to evade the intended penalty.

## Exploit Scenario
Bob acquires ELX tokens with the intent of misbehaving. To grief the protocol by making it less cost effective for him to be slashed, he distributes small amounts of his tokens among a large number of accounts and delegates them all to himself. After Bob is jailed for acting maliciously, the cost of recovering ELX from his delegators is prohibitively expensive.

## Recommendations
**Short term:** Consider implementing an additional batch slash method in the StakeManager contract that accepts an array of addresses and slashes each down to a zero balance. Some arithmetic and conditional logic can be skipped, making this a cheaper and easier way to recover funds from a large number of misbehaving accounts.

**Long term:** Keep in mind that a delegatee with a small number of large delegators may have an equal weight as a delegatee with a large number of small delegators. Consider both situations and ways an attacker may take advantage of differences such as gas economics.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Elixir Protocol |
| Report Date | N/A |
| Finders | Damilola Edwards, Emilio López, Bo Henderson, Artur Cygan |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf

### Keywords for Search

`vulnerability`

