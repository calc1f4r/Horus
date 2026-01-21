---
# Core Classification
protocol: Orbit and Governance Upgrade Actions v2.1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41445
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-offchainlabs-orbit-actions-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-offchainlabs-orbit-actions-securityreview.pdf
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
finders_count: 1
finders:
  - Gustavo Grieco
---

## Vulnerability Title

Gnosis safe deployment allows users to disrupt governance action execution

### Overview


This report highlights a bug in the configuration of a smart contract that allows any user to block the usage of a Gnosis Safe deployment, causing potential issues with the governance action. The bug occurs due to the use of a deterministic deployment method, which requires a unique salt to avoid collisions. However, if the same salt is used as a previously deployed Gnosis Safe, the action will fail. The updated code includes a salt value to mitigate this issue, but it is still possible for an attacker to front-run the deployment, causing potential harm to the rollup. The report recommends carefully monitoring the blockchain during deployment and reviewing the security assumptions of third-party code used in governance actions.

### Original Finding Content

## Diﬃculty: High

## Type: Conﬁguration

### contracts/parent-chain/fast-confirm/EnableFastConfirmAction.sol

#### Description
Any user can accidentally or intentionally block the usage of a Gnosis safe deployment to set up a fast conﬁrmer committee as part of the governance action.

The fast conﬁrmer conﬁguration action deploys a Gnosis Safe multisig in order to implement a committee of validators to fast-conﬁrm a rollup state:

```solidity
function perform(IRollupAdmin rollup, address[] calldata fastConfirmCommittee) external {
    …
    address fastConfirmer =
    IGnosisSafeProxyFactory(GNOSIS_SAFE_PROXY_FACTORY).createProxyWithNonce(
        GNOSIS_SAFE_1_3_0,
        abi.encodeWithSignature(
            "setup(address[],uint256,address,bytes,address,address,uint256,address)",
            fastConfirmCommittee,
            fastConfirmCommittee.length,
            address(0),
            "",
            GNOSIS_COMPATIBILITY_FALLBACK_HANDLER,
            address(0),
            0,
            address(0)
        ),
        uint256(keccak256(abi.encodePacked(rollup)))
    );
    rollup.setAnyTrustFastConfirmer(fastConfirmer);
    address[] memory validators = new address[](1);
    validators[0] = fastConfirmer;
    bool[] memory val = new bool[](1);
    val[0] = true;
    rollup.setValidator(validators, val);
    rollup.setMinimumAssertionPeriod(1);
}
```
*Figure 1.1: Part of the perform function from the Enable Fast Conﬁrmation action.*

However, since the deployment is performed in a deterministic way using `create2` from a factory contract, the salt must be unique to avoid collisions. Using the same salt as the one from an already-deployed Gnosis Safe will cause this action to revert.

The updated version of the code includes a salt value that mitigates this issue:

```solidity
function perform(IRollupAdmin rollup, address[] calldata fastConfirmCommittee, uint256 salt) external {
    …
    address fastConfirmer =
    IGnosisSafeProxyFactory(GNOSIS_SAFE_PROXY_FACTORY).createProxyWithNonce(
        GNOSIS_SAFE_1_3_0,
        abi.encodeWithSignature(
            "setup(address[],uint256,address,bytes,address,address,uint256,address)",
            fastConfirmCommittee,
            fastConfirmCommittee.length,
            address(0),
            "",
            GNOSIS_COMPATIBILITY_FALLBACK_HANDLER,
            address(0),
            0,
            address(0)
        ),
        salt
    );
}
```
*Figure 1.2: Part of the perform function from the fast conﬁrmation action.*

However, we stress that this is only a mitigation, as front-running this transaction in certain chains like Ethereum mainnet is still feasible.

Additionally, in the `UpgradeAndEnableFastConfirmAction` action, the rollup owner must perform the deployment of the AnyTrustFast conﬁrmer:

```solidity
function perform() external {
    … 
    // Setup AnyTrustFastConfirmer
    require(
        IRollupAdminFC(rollupAddress).anyTrustFastConfirmer() == address(0),
        "UpgradeAndEnableFastConfirmAction: Fast confirm already enabled"
    );
    IRollupAdminFC(rollupAddress).setAnyTrustFastConfirmer(anyTrustFastConfirmer);
    require(
        IRollupAdminFC(rollupAddress).anyTrustFastConfirmer() == anyTrustFastConfirmer,
        "UpgradeAndEnableFastConfirmAction: Unexpected anyTrustFastConfirmer"
    );
    // Set AnyTrustFastConfirmer as validator
    address[] memory validators = new address[](1);
    validators[0] = anyTrustFastConfirmer;
    bool[] memory values = new bool[](1);
    values[0] = true;
    IRollupAdmin(rollupAddress).setValidator(validators, values);
    require(
        IRollupCore(rollupAddress).isValidator(anyTrustFastConfirmer),
        "UpgradeAndEnableFastConfirmAction: Failed to set validator"
    );
    // Set minimum assertion period
    IRollupAdmin(rollupAddress).setMinimumAssertionPeriod(newMinimumAssertionPeriod);
    require(
        IRollupCore(rollupAddress).minimumAssertionPeriod() == newMinimumAssertionPeriod,
        "UpgradeAndEnableFastConfirmAction: Failed to set minimum assertion period"
    );
}
```
*Figure 1.3: Part of the perform function from the fast conﬁrmation and upgrade action.*

Again, if the deployment uses Gnosis Safe multisig and an attacker is able to guess and front-run the deployment, the result could be catastrophic for the rollup.

### Exploit Scenario
A malicious user front-runs the creation of the Gnosis safe deployment, blocking the governance action until it is created again.

### Recommendations
- **Short term:** Carefully monitor the blockchain during the deployment and execution of this governance action to detect potential front-running attempts.
- **Long term:** Review the security assumptions and requirements for third-party code before using it in governance actions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Orbit and Governance Upgrade Actions v2.1 |
| Report Date | N/A |
| Finders | Gustavo Grieco |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-offchainlabs-orbit-actions-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-offchainlabs-orbit-actions-securityreview.pdf

### Keywords for Search

`vulnerability`

