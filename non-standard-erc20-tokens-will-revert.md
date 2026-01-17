---
# Core Classification
protocol: Primex Contracts
chain: everychain
category: uncategorized
vulnerability_type: erc20

# Attack Vector Details
attack_type: erc20
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51129
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/primex/primex-contracts
source_link: https://www.halborn.com/audits/primex/primex-contracts
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
  - erc20
  - change_validation
  - check_return_value
  - transfer_result_check

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

NON-STANDARD ERC20 TOKENS WILL REVERT

### Overview


The bug report concerns a function in the `TokenTransfersLibrary.sol` library that is used for transferring ERC20 tokens in the protocol. The library uses the interface of `IERC20` from OpenZeppelin, which enforces a return value on transfer. However, this pattern is not followed by all ERC20 tokens, such as USDT, which causes the contract to revert and prevent the transaction from being executed. The code location of the issue is specified in the report. The BVSS score for this bug is 5.6, and the recommendation is to consider using a non-strict interface, as Compound does, for transferring ERC20 tokens. The Primex team has solved the issue by using a non-strict interface, and the commit ID for the solution is provided.

### Original Finding Content

##### Description

The library `TokenTransfersLibrary.sol` contains the function to perform ERC20 tokens transfers in the protocol. However, this library uses the interface of `IERC20` from OpenZeppelin which enforces the return value on transfer.

This pattern is not followed by all ERC20 tokens, as for example USDT. If attempting to transfer these tokens, the contract will revert, preventing the transaction to be executed.

Code Location
-------------

[TokenTransfersLibrary.sol#L12-L19](https://github.com/primex-finance/primex_contracts/blob/f809cc0471935013699407dcd9eab63b60cd2e22/src/contracts/libraries/TokenTransfersLibrary.sol#L12-L19)

#### TokenTransfersLibrary.sol

```
function doTransferFromTo(address token, address from, address to, uint256 amount) public returns (uint256) {
    uint256 balanceBefore = IERC20(token).balanceOf(to);
    // The returned value is checked in the assembly code below.
    // Arbitrary `from` should be checked at a higher level. The library function cannot be called by the user.
    // slither-disable-next-line unchecked-transfer arbitrary-send-erc20
    IERC20(token).transferFrom(from, to, amount);

    bool success;

```

[TokenTransfersLibrary.sol#L46-L51](https://github.com/primex-finance/primex_contracts/blob/f809cc0471935013699407dcd9eab63b60cd2e22/src/contracts/libraries/TokenTransfersLibrary.sol#L46-L51)

#### TokenTransfersLibrary.sol

```
function doTransferOut(address token, address to, uint256 amount) public {
    // The returned value is checked in the assembly code below.
    // slither-disable-next-line unchecked-transfer
    IERC20(token).transfer(to, amount);

    bool success;

```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:M/Y:L/R:N/S:U (5.6)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:M/Y:L/R:N/S:U)

##### Recommendation

Consider using a non-strict interface, as compound does, to transfer ERC20 tokens.

##### Remediation

**SOLVED**: The **Primex team** solved the issue by using a non-strict interface.

`Commit ID:` [88d33deeebf9c169d21e333ef871c518b10e0b33](https://github.com/primex-finance/primex_contracts/pull/956/commits/88d33deeebf9c169d21e333ef871c518b10e0b33)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Primex Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/primex/primex-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/primex/primex-contracts

### Keywords for Search

`ERC20, Change Validation, Check Return Value, Transfer Result Check`

