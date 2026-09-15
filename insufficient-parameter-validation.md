---
# Core Classification
protocol: TokenOps 3 - Vesting/Disperse
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61759
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/token-ops-3-vesting-disperse/f3fff6c8-144d-4d7f-ad0b-24c9cdfaa33e/index.html
source_link: https://certificate.quantstamp.com/full/token-ops-3-vesting-disperse/f3fff6c8-144d-4d7f-ad0b-24c9cdfaa33e/index.html
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
  - István Böhm
  - Julio Aguilar
  - Cameron Biniamow
---

## Vulnerability Title

Insufficient Parameter Validation

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `e8df50f18f24a0081c03d8260c3e8bed0fb4523d`, `3d16f3eb73f76cfd9c0c8be858e72e66cdcc9034`. The client provided the following explanation:

> Added parameter validations and tests.

**File(s) affected:**`vesting-contracts-v3/contracts/TokenVestingManager.sol`, `vesting-contracts-v3/contracts/NativeTokenVestingManager.sol`, `vesting-contracts-v3/contracts/TokenVestingManagerVotes.sol`, `vesting-contracts-v3/contracts/VestedMilestoneManager.sol`, `tokenops-disperse-v2/contracts/DisperseTokenFee.sol`, `tokenops-disperse-v2/contracts/DisperseGasFee.sol`

**Description:** It is important to validate inputs, even if they only come from trusted addresses, to avoid human error. The following is a non-exhaustive list of missing input validations.

`TokenVestingManager`:

1.   Token `FEE` in the `constructor()` can be initialized to a value greater than `BASIS_POINTS` (`10_000`). Consider verifying that `fee_ <= BASIS_POINTS` if `feeType_ != ITypes.FeeType.Gas`.
2.   `feeCollector` in the `constructor()` can be initialized to `address(0)`. Consider verifying that `feeCollector_` is not `address(0)`.
3.   The `_from` and `_to` parameters in `getAllRecipientsSliced()` and `getAllRecipientVestingsSliced()` are not validated. Consider verifying that `_from < to && _to <= recipients.length`

`TokenVestingManagerVotes`:

1.   Token `FEE` in the `constructor()` can be initialized to a value greater than `BASIS_POINTS` (`10_000`). Consider verifying that `fee_ <= BASIS_POINTS` if `feeType_ != ITypes.FeeType.Gas`.
2.   `feeCollector` in the `constructor()` can be initialized to `address(0)`. Consider verifying that `feeCollector_` is not `address(0)`.
3.   The `_from` and `_to` parameters in `getAllRecipientsSliced()` and `getAllRecipientVestingsSliced()` are not validated. Consider verifying that `_from < to && _to <= recipients.length`.

`NativeTokenVestingManager`:

1.   The `_from` and `_to` parameters in `getAllRecipientsSliced()` and `getAllRecipientVestingsSliced()` are not validated. Consider verifying that `_from < to && _to <= recipients.length`.

`VestedMilestoneManager`:

1.   Token `FEE` in the `constructor()` can be initialized to a value greater than `BASIS_POINTS` (`10_000`). Consider verifying that `fee_ <= BASIS_POINTS` if `feeType_ != ITypes.FeeType.Gas`.
2.   The `_from` and `_to` parameters in `getAllRecipientsSliced()` are not validated. Consider verifying that `_from < to && _to <= recipients.length`.

`DisperseTokenFee`:

1.   `FEE` in `constructor()` can be initialized to a value greater than `BASIS_POINTS`. Consider verifying that `params.fee <= BASIS_POINTS`. 
2.   `feeCollector` in `constructor()` is not validated to be a non-zero address.

`DisperseGasFee`:

1.   `feeCollector` in `constructor()` is not validated to be a non-zero address.
2.   Array lengths are not checked in `disperseTokenSimple()`. Consider validating that array lengths are not `0`.

`Vault`:

1.   In the `constructor()`, validate that `token`, `beneficiary`, and `vestingManager` are not set as the zero address.

`DisperseFactory` and `FactoryFeeManager`:

1.   `defaultTokenFee` in `setDefaultTokenFee()` can be configured to a value greater than `BASIS_POINTS`. Consider verifying that `newTokenFee <= BASIS_POINTS`.
2.   `tokenFee` in `setCustomFee()` can be configured to a value greater than `BASIS_POINTS`. Consider verifying that `newFee <= BASIS_POINTS if feeType == ITypes.FeeType.DistributionToken`.

**Recommendation:** Consider implementing the above recommendations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | TokenOps 3 - Vesting/Disperse |
| Report Date | N/A |
| Finders | István Böhm, Julio Aguilar, Cameron Biniamow |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/token-ops-3-vesting-disperse/f3fff6c8-144d-4d7f-ad0b-24c9cdfaa33e/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/token-ops-3-vesting-disperse/f3fff6c8-144d-4d7f-ad0b-24c9cdfaa33e/index.html

### Keywords for Search

`vulnerability`

