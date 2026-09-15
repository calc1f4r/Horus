---
# Core Classification
protocol: Beedle - Oracle free perpetual lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34495
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx
source_link: none
github_link: https://github.com/Cyfrin/2023-07-beedle

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
finders_count: 37
finders:
  - lealCodes
  - 0xdice91
  - Mlome
  - nmirchev8
  - 0xAli
---

## Vulnerability Title

Using forged/fake lending pools to steal any loan opening for auction

### Overview


The report discusses a high-risk bug in the lending pool feature of a software. The bug allows an attacker to steal loans that are up for auction by using a fake lending pool. This can cause the software to become insolvent. The bug is caused by the lack of verification that the loan's token and collateral must be the same as the new pool. The report recommends verifying this and provides a code solution to fix the bug. This bug was found through manual review. 

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L489">https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L489</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L518">https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L518</a>


## Summary

An attacker can steal any loan opening for auction by executing the `Lender::buyLoan()` and specifying the `poolId` parameter to a forged/fake pool. This vulnerability can even cause the protocol to become insolvent because an attacker moves out the stolen loans' `loanToken` and/or `collateralToken` tokens.

## Vulnerability Details

**Root cause**: the `buyLoan()` lacks verification that the loan's `loanToken` and `collateralToken` must be identical to the new pool. 

Therefore, an attacker can buy the loan using another pool of different `loanToken`/`collateralToken` pair.

To elaborate on this vulnerability, assume that a loan of 1 WETH (`loanToken`) / 2000 USDC (`collateralToken`) is opened for auction. An attacker can execute the `buyLoan()` to buy the loan by pointing to a pool of DAI (`loanToken`) / USDC (`collateralToken`). In this way, the attacker can steal the loan's debt of $2000+ using small DAI tokens (`totalDebt = 1 + lenderInterest + protocolInterest`).

```solidity
    function buyLoan(uint256 loanId, bytes32 poolId) public {
        ...

        // if they do have a big enough pool then transfer from their pool
@>      _updatePoolBalance(poolId, pools[poolId].poolBalance - totalDebt); //@audit balance subtraction from a forged pool
        pools[poolId].outstandingLoans += totalDebt;

        ...

        // update the loan with the new info
@>      loans[loanId].lender = msg.sender; //@audit the attacker becomes a new lender
        loans[loanId].interestRate = pools[poolId].interestRate;
        loans[loanId].startTimestamp = block.timestamp;
        loans[loanId].auctionStartTimestamp = type(uint256).max;
        loans[loanId].debt = totalDebt;

        ...
    }
```

- `Balance subtraction from a forged pool`: https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L489

- `The attacker becomes a new lender`: https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L518

## Impact

An attacker can steal any loan opening for auction by executing the `buyLoan()` and specifying the `poolId` parameter to a forged pool. The forged pool can even point to a pair of fake `loanToken` and `collateralToken`, which has worth $0. 

This vulnerability can even cause the protocol to become insolvent because an attacker moves out the stolen loans' `loanToken` and/or `collateralToken` tokens. Hence, I consider this vulnerability a high-risk issue.

## Tools Used

Manual Review

## Recommendations

I recommend verifying that the loan's `loanToken` and `collateralToken` must be identical to the new pool, as shown below.

```diff
    function buyLoan(uint256 loanId, bytes32 poolId) public {
        ...

+       if (loan.loanToken != pools[poolId].loanToken) revert TokenMismatch();
+       if (loan.collateralToken != pools[poolId].collateralToken) revert TokenMismatch();

        ...

        // if they do have a big enough pool then transfer from their pool
        _updatePoolBalance(poolId, pools[poolId].poolBalance - totalDebt);
        pools[poolId].outstandingLoans += totalDebt;

        ...

        // update the loan with the new info
        loans[loanId].lender = msg.sender;
        loans[loanId].interestRate = pools[poolId].interestRate;
        loans[loanId].startTimestamp = block.timestamp;
        loans[loanId].auctionStartTimestamp = type(uint256).max;
        loans[loanId].debt = totalDebt;

        ...
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beedle - Oracle free perpetual lending |
| Report Date | N/A |
| Finders | lealCodes, 0xdice91, Mlome, nmirchev8, 0xAli, qbs, xAlismx, B353N, MahdiKarimi, sonny2k, jnrlouis, serialcoder, tiesstevelink, Bughunter101, leasowillow, KupiaSec, VanGrim, 0xDanielH, Cosine, qckhp, Bernd, Aamir, 0xbepresent, ElHaj, 0xdeth, 0xlemon, dimulski, owade, PTolev, StErMi, pep7siup, hash, 0xanmol, honeymewn |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-beedle
- **Contest**: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx

### Keywords for Search

`vulnerability`

