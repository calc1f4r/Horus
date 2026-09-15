---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36648
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-05-canto
source_link: https://code4rena.com/reports/2024-05-canto
github_link: https://github.com/code-423n4/2024-05-canto-findings/issues/28

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - 0xSergeantPepper
  - zhaojie
  - 0x1771
---

## Vulnerability Title

[M-01] An attacker can DoS a coinswap pool

### Overview


The coinswap module in the Canto blockchain has a bug that can be exploited by attackers to disrupt the functionality of the module. This happens when an attacker introduces a large number of tokens through the `AddLiquidity` process and then transfers them to a target pool, causing the `k.bk.GetAllBalances` function to fail due to insufficient gas. This is because the function iterates through all token balances in a loop, and if the array of tokens is too large, it can lead to high gas consumption and transaction failure. The recommended mitigation steps include changing the `GetPoolBalances` function to only query and return the balance of certain coins and making appropriate changes for its callers. This bug has been classified as Medium severity. 

### Original Finding Content

The balance calculations are initiated by calling `k.GetPoolBalances(ctx, pool.EscrowAddress)`, which internally calls the `k.bk.GetAllBalances` function. This function iterates through all token balances in a loop. If the array of tokens is excessively large, the function may fail due to insufficient gas.

In essence, if an attacker introduces a large number of tokens, for instance through the `AddLiquidity` process, and subsequently transfers these tokens to a target pool, it can lead to an exploit. The attacker can strategically overload the array, causing significant gas consumption and ultimately causing the function to fail.

The process is as follows:

When the `AddLiquidity` or `RemoveLiquidity` functions are called within the coinswap module, the `k.GetPoolBalances` function retrieves the balance of all tokens in the pool. This function, `k.GetPoolBalances`, calls `k.bk.GetAllBalances`, which iterates through and aggregates all token balances before sorting them into an array.

Specifically, `k.bk.GetAllBalances` utilizes the following approach:

```go
func (k BaseViewKeeper) GetAllBalances(ctx context.Context, addr sdk.AccAddress) sdk.Coins {
    balances := sdk.NewCoins()
    k.IterateAccountBalances(ctx, addr, func(balance sdk.Coin) bool {
        balances = balances.Add(balance)
        return false
    })
    return balances.Sort()
}
```

Here, `sdk.NewCoins()` returns an array of type `Coins`.

When an attacker exploits the `AddLiquidity` function in the coinswap module, they can create a pool using `k.CreatePool(ctx, msg.MaxToken.Denom)` if the pool does not already exist. By generating a large number of tokens and sending them to the target pool, the attacker causes the array of balances returned by `GetPoolBalances` to become excessively large. This leads to high gas consumption and potential transaction failure due to insufficient gas, thus disrupting the functionality of the coinswap module.

### Recommended Mitigation Steps

Get only 1 token balance instead of all.

**[poorphd (Canto) confirmed and commented via duplicate Issue #20](https://github.com/code-423n4/2024-05-canto-findings/issues/20#issuecomment-2191190618):**
> **Reasoning:** As raised in the issue, if an attacker sends tokens of various denoms to the reserved pool address, `k.GetPoolBalances(ctx, pool.EscrowAddress)` could invoke `k.bk.GetAllBalances` that internally uses iteration, leading to a situation where the operation could fail if the array becomes very large.
>     
> However, pool creation is only allowed for whitelisted denoms, so it is impossible to obtain new tokens through `AddLiquidity` as raised in the issue. (See [here](https://github.com/b-harvest/Canto/blob/liquidstaking-module/x/coinswap/keeper/keeper.go#L113-L116) and [here](https://github.com/b-harvest/Canto/blob/liquidstaking-module/x/coinswap/types/params.go#L19-L36)).
>
> **Severity:** Mid → Low.
>
> In the worst-case scenario, the swap or `RemoveLiquidity` in coinswap might fail, but this only affects the auto swap during onboarding and does not impact the essential functions of the chain.
>
> **Patch:**
> -  We will patch this before v0.50 upgrade.
> - Change `k.GetPoolBalances(ctx, pool.EscrowAddress)` so that it does not use `k.bk.GetAllBalances` and only queries and returns the balance of standard coin, counter party coin, and pool coin.
> - Make appropriate changes for `GetPoolBalances` callers.
>
> ```go
> // GetPoolBalances return the liquidity pool by the specified anotherCoinDenom
> func (k Keeper) GetPoolBalances(ctx sdk.Context, pool types.Pool) (coins sdk.Coins, err error) {
> 	address, err := sdk.AccAddressFromBech32(pool.EscrowAddress)
> 	if err != nil {
>		return coins, err
>	}
>	acc := k.ak.GetAccount(ctx, address)
>	if acc == nil {
>		return nil, errorsmod.Wrap(types.ErrReservePoolNotExists, pool.EscrowAddress)
>	}
>
>	balances := sdk.NewCoins()
>	balances.Add(k.bk.GetBalance(ctx, acc.GetAddress(), pool.StandardDenom))
>	balances.Add(k.bk.GetBalance(ctx, acc.GetAddress(), pool.CounterpartyDenom))
>	balances.Add(k.bk.GetBalance(ctx, acc.GetAddress(), pool.LptDenom))
>	
>	return balances, nil
> }       

**[3docSec (judge) decreased severity to Medium](https://github.com/code-423n4/2024-05-canto-findings/issues/28#issuecomment-2191558246)**

**[3docSec (judge) commented via duplicate Issue #20](https://github.com/code-423n4/2024-05-canto-findings/issues/20#issuecomment-2191557238):**
> I find Medium to be appropriate for this group.
>
> Because Canto is connected to other Cosmos networks via IBC, an arbitrary number of token denominations can coexist (and be donated) to an existing pool to DoS its liquidity operations, without any privilege required for an attacker.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | 0xSergeantPepper, zhaojie, 0x1771 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-05-canto
- **GitHub**: https://github.com/code-423n4/2024-05-canto-findings/issues/28
- **Contest**: https://code4rena.com/reports/2024-05-canto

### Keywords for Search

`vulnerability`

