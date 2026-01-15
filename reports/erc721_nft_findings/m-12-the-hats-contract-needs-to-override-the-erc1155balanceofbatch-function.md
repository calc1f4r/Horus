---
# Core Classification
protocol: Hats
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10292
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/48
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-hats-judging/issues/85

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
  - staking_pool
  - liquid_staking
  - bridge
  - yield
  - launchpad

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - cccz
  - roguereddwarf
  - GimelSec
  - ktg
---

## Vulnerability Title

M-12: The Hats contract needs to override the ERC1155.balanceOfBatch function

### Overview


The Hats contract is a smart contract on the Ethereum blockchain that allows users to purchase, trade, and collect virtual hats. However, the Hats contract does not override the ERC1155.balanceOfBatch function, which allows balanceOfBatch to return the actual balance no matter what the circumstances. This issue was found by roguereddwarf, ktg, cccz, and GimelSec.

The impact of this issue is that balanceOfBatch may return a different result than balanceOf, which could lead to errors when integrating with other projects. The code snippet for the issue can be found at https://github.com/Hats-Protocol/hats-protocol/blob/main/src/Hats.sol#L1149-L1162 and https://github.com/Hats-Protocol/hats-protocol/blob/main/lib/ERC1155/ERC1155.sol#L118-L139. The tool used to find this issue was manual review.

The recommendation is to consider overriding the ERC1155.balanceOfBatch function in the Hats contract to return 0 when the hat is inactive or the wearer is ineligible. This was discussed by spengrah, who suggested a pull request, and zobront, who suggested replacing the code with balanceOf.

Overall, the Hats contract needs to override the ERC1155.balanceOfBatch function to prevent errors when integrating with other projects.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-hats-judging/issues/85 

## Found by 
roguereddwarf, ktg, cccz, GimelSec

## Summary
The Hats contract does not override the ERC1155.balanceOfBatch function
## Vulnerability Detail
The Hats contract overrides the ERC1155.balanceOf function to return a balance of 0 when the hat is inactive or the wearer is ineligible.
```solidity
    function balanceOf(address _wearer, uint256 _hatId)
        public
        view
        override(ERC1155, IHats)
        returns (uint256 balance)
    {
        Hat storage hat = _hats[_hatId];

        balance = 0;

        if (_isActive(hat, _hatId) && _isEligible(_wearer, hat, _hatId)) {
            balance = super.balanceOf(_wearer, _hatId);
        }
    }
```
But the Hats contract does not override the ERC1155.balanceOfBatch function, which causes balanceOfBatch to return the actual balance no matter what the circumstances.
```solidity
    function balanceOfBatch(address[] calldata owners, uint256[] calldata ids)
        public
        view
        virtual
        returns (uint256[] memory balances)
    {
        require(owners.length == ids.length, "LENGTH_MISMATCH");

        balances = new uint256[](owners.length);

        // Unchecked because the only math done is incrementing
        // the array index counter which cannot possibly overflow.
        unchecked {
            for (uint256 i = 0; i < owners.length; ++i) {
                balances[i] = _balanceOf[owners[i]][ids[i]];
            }
        }
    }
```
## Impact
This will make balanceOfBatch return a different result than balanceOf, which may cause errors when integrating with other projects
## Code Snippet
https://github.com/Hats-Protocol/hats-protocol/blob/main/src/Hats.sol#L1149-L1162
https://github.com/Hats-Protocol/hats-protocol/blob/main/lib/ERC1155/ERC1155.sol#L118-L139
## Tool used

Manual Review

## Recommendation
Consider overriding the ERC1155.balanceOfBatch function in Hats contract to return 0 when the hat is inactive or the wearer is ineligible.

## Discussion

**spengrah**

https://github.com/Hats-Protocol/hats-protocol/pull/102

**zobront**

Reverting solves the problem, but I'm curious why revert instead of just replacing:

```solidity
balances[i] = _balanceOf[owners[i]][ids[i]];
```

with...
```solidity
balances[i] = balanceOf(owners[i], ids[i]);
```

**zobront**

Reverting solves the problem, but I'm curious why revert instead of just replacing:

```solidity
balances[i] = _balanceOf[owners[i]][ids[i]];
```

with...
```solidity
balances[i] = balanceOf(owners[i], ids[i]);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Hats |
| Report Date | N/A |
| Finders | cccz, roguereddwarf, GimelSec, ktg |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-hats-judging/issues/85
- **Contest**: https://app.sherlock.xyz/audits/contests/48

### Keywords for Search

`vulnerability`

