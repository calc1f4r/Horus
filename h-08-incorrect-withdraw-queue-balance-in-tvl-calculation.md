---
# Core Classification
protocol: Renzo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33495
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-renzo
source_link: https://code4rena.com/reports/2024-04-renzo
github_link: https://github.com/code-423n4/2024-04-renzo-findings/issues/28

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

protocol_categories:
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 71
finders:
  - josephdara
  - mussucal
  - honey-k12
  - 0xAadi
  - zhaojohnson
---

## Vulnerability Title

[H-08] Incorrect withdraw queue balance in TVL calculation

### Overview


The bug report describes an issue with the calculation of TVL (Total Value Locked) in a smart contract. The contract iterates over all the operator delegators and inside it, iterates over all the collateral tokens. However, there is a mistake in fetching the balance of the `withdrawQueue` which results in an incorrect calculation of the token value. This can have a negative impact on the TVL, which is an important metric for calculating other values in the contract. The bug can be fixed by changing the index used to access the `collateralTokens` from `i` to `j`. The bug has been confirmed and mitigated by the developer. 

### Original Finding Content


When calculating TVL it iterates over all the operator delegators and inside it iterates over all the collateral tokens. 

```solidity
        for (uint256 i = 0; i < odLength; ) {
            ...

            // Iterate through the tokens and get the value of each
            uint256 tokenLength = collateralTokens.length;
            for (uint256 j = 0; j < tokenLength; ) {
                ...

                // record token value of withdraw queue
                if (!withdrawQueueTokenBalanceRecorded) {
                    totalWithdrawalQueueValue += renzoOracle.lookupTokenValue(
                        collateralTokens[i],
                        collateralTokens[j].balanceOf(withdrawQueue)
                    );
                }

                unchecked {
                    ++j;
                }
            }

            ...

            unchecked {
                ++i;
            }
        }
```

However, the balance of `withdrawQueue` is incorrectly fetched, specifically this line:

```solidity
                    totalWithdrawalQueueValue += renzoOracle.lookupTokenValue(
                        collateralTokens[i],
                        collateralTokens[j].balanceOf(withdrawQueue)
                    );
```

It uses an incorrect index of the outer loop `i` to access the `collateralTokens`. `i` belongs to the operator delegator index, thus the returned value will not represent the real value of the token. For instance, if there is 1 OD and 3 collateral tokens, it will add the balance of the first token 3 times and neglect the other 2 tokens. If there are more ODs than collateral tokens, the the execution will revert (index out of bounds).

This calculation impacts the TVL which is the essential data when calculating mint/redeem and other critical values. A miscalculation in TVL could have devastating results.

### Proof of Concept

A simplified version of the function to showcase that the same token (in this case `address(1)`) is emitted multiple times and other tokens are untouched:

```solidity
contract RestakeManager {

    address[] public operatorDelegators;

    address[] public collateralTokens;

    event CollateralTokenLookup(address token);

    constructor() {
        operatorDelegators.push(msg.sender);

        collateralTokens.push(address(1));
        collateralTokens.push(address(2));
        collateralTokens.push(address(3));
    }

    function calculateTVLs() public {
        // Iterate through the ODs
        uint256 odLength = operatorDelegators.length;

        for (uint256 i = 0; i < odLength; ) {
            // Iterate through the tokens and get the value of each
            uint256 tokenLength = collateralTokens.length;
            for (uint256 j = 0; j < tokenLength; ) {
                emit CollateralTokenLookup(collateralTokens[i]);

                unchecked {
                    ++j;
                }
            }

            unchecked {
                ++i;
            }
        }
    }
}
```

### Recommended Mitigation Steps

Change to `collateralTokens[j]`.

### Assessed type

Math

**[jatinj615 (Renzo) confirmed and commented](https://github.com/code-423n4/2024-04-renzo-findings/issues/28#issuecomment-2107661134):**
 > Yeah, the index should be `j` not `i`. 

**[Renzo mitigated](https://github.com/code-423n4/2024-06-renzo-mitigation?tab=readme-ov-file#scope)**

**Status:** Mitigation confirmed. Full details in reports from [0xCiphky](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/12), [grearlake](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/55), [Fassi\_Security](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/44), [Bauchibred](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/23), and [LessDupes](https://github.com/code-423n4/2024-06-renzo-mitigation-findings/issues/6).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Renzo |
| Report Date | N/A |
| Finders | josephdara, mussucal, honey-k12, 0xAadi, zhaojohnson, pauliax, gjaldon, p0wd3r, gesha17, ustazz, 0xnev, 14si2o\_Flint, 0xCiphky, SBSecurity, t0x1c, Greed, 0xordersol, fyamf, peanuts, grearlake, BiasedMerc, GoatedAudits, zzykxx, guhu95, carrotsmuggler, Maroutis, aman, kinda\_very\_good, rbserver, aslanbek, OMEN, 0xnightfall, KupiaSec, mt030d, tapir, twcctop, siguint, eeshenggoh, NentoR, DanielArmstrong, blutorque, 0xhacksmithh, Stefanov, maxim371, Aamir, 0rpse, Aymen0909, 0xPwned, 0x73696d616f, adam-idarrha, crypticdefense, ak1, zigtur, ilchovski, TheFabled, araj, FastChecker, 1, 2, xg, baz1ka, b0g0, hunter\_w3b, carlitox477, Fassi\_Security, shui, bigtone, lanrebayode77, LessDupes |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-renzo
- **GitHub**: https://github.com/code-423n4/2024-04-renzo-findings/issues/28
- **Contest**: https://code4rena.com/reports/2024-04-renzo

### Keywords for Search

`vulnerability`

