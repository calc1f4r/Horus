---
# Core Classification
protocol: Linea Bridge Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32794
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/linea-bridge-audit-1
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
  - OpenZeppelin
---

## Vulnerability Title

Token Bridge Reentrancy Can Corrupt Token Accounting

### Overview


The TokenBridge contract allows users to transfer tokens between different layers by calling the bridgeToken function. However, this function is vulnerable to reentrancy attacks, which could result in an attacker receiving more tokens than they initially bridged. This could lead to the theft of tokens from other users. The issue has been resolved by adding reentrancy protection.

### Original Finding Content

The `TokenBridge` contract gets deployed on both L1 and L2, allowing users to bridge tokens between the layers by calling the [`bridgeToken`](https://github.com/Consensys/linea-contracts/blob/f08c1906855198e2dc0413a47dcb38291b7087e5/contracts/tokenBridge/TokenBridge.sol#L118) function. To compute the number of tokens that are being sent, the `bridgeToken` function first retrieves its current balance, transfers the tokens from `msg.sender` to itself, and then [computes the difference](https://github.com/Consensys/linea-contracts/blob/f08c1906855198e2dc0413a47dcb38291b7087e5/contracts/tokenBridge/TokenBridge.sol#L150) between its new balance and the original one. This is done to handle tokens with unusual logic, such as those having a fee on transfers.


However, this function is vulnerable to reentrancy attacks through token callbacks, for example with [ERC-777](https://eips.ethereum.org/EIPS/eip-777) tokens. This would allow an attacker to be credited with more tokens than they initially bridged. For example, in the case of an ERC-777-compliant token called "myToken", an attacker could:


1. Register an attacker-owned contract as an `ERC777TokensSender` to the [ERC-1820 registry](https://etherscan.io/address/0x1820a4B7618BdE71Dce8cdc73aAB6C95905faD24).
2. Call `bridgeToken` with 500 tokens. The `balanceBefore` is 0 and `safeTransferFrom` is called, triggering the ERC-777 callback to the sender.
3. In the ERC-777 `tokensToSend` callback, call `bridgeToken` again with 500 additional tokens. In this subcall, `balanceBefore` is still 0, `safeTransferFrom` is called successfully and `balanceAfter` is 500.
4. The main call will end with a `balanceAfter` of 1000.


Having sent 1000 tokens in total, the attacker would be credited with 1500 tokens on L2. Assuming other users have bridged this token to L2, the attacker could withdraw the 1500 tokens, effectively stealing 500 tokens from other users. Note that some ERC-777 tokens currently have enough liquidity to motivate such an attack, such as [Skale](https://www.coingecko.com/en/coins/skale#markets), [AMP](https://www.coingecko.com/en/coins/amp#markets) or [VRA](https://www.coingecko.com/en/coins/verasity#markets).


Consider adding reentrancy protection to the `bridgeToken` function, such as OpenZeppelin's [`ReentrancyGuard`](https://docs.openzeppelin.com/contracts/4.x/api/security#ReentrancyGuard).


***Update:** Resolved at commit [bb3691b](https://github.com/Consensys/linea-contracts-fix/commit/bb3691b67101e5cc9839b781af861defa81a2986#diff-25f3d0fec85d77ddb3f064f0d83dd452e62c913e4d3a558253315cd533998265R152).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Linea Bridge Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/linea-bridge-audit-1
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

