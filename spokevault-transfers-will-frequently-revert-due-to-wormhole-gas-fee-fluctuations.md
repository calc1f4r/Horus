---
# Core Classification
protocol: M
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44292
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-11-26-cyfrin-m0-v2.0.md
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
  - Immeas
  - 0kage
---

## Vulnerability Title

SpokeVault transfers will frequently revert due to Wormhole gas fee fluctuations

### Overview


Summary:

The `SpokeVault.transferExcessM()` function in the Wormhole protocol has a bug that causes transactions to fail if the user sends an excess amount of ETH for gas fees. This is because the `SpokeVault` contract cannot receive ETH refunds. This creates a usability problem because gas fees can fluctuate between the time a user calculates the fee and when the transaction is actually executed. To fix this, the `SpokeVault.transferExcessM()` function should be updated to handle excess ETH refunds by adding a `payable receive()` function in `SpokeVault`. This bug has been fixed in the latest version of the protocol. 

### Original Finding Content

**Description:** The `SpokeVault.transferExcessM()` function forwards ETH to pay for Wormhole gas fees, but any excess ETH sent will cause the transaction to revert since `SpokeVault` lacks capability to receive ETH refunds. Current implementation only works if the user sends a fee that is exactly equal to the  wormhole gas fee at the time of transaction.

This creates a significant usability problem because Wormhole gas fees can fluctuate between the time a user calculates the fee off-chain and when their transaction is actually executed.

The following code in `ManagerBase::_prepareForTransfer` shows that any gas fee shortfall will revert the transaction. Also, any excess gas fee over and above the delivery fee is refunded back to the sender.

```solidity
// In ManagerBase.sol
function _prepareForTransfer(...) internal returns (...) {
    // ...
    if (msg.value < totalPriceQuote) {
        revert DeliveryPaymentTooLow(totalPriceQuote, msg.value);
    }

    uint256 excessValue = msg.value - totalPriceQuote;
    if (excessValue > 0) {
        _refundToSender(excessValue); // Reverts as SpokeVault can't accept ETH
    }
}

  function _refundToSender(
        uint256 refundAmount
    ) internal {
        // refund the price quote back to sender
        (bool refundSuccessful,) = payable(msg.sender).call{value: refundAmount}("");
         //@audit excess gas fee sent back to msg.sender (SpokeVault)

        // check success
        if (!refundSuccessful) {
            revert RefundFailed(refundAmount);
        }
    }
```


As a result, `transferExcessM` can only run if the user sends the exact fee. Doing so would be challenging because:

- Since this function can be called by anyone, it is likely that an average user would not know how to calculate the delivery fees
- Even if a user calculates the exact fee off-chain, it is highly likely that transaction fails due to natural gas fee fluctuation


**Impact:** If gas fee increases or decreases even slightly between quote and execution, transaction reverts.

**Proof of Concept**
Make following changes to `MockSpokePortal` and run the test below in `SpokeVault.t.sol`:

```solidity
      contract MockSpokePortal {
          address public immutable mToken;
          address public immutable registrar;

          constructor(address mToken_, address registrar_) {
              mToken = mToken_;
              registrar = registrar_;
          }

          function transfer(
              uint256 amount,
              uint16 recipientChain,
              bytes32 recipient,
              bytes32 refundAddress,
              bool shouldQueue,
              bytes memory transceiverInstructions
          ) external payable returns (uint64) {

              // mock return of excess fee back to sender
              if(msg.value > 1) {
                  payable(msg.sender).transfer(msg.value-1);
              }

          }
      }

   contract SpokeVaultTests is UnitTestBase {
        function testFail_transferExcessM() external { //@audits fails with excess fee
            uint256 amount_ = 1_000e6;
            uint256 balance_ = 10_000e6;
            uint256 fee_ = 2;
            _mToken.mint(address(_vault), balance_);
            vm.deal(_alice, fee_);

            vm.prank(_alice);
            _vault.transferExcessM{ value: fee_ }(amount_, _alice.toBytes32());
        }
   }

```

**Recommended Mitigation:** Wormhole has a specific provision to refund excess gas fee back to the sender. This is put in place to ensure reliability of transfers even with natural gas fee fluctuations.

Consider updating the `SpokeVault.transferExcessM()` function to handle excess ETH refunds by adding a `payable receive()` function in `SpokeVault`. Also, please make sure the logic forwards any received ETH back to the original caller - not doing so would result in the excess gas fee stuck inside `SpokeVault`.

**M0 Foundation**
Fixed in commit [78ac49b](https://github.com/m0-foundation/m-portal/commit/78ac49bba3ac294873a949eec00a5bfad8b41c34)

**Cyfrin**
Verified

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | M |
| Report Date | N/A |
| Finders | Immeas, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-11-26-cyfrin-m0-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

