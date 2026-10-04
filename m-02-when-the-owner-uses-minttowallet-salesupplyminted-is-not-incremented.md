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
solodit_id: 44185
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Vallarok-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-02] When The Owner Uses `mintToWallet()`, `saleSupplyMinted` Is Not Incremented

### Overview


The `mintToWallet()` function in `RunaAGI.sol` is used to mint NFTs to the wallet, but there is a bug in the code. The function does not update the `saleSupplyMinted` counter, which tracks how many tokens have been sold or allocated during specific sale events. This can cause the contract to inaccurately represent how many tokens are left for sale. To fix this, the `saleSupplyMinted` counter needs to be increased by 1 within the loop in the code. The team has fixed the bug as suggested.

### Original Finding Content

## Severity

Medium Risk

## Description

The `mintToWallet()` function in `RunaAGI.sol` is used only by the owner to mint NFT to the wallet but in the for loop where NFTs are minted, it is forgotten to add a `saleSupplyMinted` update.

The function increases `_totalSupply` each time a token is minted but does not adjust the `saleSupplyMinted` counter. This counter tracks how many tokens have been sold or allocated during specific sale events.

Additionally, because of this, the admin can accidentally set the sale supply lower than the minted supply.

## Impact

By not increasing `saleSupplyMinted` when minting tokens through `mintToWallet`, the contract might inaccurately represent how many tokens are left for sale under the sale-specific conditions.

## Location of Affected Code

File: [contracts/RunaAGI.sol#L159](https://github.com/purple-banana/contract-runa/blob/7153c2ffbf3a5e958af921f0ab92e20c5035d9bf/contracts/RunaAGI.sol#L159)

```solidity
function mintToWallet(address _to, uint256 _amount) external onlyOwner {
    require(_totalSupply + _amount <= maxSupply, "Exceeds maximum supply");
    for (uint256 i = 0; i < _amount; i++) {
        _safeMint(_to, _tokenIdCounter.current());
        _tokenIdCounter.increment();
        _totalSupply++;
    }
}
```

## Recommendation

Consider including a `saleSupplyMinted` increase by 1 within the loop to ensure that each minting operation reflects on the sale supply counter.

## Team Response

Fixed as suggested.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

