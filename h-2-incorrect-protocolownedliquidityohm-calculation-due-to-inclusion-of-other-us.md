---
# Core Classification
protocol: Olympus RBS 2.0
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29751
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/128
source_link: none
github_link: https://github.com/sherlock-audit/2023-11-olympus-judging/issues/172

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
finders_count: 2
finders:
  - hash
  - tvdung94
---

## Vulnerability Title

H-2: Incorrect ProtocolOwnedLiquidityOhm calculation due to inclusion of other user's reserves

### Overview


The bug report discusses an issue with the calculation of ProtocolOwnedLiquidityOhm in the Bunni token. This calculation includes the liquidity deposited by other users, which is not supposed to be included. This can lead to an incorrect assumption of the protocol owned liquidity and supply, which can have an economical impact. The code snippet and discussion show that the deposit function in BunniHub allows any user to deposit, which can cause this issue. The recommendation is to either guard the deposit function or compute the liquidity using shares belonging to the protocol. A fix has been proposed and implemented by the developers. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-11-olympus-judging/issues/172 

## Found by 
hash, tvdung94
## Summary
ProtocolOwnedLiquidityOhm for Bunni can include the liquidity deposited by other users which is not protocol owned

## Vulnerability Detail
The protocol owned liquidity in Bunni is calculated as the sum of reserves of all the BunniTokens
```solidity
    function getProtocolOwnedLiquidityOhm() external view override returns (uint256) {

        uint256 len = bunniTokens.length;
        uint256 total;
        for (uint256 i; i < len; ) {
            TokenData storage tokenData = bunniTokens[i];
            BunniLens lens = tokenData.lens;
            BunniKey memory key = _getBunniKey(tokenData.token);

        .........

            total += _getOhmReserves(key, lens);
            unchecked {
                ++i;
            }
        }


        return total;
    }
```

The deposit function of Bunni allows any user to add liquidity to a token. Hence the returned reserve will contain amounts other than the reserves that actually belong to the protocol
```solidity

    // @audit callable by any user
    function deposit(
        DepositParams calldata params
    )
        external
        payable
        virtual
        override
        checkDeadline(params.deadline)
        returns (uint256 shares, uint128 addedLiquidity, uint256 amount0, uint256 amount1)
    {
    }
```  
## Impact
Incorrect assumption of the protocol owned liquidity and hence the supply. An attacker can inflate the liquidity reserves
The wider system relies on the supply calculation to be correct in order to perform actions of economical impact
```text
https://discord.com/channels/812037309376495636/1184355501258047488/1184397904551628831
it will be determined to get backing
so it will have an economical impact, as we could be exchanging ohm for treasury assets at a wrong price
```

## Code Snippet
POL liquidity is calculated as the sum of bunni token reserves
https://github.com/sherlock-audit/2023-11-olympus/blob/9c8df76dc9820b4c6605d2e1e6d87dcfa9e50070/bophades/src/modules/SPPLY/submodules/BunniSupply.sol#L171-L191

BunniHub allows any user to deposit
https://github.com/sherlock-audit/2023-11-olympus/blob/9c8df76dc9820b4c6605d2e1e6d87dcfa9e50070/bophades/src/external/bunni/BunniHub.sol#L71-L106

## Tool used
Manual Review

## Recommendation
Guard the deposit function in BunniHub or compute the liquidity using shares belonging to the protocol



## Discussion

**0xJem**

This is a good catch, and the high level is justified

**0xrusowsky**

https://github.com/OlympusDAO/bophades/pull/260

**IAm0x52**

Fix looks good. OnlyOwner modifier has been added to deposits

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Olympus RBS 2.0 |
| Report Date | N/A |
| Finders | hash, tvdung94 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-11-olympus-judging/issues/172
- **Contest**: https://app.sherlock.xyz/audits/contests/128

### Keywords for Search

`vulnerability`

