---
# Core Classification
protocol: USDi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55384
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2025/04/usdi/
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
finders_count: 2
finders:
  - George Kobakhidze
  -  Vladislav Yaroshuk
                        
---

## Vulnerability Title

Risk of Backing Value Loss for Non-Whitelisted Token Holders  Acknowledged

### Overview


The report discusses a bug where the USDi token can lose its redemption guarantee if transferred to non-whitelisted addresses. This can result in price slippage and de-pegging, creating a two-tier market and diminishing user trust. The recommendation is to implement safeguards to prevent or warn against such transfers.

### Original Finding Content

...

Export to GitHub ...

Set external GitHub Repo ...

Export to Clipboard (json)

Export to Clipboard (text)

#### Resolution

USDi team has acknowledged this finding and noted that whitelisted clients that perform deposits and withdrawals are aware of such potential market mechanics.

#### Description

The `withdraw` function restricts withdrawals to whitelisted addresses via `_requireWhitelisted(msg.sender)`, ensuring that only tokens held by whitelisted users can be redeemed for their backing value. However, if tokens are transferred to non-whitelisted addresses, those tokens lose their redemption guarantee and rely solely on external market (e.g., DEX) liquidity. This can result in significant price slippage or de-pegging of the token when non-whitelisted holders attempt to sell their tokens.

Such a design introduces potential economic imbalances and creates a two-tier market. Non-whitelisted holders may unknowingly receive or hold USDi that cannot be redeemed, resulting in diminished liquidity and increased susceptibility to price manipulation. This undermines the stablecoin’s perceived value and could erode user trust.

#### Examples

**contracts/USDiCoin.sol:L28**

```
contract USDiCoin is ERC20, AccessControl, Pausable, ReentrancyGuard {

```

#### Recommendation

We recommend implementing safeguards to prevent or warn against transferring USDi tokens to non-whitelisted addresses. This could include transfer restrictions, redemption fallback mechanisms, or clearer documentation and interface signals to ensure users understand the implications of holding USDi outside the whitelist. Such measures would help preserve liquidity, protect users, and maintain the protocol’s stability.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | USDi |
| Report Date | N/A |
| Finders | George Kobakhidze,  Vladislav Yaroshuk
                         |

### Source Links

- **Source**: https://diligence.consensys.io/audits/2025/04/usdi/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

