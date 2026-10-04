---
# Core Classification
protocol: Swapexchange
chain: everychain
category: uncategorized
vulnerability_type: erc20

# Attack Vector Details
attack_type: erc20
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26172
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md
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
  - weird_erc20
  - transferfrom_vs_safetransferfrom
  - safetransfer

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Hans
  - 0kage
---

## Vulnerability Title

Use safe transfer for ERC20 tokens

### Overview


This bug report is about the protocol of a certain system not supporting all ERC20 tokens. The protocol uses the original transfer functions, and some tokens (like USDT) do not implement the EIP20 standard correctly, making their transfer/transferFrom functions return void instead of a success boolean. This causes the transaction to revert, making the tokens unusable in the protocol.

The impact of this bug is that tokens that do not correctly implement the EIP20, like USDT, will be unusable in the protocol as they revert the transaction because of the missing return value.

The recommended mitigation for this bug is to use OpenZeppelin's SafeERC20 versions with the safeTransfer and safeTransferFrom functions that handle the return value check as well as non-standard-compliant tokens. The protocol has been fixed in the commit 564f711c6f915f5a7696739266a1f8059ee9a172, and has been verified by Cyfrin.

### Original Finding Content

**Severity:** Medium

**Description:** The protocol intends to support all ERC20 tokens but the implementation uses the original transfer functions.
Some tokens (like USDT) do not implement the EIP20 standard correctly and their transfer/transferFrom function return void instead of a success boolean. Calling these functions with the correct EIP20 function signatures will revert.

```solidity
TransferUtils.sol
34:     function _transferERC20(address token, address to, uint256 amount) internal {
35:         IERC20 erc20 = IERC20(token);
36:         require(erc20 != IERC20(address(0)), "Token Address is not an ERC20");
37:         uint256 initialBalance = erc20.balanceOf(to);
38:         require(erc20.transfer(to, amount), "ERC20 Transfer failed");//@audit-issue will revert for USDT
39:         uint256 balance = erc20.balanceOf(to);
40:         require(balance >= (initialBalance + amount), "ERC20 Balance check failed");
41:     }
```

**Impact:** Tokens that do not correctly implement the EIP20 like USDT, will be unusable in the protocol as they revert the transaction because of the missing return value.

**Recommended Mitigation:** We recommend using OpenZeppelin's SafeERC20 versions with the safeTransfer and safeTransferFrom functions that handle the return value check as well as non-standard-compliant tokens.

**Protocol:** Fixed in commit [564f711](https://github.com/SwapExchangeio/Contracts/commit/564f711c6f915f5a7696739266a1f8059ee9a172)

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Swapexchange |
| Report Date | N/A |
| Finders | Hans, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-swapexchange.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`ERC20, Weird ERC20, transferFrom vs safeTransferFrom, SafeTransfer`

