---
# Core Classification
protocol: Yeti Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1207
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-yeti-finance-contest
source_link: https://code4rena.com/reports/2021-12-yetifinance
github_link: https://github.com/code-423n4/2021-12-yetifinance-findings/issues/146

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - csanuragjain
---

## Vulnerability Title

[M-03] Unwhitelisted token can cause disaster

### Overview


This bug report is about a vulnerability in the ActivePool.sol contract. It can lead to contract instability and financial loss if one of the allowed contract calls sendCollaterals with a non-whitelisted token. The proof of concept provided in the report explains how this vulnerability can be exploited. The recommended mitigation step is to add a check to see if the collateral to be transferred is whitelisted. This will ensure that the contract only processes whitelisted tokens and not non-whitelisted tokens.

### Original Finding Content

_Submitted by csanuragjain_

#### Impact

Contract instability and financial loss. This will happen if one of the allowed contract calls sendCollaterals with non whitelisted token (may happen with user input on allowed contract)

#### Proof of Concept

1.  Navigate to contract at <https://github.com/code-423n4/2021-12-yetifinance/blob/main/packages/contracts/contracts/ActivePool.sol>

2.  Assume sendCollaterals function is called by one of allowed contract with a non whitelisted token and amount as 1

```solidity
function sendCollaterals(address _to, address[] memory _tokens, uint[] memory _amounts) external override returns (bool) {
    _requireCallerIsBOorTroveMorTMLorSP();
    require(_tokens.length == _amounts.length);
    for (uint i = 0; i < _tokens.length; i++) {
        _sendCollateral(_to, _tokens[i], _amounts[i]); // reverts if send fails
    }

    if (_needsUpdateCollateral(_to)) {
        ICollateralReceiver(_to).receiveCollateral(_tokens, _amounts);
    }
    
    return true;
}
```

3.  This calls \_sendCollateral with our non whitelisted token and amount as 1

```solidity
function _sendCollateral(address _to, address _collateral, uint _amount) internal returns (bool) {
    uint index = whitelist.getIndex(_collateral);
    poolColl.amounts[index] = poolColl.amounts[index].sub(_amount);
    bool sent = IERC20(_collateral).transfer(_to, _amount);
    require(sent);

    emit ActivePoolBalanceUpdated(_collateral, _amount);
    emit CollateralSent(_collateral, _to, _amount);
}
```
4.  whitelist.getIndex(\_collateral); will return 0 as our collateral is not whitelisted and will not be present in whitelist.getIndex(\_collateral);. This means index will point to whitelisted collateral at index 0

5.  poolColl.amounts\[index] will get updated for whitelisted collateral at index 0 even though this collateral was never meant to be updated

```solidity
poolColl.amounts[index] = poolColl.amounts[index].sub(_amount);
```

6.  Finally our non supported token gets transferred to recipient and since \_needsUpdateCollateral is true so recipient poolColl.amounts gets increased even though recipient never received the whitelisted collateral

7.  Finally sender pool amount will be reduced even though it has the whitelisted collateral and recipient pool amount will be increased even though it does not have whitelisted collateral

#### Recommended Mitigation Steps

Add a check to see if collateral to be transferred is whitelisted

**[kingyetifinance (Yeti finance) disputed](https://github.com/code-423n4/2021-12-yetifinance-findings/issues/146#issuecomment-1005436938):**
 > @LilYeti: Thanks for the thorough run through. It is true, but this is abstracted away, all calls of sendCollateral are internal / between contracts in our codebase, and there are checks for valid collateral in whitelist before this. 

**[alcueca (Judge) commented](https://github.com/code-423n4/2021-12-yetifinance-findings/issues/146#issuecomment-1013823086):**
 > Validating data integrity outside a function inside the same contract would be a low severity. Validating data integrity in an external contract is medium severity. Many things can go wrong.




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Yeti Finance |
| Report Date | N/A |
| Finders | csanuragjain |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-yetifinance
- **GitHub**: https://github.com/code-423n4/2021-12-yetifinance-findings/issues/146
- **Contest**: https://code4rena.com/contests/2021-12-yeti-finance-contest

### Keywords for Search

`vulnerability`

