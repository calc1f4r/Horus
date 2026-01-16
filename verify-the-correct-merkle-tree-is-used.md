---
# Core Classification
protocol: Paladin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6866
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - DefSec
  - Jay Jonah8
  - Gerard Persoon
---

## Vulnerability Title

Verify the correct merkle tree is used

### Overview


This bug report is about the MultiMerkleDistributor.sol contract, which is a part of the balance-tree.ts code. The issue is that the contract does not verify that the merkle tree belongs to the right quest and period. If the wrong merkle tree is added, then the wrong rewards can be claimed. The likelihood of this happening is low, but the impact is high, so it has been set to a medium risk. 

A solution which does not cost any extra storage but requires a small amount of gas involves adding questid and period into the merkle tree nodes, assuring rewards can only be claimed in combination with the right questid and period. The code in the balance-tree.ts file was changed to include questID, period, index, account, and amount in the keccak256 hash, while the code in the MultiMerkleDistributor.sol file was changed to include questID, period, index, account, and amount in the keccak256 hash. The changes were implemented in #12 and acknowledged.

### Original Finding Content

## Risk Assessment

## Severity
**Medium Risk**

## Context
- **Files Affected**: 
  - `MultiMerkleDistributor.sol` (#L260-L275)
  - `balance-tree.ts` (#L30-L35)
  - `MultiMerkleDistributor.sol` (#L126-L144)

## Description
The `MultiMerkleDistributor.sol` contract does not verify that the merkle tree belongs to the right quest and period. If the wrong merkle tree is added, then the wrong rewards can be claimed.

**Note**: Set to medium risk because the likelihood of this happening is low, but the impact is high.

## Recommendation
A solution that does not cost any extra storage but requires a small amount of gas involves adding `questID` and `period` into the merkle tree nodes, ensuring rewards can only be claimed in combination with the right `questID` and `period`.

### Code Snippet - `balance-tree.ts`
```typescript
// keccak256(abi.encode(index, account, amount))
public static toNode(index: number | BigNumber, account: string, amount: BigNumber): Buffer {
    return Buffer.from(
        - utils.solidityKeccak256([ 'uint256 ','address ','uint256 '], [index, account, amount]).substr(2),
        + utils.solidityKeccak256([ 'uint256 ','uint256 ','uint256 ','address ','uint256 '],
        + [ questID, period, index, account, amount]).substr(2,
        'hex'
    )
}
```

### Code Snippet - `MultiMerkleDistributor.sol`
```solidity
function claim(uint256 questID, uint256 period, uint256 index, address account, uint256 amount, ...)
public { , !
...
// Check that the given parameters match the given Proof
- bytes32 node = keccak256(abi.encodePacked(index, account, amount));
+ bytes32 node = keccak256(abi.encodePacked(questID, period, index, account, amount));
...
}
```

## Implementation
- **Paladin**: Implemented in #12.
- **Spearbit**: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Paladin |
| Report Date | N/A |
| Finders | DefSec, Jay Jonah8, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

