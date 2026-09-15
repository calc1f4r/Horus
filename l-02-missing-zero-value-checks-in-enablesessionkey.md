---
# Core Classification
protocol: Etherspot Sessionkeyvalidator
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44041
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Etherspot-SessionKeyValidator-Security-Review.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-02] Missing Zero Value Checks in `enableSessionKey()`

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

In the `enableSessionKey()` function, the `sessionKey`, `token`, `interfaceId`, `funcSelector` and `spendingLimit` parameters lack checks for zero values / addresses.

## Location of Affected Code

File: [src/modular-etherspot-wallet/modules/validators/ERC20SessionKeyValidator.sol#L61](https://github.com/etherspot/etherspot-prime-contracts/blob/dfef1e483837b47a3ea24ab65c3e76a2fb2e0007/src/modular-etherspot-wallet/modules/validators/ERC20SessionKeyValidator.sol#L61)

```solidity
function enableSessionKey(bytes calldata _sessionData) public {
@> address sessionKey = address(bytes20(_sessionData[0:20]));
@> address token = address(bytes20(_sessionData[20:40]));
@> bytes4 interfaceId = bytes4(_sessionData[40:44]);
@> bytes4 funcSelector = bytes4(_sessionData[44:48]);
@> uint256 spendingLimit = uint256(bytes32(_sessionData[48:80]));

   // code
}
```

## Recomendation

Consider implementing the following validation checks:

```diff
+ error ERC20SKV_InvalidSessionKey(address sessionKey);
+ error ERC20SKV_InvalidToken(address token);
+ error ERC20SKV_InvalidInterfaceId(bytes4 interfaceId);
+ error ERC20SKV_InvalidFuncSelector(bytes4 funcSelector);
+ error ERC20SKV_InvalidSpendingLimit(uint256 spendingLimit);

+ if (sessionKey == address(0))
+   revert ERC20SKV_InvalidSessionKey(sessionKey);

+ if (token == address(0))
+   revert ERC20SKV_InvalidToken(token);

+ if (interfaceId == bytes4(0))
+   revert ERC20SKV_InvalidInterfaceId(token);

+ if (funcSelector == bytes4(0))
+   revert ERC20SKV_InvalidFuncSelector(funcSelector);

+ if (spendingLimit == 0)
+   revert ERC20SKV_InvalidSpendingLimit(spendingLimit);
```

## Team Response

Fixed as proposed.

## [I-01] Unused Import, Error, Return Variables

```solidity
import {ModularEtherspotWallet} from "../../wallet/ModularEtherspotWallet.sol";

error ERC20SKV_InsufficientApprovalAmount();

function checkSessionKeyPaused( address _sessionKey ) public view returns (bool paused) {

function validateSessionKeyParams( address _sessionKey, PackedUserOperation calldata userOp ) public returns (bool valid) {

function getAssociatedSessionKeys() public view returns (address[] memory keys) {

function getSessionKeyData( address _sessionKey ) public view returns (SessionData memory data) {

function validateUserOp( PackedUserOperation calldata userOp, bytes32 userOpHash ) external override returns (uint256 validationData) {
```

## [I-02] Missing Events

```solidity
function toggleSessionKeyPause(address _sessionKey) external {

function onInstall(bytes calldata data) external override {

function onUninstall(bytes calldata data) external override {
```

## [G-01] Cache array length outside of a loop

If not cached, the solidity compiler will always read the length of the array during each iteration. That is, if it is a storage array, this is an extra sload operation (100 additional extra gas for each iteration except for the first) and if it is a memory array, this is an extra mload operation (3 additional gas for each iteration except for the first).

```solidity
for (uint256 i; i < sessionKeys.length; i++) {
```

## [G-02] Should use memory instead of storage variable

```solidity
SessionData storage sd = sessionData[sessionKeySigner][msg.sender];
SessionData storage sd = sessionData[_sessionKey][msg.sender];
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Etherspot Sessionkeyvalidator |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Etherspot-SessionKeyValidator-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

