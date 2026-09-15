---
# Core Classification
protocol: Plume Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53273
audit_firm: OtterSec
contest_link: https://plumenetwork.xyz/
source_link: https://plumenetwork.xyz/
github_link: https://github.com/plumenetwork/contracts

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
finders_count: 3
finders:
  - Nicholas R. Putra
  - Robert Chen
  - Renato Eugenio Maria Marziano
---

## Vulnerability Title

Inheritance Conflict in Decimals Method

### Overview


The report discusses a vulnerability in the programming language Solidity, which is used for creating smart contracts on the Ethereum blockchain. The issue arises when a contract inherits from multiple parent contracts and overrides a function using the "super" keyword. This can cause the wrong parent contract's function to be prioritized, leading to incorrect behavior. The specific example given is in the YieldToken contract, where the decimals function is overridden and the parent contract ERC4626's implementation is prioritized over YieldDistributionToken's. This can result in incorrect decimals being returned. The suggested solution is for developers to avoid relying on the "super" keyword and explicitly define the desired behavior in the contract. The issue has been resolved in a recent patch.

### Original Finding Content

## Vulnerability in Solidity's Inheritance Hierarchy

The vulnerability lies in how Solidity’s inheritance hierarchy and the `super` keyword determine which parent implementation is prioritized when overriding a function. 

Here, `YieldToken` inherits both `YieldDistributionToken` and `ERC4626`, both of which implement the `decimals` function.

```solidity
// smart-wallets/src/token/YieldToken.sol
contract YieldToken is YieldDistributionToken, ERC4626, WalletUtils, IYieldToken, IComponentToken {
    [...]
    /// @inheritdoc ERC20
    function decimals() public view override(YieldDistributionToken, ERC4626) returns (uint8) {
        return super.decimals();
    }
    [...]
}
```

Since `super` prioritizes the parent contract that appears last in the inheritance chain, the definition of `decimals` in `ERC4626` takes precedence over that in `YieldDistributionToken`. As a result, the logic intended by `YieldDistributionToken` for `decimals` may be ignored, resulting in incorrect decimals being returned. 

- `YieldDistributionToken.decimals` is defined to always return 8, while 
- `ERC4626.decimals` dynamically calculates the value based on the underlying asset.

## Remediation

Avoid relying on the `super` resolution. `YieldToken` should explicitly define its desired behavior.

## Patch

Resolved in commit **4f16028**.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Plume Network |
| Report Date | N/A |
| Finders | Nicholas R. Putra, Robert Chen, Renato Eugenio Maria Marziano |

### Source Links

- **Source**: https://plumenetwork.xyz/
- **GitHub**: https://github.com/plumenetwork/contracts
- **Contest**: https://plumenetwork.xyz/

### Keywords for Search

`vulnerability`

