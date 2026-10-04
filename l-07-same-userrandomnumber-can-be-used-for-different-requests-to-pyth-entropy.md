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
solodit_id: 55498
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

[L-07] Same `userRandomNumber` can be used for different requests to pyth entropy

### Overview

See description below for full details.

### Original Finding Content

The game ID is calculated in `Flip.flip()` as follows:

```solidity
    bytes32 gameIdBytes =
        keccak256(abi.encodePacked(msg.sender, block.timestamp, numberOfCoins, headsRequired, nonce++));
    string memory gameId = string(abi.encodePacked(gameIdBytes));
```

This value is used in `PythRandomnessProvider.requestRandomness()` to calculate the user random number that will be sent in the call to `entropy.requestWithCallback()`:

```solidity
    bytes32 userRandomNumber = keccak256(abi.encodePacked(gameId, block.timestamp));

    uint64 sequenceNumber = entropy.requestWithCallback{value: msg.value}(entropyProvider, userRandomNumber); // CHANGED FROM GETFEE
```

There is the possibility that the same `userRandomNumber` is used for different requests if a user initiates multiple games from different contracts and uses the same parameters, in the same block. If this was the case, a malicious entropy provider would have it easier to manipulate the result of the randomness request.

It is recommended to include the address of the game contract in the `userRandomNumber` calculation to avoid this issue.

```diff
-    bytes32 userRandomNumber = keccak256(abi.encodePacked(gameId, block.timestamp));
+    bytes32 userRandomNumber = keccak256(abi.encodePacked(gameId, block.timestamp, msg.sender));
```

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

