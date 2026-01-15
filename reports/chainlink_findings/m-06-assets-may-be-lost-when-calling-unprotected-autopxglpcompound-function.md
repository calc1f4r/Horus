---
# Core Classification
protocol: Redacted Cartel
chain: everychain
category: uncategorized
vulnerability_type: slippage

# Attack Vector Details
attack_type: slippage
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6043
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-redacted-cartel-contest
source_link: https://code4rena.com/reports/2022-11-redactedcartel
github_link: https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/137

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - slippage

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 21
finders:
  - keccak123
  - 0x52
  - ladboy233
  - xiaoming90
  - pashov
---

## Vulnerability Title

[M-06] Assets may be lost when calling unprotected `AutoPxGlp::compound` function

### Overview


This bug report discusses a vulnerability found in the code of the AutoPxGlp and PirexGmx smart contracts. The issue is that anyone can call the `AutoPxGlp::compound` function and set the minimum amount of Glp and USDG tokens to virtually zero, which may cause compounded assets to be lost. The proof of concept for this vulnerability involves the use of the GMX reward router to mint and stake GLP. The amount of USGD to mint is calculated by GMX own price feed, which can be manipulated in times of market turbulence. The recommended mitigation steps are to not depend on user passing minimum amounts of usdg and glp tokens, and to use GMX oracle to get the current price and check it against another price feed. VS Code and arbiscan.io were the tools used to identify this vulnerability.

### Original Finding Content


<https://github.com/code-423n4/2022-11-redactedcartel/blob/main/src/vaults/AutoPxGlp.sol#L210>

<https://github.com/code-423n4/2022-11-redactedcartel/blob/main/src/PirexGmx.sol#L497-L516>

### Impact

Compounded assets may be lost because `AutoPxGlp::compound` can be called by anyone and minimum amount of Glp and USDG are under caller's control. The only check concerning minValues is that they are not zero (1 will work, however from the perspective of real tokens e.g. 1e6, or 1e18 it's virtually zero). Additionally, internal smart contract functions use it as well with minimal possible value (e.g. `beforeDeposit` function).

### Proof of Concept

`compound` function calls PirexGmx::depositGlp, that uses external GMX reward router to mint and stake GLP.

<https://snowtrace.io/address/0x82147c5a7e850ea4e28155df107f2590fd4ba327#code>

```solidity
141:     function mintAndStakeGlpETH(uint256 _minUsdg, uint256 _minGlp) external payable nonReentrant returns (uint256) {
    ...
148: uint256 glpAmount = IGlpManager(glpManager).addLiquidityForAccount(address(this), account, weth, msg.value, _minUsdg, _minGlp);
```

Next `GlpManager::addLiquidityForAccount` is called
<https://github.com/gmx-io/gmx-contracts/blob/master/contracts/core/GlpManager.sol#L103>

        function addLiquidityForAccount(address _fundingAccount, address _account, address _token, uint256 _amount, uint256 _minUsdg, uint256 _minGlp) external override nonReentrant returns (uint256) {
            _validateHandler();
            return _addLiquidity(_fundingAccount, _account, _token, _amount, _minUsdg, _minGlp);
        }

which in turn uses vault to swap token for specific amount of USDG before adding liquidity:
<https://github.com/gmx-io/gmx-contracts/blob/master/contracts/core/GlpManager.sol#L217>

The amount of USGD to mint is calcualted by GMX own price feed:
<https://github.com/gmx-io/gmx-contracts/blob/master/contracts/core/Vault.sol#L765-L767>

In times of market turbulence, or price oracle  manipulation, all compound value may be lost

### Tools Used

VS Code, arbiscan.io

### Recommended Mitigation Steps

Don't depend on user passing minimum amounts of usdg and glp tokens. Use GMX oracle to get current price, and additionally check it against some other price feed (e.g. ChainLink).

**[kphed (Redacted Cartel) commented](https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/137#issuecomment-1404076219):**
> We're using the following combination of mechanics in order to make front-running `compound` calls economically unattractive (or, at the very least, minimally impactful) for would-be attackers:
> - Compound incentives
> - Execution as a side effect of vault functions
> 
> Both will result in a higher frequency of the vault compounding its rewards and less resources available for potential attackers.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Redacted Cartel |
| Report Date | N/A |
| Finders | keccak123, 0x52, ladboy233, xiaoming90, pashov, rbserver, perseverancesuccess, simon135, hihen, cccz, 0xbepresent, Englave, Ruhum, pedroais, deliriusz, 0xLad, gzeon, wagmi, unforgiven, rvierdiiev, R2 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-redactedcartel
- **GitHub**: https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/137
- **Contest**: https://code4rena.com/contests/2022-11-redacted-cartel-contest

### Keywords for Search

`Slippage`

