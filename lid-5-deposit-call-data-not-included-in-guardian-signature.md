---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53470
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
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
  - Hexens
---

## Vulnerability Title

[LID-5] Deposit call data not included in guardian signature

### Overview


This bug report discusses a problem with the `depositBufferedEther` function in the `DepositSecurityModule.sol` contract. This function is used to deposit ETH to the deposit contract and create new nodes, but it requires a set of valid guardian signatures. However, the current implementation does not include the `depositCalldata` parameter in the signature, making it possible for a malicious user to manipulate the data and potentially cause issues with the staking module. The recommended solution is to include the hash of the parameter in the signature to prevent tampering. The report has been acknowledged by the team.

### Original Finding Content

**Severity:** Medium

**Path:** DepositSecurityModule.sol:depositBufferedEther#L413-L439

**Description:**

The function `depositBufferedEther` is used to make the Lido contract deposit ETH to the deposit contract and create new nodes. For this a set of valid guardian signatures is required.

However, the guardian signature only contains the block information, staking module ID, root and nonce. It does not include the parameter `depositCalldata`.

This parameter gets passed to Lido and there it gets passed to the Staking Router, which in turns passes it to the right staking module with `obtainDepositData(maxDepositsCount, _depositCalldata)` to obtain the public keys for the deposit contract.

Because the parameter is not part of the signature, it becomes possible for a malicious user to front-run the transaction and submit the signatures with arbitrary `depositCalldata`.

This can become a problem if the staking module uses this data to derive the public keys. However, `NodeOperatorRegistry.sol` currently ignores this parameter, only `ModuleSolo.sol` (mock contract) directly decodes the data into public keys.

```
function depositBufferedEther(
    uint256 blockNumber,
    bytes32 blockHash,
    bytes32 depositRoot,
    uint256 stakingModuleId,
    uint256 nonce,
    bytes calldata depositCalldata,
    Signature[] calldata sortedGuardianSignatures
) external validStakingModuleId(stakingModuleId) {
    if (quorum == 0 || sortedGuardianSignatures.length < quorum) revert DepositNoQuorum();

    bytes32 onchainDepositRoot = IDepositContract(DEPOSIT_CONTRACT).get_deposit_root();
    if (depositRoot != onchainDepositRoot) revert DepositRootChanged();

    if (!STAKING_ROUTER.getStakingModuleIsActive(stakingModuleId)) revert DepositInactiveModule();

    uint256 lastDepositBlock = STAKING_ROUTER.getStakingModuleLastDepositBlock(stakingModuleId);
    if (block.number - lastDepositBlock < minDepositBlockDistance) revert DepositTooFrequent();
    if (blockHash == bytes32(0) || blockhash(blockNumber) != blockHash) revert DepositUnexpectedBlockHash();

    uint256 onchainNonce = STAKING_ROUTER.getStakingModuleNonce(stakingModuleId);
    if (nonce != onchainNonce) revert DepositNonceChanged();

    _verifySignatures(depositRoot, blockNumber, blockHash, stakingModuleId, nonce, sortedGuardianSignatures);

    LIDO.deposit(maxDepositsPerBlock, stakingModuleId, depositCalldata);
}

function _verifySignatures(
    bytes32 depositRoot,
    uint256 blockNumber,
    bytes32 blockHash,
    uint256 stakingModuleId,
    uint256 nonce,
    Signature[] memory sigs
) internal view {
    bytes32 msgHash = keccak256(
        abi.encodePacked(ATTEST_MESSAGE_PREFIX, blockNumber, blockHash, depositRoot, stakingModuleId, nonce)
    );

    address prevSignerAddr = address(0);

    for (uint256 i = 0; i < sigs.length; ++i) {
        address signerAddr = ECDSA.recover(msgHash, sigs[i].r, sigs[i].vs);
        if (!_isGuardian(signerAddr)) revert InvalidSignature();
        if (signerAddr <= prevSignerAddr) revert SignatureNotSorted();
        prevSignerAddr = signerAddr;
    }
}
```


**Remediation:**  We would recommend to make the hash of the parameter (`keccak256(depositCalldata)`) part of the signature so it cannot be tampered with.

**Status:**  Acknowledged



- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

