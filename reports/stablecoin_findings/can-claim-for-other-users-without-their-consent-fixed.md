---
# Core Classification
protocol: Linea Token and Airdrop Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62452
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2025/07/linea-token-and-airdrop-contracts/
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
finders_count: 2
finders:
  - George Kobakhidze
  -  Heiko Fisch
                        
---

## Vulnerability Title

Can Claim for Other Users Without Their Consent ✓ Fixed

### Overview

See description below for full details.

### Original Finding Content

...

Export to GitHub ...

Set external GitHub Repo ...

Export to Clipboard (json)

Export to Clipboard (text)

#### Resolution

This has been fixed in [PR 14](https://github.com/Consensys/linea-tokens/pull/14) (last commit on the branch: [40f5d75](https://github.com/Consensys/linea-tokens/tree/40f5d753aa35a5e53098564f22314ec46d3ad16f)).

#### Description

The `TokenAirdrop` contract allows users to claim tokens based on their available calculation. This is done by executing the claim function with an address to claim for:

**src/airdrops/TokenAirdrop.sol:L120-L138**

```
/**
 * @notice Claims tokens for an account while the claiming is active.
 * @dev Claiming sets claim status pre-transferring avoiding reentry, and all multiplier tokens are soulbound avoiding
 * transfer manipulation.
 * @param _account Account being claimed for.
 */
function claim(address _account) external {
  require(block.timestamp < CLAIM_END, ClaimFinished());
  require(!hasClaimed[_account], AlreadyClaimed());

  uint256 tokenAmount = calculateAllocation(_account);

  require(tokenAmount != 0, ClaimAmountIsZero());

  hasClaimed[_account] = true;
  emit Claimed(_account, tokenAmount);

  TOKEN.safeTransfer(_account, tokenAmount);
}
```

As it can be seen above, anyone can initiate the claim for any `account`, and the tokens will indeed be transferred to the appropriate recipient. However, this is done without any explicit consent of the account. This may have two impacts.

First, this has personal implications for the `account` owner, such as tax implications. In many jurisdictions a person is taxed upon receipt of a valuable asset, whether they wanted it or not. While anyone indeed can send anything to anyone, such as stablecoins to a known ENS, in this case the user who initiated the `claim()` call does not actually spend any of their own funds. They simply claim the airdrop for the `account` and trigger a potential taxable event, which the recipient potentially wanted to delay until the next tax year, for example.

Second, not all eligible accounts may be owned by their owners securely. For example, the private keys could have been lost. In that case, claiming and sending tokens to that account could either effectively burn these tokens. Instead, these tokens could have been used by the foundation or for other needs after `CLAIM_END`.

To sum it up, the explicit consent of the owners of eligible `account` addresses would go a long way in such an airdrop contract. This is something that has also been considered in other large airdrops in the cryptocurrency industry.

#### Recommendation

Consider requiring explicit consent of the `account` address owners, such as providing a signed message from the `account` or initiating the claim transaction from the `account` address and claiming on `msg.sender`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Linea Token and Airdrop Contracts |
| Report Date | N/A |
| Finders | George Kobakhidze,  Heiko Fisch
                         |

### Source Links

- **Source**: https://diligence.consensys.io/audits/2025/07/linea-token-and-airdrop-contracts/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

