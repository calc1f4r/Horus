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
solodit_id: 6332
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-tigris-trade-contest
source_link: https://code4rena.com/reports/2022-12-tigris
github_link: https://github.com/code-423n4/2022-12-tigris-findings/issues/104

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
  - dexes
  - services
  - derivatives
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 9
finders:
  - __141345__
  - Deivitto
  - 0x4non
  - 0xNazgul
  - cccz
---

## Vulnerability Title

[M-02] Must approve 0 first

### Overview


This bug report is about an issue that affects some tokens (like USDT) when changing the allowance from an existing non-zero allowance value. It was discovered when manually revising the code found at https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/Lock.sol#L117. The impact of this bug is that the tokens do not work when changing the allowance from an existing non-zero allowance value. The recommended mitigation step is to add an approve(0) before approving. This can be done by modifying the code as follows: 

```
    function claimGovFees() public {
        address[] memory assets = bondNFT.getAssets();

        for (uint i=0; i < assets.length; i++) {
            uint balanceBefore = IERC20(assets[i]).balanceOf(address(this));
            IGovNFT(govNFT).claim(assets[i]);
            uint balanceAfter = IERC20(assets[i]).balanceOf(address(this));
            IERC20(assets[i]).approve(address(bondNFT), 0);
            IERC20(assets[i]).approve(address(bondNFT), type(uint256).max);
            bondNFT.distribute(assets[i], balanceAfter - balanceBefore);
        }
    }
```

### Original Finding Content


Some tokens (like USDT) do not work when changing the allowance from an existing non-zero allowance value. They must first be approved by zero and then the actual allowance must be approved.

### Proof of Concept

<https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/Lock.sol#L117>

```solidity
    function claimGovFees() public {
        address[] memory assets = bondNFT.getAssets();

        for (uint i=0; i < assets.length; i++) {
            uint balanceBefore = IERC20(assets[i]).balanceOf(address(this));
            IGovNFT(govNFT).claim(assets[i]);
            uint balanceAfter = IERC20(assets[i]).balanceOf(address(this));
            IERC20(assets[i]).approve(address(bondNFT), type(uint256).max);// @audit this could fail always with some tokens, 
            bondNFT.distribute(assets[i], balanceAfter - balanceBefore);
        }
    }
```

### Recommended Mitigation Steps

Add an `approve(0)` before approving;

        function claimGovFees() public {
            address[] memory assets = bondNFT.getAssets();

            for (uint i=0; i < assets.length; i++) {
                uint balanceBefore = IERC20(assets[i]).balanceOf(address(this));
                IGovNFT(govNFT).claim(assets[i]);
                uint balanceAfter = IERC20(assets[i]).balanceOf(address(this));
                IERC20(assets[i]).approve(address(bondNFT), 0);
                IERC20(assets[i]).approve(address(bondNFT), type(uint256).max);
                bondNFT.distribute(assets[i], balanceAfter - balanceBefore);
            }
      }

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-12-tigris-findings/issues/104#issuecomment-1382253859):**
 > The Warden has shown how, due to the function approving max multiple times, certain tokens, that only allow a non-zero allowance to be set starting from zero, could revert.
> 
> Because this depends on the token implementation, but there's a reasonable chance to believe that USDT will be used, I agree with Medium Severity.

**[GainsGoblin (Tigris Trade) confirmed](https://github.com/code-423n4/2022-12-tigris-findings/issues/104#issuecomment-1406959434):**
 > Since the purpose of the bonds is to lock tigAsset liquidity, only tigAsset tokens will be allowed to be locked, which don't have this issue.

**[GainsGoblin (Tigris Trade) resolved](https://github.com/code-423n4/2022-12-tigris-findings/issues/104#issuecomment-1407862000):**
 > Mitigation: https://github.com/code-423n4/2022-12-tigris/pull/2#issuecomment-1419177578 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Tigris Trade |
| Report Date | N/A |
| Finders | __141345__, Deivitto, 0x4non, 0xNazgul, cccz, kwhuo68, imare, rvierdiiev, eierina |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tigris
- **GitHub**: https://github.com/code-423n4/2022-12-tigris-findings/issues/104
- **Contest**: https://code4rena.com/contests/2022-12-tigris-trade-contest

### Keywords for Search

`vulnerability`

