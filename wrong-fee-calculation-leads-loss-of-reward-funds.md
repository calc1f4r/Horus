---
# Core Classification
protocol: Hyphen V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50247
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/biconomy/hyphen-v2-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/biconomy/hyphen-v2-smart-contract-security-assessment
github_link: none

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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

WRONG FEE CALCULATION LEADS LOSS OF REWARD FUNDS

### Overview


The bug report is about a contract called `LiquidityPool` which has two functions to claim gas fees, one for ERC20 tokens and one for the native token. However, there is a problem with the function for claiming gas fees for the native token, which makes it impossible to withdraw the fees. This is because of an error in the calculation of the fee amount in the function. The code for this function can be found in the `LiquidityPool.sol` file. The `Biconomy team` has solved this issue by correcting the math operation that was causing the loss of funds. The impact and likelihood of this bug are both rated as 5. The solution can be found in the `fab4b8c0a10a3e0185b2a06b10248391837c07de` commit ID.

### Original Finding Content

##### Description

The `LiquidityPool` contract has claim gas fee mechanism for both ERC20 tokens and Native token. There are two functions to claim gas fee. The first function is `withdrawErc20GasFee`, used for claiming gas fee for ERC20 tokens. The `withdrawNativeGasFee` function is used for claiming gas fee for native token.

It is impossible to withdraw native gas fees due to wrong fee amount of calculation on `withdrawNativeGasFee` function.

#### LiquidityPool.sol

```
gasFeeAccumulatedByToken[NATIVE] = 0;
gasFeeAccumulatedByToken[NATIVE] = gasFeeAccumulatedByToken[NATIVE] - _gasFeeAccumulated;

```

Basically, this function tries to substract `_gasFeeAccumulated` variable from `0`. Therefore, this function will always revert, and native gas fees will remain in the contract.

Code Location
-------------

#### LiquidityPool.sol

```
function withdrawNativeGasFee() external onlyOwner whenNotPaused {
        uint256 _gasFeeAccumulated = gasFeeAccumulated[NATIVE][_msgSender()];
        require(_gasFeeAccumulated != 0, "Gas Fee earned is 0");
        gasFeeAccumulatedByToken[NATIVE] = 0;
        gasFeeAccumulatedByToken[NATIVE] = gasFeeAccumulatedByToken[NATIVE] - _gasFeeAccumulated;
        gasFeeAccumulated[NATIVE][_msgSender()] = 0;
        bool success = payable(_msgSender()).send(_gasFeeAccumulated);
        require(success, "Native Transfer Failed");

        emit GasFeeWithdraw(address(this), _msgSender(), _gasFeeAccumulated);
    }

```

##### Score

Impact: 5  
Likelihood: 5

##### Recommendation

**SOLVED:** The `Biconomy team` solved this issue by correcting the math operation that was causing the loss of funds.

`Commit ID:` \href{https://github.com/bcnmy/hyphen-contract/commit/fab4b8c0a10a3e0185b2a06b10248391837c07de}{fab4b8c0a10a3e0185b2a06b10248391837c07de}

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Hyphen V2 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/biconomy/hyphen-v2-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/biconomy/hyphen-v2-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

