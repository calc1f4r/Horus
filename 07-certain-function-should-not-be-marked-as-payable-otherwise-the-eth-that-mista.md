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
solodit_id: 25857
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/107

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[07] Certain function should not be marked as payable, otherwise the ETH that mistakenly sent along with the function call is locked in the contract

### Overview

See description below for full details.

### Original Finding Content


In AstariaRouter.sol deposit, mint, withdraw, redeem are payable

```solidity
  function mint(
    IERC4626 vault,
    address to,
    uint256 shares,
    uint256 maxAmountIn
  )
    public
    payable
    virtual
    override
    validVault(address(vault))
    returns (uint256 amountIn)
  {
    return super.mint(vault, to, shares, maxAmountIn);
  }

  function deposit(
    IERC4626 vault,
    address to,
    uint256 amount,
    uint256 minSharesOut
  )
    public
    payable
    virtual
    override
    validVault(address(vault))
    returns (uint256 sharesOut)
  {
    return super.deposit(vault, to, amount, minSharesOut);
  }

  function withdraw(
    IERC4626 vault,
    address to,
    uint256 amount,
    uint256 maxSharesOut
  )
    public
    payable
    virtual
    override
    validVault(address(vault))
    returns (uint256 sharesOut)
  {
    return super.withdraw(vault, to, amount, maxSharesOut);
  }

  function redeem(
    IERC4626 vault,
    address to,
    uint256 shares,
    uint256 minAmountOut
  )
    public
    payable
    virtual
    override
    validVault(address(vault))
    returns (uint256 amountOut)
  {
    return super.redeem(vault, to, shares, minAmountOut);
  }
```

The function pullToken is also marked as payable

```solidity
  function pullToken(
    address token,
    uint256 amount,
    address recipient
  ) public payable override {
    RouterStorage storage s = _loadRouterSlot();
    s.TRANSFER_PROXY.tokenTransferFrom(
      address(token),
      msg.sender,
      recipient,
      amount
    );
  }
```

These function only performs ERC20 token and are not designed to receive ETH.

The ETH that mistakenly sent along with the function call is locked in the contract In AstariaRouter.sol.

### Recommended Mitigation Steps

We recommend the protocol remove the payable keywords for the above mentioned function.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/107
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

