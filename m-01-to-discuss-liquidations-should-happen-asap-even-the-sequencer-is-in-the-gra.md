---
# Core Classification
protocol: Quill Finance Report
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53918
audit_firm: Recon Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-23-Quill_Finance_Report.md
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
  - Alex The Entreprenerd
---

## Vulnerability Title

[M-01] To Discuss - Liquidations should happen asap even the sequencer is in the grace period

### Overview


The report discusses potential issues with the liquidation process in a system called Scroll. The author believes that the current system may be unfair to users and could result in high costs or bad debt. They suggest implementing a grace period to allow users time to recapitalize in case of downtime or dropped transactions. The author believes that this change would protect the system and can be documented for transparency. 

### Original Finding Content

**Impact**

Liquidations are safer for the system

Liquidations could be extremely unfair to the user

I describe 2 scenarios that are extreme as a means to discuss both sides of the coin

**System Description**

At this time I believe that:
- Scroll has a centralized sequencer
- Scroll processes calls as FIFO (fair ordering from their POV)
- In the case of downtime, all txs will be dropped, and will have to be re-submitted
- Scroll uses EIP1559 to price it's blocks

Assuming this, the cost of a 15 minute DOS may be plausible (TODO)
Anything past 15 minutes will most likely cost millions of dollars, making it unlikely to be worth it unless Quill has a very high TVL


TO FINISH

**Unfair liquidation due to oracle not updating**

The scenario that waiting for the GracePeriod address is an unfair liquidation

Assuming a borrower had to be liquidated or they became liquidatable due to interesting during the Sequencer Downtime

However, per this logic we'd expect that it would be fair to liquidate them, this is due to their negligence and not any chain nor protocol downtime

**Lack of Oracle Update due to TX being dropped due to shutdown**

This is the wort case scenario from the above, if the Oracle update should have prevented the liquidation but didn't because it got dropped, then an argument could be made in favour of the Grace Period, as the Grace Period would grant them sufficient time to recapitalize

**Bad debt due to oracle updating**

This is the scenario we want to avoid

We had a user that was negligent, we couldn't liquidate them and the next oracle update will lock in bad debt to the protocol

This scenario is the tail risk the current code is taking, as you can have a liquidation that should happen, but couldn't and soon that liquidation will happen but the execution will be worse for the protocol

**Conclusion**

I believe either option has tradeoffs

My perspective is this won't happen with high likelihood

But if it will, it would be best to liquidate the user as to protect the protocol rather than risk locking in bad debt

I think the change is consistent in that way, and it can be flagged in the documentation

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Recon Audits |
| Protocol | Quill Finance Report |
| Report Date | N/A |
| Finders | Alex The Entreprenerd |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-23-Quill_Finance_Report.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

