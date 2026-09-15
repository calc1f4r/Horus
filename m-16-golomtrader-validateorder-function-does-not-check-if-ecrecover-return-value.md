---
# Core Classification
protocol: Golom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8753
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-golom-contest
source_link: https://code4rena.com/reports/2022-07-golom
github_link: https://github.com/code-423n4/2022-07-golom-findings/issues/357

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_marketplace
  - options_vault

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - cccz
  - joestakey
  - 0xHarry
  - teddav
  - AuditsAreUS
---

## Vulnerability Title

[M-16] `GolomTrader`: `validateOrder` function does not check if ecrecover return value is 0

### Overview


A bug has been discovered in the GolomTrader contract’s validateOrder function, which calls the Solidity ecrecover function directly to verify the given signatures. The return value of ecrecover may be 0, indicating an invalid signature, but the check can be bypassed when signer is 0. This bug could have a serious impact, as it could allow someone to bypass the signature verification process.

To fix this issue, it is recommended to use the recover function from OpenZeppelin’s ECDSA library for signature verification. This library provides a secure and reliable way to verify signatures, and should be used instead of the ecrecover function. By using this library, the bug can be fixed, and the signature verification process can be made secure.

### Original Finding Content


The validateOrder function of GolomTrader calls the Solidity ecrecover function directly to verify the given signatures.
The return value of ecrecover may be 0, which means the signature is invalid, but the check can be bypassed when signer is 0.

### Proof of Concept

<https://github.com/code-423n4/2022-07-golom/blob/e5efa8f9d6dda92a90b8b2c4902320acf0c26816/contracts/core/GolomTrader.sol#L176-L177>

### Recommended Mitigation Steps

Use the recover function from OpenZeppelin's ECDSA library for signature verification.

**[kenzo (warden) commented](https://github.com/code-423n4/2022-07-golom-findings/issues/357#issuecomment-1205955355):**
 > Seems invalid or QA at best. No impact on protocol as far as I see, invalid orders from "address 0" will revert.<br>
> In fillAsk if the `o.signer` is address 0, the function will try to pull tokens from address 0 and will fail.<br>
> In fillBid/criteria, function will try to transfer msg.sender's tokens to address 0 and pull weth from address 0. So will fail.<br>

**[0xsaruman (Golom) disputed](https://github.com/code-423n4/2022-07-golom-findings/issues/357)**

**[LSDan (judge) commented](https://github.com/code-423n4/2022-07-golom-findings/issues/357#issuecomment-1277605944):**
 > This is valid as a medium risk. It opens a griefing attack where a bad actor spams any system that relies on this function. The fact that the fill will fail while the order appears valid is specifically what makes this griefing attack possible.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Golom |
| Report Date | N/A |
| Finders | cccz, joestakey, 0xHarry, teddav, AuditsAreUS, jayjonah8, djxploit, 0x1f8b |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-golom
- **GitHub**: https://github.com/code-423n4/2022-07-golom-findings/issues/357
- **Contest**: https://code4rena.com/contests/2022-07-golom-contest

### Keywords for Search

`vulnerability`

