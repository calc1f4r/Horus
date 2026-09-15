---
# Core Classification
protocol: Earnm Dropbox
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41181
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
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
  - Dacian
---

## Vulnerability Title

Use named imports instead of importing the entire namespace

### Overview

See description below for full details.

### Original Finding Content

**Description:** Use named imports as they offer a number of [advantages](https://ethereum.stackexchange.com/a/117173) compared to importing the entire namespace.

File: `DropBox.sol`
```solidity
// DropBoxFractalProtocol
import {DropBoxFractalProtocol} from "./DropBoxFractalProtocol.sol";

// VRF Handler Interface
import {IVRFHandler} from "./IVRFHandler.sol";
import {IVRFHandlerReceiver} from "./IVRFHandlerReceiver.sol";

// LimitBreak implementations of ERC721C and Programmable Royalties
import {OwnableBasic, OwnablePermissions} from "@limitbreak/creator-token-standards/src/access/OwnableBasic.sol";
import {ERC721C, ERC721OpenZeppelin} from "@limitbreak/creator-token-standards/src/erc721c/ERC721C.sol";
import {BasicRoyalties, ERC2981} from "@limitbreak/creator-token-standards/src/programmable-royalties/BasicRoyalties.sol";

// OpenZeppelin
import {ReentrancyGuard} from "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";
```

File: `VRFHandler.sol`
```solidity
// VRF Handler Interface
import {IVRFHandler} from "./IVRFHandler.sol";
import {IVRFHandlerReceiver} from "./IVRFHandlerReceiver.sol";

// Chainlink
import {VRFConsumerBaseV2Plus} from "@chainlink/contracts/src/v0.8/vrf/dev/VRFConsumerBaseV2Plus.sol";
import {IVRFCoordinatorV2Plus} from "@chainlink/contracts/src/v0.8/vrf/dev/interfaces/IVRFCoordinatorV2Plus.sol";
import {VRFV2PlusClient} from "@chainlink/contracts/src/v0.8/vrf/dev/libraries/VRFV2PlusClient.sol";
```

**Mode:**
Fixed in commit [9afe010](https://github.com/Earnft/dropbox-smart-contracts/commit/9afe0109afb01cd30f00393bf00f817c3a39a205).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Earnm Dropbox |
| Report Date | N/A |
| Finders | Dacian |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

