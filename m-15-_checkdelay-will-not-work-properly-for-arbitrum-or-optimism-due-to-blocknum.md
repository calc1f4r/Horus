---
# Core Classification
protocol: Tigris Trade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6345
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-tigris-trade-contest
source_link: https://code4rena.com/reports/2022-12-tigris
github_link: https://github.com/code-423n4/2022-12-tigris-findings/issues/419

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

protocol_categories:
  - dexes
  - services
  - derivatives
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

[M-15] _checkDelay will not work properly for Arbitrum or Optimism due to block.number 

### Overview


This bug report is about a vulnerability that allows users to exploit multiple valid prices by bypassing a trade delay on Arbitrum. The trade delay is enforced by the function _checkDelay which uses block.number to measure the delay. However, since the block.number is only synced once per minute, users can open and close their position within the same Arbitrum block, appearing as if the delay was respected when it wasn't. The same issue occurs on Optimism, where each transaction is its own block.

The recommended mitigation step is to use block.timestamp instead of block.number to measure the delay. This way, the delay will be respected regardless of how many transactions are included in the same block.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-12-tigris/blob/588c84b7bb354d20cbca6034544c4faa46e6a80e/contracts/Trading.sol#L857-L868


## Vulnerability details

## Impact

Trade delay will not work correctly on Arbitrum allowing users to exploit multiple valid prices 

## Proof of Concept

    function _checkDelay(uint _id, bool _type) internal {
        unchecked {
            Delay memory _delay = blockDelayPassed[_id];
            //in those situations
            if (_delay.actionType == _type) {
                blockDelayPassed[_id].delay = block.number + blockDelay;
            } else {
                if (block.number < _delay.delay) revert("0"); //Wait
                blockDelayPassed[_id].delay = block.number + blockDelay;
                blockDelayPassed[_id].actionType = _type;
            }
        }
    }

_checkDelay enforces a delay of a specific number of block between opening and closing a position. While this structure will work on mainnet, it is problematic for use on Arbitrum. According to Arbitrum [Docs](https://developer.offchainlabs.com/time) `block.number` returns the most recently synced L1 block number. Once per minute the block number in the Sequencer is synced to the actual L1 block number. This period could be abused to completely bypass this protection. The user would open their position 1 Arbitrum block before the sync happens, the close it the very next block. It would appear that there has been 5 block (60 / 12) since the last transaction but in reality it has only been 1 Arbitrum block. Given that Arbitrum has 2 seconds blocks I would be impossible to block this behavior through parameter changes.

It also presents an issue for [Optimism](https://community.optimism.io/docs/developers/build/differences/#block-numbers-and-timestamps) because each transaction is it's own block. No matter what value is used for the block delay, the user can pad enough tiny transactions to allow them to close the trade immediately. 

## Tools Used

Manual Review

## Recommended Mitigation Steps

The delay should be measured using block.timestamp rather than block.number

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Tigris Trade |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tigris
- **GitHub**: https://github.com/code-423n4/2022-12-tigris-findings/issues/419
- **Contest**: https://code4rena.com/contests/2022-12-tigris-trade-contest

### Keywords for Search

`vulnerability`

