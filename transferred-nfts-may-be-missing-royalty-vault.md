---
# Core Classification
protocol: Camp - NFT
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62793
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/camp-nft/94cdb738-1a01-4f6c-8632-3bdec427161e/index.html
source_link: https://certificate.quantstamp.com/full/camp-nft/94cdb738-1a01-4f6c-8632-3bdec427161e/index.html
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
  - Paul Clemson
  - Gereon Mendler
  - Tim Sigl
---

## Vulnerability Title

Transferred NFTs May Be Missing Royalty Vault

### Overview


The client has reported a bug in the `IpNFT.sol` file where token owners are not receiving their royalty payments and rewards for dispute settlements. This is because the contracts that are supposed to receive these funds are only created during the minting process, and when a token is transferred to a new owner, they may not have a contract registered in the `royaltyVaults` mapping. This results in the funds being sent to the zero address and lost. 

To fix this issue, the report suggests implementing the factory pattern, which would create contracts only when needed and the user buying access would pay for the gas. This could be achieved by making the vault mapping private and exposing a function that retrieves or creates contracts for queried addresses. This would ensure that all token owners have a contract to receive their funds. 

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `efb615e3aef4e38ad324b2e9be5c5da16f0e7c83`.

**File(s) affected:**`IpNFT.sol`

**Description:** The token owners receive royalty payments for subscriptions, and may also be rewarded for dispute settlements. These rewards are paid to the token owner, but not directly to avoid DoS attack vectors. Instead, each token owner is supposed to have a `RoyaltyVault` contract to receive these funds. These contracts are currently created during the minting process. However, when a token is transferred to a new owner, they may not have a vault registered in the `royaltyVaults` mapping. In this case, royalty payments will be transferred to the zero address, resulting in a loss of funds due to the following code:

```
if (token == address(0)) {
    SafeTransferLib.safeTransferETH(ipToken.royaltyVaults(recipient), share);
} else {
    SafeTransferLib.safeTransferFrom(token, payer, ipToken.royaltyVaults(recipient), share);
}
```

Furthermore, there's no way for the new owner or the contract owner to create and register a vault to solve this issue.

**Exploit Scenario:**

1.   Alice mints token 1. A vault is generated for Alice.
2.   Alice transfers token 1 to Bob, who has no vault yet. 
3.   Charlie buys access for token 1.
4.   The royalty payment is sent to the zero address, as there's no vault for Bob.

**Recommendation:** There are various options to address this issue. We suggest implementing the factory pattern, which tracks the created vaults, and exposes a function `getOrCreateVault(address)` that retrieves or creates vaults for queried addresses. This would create vaults only when needed to receive funds, and the gas is paid by the user buying access in the marketplace.

This could be adopted in a minimized form inside the token contract. This could be achieved by making the vault mapping private and exposing a `getOrCreateVault()` function that attempts to retrieve the value from `_royaltyVaults`, and otherwise creates a new vault.

```
mapping(address => address) private _royaltyVaults;
function getOrCreateRoyaltyVault(address tokenOwner) external returns (address vault) {
    vault = _royaltyVaults[tokenOwner];
    if (vault == address(0)) { // <-- Create a new vault if there is no map entry
        vault = address(new RoyaltyVault(tokenOwner));
        royaltyVaults[tokenOwner] = vault;
    }
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Camp - NFT |
| Report Date | N/A |
| Finders | Paul Clemson, Gereon Mendler, Tim Sigl |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/camp-nft/94cdb738-1a01-4f6c-8632-3bdec427161e/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/camp-nft/94cdb738-1a01-4f6c-8632-3bdec427161e/index.html

### Keywords for Search

`vulnerability`

