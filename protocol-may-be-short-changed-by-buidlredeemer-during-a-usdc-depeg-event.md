---
# Core Classification
protocol: Ondo Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31341
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
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

protocol_categories:
  - leveraged_farming
  - rwa
  - services
  - cdp
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Dacian
---

## Vulnerability Title

Protocol may be short-changed by `BuidlRedeemer` during a USDC depeg event

### Overview

See description below for full details.

### Original Finding Content

**Description:** `OUSGInstantManager::_redeemBUIDL` assumes that 1 BUIDL = 1 USDC as it [enforces](https://github.com/ondoprotocol/rwa-internal/blob/6747ebada1c867a668a8da917aaaa7a0639a5b7a/contracts/ousg/ousgInstantManager.sol#L453-L459) receiving 1 USDC for every 1 BUIDL it redeems:
```solidity
uint256 usdcBalanceBefore = usdc.balanceOf(address(this));
buidl.approve(address(buidlRedeemer), buidlAmountToRedeem);
buidlRedeemer.redeem(buidlAmountToRedeem);
require(
  usdc.balanceOf(address(this)) == usdcBalanceBefore + buidlAmountToRedeem,
  "OUSGInstantManager::_redeemBUIDL: BUIDL:USDC not 1:1"
);
```
In the event of a USDC depeg (especially if the depeg is sustained), `BUIDLRedeemer` should return greater than a 1:1 ratio since 1 USDC would not be worth $1, hence 1 BUIDL != 1 USDC meaning the value of the protocol's BUIDL is worth more USDC. However `BUIDLReceiver` does not do this, it only ever [returns](https://etherscan.io/address/0x9ba14Ce55d7a508A9bB7D50224f0EB91745744b7#code) 1:1.

**Impact:** In the event of a USDC depeg the protocol will be short-changed by `BuidlRedeemer` since it will happily receive only 1 USDC for every 1 BUIDL redeemed, even though the value of 1 BUIDL would be greater than the value of 1 USDC due to the USDC depeg.

**Recommended Mitigation:** To prevent this situation the protocol would need to use an oracle to check whether USDC had depegged and if so, calculate the amount of USDC it should receive in exchange for its BUIDL. If it is short-changed it would either have to revert preventing redemptions or allow the redemption while saving the short-changed amount to storage then implement an off-chain process with BlackRock to receive the short-changed amount.

Alternatively the protocol may simply accept this as a risk to the protocol that it will be willingly short-changed during a USDC depeg in order to allow redemptions to continue.

**Ondo:**
Fixed in commits [408bff1](https://github.com/ondoprotocol/rwa-internal/commit/408bff112c39f393f67dde6c30a6addf3b221ee9), [8a9cae9](https://github.com/ondoprotocol/rwa-internal/commit/8a9cae9af5787f06db42b4224b147d60493e0133). We now use Chainlink USDC/USD Oracle and if USDC depegs below our tolerated minimum value both minting and redemptions will be stopped.

**Cyfrin:** Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Ondo Finance |
| Report Date | N/A |
| Finders | Dacian |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

