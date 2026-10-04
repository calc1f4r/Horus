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
solodit_id: 44291
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

Cross-chain token transfer from `SpokeVault` fails due to approval from implementation contract instead of proxy

### Overview


The bug report is about a contract called `SpokeVault` that holds excess M tokens and transfers them to a different contract called `HubVault`. The contract is set up with an infinite approval for the `SpokePortal` to transfer the tokens. However, the contract is deployed as a proxy, which means that the approval only applies to the original contract and not to the proxy. This means that the `SpokeVault` contract will not be able to transfer the tokens as intended, leaving them effectively stuck. A proof of concept has been provided to show how this can be fixed by setting token approvals only when needed and removing the approval from the constructor. The bug has been fixed in a recent commit and verified by a third party.

### Original Finding Content

**Description:** [`SpokeVault`](https://github.com/m0-foundation/m-portal/blob/8f909076f4fc1f22028cabd6df8a9e6b5be4b078/src/SpokeVault.sol) is a contract that holds excess M tokens from Smart M and can transfer this excess to `HubVault` on mainnet via [`SpokeVault::transferExcessM`](https://github.com/m0-foundation/m-portal/blob/8f909076f4fc1f22028cabd6df8a9e6b5be4b078/src/SpokeVault.sol#L69-L89).

To enable this, an infinite approval is set in the [`SpokeVault` constructor](https://github.com/m0-foundation/m-portal/blob/8f909076f4fc1f22028cabd6df8a9e6b5be4b078/src/SpokeVault.sol#L63-L64):
```solidity
// Approve the SpokePortal to transfer M tokens.
IERC20(mToken).approve(spokePortal_, type(uint256).max);
```

However, `SpokeVault` is deployed as a proxy, as seen in [`DeployBase::_deploySpokeVault`](https://github.com/m0-foundation/m-portal/blob/8f909076f4fc1f22028cabd6df8a9e6b5be4b078/script/deploy/DeployBase.sol#L221-L235):
```solidity
spokeVaultImplementation_ = address(
    new SpokeVault(spokePortal_, hubVault_, destinationChainId_, migrationAdmin_)
);

spokeVaultProxy_ = _deployCreate3Proxy(address(spokeVaultImplementation_), _computeSalt(deployer_, "Vault"));
```
Where [`_deployCreate3Proxy`](https://github.com/m0-foundation/m-portal/blob/8f909076f4fc1f22028cabd6df8a9e6b5be4b078/script/helpers/Utils.sol#L102-L108) deploys an `ERC1967Proxy`.

As a result, the approval set in the constructor applies only to the implementation contract, not to the proxy, which holds the tokens and initiates the transfers.

**Impact:** `SpokeVault::transferExcessM` will not function as intended because the `Portal` requires approval to transfer tokens. The M tokens in `SpokeVault` will be effectively stuck, though not permanently, as the contract is upgradeable.

**Proof of Concept:** Adding a token transfer in [`MockSpokePortal::transfer`](https://github.com/m0-foundation/m-portal/blob/8f909076f4fc1f22028cabd6df8a9e6b5be4b078/test/mocks/MockSpokePortal.sol#L14-L21) will cause [`SpokeVaultTests::test_transferExcessM`](https://github.com/m0-foundation/m-portal/blob/8f909076f4fc1f22028cabd6df8a9e6b5be4b078/test/unit/Spokevault.t.sol#L115-L138) to fail:
```diff
+import { IERC20 } from "../../lib/common/src/interfaces/IERC20.sol";
...
    function transfer(
        uint256 amount,
        uint16 recipientChain,
        bytes32 recipient,
        bytes32 refundAddress,
        bool shouldQueue,
        bytes memory transceiverInstructions
    ) external payable returns (uint64) {
+       IERC20(mToken).transferFrom(msg.sender, address(this), amount);
    }
```

**Recommended Mitigation:** Consider setting token approvals only as needed in `transferExcessM` and removing the approval from the constructor:
```diff
+ IERC20(mToken).approve(spokePortal_, amount_);
  messageSequence_ = INttManager(spokePortal).transfer{ value: msg.value }(
      amount_,
      destinationChainId,
      hubVault_,
      refundAddress_,
      false,
      new bytes(1)
   );
```
In addition, this approach eliminates the infinite approval to an upgradeable contract, enhancing security.

**M0 Foundation**
Fixed in commit [78ac49b](https://github.com/m0-foundation/m-portal/commit/78ac49bba3ac294873a949eec00a5bfad8b41c34)

**Cyfrin**
Verified

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

