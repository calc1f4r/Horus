---
# Core Classification
protocol: Vallarok
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44182
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Vallarok-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[H-01] Malicious User Can Mint Unlimited Amount of NFTs Due to Reentrancy in `whitelistMint()` and `FCFSMint()`

### Overview


The report states that there is a high risk bug in the `whitelistMint()` and `FCFSMint()` functions in the `RunaAGI.sol` file. These functions are vulnerable to reentrancy, which means that a malicious user can exploit them to mint an unlimited number of NFTs. The bug is caused by the lack of a reentrancy modifier in the code, which allows the attacker to continuously call the `_safeMint()` function. The recommended solution is to add a reentrancy modifier to these functions. The team has acknowledged the bug and has fixed it as suggested.

### Original Finding Content

## Severity

High Risk

## Description

The `whitelistMint()` and `FCFSMint()` functions are vulnerable to reentrancy. We can see that the function fails to apply a reentrancy modifier.

When a malicious user calls them, they can do a reentrancy attack via the `_safeMint()` function that is called. We can see that absolutely all variables are updated afterwards. Thus, a malicious user can mint as many NFTs as he wants.

## Location of Affected Code

File: [contracts/RunaAGI.sol](https://github.com/purple-banana/contract-runa/blob/7153c2ffbf3a5e958af921f0ab92e20c5035d9bf/contracts/RunaAGI.sol)

```solidity
function whitelistMint(uint256 _salt, bytes32 _msgHash, bytes memory _signature) external payable {
    // code
    _safeMint(msg.sender, _tokenIdCounter.current());
    _tokenIdCounter.increment();
    _totalSupply++;
    saleSupplyMinted++;
}

function FCFSMint(uint256 _salt, bytes32 _msgHash, bytes memory _signature) external payable {
    // code
    _safeMint(msg.sender, _tokenIdCounter.current());
    _tokenIdCounter.increment();
    _totalSupply++;
    saleSupplyMinted++;
    fcfsMinted[msg.sender] += 1;
}
```

## Recommendation

Consider adding a reentrancy modifier on `whitelistMint()` and `FCFSMint()`.

## Team Response

Fixed as suggested.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Vallarok |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Vallarok-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

