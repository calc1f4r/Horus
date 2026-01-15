---
# Core Classification
protocol: Coinflip_2025-02-05
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55492
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Coinflip-security-review_2025-02-05.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-01] Excessive `msg.value` is not transferred to the player after the `requestRandomness` call

### Overview

See description below for full details.

### Original Finding Content

The `pythRandomnessProvider::requestRandomness` function is called by the `Flip::flip` contract to retrieve the `random number` to compute whether the player has won the game. The `requestRandomness` function calls the `entropy::requestWithCallback` function with the respective `fee amount for the default provider` as shown below:

```solidity

        uint64 sequenceNumber = entropy.requestWithCallback{value: msg.value}(entropyProvider, userRandomNumber);

```

The `feeAmount` is passed onto this call via the `Flip::flip` as shown below:

```solidity

            uint256 fee = randomnessProvider.getFee();

            require(msg.value >= fee, “Insufficient fee for randomness”);

```

The issue here is that the returned fee amount by the `randomnessProvider.getFee()` changes based on the prevailing gas price on-chain as mentioned in the pyth documentation.

> The following tables shows the total fees payable when using the default provider. Note that the fees shown below will vary over time with prevailing gas prices on each chain.

https://docs.pyth.network/entropy/current-fees

Hence by the time the `flip transaction is executed` if the `default provider fee is decreased` the excessive `msg.value` will be stuck in the `Flip.sol` contract.

Hence it is recommended to transfer the `excessive fee amount (msg.value - fee)` back to the `player (msg.sender)` after the `randomnessProvider.requestRandomness` call is made.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Coinflip_2025-02-05 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Coinflip-security-review_2025-02-05.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

