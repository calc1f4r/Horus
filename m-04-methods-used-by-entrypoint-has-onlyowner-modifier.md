---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6450
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest
source_link: https://code4rena.com/reports/2023-01-biconomy
github_link: https://github.com/code-423n4/2023-01-biconomy-findings/issues/390

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 11
finders:
  - hihen
  - immeas
  - 0xbepresent
  - 0xDave
  - betweenETHlines
---

## Vulnerability Title

[M-04] Methods used by EntryPoint has `onlyOwner` modifier

### Overview


This bug report is about a vulnerability in the SmartAccount.sol file of the code-423n4/2023-01-biconomy repository. The `execute` and `executeBatch` functions in this file are only allowed to be called by the owner, not by the EntryPoint. This breaks the interaction with the EntryPoint, which is not supposed to be the case. To prove this concept, the reference implementation of the SimpleAccount.sol file from the eth-infinitism/account-abstraction repository was used, which does not have any `onlyOwner` modifier on the `execute` and `executeBatch` functions. To fix this vulnerability, the `onlyOwner` modifier should be removed from the `execute` and `executeBatch` functions in the SmartAccount.sol file.

### Original Finding Content


[contracts/smart-contract-wallet/SmartAccount.sol#L460-L461](https://github.com/code-423n4/2023-01-biconomy/blob/main/scw-contracts/contracts/smart-contract-wallet/SmartAccount.sol#L460-L461)<br>
[contracts/smart-contract-wallet/SmartAccount.sol#L465-L466](https://github.com/code-423n4/2023-01-biconomy/blob/main/scw-contracts/contracts/smart-contract-wallet/SmartAccount.sol#L465-L466)

`execute` and `executeBatch` in `SmartAccount.sol` can only be called by owner, not EntryPoint:

```javascript
File: SmartAccount.sol

460:    function execute(address dest, uint value, bytes calldata func) external onlyOwner{
461:        _requireFromEntryPointOrOwner();
462:        _call(dest, value, func);
463:    }
464:
465:    function executeBatch(address[] calldata dest, bytes[] calldata func) external onlyOwner{
466:        _requireFromEntryPointOrOwner();
467:        require(dest.length == func.length, "wrong array lengths");
468:        for (uint i = 0; i < dest.length;) {
469:            _call(dest[i], 0, func[i]);
470:            unchecked {
471:                ++i;
472:            }
473:        }
474:    }
```

From [EIP-4337](https://eips.ethereum.org/EIPS/eip-4337):

> *   **Call the account with the `UserOperation`’s calldata.** It’s up to the account to choose how to parse the calldata; an expected workflow is for the account to have an execute function that parses the remaining calldata as a series of one or more calls that the account should make.

### Impact

This breaks the interaction with EntryPoint.

### Proof of Concept

The reference implementation has both these functions without any onlyOwner modifiers:

<https://github.com/eth-infinitism/account-abstraction/blob/develop/contracts/samples/SimpleAccount.sol#L56-L73>

```javascript
56:    /**
57:     * execute a transaction (called directly from owner, not by entryPoint)
58:     */
59:    function execute(address dest, uint256 value, bytes calldata func) external {
60:        _requireFromEntryPointOrOwner();
61:        _call(dest, value, func);
62:    }
63:
64:    /**
65:     * execute a sequence of transaction
66:     */
67:    function executeBatch(address[] calldata dest, bytes[] calldata func) external {
68:        _requireFromEntryPointOrOwner();
69:        require(dest.length == func.length, "wrong array lengths");
70:        for (uint256 i = 0; i < dest.length; i++) {
71:            _call(dest[i], 0, func[i]);
72:        }
73:    }
```

### Tools Used

vscode

### Recommended Mitigation Steps

Remove `onlyOwner` modifier from `execute` and `executeBatch`.

**[livingrockrises (Biconomy) confirmed](https://github.com/code-423n4/2023-01-biconomy-findings/issues/390#issuecomment-1404615354)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | hihen, immeas, 0xbepresent, 0xDave, betweenETHlines, wait, HE1M, hansfriese, peanuts, Kutu, prc |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-biconomy
- **GitHub**: https://github.com/code-423n4/2023-01-biconomy-findings/issues/390
- **Contest**: https://code4rena.com/contests/2023-01-biconomy-smart-contract-wallet-contest

### Keywords for Search

`vulnerability`

