---
# Core Classification
protocol: StationX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41396
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-12] Adversary can block the counterpart deployment of cross-chain DAOs

### Overview


The report discusses a bug in the `deploySAFE()` function of the `Deployer` contract which creates a Safe for a DAO. The bug can cause a transaction to fail if another Safe with the same `nonce` has been created on the same chain. This can be exploited by an attacker to prevent the creation of a DAO on another chain. The report suggests a solution to remove the `try/catch` block and precompute the expected address of the Safe to prevent this issue.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

The `deploySAFE()` function in `Deployer` attempts to create a Safe for the DAO via `SafeProxyFactory::createProxyWithNonce()`. It uses a `try/catch` pattern, but it will always revert if another Safe with the same `nonce` was created beforehand on that chain.

Notice how a `revert` inside a `catch` block will make the whole transaction revert:

```solidity
uint256 nonce = getNonce(_daoAddress);
do {
    try ISafe(safe).createProxyWithNonce(singleton, _initializer, nonce) returns (address _deployedSafe) {
        SAFE = _deployedSafe;
    } catch Error(string memory reason) {
        nonce = getNonce(_daoAddress);
        revert SafeProxyCreationFailed(reason);
    } catch {
        revert SafeProxyCreationFailed("Safe proxy creation failed");
    }
} while (SAFE == address(0));
```

An adversary can directly call [SafeProxyFactory::createProxyWithNonce()](https://github.com/safe-global/safe-smart-account/blob/a9e3385bb38c29d45b3901ff7180b59fcee86ac9/contracts/proxies/SafeProxyFactory.sol#L56) on the destination chain while the cross-chain transaction is being processed by LayerZero.

Using the same `nonce` generated for the victim `_daoAddress()` and the same `initialize` parameters will guarantee it will create a Safe with the same address.

This is problematic since it will make the cross-chain transaction revert when trying to execute `deploySAFE()` in `createCrossChainERC20DAO()`:

```solidity
function createCrossChainERC20DAO(...) {
    address _safe = IDeployer(deployer).deploySAFE(_admins, _safeThreshold, _daoAddress);

    _createERC20DAO(...);
    ccDetails[_daoAddress] = CrossChainDetails(_commLayerId, _depositChainIds, false, msg.sender, _onlyAllowWhitelist);
}
```

It will be impossible to finish the creation of the DAO counterpart on the destination chain, and buy operations will not be available there.

Note: There's also a secondary, less severe impact of this finding that involves frontrunning the transaction on the source chain, and preventing the creation of any DAO altogether. In this case, there is no risk as no DAO was created on any chain, but it can be considered a griefing attack. The recommendation covers this scenario as well.

## Recommendations

One possible solution is to remove the `try/catch` block, [precompute](https://solidity-by-example.org/app/create2/) the expected address of the Safe [proxy](https://github.com/safe-global/safe-smart-account/blob/a9e3385bb38c29d45b3901ff7180b59fcee86ac9/contracts/proxies/SafeProxyFactory.sol#L15), check if it exists (has code), and only create it if not.

If the contract for the corresponding address was already deployed, it shouldn't pose any risks, as it had to be created for the corresponding `daoAddress`, with the expected admins, and other parameters set on its initializer.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StationX |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StationX-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

