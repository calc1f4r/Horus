---
# Core Classification
protocol: Starbase
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43940
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2024/08/starbase/
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
finders_count: 2
finders:
  - Sergii Kravchenko
  -  Vladislav Yaroshuk
                        
---

## Vulnerability Title

Missing Validation of _FEE_RATE_ Variable ✓ Fixed

### Overview


The bug report is about a problem with the code in the `2b508ff772206751317e8b0c6f5f70d4987a2b5e` commit. The issue was only partially fixed and the fix was only applied to one function in the `StarBaseDCA` contract. This means that the problem still exists in other functions and the `constructor` of the contract. Additionally, there is a mistake in the comment for a new variable, which could cause confusion. The report recommends adding validation checks and fixing the comment to avoid any further issues. 

In an update, the maximum fee limit was changed to 10%. However, this could still be a problem because the protocol owner can change the fees without giving users enough time to cancel their orders. It is suggested to add a timelock mechanism to prevent this issue. 

The bug is caused by the `_FEE_RATE_` variable being able to be set to any `uint160` value, which could result in fees as high as 100%. This could be exploited by the owner to steal tokens and cause excessive fees during transactions. The report recommends adding checks to limit the fee rate to a more reasonable amount, such as below 100%.

### Original Finding Content

#### Resolution



In the `2b508ff772206751317e8b0c6f5f70d4987a2b5e` commit provided for the fix review the issue has been only partially fixed with the comment “solved `require(feeRate <= MAX_FEE_RATE, "Fee rate too high");`”, but apparently this fix has been added only to the `changeFeeFeeRate` function of the `StarBaseDCA` contract, and haven’t been added to other contracts functions and `constructor`. Also, the new variable `uint160 constant MAX_FEE_RATE = 5000; // 100%` has a comment `100` %, while in reality it’s `50` %. We recommend adding validation to leftover functions and `constructor`’s, fixing the comment, and setting the max fee to `20` % at most.


**Update (commit hash `7415929c5d5d1958f131847242d853290b378597`):** The `_FEE_RATE_` is now limited to 10%. The protocol owner can instantly change the fees to a higher amount, and existing orders won’t have time to cancel if they disagree. Since the system is designed to be trustless, it would be good to add a timelock mechanism for updating the fees. However, because the maximum fee limit is 10%, the impact on users is limited and everyone should be aware of that risk. It’s the responsibility of the protocol to warn users beforehand about changing the fees.




#### Description


In the `init` and `changeFeeReceiver` functions of the `StarBaseDCA` contract, as well as in the `init` and `changeFeeRate` functions of the `StarBaseLimitOrder` contract and the `changeFeeRate` function of the `StarBaseLimitOrderBot` contract, the `_FEE_RATE_` variable can be set to any `uint160` value, while the denominator is `10000`. This allows the fee rate to be set as high as 100%, which is problematic since a trustless system is expected. This could enable the owner to steal all of the tokens with every trade, leading to excessive fees being charged during transactions, as well as a full block of other function execution when the fee is higher than 100%.


#### Examples


**starbase\-limitorder/src/StarBaseDCA.sol:L69\-L73**



```
function init(address owner, address StarBaseApproveProxy, address feeReciver, uint160 feeRate) external {
    initOwner(owner);
    _StarBase_APPROVE_PROXY_ = StarBaseApproveProxy;
    _FEE_RECEIVER_ = feeReciver;
    _FEE_RATE_ = feeRate;

```
**starbase\-limitorder/src/StarBaseDCA.sol:L191\-L194**



```
function changeFeeReceiver(uint160 feeRate) public onlyOwner {
    _FEE_RATE_ = feeRate;
    emit ChangeFeeRate(feeRate);
}

```
**starbase\-limitorder/src/StarBaseLimitOrder.sol:L56\-L60**



```
function init(address owner, address StarBaseApproveProxy, address feeReciver,uint160 feeRate) external {
    initOwner(owner);
    _StarBase_APPROVE_PROXY_ = StarBaseApproveProxy;
    _FEE_RECEIVER_ = feeReciver;
    _FEE_RATE_ = feeRate;

```
**starbase\-limitorder/src/StarBaseLimitOrder.sol:L183\-L185**



```
function changeFeeRate (uint160 feeRate) public onlyOwner {
    _FEE_RATE_ = feeRate;
    emit ChangeFeeRate(feeRate);

```
**starbase\-limitorder/src/StarBaseLimitOrderBot.sol:L119\-L122**



```
function changeFeeRate (uint160 feeRate) public onlyOwner {
    _FEE_RATE_ = feeRate;
    emit ChangeFeeRate(feeRate);
}

```
#### Recommendation


We recommend adding validation checks for the `_FEE_RATE_` to ensure it is within an acceptable range, such as below 100%.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Starbase |
| Report Date | N/A |
| Finders | Sergii Kravchenko,  Vladislav Yaroshuk
                         |

### Source Links

- **Source**: https://diligence.consensys.io/audits/2024/08/starbase/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

