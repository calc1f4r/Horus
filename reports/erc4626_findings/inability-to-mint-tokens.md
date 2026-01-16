---
# Core Classification
protocol: Gloop
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47569
audit_firm: OtterSec
contest_link: https://gloop.finance/
source_link: https://gloop.finance/
github_link: https://github.com/gloop-finance/gmi

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
finders_count: 4
finders:
  - Nicholas R. Putra
  - Robert Chen
  - Matteo Oliva
  - OtterSec
---

## Vulnerability Title

Inability To Mint Tokens

### Overview


This bug report is about a problem that occurs when trying to deposit GMI tokens for the first time. The issue is that the deposit fails to handle a scenario where the total supply of GMI tokens is zero. This results in the formula for determining the amount of tokens to be minted to be initialized to zero, which means that no tokens are actually minted for the depositor. This is because the fee calculation and final minting amount are dependent on the value of the mintAmount, which is set to zero in this case.

The code snippet provided in the report is from the GMIndex.sol file, specifically the deposit function. The function checks for the total value of controlled assets, the price of the deposit token, the total supply of GMI tokens, the bank balance, and the target balance before calculating the mintAmount. However, since the totalSupply is zero for the first deposit, the mintAmount is also set to zero, causing the issue.

To fix this problem, the report suggests checking whether the totalSupply is zero before calculating the mintAmount. If it is zero, then the mintAmount should be set to a value that is proportional to the deposited amount and the initial weights of the deposit token. This will ensure that the deposit is handled correctly and the appropriate amount of GMI tokens are minted for the depositor.

The bug has been fixed in the b3d224a patch. It is important for beginners to understand that bugs are common in software development and it is important to thoroughly test and fix them to ensure the smooth functioning of the program. In this case, the bug was identified and fixed by checking for a specific scenario and making the necessary adjustments to the code. 

### Original Finding Content

## Deposit Issue in GMIndex.sol

When depositing for the first time, the deposit function fails to appropriately handle a scenario where the total supply of GMI tokens is zero. As a result, the formula that derives `mintAmount` initializes it to zero since `totalSupply` is zero for the first deposit. Subsequently, no GMI tokens are minted for the depositor, as both the fee calculation and the final minting amount are contingent on the value of `mintAmount`.

## Code Snippet

```solidity
function deposit(bytes32 name, address _recipient, uint256 _amount, uint256 _minAmountOut) public {
    [...]
    {
        uint256 totalValue = totalControlledValue();
        uint256 depositTokenPrice = _getPrice(name);
        uint256 totalSupply = totalSupply();
        uint256 bankBalance = _bankBalance(name);
        IERC20 token = vaults[name].token;
        uint256 depositTokenValue = (_amount * depositTokenPrice) / 10 ** IERC20Metadata(address(token)).decimals();
        uint256 targetBalance = _targetBalance(name);
        mintAmount = (depositTokenValue * totalSupply) / totalValue;
        [...]
    }
    [...]
}
```

## Remediation

Check whether `totalSupply` is zero on deposit. In such a case, set `mintAmount` to a value proportional to the deposited amount and the initial weights of the deposit token.

## Patch

Fixed in commit `b3d224a`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Gloop |
| Report Date | N/A |
| Finders | Nicholas R. Putra, Robert Chen, Matteo Oliva, OtterSec |

### Source Links

- **Source**: https://gloop.finance/
- **GitHub**: https://github.com/gloop-finance/gmi
- **Contest**: https://gloop.finance/

### Keywords for Search

`vulnerability`

