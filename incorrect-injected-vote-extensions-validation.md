---
# Core Classification
protocol: Ethos Cosmos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47220
audit_firm: OtterSec
contest_link: https://www.ethosstake.com/
source_link: https://www.ethosstake.com/
github_link: https://github.com/Ethos-Works/ethos

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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Naoya Okanami
  - First Last
---

## Vulnerability Title

Incorrect Injected Vote Extensions Validation

### Overview


The bug report is about a function called ValidateVoteExtensions that relies on data injected by the proposer, which can be manipulated to misrepresent the voting power of validators. This can lead to incorrect consensus decisions and compromised voting process. The report recommends applying a patch to fix the issue.

### Original Finding Content

## ValidateVoteExtensions Vulnerability

ValidateVoteExtensions relies on proposer-injected VoteExtension data, which may be manipulated to misrepresent the voting power of validators. The function calculates the total voting power (`totalVP`) based on this injected data. A malicious proposer could distort this calculation by either including only their own vote extension or altering the voting power values, thereby skewing the total voting power.

## Code Snippet

```go
// Sample code for ValidateVoteExtensions function
func ValidateVoteExtensions(
[...]
) error {
    cp := ctx.ConsensusParams()
    // Start checking vote extensions only **after** the vote extensions enable height,
    // because when `currentHeight == VoteExtensionsEnableHeight`
    // PrepareProposal doesn't get any vote extensions in its request.
    extsEnabled := cp.Abci != nil && currentHeight > cp.Abci.VoteExtensionsEnableHeight &&
    cp.Abci.VoteExtensionsEnableHeight != 0

    marshalDelimitedFn := func(msg proto.Message) ([]byte, error) {
        var buf bytes.Buffer
        if err := protoio.NewDelimitedWriter(&buf).WriteMsg(msg); err != nil {
            return nil, err
        }
        return buf.Bytes(), nil
    }

    var (
        // Total voting power of all vote extensions.
        totalVP int64
        // Total voting power of all validators that submitted valid vote extensions.
        sumVP int64
    )
    [...]
}
```

Manipulated vote extensions may result in incorrect consensus decisions; consequently, the state machine may accept invalid blocks or reject valid ones. The proposer may craft vote extensions to prevent reaching the required voting power, resulting in delays or halts in the blockchain’s operation. Compromised vote extension validation will undermine the integrity of the entire voting process.

## Remediation

Apply the patch for the `ValidateVoteExtensions` issue.

---

© 2024 Otter Audits LLC. All Rights Reserved. 6/15  
Ethos Cosmos Audit 04 — Vulnerabilities  
Patch: Fixed in 646cd54.  
© 2024 Otter Audits LLC. All Rights Reserved. 7/15

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Ethos Cosmos |
| Report Date | N/A |
| Finders | Naoya Okanami, First Last |

### Source Links

- **Source**: https://www.ethosstake.com/
- **GitHub**: https://github.com/Ethos-Works/ethos
- **Contest**: https://www.ethosstake.com/

### Keywords for Search

`vulnerability`

