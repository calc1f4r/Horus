---
# Core Classification
protocol: Taiko
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36003
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/taiko/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/taiko/review.pdf
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

protocol_categories:
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Migration Of BridgedERC20 Tokens Is Missing Access Control

### Overview


The report discusses a bug found during a migration process for a token. The bug allows anyone to migrate by burning their old tokens and minting new ones, but there is no access control in place. This means that a malicious actor could call the burn() function on tokens locked in a smart contract, leaving the user's new tokens stuck in the contract. The recommendation is to add access controls so that only the user can burn their own tokens. However, this may make it difficult to fully migrate away from the old token in the future. The resolution is to add access control to the burn() function in a new update. 

### Original Finding Content

## Description

During a migration from an old bridged token (bToken) to a new bToken, the `burn()` function allows anyone to migrate by burning their old bTokens and minting new bTokens. However, no access control is placed on this functionality. As a result, if a user has their bTokens locked in a smart contract (such as a liquidity pool), a malicious actor can call `burn()` on the tokens in the LP. This would result in the user’s new bTokens being stuck in the smart contract.

```solidity
function burn(address account, uint256 amount) public nonReentrant whenNotPaused {
    if (migratingAddress != address(0) && !migratingInbound) {
        // Outbond migration
        emit MigratedTo(migratingAddress, account, amount);
        // Ask the new bridged token to mint token for the user.
        IBridgedERC20(migratingAddress).mint(account, amount); //@audit no access control on `account`
    } else if (msg.sender != resolve("erc20_vault", true)) {
        // Bridging to vault
        revert RESOLVER_DENIED();
    }
    _burnToken(account, amount);
}
```

## Recommendations

- Add access controls such that a user can only `burn()` (migrate) their own bTokens.
- One consideration to make with adding access control is that it is no longer possible to fully migrate away from an old bToken. There will most likely always remain some unmigrated tokens. Previously the team could migrate the remaining tokens for inactive users, but this would no longer be possible. This may lead to complications if the new bTokens need to be migrated away from at a later date, since a bToken cannot have an inbound and an outbound migration simultaneously.
- A solution to this second issue could be to allow the owner to migrate other users’ tokens.

## Resolution

Access control has been added to the function `burn()` such that it may only be called by the address which is migrating tokens. This can be seen in PR #15566.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Taiko |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/taiko/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/taiko/review.pdf

### Keywords for Search

`vulnerability`

