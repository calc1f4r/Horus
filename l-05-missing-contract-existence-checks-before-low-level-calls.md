---
# Core Classification
protocol: Axelar Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24964
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-04-axelar
source_link: https://code4rena.com/reports/2022-04-axelar
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

protocol_categories:
  - dexes
  - bridge
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-05] Missing contract-existence checks before low-level calls

### Overview

See description below for full details.

### Original Finding Content


Low-level calls return success if there is no code present at the specified address. In addition to the zero-address checks, add a check to verify that `<address>.code.length > 0`

1.  File: src/AxelarGateway.sol (lines [398-415](https://github.com/code-423n4/2022-04-axelar/blob/dee2f2d352e8f20f20027977d511b19bfcca23a3/src/AxelarGateway.sol#L398-L415))

```solidity
        if (tokenAddress == address(0)) revert TokenDoesNotExist(symbol);

        if (_getTokenType(symbol) == TokenType.External) {
            _checkTokenStatus(symbol);

            DepositHandler depositHandler = new DepositHandler{ salt: salt }();

            (bool success, bytes memory returnData) = depositHandler.execute(
                tokenAddress,
                abi.encodeWithSelector(
                    IERC20.transfer.selector,
                    address(this),
                    IERC20(tokenAddress).balanceOf(address(depositHandler))
                )
            );

            if (!success || (returnData.length != uint256(0) && !abi.decode(returnData, (bool))))
                revert BurnFailed(symbol);
```

2.  File: src/AxelarGatewayProxy.sol (line [19](https://github.com/code-423n4/2022-04-axelar/blob/dee2f2d352e8f20f20027977d511b19bfcca23a3/src/AxelarGatewayProxy.sol#L19))

```solidity
        (bool success, ) = gatewayImplementation.delegatecall(
```

3.  File: src/AxelarGatewayProxy.sol (line [34](https://github.com/code-423n4/2022-04-axelar/blob/dee2f2d352e8f20f20027977d511b19bfcca23a3/src/AxelarGatewayProxy.sol#L34))

```solidity
            let result := delegatecall(gas(), implementation, 0, calldatasize(), 0, 0)
```

4.  File: src/AxelarGateway.sol (line [350](https://github.com/code-423n4/2022-04-axelar/blob/dee2f2d352e8f20f20027977d511b19bfcca23a3/src/AxelarGateway.sol#L350))

```solidity
            (bool success, bytes memory data) = TOKEN_DEPLOYER_IMPLEMENTATION.delegatecall(
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Axelar Network |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-axelar
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-04-axelar

### Keywords for Search

`vulnerability`

