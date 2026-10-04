---
# Core Classification
protocol: Exchange Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50195
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/pangolin/exchange-contracts-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/pangolin/exchange-contracts-smart-contract-security-assessment
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

MINT FUNCTION IS MISSING MOVEDELEGATES CALL

### Overview


The `Png` contract has a bug where the function `mint()` does not call the `_moveDelegates()` function. This means that every time `Png` tokens are minted, users will have to manually call `delegate()` to update their voting power in the smart contract. The impact and likelihood of this bug are both rated as 3 out of 5. The recommendation is to update the contract with the fix provided by the Pangolin team in commit id bbbf14abf0283fa7ea3ccf07288fecdc177ed8f9.

### Original Finding Content

##### Description

In the `Png` contract, the function `mint()` does not call the `_moveDelegates()` function:

#### PNG.sol

```
function mint(address dst, uint rawAmount) external returns (bool) {
    require(msg.sender == minter && minter != address(0), "Png::mint: unauthorized");
    uint96 amount = safe96(rawAmount, "Png::mint: amount exceeds 96 bits");
    _mintTokens(dst, amount);
    return true;
}

```

#### PNG.sol

```
function _mintTokens(address dst, uint96 amount) internal {
    require(dst != address(0), "Png::_mintTokens: cannot mint to the zero address");

    totalSupply = SafeMath.add(totalSupply, uint(amount));
    balances[dst] = add96(balances[dst], amount, "Png::_mintTokens: mint amount overflows");
    emit Transfer(address(0), dst, amount);

    require(totalSupply <= maxSupply, "Png::_mintTokens: mint result exceeds max supply");
}

```

This causes that every time `Png` tokens are minted the users will have to manually call `delegate()` passing their own address as parameter so their voting power is correctly accounted/updated in the smart contract:

![1.png](https://halbornmainframe.com/proxy/audits/images/659e68a5a1aa3698c0e743c1)

##### Score

Impact: 3  
Likelihood: 3

##### Recommendation

**SOLVED**: `Pangolin team` solved the issue in the commit id [bbbf14abf0283fa7ea3ccf07288fecdc177ed8f9](https://github.com/pangolindex/exchange-contracts/commit/bbbf14abf0283fa7ea3ccf07288fecdc177ed8f9).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Exchange Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/pangolin/exchange-contracts-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/pangolin/exchange-contracts-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

