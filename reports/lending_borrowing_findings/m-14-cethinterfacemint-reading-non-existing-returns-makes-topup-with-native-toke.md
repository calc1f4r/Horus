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
solodit_id: 2103
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-backd-contest
source_link: https://code4rena.com/reports/2022-04-backd
github_link: https://github.com/code-423n4/2022-04-backd-findings/issues/125

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

[M-14] `CEthInterface#mint()` reading non-existing returns makes `topUp()` with native token always revert

### Overview


This bug report is about a vulnerability in the code of the github repository https://github.com/code-423n4/2022-04-backd. The vulnerability is in the file CTokenInterfaces.sol at line 345, which contains the function mint(). This function is used for both the native cToken (CEther) and the CErc20 token. The problem is that the function returns nothing when used with the native token, while the interface defines it to return a uint256. As a result, the transaction will revert with the error “function returned an unexpected amount of data” when used with the native token. The bug is further illustrated with the example of the Compound cToken mint doc, the Compound CEther.mint() and the Compound CErc20.mint().

### Original Finding Content

_Submitted by WatchPug_

[CTokenInterfaces.sol#L345](https://github.com/code-423n4/2022-04-backd/blob/c856714a50437cb33240a5964b63687c9876275b/backd/interfaces/vendor/CTokenInterfaces.sol#L345)<br>

```solidity
function mint() external payable returns (uint256);
```

`mint()` for native cToken (`CEther`) will return nothing, while the current `CEthInterface` interface defines the returns as `(uint256)`.

In the current implementation, the interface for `CToken` is used for both `CEther` and `CErc20`.

As a result, the transaction will revert with the error: `function returned an unexpected amount of data` when `topUp()` with the native token (ETH).

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

Ref:

| method  | CEther | CErc20 |
|----------|------------|-------------|
| mint()   | revert      | error code  |
| redeem() | error code | error code  |
| repayBorrow() | revert | error code  |
| repayBorrowBehalf() | revert | error code  |

- [Compound's cToken mint doc](https://compound.finance/docs/ctokens#mint)<br>
- [Compound CEther.mint()](https://github.com/compound-finance/compound-protocol/blob/v2.8.1/contracts/CEther.sol#L46)<br>
- [Compound CErc20.mint()](https://github.com/compound-finance/compound-protocol/blob/v2.8.1/contracts/CErc20.sol#L46)<br>

**[chase-manning (Backd) confirmed](https://github.com/code-423n4/2022-04-backd-findings/issues/125)**



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
- **GitHub**: https://github.com/code-423n4/2022-04-backd-findings/issues/125
- **Contest**: https://code4rena.com/contests/2022-04-backd-contest

### Keywords for Search

`vulnerability`

