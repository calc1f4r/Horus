---
# Core Classification
protocol: Boba 1 (Bridges and LP floating fee)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60702
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html
source_link: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html
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
finders_count: 5
finders:
  - Pavel Shabarkin
  - Ibrahim Abouzied
  - Andy Lin
  - Adrian Koegl
  - Valerian Callens
---

## Vulnerability Title

Stealing Liquidity Pool Fund with Reorg

### Overview


The report discusses a bug found in the Boba Network's code that could potentially lead to a 51% attack. This attack could allow a malicious user to manipulate the network and steal funds. The bug is related to a function called `_updateDepositHash()` which is used to protect against reorg-ed messages. However, the new `L1LiquidityPool.clientDepositL1Batch()` function does not call this function, leaving the network vulnerable. The report recommends calling the `_updateDepositHash()` function and increasing the confirmation time from 8 blocks to 64 blocks to improve network security. 

### Original Finding Content

**Update**
Regarding the confirmation time, we discussed with the team and they confirmed that they will update the confirmation time to 64 blocks in the future. However, they have had to delay the change because some UI/UX components are associated with it, and it might take some time to implement the change in practice.

![Image 51: Alert icon](blob:http://localhost/542c9b08ab7b8ff1c3683eefe75dc1a0)

**Update**
The team added the `_updateDepositHash()` call in the `clientDepositL1Batch()` functions in both `L1LiquidityPool` and `L1LiquidityPoolAltL1` contracts in the commit `d578b81f`.

**File(s) affected:**`LP/L1LiquidityPool.sol`, `LP/L2LiquidityPool.sol`

**Description:** The `_updateDepositHash()` is used to update the deposit-related data hashes to protect from relaying reorg-ed messages (see: `L1CrossDomainMessengerFast.relay()` function). The function is introduced as the fix for the QSP-1 in the previous audit (see: [report](https://github.com/bobanetwork/boba/blob/6fb695a61039c17741cfeaebc07e21f7cb938970/boba_audits/Boba%20Network%20-%20Final%20Report.pdf)). However, the new `L1LiquidityPool.clientDepositL1Batch()` function does not call the `_updateDepositHash()` function. This means it will not update the deposit hashes, and the reorg protection will be bypassed.

The reorg risk lowered as Ethereum moved to POS, and the network has a better-defined finality. With the current consensus, the chain is considered "finalized" after two epochs, which is 64 blocks. However, if the liquidity pool of Boba exceeds the stake for the consensus on Ethereum, it can still be beneficial for the attacker to conduct a 51% attack.

**Exploit Scenario:** Here is a potential scenario:

1.   Alice starts a 51% attack on L1. Let's say the canonical chain should be `chain1`, and Alice forked to `chain2` with a short period of 51% attack.
2.   Alice bridges ETH and Boba from L1 to L2 with `tx1` on `chain2` using `L1LiquidityPool.clientDepositL1Batch()` function.
3.   Alice immediately bridges Boba from L2 to L1, using the liquidity pool to withdraw quickly.
4.   The `L1LiquidityPool.clientPayL1()` transaction pays Alice the withdrawal fund in `tx2`.
5.   Alice cancels her 51% attack, and the longest chain becomes `chain1` again. However, `tx1` is no longer existing in `chain1`. However, `tx2` will still eventually be relayed. The validation in the `L1CrossDomainMessengerFast._verifyDepositHashes()` will not fail because the `tx1` does not change the deposit hash.

**Recommendation:** Call `_updateDepositHash()` once as part of the `L1LiquidityPool.clientDepositL1Batch()` function. Also, from the discussion with the Boba team, they only wait for 8 blocks of confirmation. We recommend increasing it to a minimum of 64 blocks to wait for the Ethereum finality.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Boba 1 (Bridges and LP floating fee) |
| Report Date | N/A |
| Finders | Pavel Shabarkin, Ibrahim Abouzied, Andy Lin, Adrian Koegl, Valerian Callens |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/boba-1-bridges-and-lp-floating-fee/1e5a1e09-bde0-417d-83cd-083234b1409c/index.html

### Keywords for Search

`vulnerability`

