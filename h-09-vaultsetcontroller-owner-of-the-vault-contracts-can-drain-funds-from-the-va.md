---
# Core Classification
protocol: InsureDAO
chain: everychain
category: uncategorized
vulnerability_type: admin

# Attack Vector Details
attack_type: admin
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1302
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-insuredao-contest
source_link: https://code4rena.com/reports/2022-01-insure
github_link: https://github.com/code-423n4/2022-01-insure-findings/issues/271

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 0

# Context Tags
tags:
  - admin

protocol_categories:
  - services
  - cross_chain
  - indexes
  - insurance

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WatchPug
---

## Vulnerability Title

[H-09] Vault#setController() owner of the Vault contracts can drain funds from the Vault

### Overview


This bug report is about a vulnerability in the Vault contract of the 2022-01-insure repository. The owner of the Vault contract can set an arbitrary address as the `controller`. This malicious `controller` contract can then transfer funds from the Vault to the attacker. A malicious/compromised user can call the `Vault#setController()` and set `controller` to a malicious contract, and then call `Vault#utilize()` to deposit all the balance in the Vault contract into the malicious controller contract. The attacker can then withdraw all the funds from the malicious controller contract. To fix this vulnerability, it is recommended to consider disallowing the `Vault#setController()` to set a new address if a controller is existing, or to put a timelock to this function at least.

### Original Finding Content

## Handle

WatchPug


## Vulnerability details

https://github.com/code-423n4/2022-01-insure/blob/19d1a7819fe7ce795e6d4814e7ddf8b8e1323df3/contracts/Vault.sol#L485-L496

```solidity
function setController(address _controller) public override onlyOwner {
    require(_controller != address(0), "ERROR_ZERO_ADDRESS");

    if (address(controller) != address(0)) {
        controller.migrate(address(_controller));
        controller = IController(_controller);
    } else {
        controller = IController(_controller);
    }

    emit ControllerSet(_controller);
}
```

The owner of the Vault contract can set an arbitrary address as the `controller`.

https://github.com/code-423n4/2022-01-insure/blob/19d1a7819fe7ce795e6d4814e7ddf8b8e1323df3/contracts/Vault.sol#L342-L352

```solidity
function utilize() external override returns (uint256 _amount) {
    if (keeper != address(0)) {
        require(msg.sender == keeper, "ERROR_NOT_KEEPER");
    }
    _amount = available(); //balance
    if (_amount > 0) {
        IERC20(token).safeTransfer(address(controller), _amount);
        balance -= _amount;
        controller.earn(address(token), _amount);
    }
}
```

A malicious `controller` contract can transfer funds from the Vault to the attacker.

## PoC

A malicious/compromised can:

1. Call `Vault#setController()` and set `controller` to a malicious contract;
    -   L489 the old controller will transfer funds to the new, malicious controller.
2. Call `Vault#utilize()` to deposit all the balance in the Vault contract into the malicious controller contract.
3. Withdraw all the funds from the malicious controller contract.

## Recommendation

Consider disallowing `Vault#setController()` to set a new address if a controller is existing, which terminates the possibility of migrating funds to a specified address provided by the owner. Or, putting a timelock to this function at least.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | InsureDAO |
| Report Date | N/A |
| Finders | WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-insure
- **GitHub**: https://github.com/code-423n4/2022-01-insure-findings/issues/271
- **Contest**: https://code4rena.com/contests/2022-01-insuredao-contest

### Keywords for Search

`Admin`

