---
# Core Classification
protocol: Popcorn
chain: everychain
category: uncategorized
vulnerability_type: delegate

# Attack Vector Details
attack_type: delegate
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 22018
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-popcorn
source_link: https://code4rena.com/reports/2023-01-popcorn
github_link: https://github.com/code-423n4/2023-01-popcorn-findings/issues/435

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
  - delegate

protocol_categories:
  - yield
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cccz
  - bin2chen
---

## Vulnerability Title

[M-21] AdapterBase should always use delegatecall to call the functions in the strategy

### Overview


A bug was found in the AdapterBase contract of the RedVeil (Popcorn) protocol. The strategy contract was supposed to let the Adapter contract use delegatecall to call its functions, but in AdapterBase._verifyAndSetupStrategy, the verifyAdapterSelectorCompatibility/verifyAdapterCompatibility/setUp functions were not called with delegatecall, which caused the context of these functions to be the strategy contract. Since the strategy contract does not implement the interface of the Adapter contract, these functions failed, making it impossible to create a Vault using that strategy. This could also lead to later errors when calling the harvest function because the settings in setup are invalid. To fix the bug, the verifyAdapterSelectorCompatibility/verifyAdapterCompatibility/setUp functions should be called with delegatecall. RedVeil (Popcorn) has since confirmed the bug and released a fix.

### Original Finding Content


The strategy contract will generally let the Adapter contract use delegatecall to call its functions.

So IAdapter(address(this)).call is used frequently in strategy contracts, because when the Adapter calls the strategy's functions using delegatecall, address(this) is the Adapter:

```solidity
  function harvest() public override {
    address router = abi.decode(IAdapter(address(this)).strategyConfig(), (address));
    address asset = IAdapter(address(this)).asset();
    ...
```

But in AdapterBase.\_verifyAndSetupStrategy, the verifyAdapterSelectorCompatibility/verifyAdapterCompatibility/setUp functions are not called with delegatecall, which causes the context of these functions to be the strategy contract:

```solidity
    function _verifyAndSetupStrategy(bytes4[8] memory requiredSigs) internal {
        strategy.verifyAdapterSelectorCompatibility(requiredSigs);
        strategy.verifyAdapterCompatibility(strategyConfig);
        strategy.setUp(strategyConfig);
    }
```

And since the strategy contract does not implement the interface of the Adapter contract, these functions will fail, making it impossible to create a Vault using that strategy.

```solidity
  function verifyAdapterCompatibility(bytes memory data) public override {
    address router = abi.decode(data, (address));
    address asset = IAdapter(address(this)).asset();
```

More dangerously, if functions such as setup are executed successfully because they do not call the Adapter's functions, they may later error out when calling the harvest function because the settings in setup are invalid.

### Proof of Concept

<https://github.com/code-423n4/2023-01-popcorn/blob/d95fc31449c260901811196d617366d6352258cd/src/vault/adapter/abstracts/AdapterBase.sol#L479-L483>

### Recommended Mitigation Steps

In `AdapterBase.\_verifyAndSetupStrategy`, the verifyAdapterSelectorCompatibility/verifyAdapterCompatibility/setUp functions are called using delegatecall.

**[RedVeil (Popcorn) confirmed](https://github.com/code-423n4/2023-01-popcorn-findings/issues/435)** 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Popcorn |
| Report Date | N/A |
| Finders | cccz, bin2chen |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-popcorn
- **GitHub**: https://github.com/code-423n4/2023-01-popcorn-findings/issues/435
- **Contest**: https://code4rena.com/reports/2023-01-popcorn

### Keywords for Search

`Delegate`

