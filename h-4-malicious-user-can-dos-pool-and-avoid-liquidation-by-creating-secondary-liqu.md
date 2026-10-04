---
# Core Classification
protocol: Isomorph
chain: everychain
category: dos
vulnerability_type: denial-of-service

# Attack Vector Details
attack_type: denial-of-service
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5687
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/22
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-isomorph-judging/issues/72

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - denial-of-service
  - liquidation
  - dos

protocol_categories:
  - liquid_staking
  - yield
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

H-4: Malicious user can DOS pool and avoid liquidation by creating secondary liquidity pool for Velodrome token pair

### Overview


This bug report is about a vulnerability found in the Velodrome token pair on the Velo deposit tokens contract. The issue is that a malicious user can avoid liquidation by creating a secondary liquidity pool. This is done by calling the priceLiquidity function in the corresponding DepositReceipt. This function calls the router, which will return the best rate between the volatile and stable pool. If the wrong pool gives the better rate, then the transaction will revert. A malicious user can manipulate the price of the opposite pool so that any call to liquidate them will route through the wrong pool and revert. This would enable them to avoid liquidation.

The code snippet provided in the report shows the code of the priceLiquidity function which is vulnerable to this malicious user. The recommendation given is to query the correct pool directly instead of quoting from the router. This was confirmed by the sponsor and fixed in a commit on GitHub.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-isomorph-judging/issues/72 

## Found by 
0x52

## Summary

For every Vault_Velo interaction the vault attempts to price the liquidity of the user. This calls priceLiquidity in the corresponding DepsoitReciept. The prices the underlying assets by swapping them through the Velodrome router. Velodrome can have both a stable and volatile pool for each asset pair. When calling the router directly it routes through the pool that gives the best price. In priceLiquidity the transaction will revert if the router routes through the wrong pool (i.e. trading the volatile pool instead of the stable pool). A malicious user can use this to their advantage to avoid being liquidated.  They could manipulate the price of the opposite pool so that any call to liquidate them would route through the wrong pool and revert.

## Vulnerability Detail

        uint256 amountOut; //amount received by trade
        bool stablePool; //if the traded pool is stable or volatile.
        (amountOut, stablePool) = router.getAmountOut(HUNDRED_TOKENS, token1, USDC);
        require(stablePool == stable, "pricing occuring through wrong pool" );

DepositReceipt uses the getAmountOut call the estimate the amountOut. The router will return the best rate between the volatile and stable pool. If the wrong pool give the better rate then the transaction will revert. Since pricing is called during liquidation, a malicious user could manipulate the price of the wrong pool so that it returns the better rate and always reverts the liquidation call.

## Impact

Malicious user can avoid liquidation

## Code Snippet

https://github.com/sherlock-audit/2022-11-isomorph/blob/main/contracts/Velo-Deposit-Tokens/contracts/DepositReceipt_USDC.sol#L75-L130

## Tool used

Manual Review

## Recommendation

Instead of quoting from the router, query the correct pool directly:

            uint256 amountOut; //amount received by trade
    -       bool stablePool; //if the traded pool is stable or volatile.

    -       (amountOut, stablePool) = router.getAmountOut(HUNDRED_TOKENS, token1, USDC);
    -       require(stablePool == stable, "pricing occuring through wrong pool" );
    +       address pair;

    +       pair = router.pairFor(token1, USDC, stable)
    +       amountOut = IPair(pair).getAmountOut(HUNDRED_TOKENS, token1)

## Discussion

**kree-dotcom**

Sponsor confirmed, will fix.

**kree-dotcom**

Fixed https://github.com/kree-dotcom/Velo-Deposit-Tokens/commit/58b8f3e14b416630971b7b17b500bbe22d2016aa

Note there are two fixes in this commit relating to the priceLiquidity function. The other fix is for issue #145 , the code for these changes doesn't overlap so should be clear, please ask me if it is not.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Isomorph |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-isomorph-judging/issues/72
- **Contest**: https://app.sherlock.xyz/audits/contests/22

### Keywords for Search

`Denial-Of-Service, Liquidation, DOS`

