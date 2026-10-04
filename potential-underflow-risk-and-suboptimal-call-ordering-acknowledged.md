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
solodit_id: 55389
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2025/04/usdi/
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
  -  Vladislav Yaroshuk
                        
---

## Vulnerability Title

Potential Underflow Risk and Suboptimal Call Ordering  Acknowledged

### Overview

See description below for full details.

### Original Finding Content

...

Export to GitHub ...

Set external GitHub Repo ...

Export to Clipboard (json)

Export to Clipboard (text)

#### Resolution

The USDi team acknowledged this and plans to address in future versions.

#### Description

The `deposit` and `withdraw` functions calculate a `fee` based on the deposit or withdrawal `amount` and then subtract this `fee` to determine the net amount used for minting or burning. However, if the `amount` is less than the `minimumFee`, the subtraction may underflow and revert with a panic error before any validations are reached. Additionally, the token transfer is executed before fee calculation, which can lead to suboptimal error handling and unnecessary gas consumption in failing transactions.

The code structure would be improved by removing the early `require(amount > 0)` validation and instead performing the fee calculation first, followed by a check such as `require(netAmount > 0)`. This would preserve the original intention while improving gas efficiency and clarity. In any case, the `amount` must still be greater than `0` for minting or burning to succeed.

Moreover, the contract does not verify whether sufficient backing funds have been injected by the admin before allowing deposits. This implicitly relies on user trust that the protocol is adequately funded. Failing to verify this could result in users depositing funds into an under-collateralized system, potentially affecting their ability to redeem in the future.

#### Examples

**contracts/USDiCoin.sol:L436-L502**

```
/// @notice Allows a user to deposit backing tokens and mint USDi adjusted by CPI
/// Fees are deducted if and only if the deposit succeeds. If anything fails, no fees are collected.
function deposit(uint256 amount) external nonReentrant whenNotPaused {
    _requireWhitelisted(msg.sender);
    // Check if the backing token remains in the accepted peg range around $1
    _requireBackingTokenPegInRange();

    require(amount > 0, "Amount must be greater than 0");

    // Transfer entire deposit in one call
    backingToken.safeTransferFrom(msg.sender, address(this), amount);

    // Compute fee, ensure min
    uint256 fee = getFee(amount, true);
    if (fee < minimumFee) {
        fee = minimumFee;
    }
    // The net portion used for minting
    uint256 netAmount = amount - fee;
    require(netAmount > 0, "Fee exceeds deposit");

    // Calculate minted amount from net deposit
    uint256 currentCPI = getProratedCPI();
    uint256 adjustedAmount = (netAmount * startingCPI) / currentCPI;

    // Mint the tokens to the user
    _mint(msg.sender, adjustedAmount);

    // Transfer fee to the treasury
    backingToken.safeTransfer(treasury, fee);

    emit Deposit(msg.sender, amount, fee);
}

/// @notice Allows a user to burn USDi and withdraw backing tokens adjusted by CPI
/// Fees are deducted if and only if the withdrawal succeeds. If anything fails, no fees are collected.
function withdraw(uint256 amount) external nonReentrant whenNotPaused {
    _requireWhitelisted(msg.sender);
    _requireBackingTokenPegInRange();

    require(amount > 0, "Amount must be greater than 0");
    require(balanceOf(msg.sender) >= amount, "Insufficient balance");

    // Compute fee, ensure min
    uint256 fee = getFee(amount, false);
    if (fee < minimumFee) {
        fee = minimumFee;
    }
    uint256 netAmount = amount - fee;
    require(netAmount > 0, "Fee exceeds withdrawal");

    // Calculate how many backing tokens the user receives
    uint256 currentCPI = getProratedCPI();
    uint256 backingAmount = (netAmount * currentCPI) / startingCPI;

    // Burn user's USDi
    _burn(msg.sender, amount);

    // Transfer net backing to user
    backingToken.safeTransfer(msg.sender, backingAmount);

    // Transfer fee to treasury
    backingToken.safeTransfer(treasury, fee);

    lastWithdrawTime[msg.sender] = block.timestamp;
    emit Withdrawal(msg.sender, backingAmount, fee);
}

```

#### Recommendation

We recommend reordering the logic so that fee calculations and validations occur before any token transfers are executed. Additionally, we recommend adding a check to verify that sufficient backing funds have been injected into the contract before allowing deposits. This ensures a more robust and user-safe experience while maintaining proper economic guarantees.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

