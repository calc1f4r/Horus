---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25837
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/247

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

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - cccz
  - KIntern\_NA
---

## Vulnerability Title

[M-21] When a private vault offers a loan in ERC777 tokens, the private vault can refuse to receive repayment in the safeTransferFrom callback to force liquidation of the borrower's collateral

### Overview


This bug report is about the LienToken.makePayment function in the Astaria protocol. When a borrower calls this function to repay a loan, it uses the safeTransferFrom function to send tokens to the recipient of the vault. However, if the token for the loan is an ERC777 token, a malicious private vault owner can refuse to receive repayment in the callback, which results in the borrower not being able to repay the loan and the borrower's collateral being auctioned off when the loan expires. To mitigate this issue, it is recommended to send tokens to the vault first when a borrower repays, and the private vault owner can later claim it. The protocol is not designed to work with ERC777 tokens, and this issue has been flagged as a duplicate of another issue related to the lack of ERC777 support.

### Original Finding Content


When the borrower calls LienToken.makePayment to repay the loan, safeTransferFrom is used to send tokens to the recipient of the vault, which in the case of a private vault is the owner of the private vault.

```solidity
    s.TRANSFER_PROXY.tokenTransferFrom(stack.lien.token, payer, payee, amount);
...
  function tokenTransferFrom(
    address token,
    address from,
    address to,
    uint256 amount
  ) external requiresAuth {
    ERC20(token).safeTransferFrom(from, to, amount);
  }
...
  function recipient() public view returns (address) {
    if (IMPL_TYPE() == uint8(IAstariaRouter.ImplementationType.PublicVault)) {
      return address(this);
    } else {
      return owner();
    }
  }
```

If the token for the loan is an ERC777 token, a malicious private vault owner can refuse to receive repayment in the callback, which results in the borrower not being able to repay the loan and the borrower's collateral being auctioned off when the loan expires.

### Proof of Concept

<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/LienToken.sol#L849-L850><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/TransferProxy.sol#L28-L35><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/LienToken.sol#L900-L909><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/VaultImplementation.sol#L366-L372>

### Recommended Mitigation Steps

For private vaults, when the borrower repays, sending tokens to the vault, and the private vault owner claims it later.

**[androolloyd (Astaria) acknowledged and commented via duplicate issue `#248`](https://github.com/code-423n4/2023-01-astaria-findings/issues/248#issuecomment-1413601598):**
> ERC777 issues can be quite problematic, the procotol isn't designed to work with 777, fee on transfer tokens, rebasing tokens.

**[Picodes (judge) commented](https://github.com/code-423n4/2023-01-astaria-findings/issues/247#issuecomment-1443371103):**
 > Flagging as duplicate of this issue all findings related to the lack of ERC777 support.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | cccz, KIntern\_NA |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/247
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

