---
# Core Classification
protocol: Nibiru
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49291
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-11-nibiru
source_link: https://code4rena.com/reports/2024-11-nibiru
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[07] Some lower decimal tokens cannot be transferred in Nibiru

### Overview

See description below for full details.

### Original Finding Content


[`x/evm/keeper/erc20.go`](https://github.com/code-423n4/2024-11-nibiru/blob/main/x/evm/keeper/erc20.go):

```go
// Transfer sends ERC20 tokens from one account to another
func (e ERC20) Transfer(
    contractAddr gethcommon.Address,
    from gethcommon.Address,
    to gethcommon.Address,
    amount *big.Int,
    ctx sdk.Context,
) (*big.Int, *types.MsgEthereumTxResponse, error) {
    // ... transfer logic ...

    // Amount is always handled in wei (10^18)
    if amount.Cmp(big.NewInt(1e12)) < 0 {
        return nil, nil, fmt.Errorf("amount too small, minimum transfer is 10^12 wei")
    }
}
```

[`x/evm/types/params.go`](https://github.com/code-423n4/2024-11-nibiru/blob/main/x/evm/types/params.go):

```go
const (
    // DefaultEVMDenom defines the default EVM denomination on Nibiru: unibi
    DefaultEVMDenom = "unibi"
    // WeiFactor is the factor between wei and unibi (10^12)
    WeiFactor = 12
)
```

The protocol enforces a minimum transfer amount of `10^12` wei, which creates issues for tokens with decimals less than 18. For example:

1. USDC (6 decimals): `1 USDC = 10^6 units`.
2. WBTC (8 decimals): `1 WBTC = 10^8 units`.

These tokens cannot be transferred in small amounts because their decimal places are below the minimum transfer threshold.

### Impact

MEDIUM. The strict minimum transfer requirement of `10^12 wei` causes:

1. Inability to transfer small amounts of low-decimal tokens.
2. Poor UX for common stablecoins like USDC and USDT.
3. Limited functionality for tokens with `< 18` decimals.
4. Potential adoption barriers for DeFi protocols that rely on precise token amounts.
5. Incompatibility with existing Ethereum token standards and practices.

### Recommended Mitigation Steps

1. Implement decimal-aware transfer minimums:

```go
func (e ERC20) Transfer(...) {
    decimals, err := e.Decimals(contractAddr, ctx)
    if err != nil {
        return nil, nil, err
    }

    // Adjust minimum based on token decimals
    minTransfer := new(big.Int).Exp(big.NewInt(10), big.NewInt(int64(decimals)-6), nil)
    if amount.Cmp(minTransfer) < 0 {
        return nil, nil, fmt.Errorf("amount too small, minimum transfer is %s", minTransfer)
    }
}
```

2. Add configuration option for minimum transfer amounts per token:

```go
type TokenConfig struct {
    MinTransferAmount *big.Int
    Decimals         uint8
}

func (e ERC20) GetTokenConfig(contractAddr common.Address) TokenConfig {
    // Return custom configuration per token
}
```

3. Document the limitation clearly in the protocol specifications if it must be maintained:

	**Token Transfer Limitations:**
	- Minimum transfer amount: 10^12 wei
	- Affects tokens with < 18 decimals
	- Consider aggregating smaller amounts before transfer

4. Consider removing the minimum transfer restriction entirely to maintain full ERC20 compatibility.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Nibiru |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-11-nibiru
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-11-nibiru

### Keywords for Search

`vulnerability`

