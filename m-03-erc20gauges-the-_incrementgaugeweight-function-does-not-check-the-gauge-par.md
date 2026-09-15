---
# Core Classification
protocol: Tribe
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2069
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-xtribe-contest
source_link: https://code4rena.com/reports/2022-04-xtribe
github_link: https://github.com/code-423n4/2022-04-xtribe-findings/issues/5

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - validation
  - business_logic

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cccz
  - 0x52
---

## Vulnerability Title

[M-03] `ERC20Gauges`: The `_incrementGaugeWeight` function does not check the gauge parameter enough, so the user may lose rewards

### Overview


A bug was found in the _incrementGaugeWeight function of the ERC20Gauges.sol smart contract. This function is used to increase the user's weight on the gauge, but it only checks that the gauge parameter is not in _deprecatedGauges, not that it is in _gauges. If the wrong gauge parameter is used, the function will be executed without any warning, which can lead to user loss. A proof of concept can be found in the given link. To mitigate this bug, the code should be changed to check that the gauge parameter is not in _deprecatedGauges and is in _gauges.

### Original Finding Content

_Submitted by cccz, also found by 0x52_

The \_incrementGaugeWeight function is used to increase the user's weight on the gauge. However, in the \_incrementGaugeWeight function, it is only checked that the gauge parameter is not in \_deprecatedGauges, but not checked that the gauge parameter is in \_gauges. If the user accidentally uses the wrong gauge parameter, the function will be executed smoothly without any warning, which will cause user loss reward.

        function _incrementGaugeWeight(
            address user,
            address gauge,
            uint112 weight,
            uint32 cycle
        ) internal {
            if (_deprecatedGauges.contains(gauge)) revert InvalidGaugeError();
            unchecked {
                if (cycle - block.timestamp <= incrementFreezeWindow) revert IncrementFreezeError();
            }

            bool added = _userGauges[user].add(gauge); // idempotent add
            if (added && _userGauges[user].length() > maxGauges && !canContractExceedMaxGauges[user])
                revert MaxGaugeError();

            getUserGaugeWeight[user][gauge] += weight;

            _writeGaugeWeight(_getGaugeWeight[gauge], _add, weight, cycle);

            emit IncrementGaugeWeight(user, gauge, weight, cycle);
        }
        ...
        function _writeGaugeWeight(
            Weight storage weight,
            function(uint112, uint112) view returns (uint112) op,
            uint112 delta,
            uint32 cycle
        ) private {
            uint112 currentWeight = weight.currentWeight; // @audit  currentWeight = 0
            // If the last cycle of the weight is before the current cycle, use the current weight as the stored.
            uint112 stored = weight.currentCycle < cycle ? currentWeight : weight.storedWeight; // @audit  stored = 0 < cycle ? 0 : 0
            uint112 newWeight = op(currentWeight, delta); // @audit newWeight = 0 + delta

            weight.storedWeight = stored;
            weight.currentWeight = newWeight;
            weight.currentCycle = cycle;
        }

### Proof of Concept

[ERC20Gauges.sol#L257](https://github.com/fei-protocol/flywheel-v2/blob/77bfadf388db25cf5917d39cd9c0ad920f404aad/src/token/ERC20Gauges.sol#L257)<br>

### Recommended Mitigation Steps

        function _incrementGaugeWeight(
            address user,
            address gauge,
            uint112 weight,
            uint32 cycle
        ) internal {
    -       if (_deprecatedGauges.contains(gauge)) revert InvalidGaugeError();
    +       if (_deprecatedGauges.contains(gauge) || !_gauges.contains(gauge)) revert InvalidGaugeError();
            unchecked {
                if (cycle - block.timestamp <= incrementFreezeWindow) revert IncrementFreezeError();
            }

            bool added = _userGauges[user].add(gauge); // idempotent add
            if (added && _userGauges[user].length() > maxGauges && !canContractExceedMaxGauges[user])
                revert MaxGaugeError();

            getUserGaugeWeight[user][gauge] += weight;

            _writeGaugeWeight(_getGaugeWeight[gauge], _add, weight, cycle);

     }

**[Joeysantoro (xTRIBE) disagreed with High severity and commented](https://github.com/code-423n4/2022-04-xtribe-findings/issues/5#issuecomment-1109219762):**
 > This is absolutely a valid logic bug. I disagree with the severity, as it would be user error to increment a gauge which was incapable of receiving any weight. Should be medium.

**[0xean (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-04-xtribe-findings/issues/5#issuecomment-1130311075):**
 > This is a tough one to call between medium and high severity. Assets can directly be lost, but putting the wrong address into ANY function call in general is an easy way for a user to lose funds and isn't unique to this protocol.  I am going to side with the sponsor and downgrade to medium severity. 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Tribe |
| Report Date | N/A |
| Finders | cccz, 0x52 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-xtribe
- **GitHub**: https://github.com/code-423n4/2022-04-xtribe-findings/issues/5
- **Contest**: https://code4rena.com/contests/2022-04-xtribe-contest

### Keywords for Search

`Validation, Business Logic`

