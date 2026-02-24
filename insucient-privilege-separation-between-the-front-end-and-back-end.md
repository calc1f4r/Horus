---
# Core Classification
protocol: Subspace Network, Subspace Desktop
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17473
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-subspacenetwork-subspacenetworkdesktopfarmer-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-subspacenetwork-subspacenetworkdesktopfarmer-securityreview.pdf
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
  - Artur Cygan
  - Vasco Franco
---

## Vulnerability Title

Insu�cient privilege separation between the front end and back end

### Overview


The Subspace Desktop application is vulnerable to privilege escalation attacks. This means that malicious front end code could gain the ability to execute code when the user opens a shell, or read a user's GitHub private key stored in ~/.ssh and steal all of the user's private repositories. Tauri was designed to provide a defense-in-depth mechanism to prevent a complete system compromise if an attacker finds and exploits an XSS or open redirect vulnerability. To take advantage of this, the front end should invoke the Rust back end when performing any privileged operations. 

An attacker could find an XSS vulnerability in the front end and use it to list all of a user's directories and leak the user's private keys in ~/.ssh and the user's farmer signing key. They could then use the private keys to extract private repositories from the user's GitHub account. 

To prevent this, the Tauri should be configured to disallow the front end from reading arbitrary files, writing to files, executing shell commands, and performing any other privileged operations. Instead, the privileged operations should be implemented in the Rust back end and exposed as commands that can be invoked by the front end. On the back end, code should be added to validate the commands' inputs to prevent a malicious front end from elevating its privileges.

### Original Finding Content

## Subspace Network Security Assessment

**Difficulty:** High  
**Type:** Patching  
**Target:** The Subspace Desktop architecture  

## Description
The Subspace Desktop application’s JavaScript front end can perform many privileged operations, allowing it to elevate its privileges. For example, in Linux, a malicious front end could write to a user’s `.bashrc` file and gain the ability to execute code when the user opens a shell; a malicious front end could also read a user’s GitHub private key stored in `~/.ssh` and steal all of the user’s private repositories.

Although the desktop application has a small attack surface for XSS attacks, this architecture does not provide a defense-in-depth mechanism to prevent a complete system compromise if an attacker finds and exploits an XSS or open redirect vulnerability. Tauri was explicitly designed with this defense-in-depth mechanism in mind. The Rust back end runs the privileged operations (e.g., writing files to disk, creating connections to databases), and the front end provides the UI without needing to call any privileged operations directly. Read [Tauri's introduction](https://tauri.studio/docs/getting-started/intro) and [process model](https://tauri.studio/docs/writing/architecture) for more information about Tauri's philosophy.

To take advantage of this Tauri defense-in-depth mechanism, we recommend having the front end invoke the Rust back end when performing any privileged operations, such as writing to configuration files, writing to autostart files, running shell commands, and opening files with the system’s default application.

## Exploit Scenario
An attacker finds an XSS vulnerability in the front end. She lists all of a user’s directories and leaks the user’s private keys in `~/.ssh/` and the user’s farmer signing key. She uses the private keys in `~/.ssh/` to extract private repositories from the user’s GitHub account.

## Recommendations
Short term, configure Tauri to disallow the front end from reading arbitrary files, writing to files, executing shell commands, and performing any other privileged operations. Instead, implement all of these privileged operations in the Rust back end and expose them as commands that can be invoked by the front end. On the back end, add code to validate the commands’ inputs to prevent a malicious front end from elevating its privileges.

---

**Trail of Bits**  
**Subspace Network Security Assessment - PUBLIC**

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Subspace Network, Subspace Desktop |
| Report Date | N/A |
| Finders | Artur Cygan, Vasco Franco |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-subspacenetwork-subspacenetworkdesktopfarmer-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-subspacenetwork-subspacenetworkdesktopfarmer-securityreview.pdf

### Keywords for Search

`vulnerability`

