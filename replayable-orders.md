---
# Core Classification
protocol: Torch Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58797
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/torch-finance/9edd725c-737d-4273-b2ca-6e65ce7b7575/index.html
source_link: https://certificate.quantstamp.com/full/torch-finance/9edd725c-737d-4273-b2ca-6e65ce7b7575/index.html
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
finders_count: 3
finders:
  - Julio Aguilar
  - Michael Boyle
  - Cameron Biniamow
---

## Vulnerability Title

Replayable Orders

### Overview

See description below for full details.

### Original Finding Content

**Update**
The client acknowledged the issue and provided the following explanation:

> Our current plan is to support only blue-chip stablecoins (such as USDT and USDC). Since all supported assets are stablecoins, the impact of replay attacks would be relatively limited. In addition, we have implemented expiration constraints, so we believe this risk is manageable.

**File(s) affected:**`contracts/tgusd-engine/main.tolk`

**Description:** When users deposit collateral tokens to mint tgUSD or burn tgUSD to redeem collateral tokens, the user must obtain `order` data from the Torch backend. Order data includes details such as the order type, collateral asset, collateral amount, tgUSD amount, expiration time, and a signature from the `signerKey` verifying the order data. However, the `order` data does not include a nonce consumed in the `tgusd-engine` contract. Therefore, the order is replayable up until the expiration time has been reached. While orders are only valid when the `order.minter` or `order.redeemer` is the `jettonSender`, and require the `jettonSender` to transfer or burn their tgUSD to execute the order, the Torch admins may not want to allow tgUSD mints or collateral redeems for amounts greater than what is specified in the order.

**Exploit Scenario:**

1.   Bob obtains order data from the Torch backend to deposit 1,000 USDT and mint 1,000 tgUSD. The order contains an expiration time of five minutes in the future.
2.   Bob transfers 1,000 USDT to the `tgusd-engine` Jetton wallet and includes the order data in the forward payload.
3.   The chain of transactions is executed, and Bob is minted 1,000 tgUSD.
4.   Before expiration, Bob repeats steps (2 - 3) four more times.
5.   Bob has now deposited 5,000 USDT and is minted 5,000 tgUSD.

**Recommendation:** Include a nonce in the order data obtained from the Torch backend. In the `tgusd-engine` contract, consume and increment the nonce for the user to prevent replay attacks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Torch Finance |
| Report Date | N/A |
| Finders | Julio Aguilar, Michael Boyle, Cameron Biniamow |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/torch-finance/9edd725c-737d-4273-b2ca-6e65ce7b7575/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/torch-finance/9edd725c-737d-4273-b2ca-6e65ce7b7575/index.html

### Keywords for Search

`vulnerability`

