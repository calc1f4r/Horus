---
# Core Classification
protocol: Linea - Burn Mechanism
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63337
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2025/10/linea-burn-mechanism/
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
  - Arturo Roura
  -  Martin Ortner
                        
---

## Vulnerability Title

RollupRevenueVault - Missing Validation for Future lastInvoiceDate ✓ Fixed

### Overview

See description below for full details.

### Original Finding Content

...

Export to GitHub ...

Set external GitHub Repo ...

Export to Clipboard (json)

Export to Clipboard (text)

#### Resolution

Fixed in commit [bd2f0b28f59601d40d4ab63243632ccc16d9cf8a](https://github.com/Consensys/linea-monorepo/pull/1600/commits/bd2f0b28f59601d40d4ab63243632ccc16d9cf8a). The Linea team added `require(_lastInvoiceDate < block.timestamp, TimestampInTheFutureNotAllowed());` on reinitialization, invoice submission and when updating invoice arrears.

#### Description

The contract does not enforce validation to prevent `lastInvoiceDate` from being set to a future timestamp. This can permanently block invoice submissions, affecting normal invoice operations, potentially resulting in a denial of service until manual intervention occurs.

#### Examples

Several functions allow `lastInvoiceDate` to be set to future values without proper checks:

Invoice Submissions:

**contracts/src/operational/RollupRevenueVault.sol:L162-L184**

```
/**
 * @notice Submit invoice to pay to the designated receiver.
 * @param _startTimestamp Start of the period the invoice is covering.
 * @param _endTimestamp End of the period the invoice is covering.
 * @param _invoiceAmount New invoice amount.
 */
function submitInvoice(
  uint256 _startTimestamp,
  uint256 _endTimestamp,
  uint256 _invoiceAmount
) external payable onlyRole(INVOICE_SUBMITTER_ROLE) {
  require(_startTimestamp == lastInvoiceDate + 1, TimestampsNotInSequence());
  require(_endTimestamp > _startTimestamp, EndTimestampMustBeGreaterThanStartTimestamp());
  require(_invoiceAmount != 0, ZeroInvoiceAmount());

  address payable receiver = payable(invoicePaymentReceiver);
  uint256 balanceAvailable = address(this).balance;

  uint256 totalAmountOwing = invoiceArrears + _invoiceAmount;
  uint256 amountToPay = (balanceAvailable < totalAmountOwing) ? balanceAvailable : totalAmountOwing;

  invoiceArrears = totalAmountOwing - amountToPay;
  lastInvoiceDate = _endTimestamp;
```

If `lastInvoiceDate` is set to a future timestamp (e.g., year 2030), subsequent invoice submissions must have `_startTimestamp = lastInvoiceDate + 1`, effectively soft-locking the system until that future date is reached or forcing submissions to shift in the future. Setting this to `uint_MAX` will permanently prevent submissions until an admin resolves it.

Initialization:

**contracts/src/operational/RollupRevenueVault.sol:L125-L152**

```
function __RollupRevenueVault_init(
  uint256 _lastInvoiceDate,
  address _defaultAdmin,
  address _invoiceSubmitter,
  address _burner,
  address _invoicePaymentReceiver,
  address _tokenBridge,
  address _messageService,
  address _l1LineaTokenBurner,
  address _lineaToken,
  address _dex
) internal onlyInitializing {
  require(_lastInvoiceDate != 0, ZeroTimestampNotAllowed());
  require(_defaultAdmin != address(0), ZeroAddressNotAllowed());
  require(_invoiceSubmitter != address(0), ZeroAddressNotAllowed());
  require(_burner != address(0), ZeroAddressNotAllowed());
  require(_invoicePaymentReceiver != address(0), ZeroAddressNotAllowed());
  require(_tokenBridge != address(0), ZeroAddressNotAllowed());
  require(_messageService != address(0), ZeroAddressNotAllowed());
  require(_l1LineaTokenBurner != address(0), ZeroAddressNotAllowed());
  require(_lineaToken != address(0), ZeroAddressNotAllowed());
  require(_dex != address(0), ZeroAddressNotAllowed());

  _grantRole(DEFAULT_ADMIN_ROLE, _defaultAdmin);
  _grantRole(INVOICE_SUBMITTER_ROLE, _invoiceSubmitter);
  _grantRole(BURNER_ROLE, _burner);

  lastInvoiceDate = _lastInvoiceDate;
```

Admin Updates:

**contracts/src/operational/RollupRevenueVault.sol:L238-L252**

```
/**
 * @notice Update the invoice arrears.
 * @param _newInvoiceArrears New invoice arrears value.
 * @param _lastInvoiceDate Timestamp of the last invoice.
 */
function updateInvoiceArrears(
  uint256 _newInvoiceArrears,
  uint256 _lastInvoiceDate
) external onlyRole(DEFAULT_ADMIN_ROLE) {
  require(_lastInvoiceDate >= lastInvoiceDate, InvoiceDateTooOld());

  invoiceArrears = _newInvoiceArrears;
  lastInvoiceDate = _lastInvoiceDate;
  emit InvoiceArrearsUpdated(_newInvoiceArrears, _lastInvoiceDate);
}
```

Setter: Note - This allows the admin to skip settling existing debt.

**contracts/src/operational/RollupRevenueVault.sol:L238-L252**

```
/**
 * @notice Update the invoice arrears.
 * @param _newInvoiceArrears New invoice arrears value.
 * @param _lastInvoiceDate Timestamp of the last invoice.
 */
function updateInvoiceArrears(
  uint256 _newInvoiceArrears,
  uint256 _lastInvoiceDate
) external onlyRole(DEFAULT_ADMIN_ROLE) {
  require(_lastInvoiceDate >= lastInvoiceDate, InvoiceDateTooOld());

  invoiceArrears = _newInvoiceArrears;
  lastInvoiceDate = _lastInvoiceDate;
  emit InvoiceArrearsUpdated(_newInvoiceArrears, _lastInvoiceDate);
}
```

#### Recommendation

Implement timestamp validation in all relevant functions to prevent future dates.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Linea - Burn Mechanism |
| Report Date | N/A |
| Finders | Arturo Roura,  Martin Ortner
                         |

### Source Links

- **Source**: https://diligence.consensys.io/audits/2025/10/linea-burn-mechanism/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

