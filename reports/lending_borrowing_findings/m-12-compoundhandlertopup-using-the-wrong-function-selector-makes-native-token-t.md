---
# Core Classification
protocol: Backd
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2101
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-backd-contest
source_link: https://code4rena.com/reports/2022-04-backd
github_link: https://github.com/code-423n4/2022-04-backd-findings/issues/120

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
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WatchPug
---

## Vulnerability Title

[M-12] `CompoundHandler#topUp()` Using the wrong function selector makes native token `topUp()` always revert

### Overview


This bug report is about a vulnerability found in the Compound Protocol on GitHub. The vulnerability affects the mint() function for the native cToken (CEther). The issue is that the function does not have any parameters, and when a nonexisting parameter is added, the Function Selector will be incorrect. This is because the same CToken interface is used for both CEther and CErc20 in topUp(), and the function mint(uint256 mintAmount) does not exist for CEther. As a result, the native token topUp() always reverts. The bug report provides links to the GitHub code and Compound's cToken mint documentation.

### Original Finding Content

_Submitted by WatchPug_

[compound-finance/CEther.sol#L44-L47](https://github.com/compound-finance/compound-protocol/blob/v2.8.1/contracts/CEther.sol#L44-L47)<br>

```solidity
function mint() external payable {
    (uint err,) = mintInternal(msg.value);
    requireNoError(err, "mint failed");
}
```

`mint()` for native cToken (`CEther`) does not have any parameters, as the `Function Selector` is based on `the function name with the parenthesised list of parameter types`, when you add a nonexisting `parameter`, the `Function Selector` will be incorrect.

[CTokenInterfaces.sol#L316](https://github.com/code-423n4/2022-04-backd/blob/c856714a50437cb33240a5964b63687c9876275b/backd/interfaces/vendor/CTokenInterfaces.sol#L316)<br>

```solidity
function mint(uint256 mintAmount) external payable virtual returns (uint256);
```

The current implementation uses the same `CToken` interface for both `CEther` and `CErc20` in `topUp()`, and `function mint(uint256 mintAmount)` is a nonexisting function for `CEther`.

As a result, the native token `topUp()` always revert.

[CompoundHandler.sol#L57-L70](https://github.com/code-423n4/2022-04-backd/blob/c856714a50437cb33240a5964b63687c9876275b/backd/contracts/actions/topup/handlers/CompoundHandler.sol#L57-L70)<br>

```solidity
CToken ctoken = cTokenRegistry.fetchCToken(underlying);
uint256 initialTokens = ctoken.balanceOf(address(this));

address addr = account.addr();

if (repayDebt) {
    amount -= _repayAnyDebt(addr, underlying, amount, ctoken);
    if (amount == 0) return true;
}

uint256 err;
if (underlying == address(0)) {
    err = ctoken.mint{value: amount}(amount);
}
```

See also:

*   [Compound's cToken mint doc](https://compound.finance/docs/ctokens#mint)

**[samwerner (Backd) confirmed and resolved](https://github.com/code-423n4/2022-04-backd-findings/issues/120)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Backd |
| Report Date | N/A |
| Finders | WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-backd
- **GitHub**: https://github.com/code-423n4/2022-04-backd-findings/issues/120
- **Contest**: https://code4rena.com/contests/2022-04-backd-contest

### Keywords for Search

`vulnerability`

