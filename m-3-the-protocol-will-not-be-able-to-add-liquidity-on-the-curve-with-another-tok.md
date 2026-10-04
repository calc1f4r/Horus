---
# Core Classification
protocol: Blueberry Update
chain: everychain
category: uncategorized
vulnerability_type: missing-logic

# Attack Vector Details
attack_type: missing-logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18497
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/69
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/47

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
  - missing-logic
  - deposit/reward_tokens
  - coding-bug

protocol_categories:
  - lending
  - leveraged_farming
  - options_vault

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Bauer
  - nobody2018
---

## Vulnerability Title

M-3: The protocol  will not be able to add liquidity on the curve with another token with a balance.

### Overview


This bug report is about the `CurveSpell` protocol, which is used to open leveraged positions in a yield farming strategy. The protocol only ensures approve curve pool to spend its borrow token, and hence it will not be able to add liquidity on the curve with another token with a balance. This is because the `openPositionFarm()` function creates an array of the supplied token amounts to be passed to the add_liquidity function, but it only checks the number of tokens in the pool and not the balance of the tokens.

The impact of this bug is that the protocol will not be able to add liquidity on the curve with another token with a balance. The code snippet for this bug can be found at https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/CurveSpell.sol#L90-L115. This bug was found by Bauer and nobody2018 using manual review.

The recommendation to fix this bug is to allow the curve pool to spend tokens that have a balance in the protocol to add liquidity.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/47 

## Found by 
Bauer, nobody2018
## Summary
The `CurveSpell` protocol only ensure approve curve pool to spend its borrow token. Hence, it will not be able to add liquidity on the curve with another token with a balance.

## Vulnerability Detail
The  `openPositionFarm()` function enables user to open a leveraged position in a yield farming strategy by borrowing funds and using them to add liquidity to a Curve pool, while also taking into account certain risk management parameters such as maximum LTV and position size. When add liquidity on curve ,the protocol use the borrowed token and the collateral token, it checks the number of tokens in the pool and creates an array of the supplied token amounts to be passed to the add_liquidity function. Then the curve will transfer the tokens from the protocol and mint lp tokens to the protocol. However, the protocol only ensure approve curve pool to spend its borrow token. Hence, it will not be able to add liquidity on the curve with another token with a balance.
```solidity
 // 3. Add liquidity on curve
        _ensureApprove(param.borrowToken, pool, borrowBalance);
        if (tokens.length == 2) {
            uint256[2] memory suppliedAmts;
            for (uint256 i = 0; i < 2; i++) {
                suppliedAmts[i] = IERC20Upgradeable(tokens[i]).balanceOf(
                    address(this)
                );
            }
            ICurvePool(pool).add_liquidity(suppliedAmts, minLPMint);
        } else if (tokens.length == 3) {
            uint256[3] memory suppliedAmts;
            for (uint256 i = 0; i < 3; i++) {
                suppliedAmts[i] = IERC20Upgradeable(tokens[i]).balanceOf(
                    address(this)
                );
            }
            ICurvePool(pool).add_liquidity(suppliedAmts, minLPMint);
        } else if (tokens.length == 4) {
            uint256[4] memory suppliedAmts;
            for (uint256 i = 0; i < 4; i++) {
                suppliedAmts[i] = IERC20Upgradeable(tokens[i]).balanceOf(
                    address(this)
                );
            }
            ICurvePool(pool).add_liquidity(suppliedAmts, minLPMint);
        }

```

## Impact
The protocol  will not be able to add liquidity on the curve with another token with a balance.
## Code Snippet
https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/spell/CurveSpell.sol#L90-L115
## Tool used

Manual Review

## Recommendation
Allow the curve pool to spend tokens that have a balance in the protocol to add liquidity

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update |
| Report Date | N/A |
| Finders | Bauer, nobody2018 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/47
- **Contest**: https://app.sherlock.xyz/audits/contests/69

### Keywords for Search

`Missing-Logic, Deposit/Reward tokens, Coding-Bug`

