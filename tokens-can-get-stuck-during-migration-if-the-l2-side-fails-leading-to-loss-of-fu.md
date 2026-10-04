---
# Core Classification
protocol: Beanstalk: The Finale
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36263
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clw9e11e4001gdv0iigjylx5n
source_link: none
github_link: https://github.com/Cyfrin/2024-05-beanstalk-the-finale

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - holydevoti0n
  - golanger85
---

## Vulnerability Title

Tokens can get stuck during migration if the L2 side fails leading to loss of funds

### Overview


This bug report discusses a potential issue with the migration process between two contracts, `BeanL1ReceiverFacet` and `BeanL2MigrationFacet`. If a transaction fails on the second contract, tokens can be permanently lost without any way to retrieve them. This can happen if the message sent from the first contract to the second fails or if there is not enough gas to complete the transaction. The impact of this bug is that users can lose their tokens and there is currently no way to recover them. The report recommends implementing a mechanism to retry failed transactions and track migration requests to prevent this issue.

### Original Finding Content

## Summary

During the mirgration process between `BeanL1ReceiverFacet` and `BeanL2MigrationFacet`, when transactions fail on the L2 side, tokens are forever burnt with no existing method to reclaw them.

## Vulnerability Details

The migration process involves two key contracts: `BeanL1ReceiverFacet` and `BeanL2MigrationFacet`. The process starts on L1 where tokens are burned, and a message is sent to L2 to mint the equivalent amount of tokens.

**Steps Involved:**

1. **Burning on L1:** The `BeanL2MigrationFacet` contract burns the tokens from the user's L1 balance.
2. **Message to L2:** The contract then sends a message to L2 using the `IL2Bridge` interface, instructing the L2 contract to mint the equivalent amount of tokens.

**Vulnerable Scenario:**

* If the message sent from L1 to L2 fails to execute successfully on L2 (e.g., due to contract limitations or gas issues), the tokens will have already been burned on L1, but the user will not receive the corresponding tokens on L2.
* Specifically, the `recieveL1Beans` function on L2 could revert due to various reasons such as exceeding the maximum migrated beans or other contract-specific checks.



```Solidity
function recieveL1Beans(address reciever, uint256 amount) external nonReentrant {
    require(
        msg.sender == address(BRIDGE) &&
        IL2Messenger(BRIDGE).xDomainMessageSender() == L1BEANSTALK
    );
    s.sys.migration.migratedL1Beans += amount;
    require(
        EXTERNAL_L1_BEANS >= s.sys.migration.migratedL1Beans,
        "L2Migration: exceeds maximum migrated"
    );
    C.bean().mint(reciever, amount);
}

```

```Solidity
function migrateL2Beans(
    address reciever,
    address L2Beanstalk,
    uint256 amount,
    uint32 gasLimit
) external nonReentrant {
    C.bean().burnFrom(msg.sender, amount);

    IL2Bridge(BRIDGE).sendMessage(
        L2Beanstalk,
        abi.encodeCall(IBeanL1RecieverFacet(L2Beanstalk).recieveL1Beans, (reciever, amount)),
        gasLimit
    );
}

```

## Impact

If a migration request causes the total migrated beans to exceed this limit, the `recieveL1Beans` function will revert with the error "L2Migration: exceeds maximum migrated". Additionally, if the specified gas limit (`gasLimit`) is too low, the transaction might run out of gas during execution on L2.

Users will permanently lose their tokens as they are burned on L1 but not minted on L2.

## Tools Used

Manual Review

## Recommendation

It is recommended to comprise a refund/reclaw mechanism for failed transactions on L2, so that tokens can be retrieved.

By implementing a retry mechanism and tracking migration requests, the potential issue of tokens getting stuck during the L1 to L2 migration can be mitigated. This approach ensures that users do not lose their tokens even if there are issues during the migration process.

```Solidity
function recieveL1Beans(address reciever, uint256 amount) external nonReentrant {
    require(
        msg.sender == address(BRIDGE) &&
        IL2Messenger(BRIDGE).xDomainMessageSender() == L1BEANSTALK
    );
    s.sys.migration.migratedL1Beans += amount;
    require(
        EXTERNAL_L1_BEANS >= s.sys.migration.migratedL1Beans,
        "L2Migration: exceeds maximum migrated"
    );
    C.bean().mint(reciever, amount);

    // Mark the migration as completed on L1
    bytes32 requestId = keccak256(abi.encodePacked(reciever, amount, block.timestamp));
    IL2Bridge(BRIDGE).sendMessage(
        L1Beanstalk,
        abi.encodeCall(BeanL2MigrationFacet(L1Beanstalk).markMigrationCompleted, (requestId)),
        gasLimit
    );
}

```

```Solidity
mapping(bytes32 => MigrationRequest) public migrationRequests;

struct MigrationRequest {
    address reciever;
    uint256 amount;
    uint256 timestamp;
    bool completed;
}

function migrateL2Beans(
    address reciever,
    address L2Beanstalk,
    uint256 amount,
    uint32 gasLimit
) external nonReentrant {
    C.bean().burnFrom(msg.sender, amount);

    bytes32 requestId = keccak256(abi.encodePacked(reciever, amount, block.timestamp));
    migrationRequests[requestId] = MigrationRequest(reciever, amount, block.timestamp, false);

    IL2Bridge(BRIDGE).sendMessage(
        L2Beanstalk,
        abi.encodeCall(IBeanL1RecieverFacet(L2Beanstalk).recieveL1Beans, (reciever, amount)),
        gasLimit
    );
}

function refundFailedMigration(bytes32 requestId) external {
    MigrationRequest storage request = migrationRequests[requestId];
    require(!request.completed, "Migration already completed");
    require(block.timestamp > request.timestamp + 1 days, "Migration still in process");

    C.bean().mint(request.reciever, request.amount);
    request.completed = true;
}

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beanstalk: The Finale |
| Report Date | N/A |
| Finders | holydevoti0n, golanger85 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-05-beanstalk-the-finale
- **Contest**: https://codehawks.cyfrin.io/c/clw9e11e4001gdv0iigjylx5n

### Keywords for Search

`vulnerability`

