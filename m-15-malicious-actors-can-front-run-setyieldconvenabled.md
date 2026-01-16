---
# Core Classification
protocol: Peapods
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52767
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/749
source_link: none
github_link: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/313

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - pashap9990
---

## Vulnerability Title

M-15: Malicious actors can front-run setYieldConvEnabled

### Overview


The report discusses a bug in the AutoCompoundingPodLp contract that allows malicious actors to front-run the setYieldConvEnabled function. This function is used to enable or disable reward token processing, and when it is enabled, it causes a sharp increase in the total assets of the contract. This can be exploited by a malicious actor who can deposit their assets and withdraw them with additional profits before the function is executed by the contract owner. The impact of this bug is that malicious actors can steal other users' profits. To mitigate this issue, the owner should pause the deposit function when calling the setYieldConvEnabled function. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/313 

## Found by 
pashap9990

### Root Cause

AutoCompoundingPodLp'owner can enable or disable processing reward tokens through `AutoCompoundingPodLp::setYieldConvEnabled` but when owner decides to enable with sets yieldConvEnabled to true this causes _totalAssets will be increase sharply

```solidity
    function _processRewardsToPodLp(uint256 _amountLpOutMin, uint256 _deadline) internal returns (uint256 _lpAmtOut) {
@>>>>        if (!yieldConvEnabled) {
            return _lpAmtOut;
        }
        address[] memory _tokens = ITokenRewards(IStakingPoolToken(_asset()).POOL_REWARDS()).getAllRewardsTokens();
        uint256 _len = _tokens.length + 1;
        for (uint256 _i; _i < _len; _i++) {
            address _token = _i == _tokens.length ? pod.lpRewardsToken() : _tokens[_i];
            uint256 _bal =
                IERC20(_token).balanceOf(address(this)) - (_token == pod.PAIRED_LP_TOKEN() ? _protocolFees : 0);
            if (_bal == 0) {
                continue;
            }
            uint256 _newLp = _tokenToPodLp(_token, _bal, 0, _deadline);
            _lpAmtOut += _newLp;
        }
@>>>        _totalAssets += _lpAmtOut;
        require(_lpAmtOut >= _amountLpOutMin, "M");
    }
```

### Internal Conditions

yieldConvEnabled = false

### PoC

Let's assume there is reward tokens in AutoCompoundingPodLp contract and `AutoCompoundingPodLp::setYieldConvEnabled` will be called by contract's owner and then malicious actor see transaction in mempool and calls `AutoCompoundingPodLp:deposit`. hence, totalAssets wouldn't update because yieldConvEnabled is false and when owner's transaction will be executed
totalAssets will be updated and malicious actor can withdraw his/her assets plus profit

### Code Snippet

https://github.com/sherlock-audit/2025-01-peapods-finance/blob/main/contracts/contracts/AutoCompoundingPodLp.sol#L463

https://github.com/sherlock-audit/2025-01-peapods-finance/blob/main/contracts/contracts/AutoCompoundingPodLp.sol#L214

### Impact

Malicious actor can steal other users profit

### Mitigation

Owner should pause deposit function when he/she wants to call `AutoCompoundingPodLp::setYieldConvEnabled`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Peapods |
| Report Date | N/A |
| Finders | pashap9990 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/313
- **Contest**: https://app.sherlock.xyz/audits/contests/749

### Keywords for Search

`vulnerability`

