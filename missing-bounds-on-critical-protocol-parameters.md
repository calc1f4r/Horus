---
# Core Classification
protocol: Sidekick Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52536
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/sidekick/sidekick-contracts
source_link: https://www.halborn.com/audits/sidekick/sidekick-contracts
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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Missing bounds on critical protocol parameters

### Overview

See description below for full details.

### Original Finding Content

##### Description

Throughout the files in scope, several critical admin-controlled parameters lack appropriate validation:

  

In `BoostSideKick` contract:

* The`sidekickPercentage` and `feePercent` >= 100% could take entire transaction amount or fail.
* The `changeSidekickWallet()` allows setting zero address.
* The `sidekickWallet` could be set to the zero address in the constructor.
* The `usdt` could be set to the zero address in the constructor.

  

In `Escrow` contract:

* The `feePercent` set in the constructor and `setFeePercent` lacks an upper bound (could be set > 100%).
* The `usdt` could be set to the zero address in the constructor.
* The `blocktime` set in the constructor and `setBlockTime` could be set to impractically high values.
* The `feeForGasUsdt` set in the constructor and `setfeeForGasUsdt` has no maximum limit.

  

In `SideKickTransfer` contract

* The `usdt` could be set to the zero address in the constructor.
* The `adminWallet` could be set to the zero address in the constructor.
* The `feePercentage` set in the constructor lacks an upper bound, and in `setFeePercentage` it could be set to 100%.

  

Misconfigured parameters could disrupt protocol economics and ultimately render the codebase unusable.

##### BVSS

[AO:S/AC:L/AX:L/R:N/S:U/C:C/A:C/I:C/D:C/Y:N (3.5)](/bvss?q=AO:S/AC:L/AX:L/R:N/S:U/C:C/A:C/I:C/D:C/Y:N)

##### Recommendation

Validate all constructor parameters, adding reasonable bounds for fees, block time bounds and zero-address checks.

##### Remediation

**RISK ACCEPTED:** The **SideKick team** made a business decision to accept the risk of this finding and not alter the contracts, stating:

*Agreed, but we believe that we can ignore this as it is low risk.*

##### References

[livegame-labs/sidekick-contracts/contracts/BoostSideKick.sol#L41-L44](https://github.com/livegame-labs/sidekick-contracts/blob/c116e404a03cb9240a4e8f48773bdfa81e2697e7/contracts/BoostSideKick.sol#L41-L44)

[livegame-labs/sidekick-contracts/contracts/BoostSideKick.sol#L129-L131](https://github.com/livegame-labs/sidekick-contracts/blob/c116e404a03cb9240a4e8f48773bdfa81e2697e7/contracts/BoostSideKick.sol#L129-L131)

[livegame-labs/sidekick-contracts/contracts/BoostSideKick.sol#L137-L139](https://github.com/livegame-labs/sidekick-contracts/blob/c116e404a03cb9240a4e8f48773bdfa81e2697e7/contracts/BoostSideKick.sol#L137-L139)

[livegame-labs/sidekick-contracts/contracts/Escrow.sol#L76-L91](https://github.com/livegame-labs/sidekick-contracts/blob/c116e404a03cb9240a4e8f48773bdfa81e2697e7/contracts/Escrow.sol#L76-L91)

[livegame-labs/sidekick-contracts/contracts/Escrow.sol#L266-L270](https://github.com/livegame-labs/sidekick-contracts/blob/c116e404a03cb9240a4e8f48773bdfa81e2697e7/contracts/Escrow.sol#L266-L270)

[livegame-labs/sidekick-contracts/contracts/Escrow.sol#L272-L278](https://github.com/livegame-labs/sidekick-contracts/blob/c116e404a03cb9240a4e8f48773bdfa81e2697e7/contracts/Escrow.sol#L272-L278)

[livegame-labs/sidekick-contracts/contracts/Escrow.sol#L280-L284](https://github.com/livegame-labs/sidekick-contracts/blob/c116e404a03cb9240a4e8f48773bdfa81e2697e7/contracts/Escrow.sol#L280-L284)

[livegame-labs/sidekick-contracts/contracts/SideKickTransfer.sol#L22](https://github.com/livegame-labs/sidekick-contracts/blob/c116e404a03cb9240a4e8f48773bdfa81e2697e7/contracts/SideKickTransfer.sol#L22)

<https://opbnbscan.com/address/0x411F7A163Ac543d203A2D3Dad0fAA801A226d119?tab=Contract&p=1 (Lines 647-650, 654)>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Sidekick Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/sidekick/sidekick-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/sidekick/sidekick-contracts

### Keywords for Search

`vulnerability`

