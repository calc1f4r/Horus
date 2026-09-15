---
# Core Classification
protocol: INIT Capital
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29593
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-12-initcapital
source_link: https://code4rena.com/reports/2023-12-initcapital
github_link: https://github.com/code-423n4/2023-12-initcapital-findings/issues/36

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
  - lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x73696d616f
---

## Vulnerability Title

[M-02] Decimals of LendingPool don't take into account the offset introduced by VIRTUAL\_SHARES

### Overview


This bug report discusses a finding that could potentially affect the marketing and data fetching aspect of a token exchange. It involves an incorrect calculation of the value of shares compared to the underlying token, which could impact the perceived value of the shares. The report includes a proof of concept and recommends a mitigation step to include the virtual shares decimals in the `decimals()` function. The tools used for this report were Vscode and Foundry. The bug has been confirmed by the team responsible for the token (INIT).

### Original Finding Content


The impact of this finding is more on the marketing/data fetching side, on exchanges it would appear that the shares are worth less `VIRTUAL_SHARES` than the underlying token. Given that it would influence the perception of the value of the shares token, medium severity seems appropriate.

### Proof of Concept

The Openzeppelin [implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/ERC4626.sol#L106-L108) includes the decimals offset (log10(`VIRTUAL_SHARES`) in LendingPool) in the `decimals()` function. However, INIT only places the decimals of the [underlying](https://github.com/code-423n4/2023-12-initcapital/blob/main/contracts/lending_pool/LendingPool.sol#L95-L97).

A POC was built, add it to `TestLendingPool.sol`:

```solidity
function test_POC_WrongDecimals() public {
    uint256 _wbtcAmount = 3e8; // 3 BTC
    address _user = makeAddr("user");
    _mintPool(_user, WBTC, _wbtcAmount);
    uint256 _wbtcDecimals = 1e8;
    uint256 VIRTUAL_SHARES = 1e8;
    uint256 _poolDecimals = 10**lendingPools[WBTC].decimals();
    uint256 _userBalance = lendingPools[WBTC].balanceOf(_user);
    assertEq(_userBalance/_poolDecimals, _wbtcAmount/_wbtcDecimals*VIRTUAL_SHARES);
    assertEq(_userBalance/_poolDecimals, 3e8);
    assertEq(_userBalance, _wbtcAmount*VIRTUAL_SHARES);
}
```

### Tools Used

Vscode, Foundry

### Recommended Mitigation Steps

Include the virtual shares decimals in the `decimals()` function:

```solidity
uint private constant VIRTUAL_SHARES = 8;
...
function decimals() public view override returns (uint8) {
    return IERC20Metadata(underlyingToken).decimals() + VIRTUAL_SHARES;
}
...
function _toShares(uint _amt, uint _totalAssets, uint _totalShares) internal pure returns (uint shares) {
    return _amt.mulDiv(_totalShares + 10**VIRTUAL_SHARES, _totalAssets + VIRTUAL_ASSETS);
}
...
function _toAmt(uint _shares, uint _totalAssets, uint _totalShares) internal pure returns (uint amt) {
    return _shares.mulDiv(_totalAssets + VIRTUAL_ASSETS, _totalShares + 10**VIRTUAL_SHARES);
}
```

**[fez-init (INIT) confirmed](https://github.com/code-423n4/2023-12-initcapital-findings/issues/36#issuecomment-1870338593)**


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | INIT Capital |
| Report Date | N/A |
| Finders | 0x73696d616f |

### Source Links

- **Source**: https://code4rena.com/reports/2023-12-initcapital
- **GitHub**: https://github.com/code-423n4/2023-12-initcapital-findings/issues/36
- **Contest**: https://code4rena.com/reports/2023-12-initcapital

### Keywords for Search

`vulnerability`

