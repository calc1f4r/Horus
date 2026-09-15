---
# Core Classification
protocol: Autonomint Colored Dollar V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45500
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/438

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x37
---

## Vulnerability Title

M-10: Non-functional wrapper in BorrowLiquidation

### Overview


This bug report discusses an issue with the synthetix's wrapper in the OP Chain, which is causing a problem with the liquidation process. The wrapper is supposed to help wrap WETH to sETH, but it is currently empty and does not support the necessary mint() interface. This means that the liquidation type 2 cannot work in the OP Chain. The root cause of this issue is that the synthetix's wrapper in the OP Chain is different from the one in Ethereum. This can be seen by comparing the wrapper addresses on the developer.synthetix.io website. As a result, the liquidation process is being reverted. This bug is important to fix because the liquidation type 1 may also not work in some cases, and it is crucial to ensure that the liquidation process can always work properly. The report suggests that synthetix may be able to support the exchange of WETH to sUSD directly as a workaround for this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/438 

## Found by 
0x37

### Summary

The synthetix's wrapper in OP Chain is empty. It cannot help us to wrap WETH to sETH.

### Root Cause

In [borrowLiquidation.sol:348](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L348), we will wrap WETH to sETH via synthetix's wrapper.

The problem is that I find out that the synthetix's wrapper in OP Chain is different with Ethereum's wrapper.  The synthetix's wrapper in OP Chainis one empty wrapper chain(https://optimistic.etherscan.io/address/0xc3Ee42caBD773A608fa9Ec951982c94BD6F33d59) after checking from (https://developer.synthetix.io/addresses/).

So in OP chain, the empty wrapper does not support mint() interface. So this liquidation will be reverted.
```solidity
    function liquidationType2(
        address user,
        uint64 index,
        uint64 currentEthPrice
    ) internal {
        ...
        wrapper.mint(amount);
}
```
### Internal pre-conditions

N/A

### External pre-conditions

N/A

### Attack Path

N/A

### Impact

The liquidation type 2 cannot work in OP chain.
Considering that liquidation type 1 cannot work in some cases, e.g. there is not enough cds owners who opt in the liquidation, it's important to make sure that the liquidation type 2 can always work well.

### PoC

N/A

### Mitigation

synthetix support to exchange WETH to sUSD directly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | 0x37 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/438
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

