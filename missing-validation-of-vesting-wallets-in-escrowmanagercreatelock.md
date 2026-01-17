---
# Core Classification
protocol: EYWA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44331
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/EYWA/DAO/README.md#1-missing-validation-of-vesting-wallets-in-escrowmanagercreatelock
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

protocol_categories:
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Missing validation of vesting wallets in `EscrowManager.createLock()`

### Overview


The bug report describes a vulnerability in the `EscrowManager.createLock()` function. This function does not properly check the addresses of the vesting wallets, which can be exploited by an attacker to artificially increase their voting power in the system. The report recommends implementing a validation process for the wallet addresses, such as whitelisting or using a factory. This will prevent the use of "poisoned" wallets and make the system more secure.

### Original Finding Content

##### Description
`EscrowManager.createLock()` lacks whitelist verification for the `vestingWallets_` parameter. This allows an attacker to use the same "poisoned" vesting wallet multiple times to artificially increase voting power in the system.

The poisoned wallet is a custom contract that does nothing on `transfer()`.

```solidity
function createLock(
    uint256 lockDuration_, 
    address recipient_, 
    address[] calldata vestingWallets_
) external {
    if (vestingWallets_.length == 0) {
        revert InvalidArrayLength();
    }
    uint256 m_lockAmount;
    IVestingWallet m_vestingWallet;
    for (uint256 i = 0; i < vestingWallets_.length; ++i) {
        m_vestingWallet = IVestingWallet(vestingWallets_[i]);
        // Only beneficiary is checked, but not the wallet address itself
        if (m_vestingWallet.beneficiary() != msg.sender) {
            revert InvalidBeneficiary();
        }
        m_lockAmount += EYWA.balanceOf(address(m_vestingWallet));
        m_vestingWallet.transfer(address(this));
    }
    ...
}
```
https://gitlab.ubertech.dev/blockchainlaboratory/eywa-dao/blob/29465033f28c8d3f09cbc6722e08e44f443bd3b2/contracts/EscrowManager.sol#L175-180

##### Recommendation

We recommend validating vesting wallet addresses. For example, this can be done via whitelisting or via a factory.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | EYWA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/EYWA/DAO/README.md#1-missing-validation-of-vesting-wallets-in-escrowmanagercreatelock
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

