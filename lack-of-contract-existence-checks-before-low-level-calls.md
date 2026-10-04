---
# Core Classification
protocol: Maple Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18096
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/MapleFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/MapleFinance.pdf
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
finders_count: 3
finders:
  - Paweł Płatek
  - Maximilian Krüger
  - Michael Colburn
---

## Vulnerability Title

Lack of contract existence checks before low-level calls

### Overview


A bug has been identified in the ERC20Helper contract, which is similar to OpenZeppelin's SafeERC20 contract. When the transfer and approve functions are called on an address that is not a token contract address, the ERC20Helper functions will appear to silently succeed without transferring or approving any tokens, resulting in undefined behavior. This bug can be exploited by a malicious actor if a token contract is destroyed, as all transfers of the destroyed token will appear to succeed without any contract existence checks.

To solve this bug, short term solutions include adding a contract existence check before each of the low-level calls mentioned in the report, while long term solutions should include adding contract existence checks before all low-level CALLs, DELEGATECALLs, and STATICCALLs. These checks are inexpensive and would add an important layer of defense.

### Original Finding Content

## Difficulty: Medium

## Type: Data Validation

### Target: Throughout the codebase

## Description
The `ERC20Helper` contract fills a purpose similar to that of OpenZeppelin's `SafeERC20` contract. However, while OpenZeppelin's `SafeERC20` transfer and approve functions will revert when called on an address that is not a token contract address (i.e., one with zero-length bytecode), `ERC20Helper`’s functions will appear to silently succeed without transferring or approving any tokens.

If the address of an externally owned account (EOA) is used as a token address in the protocol, all transfers to it will appear to succeed without any tokens being transferred. This will result in undefined behavior.

Contract existence checks are usually performed via the `EXTCODESIZE` opcode. Since the `EXTCODESIZE` opcode would precede a `CALL` to a token address, adding `EXTCODESIZE` would make the `CALL` a “warm” access. As a result, adding the `EXTCODESIZE` check would increase the gas cost by only a little more than 100. Assuming a high gas price of 200 gwei and a current ether price of $4,200, that equates to an additional cost of 10 cents for each call to the functions of `ERC20Helper`, which is a low price to pay for increased security.

The following functions lack contract existence checks:
- **ERC20Helper**
  - `call` in `_call`
- **ProxyFactory**
  - `call` in `_initializeInstance`
  - `call` in `_upgradeInstance` (line 66)
  - `call` in `_upgradeInstance` (line 72)
- **Proxied**
  - `delegatecall` in `_migrate`
- **Proxy**
  - `delegatecall` in `_fallback`
- **MapleLoanInternals**
  - `delegatecall` in `_acceptNewTerms`

## Exploit Scenario
A token contract is destroyed. However, since all transfers of the destroyed token will succeed, all Maple protocol users can transact as though they have an unlimited balance of that token. If contract existence checks were executed before those transfers, all transfers of the destroyed token would revert.

## Recommendations
- **Short term**: Add a contract existence check before each of the low-level calls mentioned above.
- **Long term**: Add contract existence checks before all low-level `CALL`s, `DELEGATECALL`s, and `STATICCALL`s. These checks are inexpensive and add an important layer of defense.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Maple Labs |
| Report Date | N/A |
| Finders | Paweł Płatek, Maximilian Krüger, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/MapleFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/MapleFinance.pdf

### Keywords for Search

`vulnerability`

