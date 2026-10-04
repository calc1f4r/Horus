---
# Core Classification
protocol: Etherspot Credibleaccountmodule
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61416
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Etherspot-CredibleAccountModule-Security-Review.md
github_link: none

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
  - Shieldify Security
---

## Vulnerability Title

[M-02] The `pre/postCheck()` Is Not Checking the Hook Initialization of the Sender

### Overview


The report describes a bug in the `CredibleAccountModule` where any wallet, whether a Modular wallet or a Smart wallet, can change the lifespan of session keys of other users. This is because the module does not check whether the caller is initializing the hook or not. This allows for unauthorized access to session keys and breaks the access control of the Locking token mechanism. The team has fixed the issue and recommends checking that the caller is a Smart wallet that initialized the module as a hook. The affected code can be found in the `CredibleAccountModule.sol` file. The bug is considered a medium risk and has now been resolved. 

### Original Finding Content


## Severity

Medium Risk

## Description

In order for the Smart Wallets to use `CredibleAccountModule` as a Hook, they call `onInstall()` and install it as a Hook.

```solidity
function onInstall(bytes calldata data) external override {
    // code
    if (moduleType == MODULE_TYPE_VALIDATOR) { ... }
    else if (moduleType == MODULE_TYPE_HOOK) {
>>      moduleInitialized[msg.sender].hookInitialized = true;
    } else {
        revert CredibleAccountModule_InvalidModuleType();
    }
}
```

When executing the tx on `ModularEtherspotWallet`, we call it with the `withHook()` modifier. and since this hook can be installed. The wallet will call `preCheck()` before execution and call `postCheck()` after execution.

```solidity
modifier withHook() {
    address hook = _getHook();
    if (hook == address(0)) {
        _;
    } else {
        bytes memory hookData = IHook(hook).preCheck(
            msg.sender,
            msg.value,
            msg.data
        );
        _;
        IHook(hook).postCheck(hookData);
    }
}

// -----

function execute( ... ) external payable onlyEntryPointOrSelf withHook { ... }
```

But in `CredibleAccountModule`, there is no checking whether the `msg.sender` is initialising that Hook or not:

```solidity
function preCheck(address msgSender, uint256 msgValue, bytes calldata msgData) external override returns (bytes memory hookData) {
    (address sender,) = abi.decode(msgData, (address, bytes));
    return abi.encode(sender, _cumulativeLockedForWallet(sender));
}

// -----

function postCheck(bytes calldata hookData) external {
    // code
}
```

This will make any wallet either a Modular wallet or a Smart wallet, call these functions, allowing them to change the `liveness` of the session keys of other users, breaking the access control of the Locking token mechanism.

## Location of Affected Code

File: [src/modules/validators/CredibleAccountModule.sol](https://github.com/etherspot/etherspot-modular-accounts/blob/d4774db9f544cc6f69000c55e97627f93fe7242b/src/modules/validators/CredibleAccountModule.sol)

## Impact

Unauthorised access by anyone to session keys allowing them to change the lifespan.

## Recommendation

We should check that the caller is a Smart wallet that initialised the Module as Hook.

## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Etherspot Credibleaccountmodule |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Etherspot-CredibleAccountModule-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

