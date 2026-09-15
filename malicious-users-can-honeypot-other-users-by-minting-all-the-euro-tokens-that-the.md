---
# Core Classification
protocol: The Standard
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41605
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clql6lvyu0001mnje1xpqcuvl
source_link: none
github_link: https://github.com/Cyfrin/2023-12-the-standard

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
finders_count: 2
finders:
  - dimulski
  - matej
---

## Vulnerability Title

Malicious users can honeypot other users by minting all the ``EURO`` tokens that the vault's ``collateralRate`` allows right before sale

### Overview


The report explains a bug in the SmartVaultManagerV5.sol contract where malicious users can take advantage of the sale of Smart Vault NFTs. These NFTs represent ownership of a smart vault and allow users to sell their vault's collateral and debt on NFT marketplaces. The bug allows a malicious user to front run a buyer's transaction and mint all the EURO tokens that the vault's collateralRate allows, while still receiving the payment for the NFT. This can result in the buyer receiving a vault that cannot mint any EURO tokens without additional collateral. The bug was detected through manual review and the report recommends implementing a mechanism to pause all interactions when a vault is put up for sale.

### Original Finding Content

## Summary
Each smart vault is represented by an NFT that is owned inittialy by the user who minted it by calling  the ```mint()``` function in ``SmartVaultManagerV5.sol`` contract:
```solidity
function mint() external returns (address vault, uint256 tokenId) {
        tokenId = lastToken + 1;
        _safeMint(msg.sender, tokenId);
        lastToken = tokenId;
        vault = ISmartVaultDeployer(smartVaultDeployer).deploy(address(this), msg.sender, euros);
        smartVaultIndex.addVaultAddress(tokenId, payable(vault));
        IEUROs(euros).grantRole(IEUROs(euros).MINTER_ROLE(), vault);
        IEUROs(euros).grantRole(IEUROs(euros).BURNER_ROLE(), vault);
        emit VaultDeployed(vault, msg.sender, euros, tokenId);
    }
```

As per the whitepaper: ``Vault NFT: A cutting-edge NFT representing the key attached to the Smart Vault. This NFT
allows users to sell their Smart Vault collateral and debt on OpenSea or other reputable NFT
marketplaces. The NFT's ownership grants control over the Smart Vault.
`` If the NFT is put for sale and has an amount of ``EURO`` that can be minted, without the buyer having to provide additional collateral a malicious user can front run the buyer transaction to buy the NFT and mint all the ``EURO`` that the ``collateralRate`` of the vault allows, and still receive the price paid by the buyer for the NFT.

## Vulnerability Details
If for example the smart vault is overcollateralized and the owner can still mint ``1000 EUROs`` and he has put the NFT for sale  for ``$800`` he can front run the buy transaction from the buyer and mint the ``1000 EUROs``, and still receive the ``$800`` paid by the pair for the NFT.

1. User A owns Smart Vault 1
2. Smart Vault 1 has enough collateral to mint ``1000 EUROs``
3. User A lists Smart Vault 1 for ``$800``
4. User B buys Smart Vault 1
5. User A sees the transaction in the mempool and quickly front runs it in order to mint ``1000 EUROs``
6. User A mints additional ``1000 EUROs``  and User B now has a vault that can't mint any ``EUROs`` without additional collateral being provided

## Impact
Malicious users can honeypot other users

## Tools Used
Manual review

## Recommendations
Consider implementing a mechanism where the owner of the vault is required to pause all interactions if he puts the vault represented by an NFT for sale.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | The Standard |
| Report Date | N/A |
| Finders | dimulski, matej |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-12-the-standard
- **Contest**: https://codehawks.cyfrin.io/c/clql6lvyu0001mnje1xpqcuvl

### Keywords for Search

`vulnerability`

