---
# Core Classification
protocol: Next Generation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56700
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-01-next-generation
source_link: https://code4rena.com/reports/2025-01-next-generation
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
finders_count: 0
finders:
---

## Vulnerability Title

[06] Missing blacklist validation in `approve()` and `permit()` functions

### Overview

See description below for full details.

### Original Finding Content


The `Token` contract fails to implement blacklist validations in the `approve()` and `permit()` functions, contrary to the technical specification which explicitly requires that neither the owner nor spender should be blacklisted.

Link to the docs [here](https://github.com/code-423n4/2025-01-next-generation/blob/main/docbot/eurf-sc-technical-specification.md# approve).

Here is the `ERC20MetaTxUpgradeable::permit()` function:
```

    function permit(
        address owner,
        address spender,
        uint256 value,
        uint256 deadline,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) public virtual {
        if (block.timestamp > deadline) revert DeadLineExpired(deadline);

        bytes32 structHash = keccak256(abi.encode(_PERMIT_TYPEHASH, owner, spender, value, _useNonce(owner), deadline));

        bytes32 hash = _hashTypedDataV4(structHash);

        address signer = ECDSA.recover(hash, v, r, s);
        if (signer != owner) revert InvalidSignature();

        _approve(owner, spender, value);
    }
```

And the `ERC20Upgradeable` functions:
```

    function approve(address spender, uint256 value) public virtual returns (bool) {
        address owner = _msgSender();
        _approve(owner, spender, value);
        return true;
    }

    function _approve(address owner, address spender, uint256 value) internal {
        _approve(owner, spender, value, true);
    }

    function _approve(address owner, address spender, uint256 value, bool emitEvent) internal virtual {
        ERC20Storage storage $ = _getERC20Storage();
        if (owner == address(0)) {
            revert ERC20InvalidApprover(address(0));
        }
        if (spender == address(0)) {
            revert ERC20InvalidSpender(address(0));
        }
        $._allowances[owner][spender] = value;
        if (emitEvent) {
            emit Approval(owner, spender, value);
        }
    }
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Next Generation |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2025-01-next-generation
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2025-01-next-generation

### Keywords for Search

`vulnerability`

