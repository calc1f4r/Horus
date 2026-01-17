---
# Core Classification
protocol: Colbfinance Vault Extended
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63356
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/ColbFinance-Vault-Extended-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[L-03] Operator Has Full Control Over Mint vs. Reimburse - Relying Entirely on Ratio Bounds

### Overview

See description below for full details.

### Original Finding Content


## Severity

Low Risk

## Description

The `processDeposit()` function allows the operator to manually input both `amountMinted` and `amountReimbursed` for a deposit. While ratio bounds (`minRatio` and `maxRatio`) are enforced, the contract does not check that the sum of `amountMinted + amountReimbursed` matches the original deposit amount.

This opens the door for value mismatches where:

- Some deposit value remains unaccounted (ghost value).
- The user receives fewer tokens than expected.

## Location of Affected Code:

File: [contracts/vault/Vault.sol#L411](https://github.com/COLB-DEV/SmartContracts/blob/d569a17dfdf96fc029d2664beafa3dd1a54495fc/contracts/vault/Vault.sol#L411)

```solidity
function processDeposit(
    uint256 processIndex,
    uint256 amountMinted,
    uint256 amountReimbursed
) external onlyRole(factory.OPERATOR_ROLE()) whenNotPaused {
    if (block.timestamp <= investmentEnd)
        revert InvestmentPeriodNotFinish();
    // If we process during a batch, the calculations would be incorrect
    if (inBatchProcess) revert BatchNotFinished();

    uint256 indexDeposit = depositToProcess[processIndex];
    DepositInfo storage deposit = deposits[indexDeposit];
    uint256 amountDeposited = deposit.amount;

    // ratio calculation prevents errors in share distribution
    uint256 currentRatio = (amountMinted * BASE_RATIO) / amountDeposited;

    if (currentRatio < minRatio) revert UnderflowRatio();
    if (currentRatio > maxRatio) revert OverflowRatio();

    _mint(address(this), amountMinted);
    _processDeposit(indexDeposit, amountMinted, amountReimbursed);
    _removeAtIndex(depositToProcess, processIndex);
}
```

## Recommendation

Enforce a value-preserving invariant:

```solidity
require(amountMinted + amountReimbursed == deposit.amount, "Value mismatch");
```

## Team Response

Acknowledged.

## [I-01] Missing Validation on `investmentEnd()` in `VaultFactory` Allows Dead-On-Arrival Vaults

## Severity

Informational Risk

## Description

The `deploy()` function in `VaultFactory` accepts `investmentEnd` as a constructor argument:

```solidity
function deploy(
    // code
    uint256 investmentEnd
) external onlyRole(OPERATOR_ROLE) returns (address)
```

However, there is no check that `investmentEnd > block.timestamp`.

This allows possible misconfiguration and creation of vaults where **the investment period has already ended**, making them:

- Unusable on deployment
- Unavailable for deposits or withdrawals
- Requiring manual remediation

## Location of Affected Code

File: [contracts/vault/VaultFactory.sol#L151](https://github.com/COLB-DEV/SmartContracts/blob/d569a17dfdf96fc029d2664beafa3dd1a54495fc/contracts/vault/VaultFactory.sol#L151)

```solidity
function deploy(
    string calldata name,
    string calldata symbol,
    address token,
    uint256 minDepositByUser,
    uint256 minTotalDeposit,
    uint256 maxDepositByUser,
    uint256 maxTotalDeposit,
    uint256 investmentEnd
) external onlyRole(OPERATOR_ROLE) returns (address) {
    if (!allowedTokens[token]) revert InvalidConfiguration();

    // create data to call initialize method
    bytes memory data = abi.encodeCall(
        IVault.initialize,
        (
            name,
            symbol,
            whitelist,
            token,
            minDepositByUser,
            minTotalDeposit,
            maxDepositByUser,
            maxTotalDeposit,
            investmentEnd
        )
    );

    // use beacon proxy and not clone to deploy a vault
    BeaconProxy newVault = new BeaconProxy(address(vaultBeaconProxy), data);

    uint256 _vaultId = vaultId;

    vaults[_vaultId] = address(newVault);
    isVault[address(newVault)] = true;
    vaultId++;

    emit VaultDeployed(msg.sender, address(newVault), vaultId);

    return address(newVault);
}
```

## Recommendation

Add a simple validation check to ensure the investment period is in the future:

```solidity
if (investmentEnd <= block.timestamp) revert InvalidConfiguration();
```

## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Colbfinance Vault Extended |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/ColbFinance-Vault-Extended-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

