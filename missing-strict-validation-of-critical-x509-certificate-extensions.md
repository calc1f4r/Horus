---
# Core Classification
protocol: Datachain LCP-zkDCAP
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58806
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/datachain-lcp-zk-dcap/15bac7cd-3b90-47c7-a25e-b0c3214c6630/index.html
source_link: https://certificate.quantstamp.com/full/datachain-lcp-zk-dcap/15bac7cd-3b90-47c7-a25e-b0c3214c6630/index.html
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
finders_count: 3
finders:
  - Gereon Mendler
  - Mustafa Hasan
  - Andy Lin
---

## Vulnerability Title

Missing Strict Validation of Critical x.509 Certificate Extensions

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `80cc77a92d597d163621e887a01ecc599f41c259`.

**Update:** Fixed as recommended by introducing the `validate_cert_extensions()` function and applying it to the corresponding certificates.

**File(s) affected:**`crates/quote-verifier/src/pck.rs`, `crates/quote-verifier/src/tcb_info.rs`

**Description:** The current implementation of Intel SGX PCK certificate validation logic does not explicitly verify critical X.509 extensions such as `Key Usage` (OID: `2.5.29.15`) and `Basic Constraints` (OID: `2.5.29.19`). According to [RFC5280 section 4.2](https://datatracker.ietf.org/doc/html/rfc5280), a certificate-using system must reject a certificate if it encounters a critical extension it does not recognize or a critical extension that contains information it cannot process. According to the [Intel SGX PCK Certificate specification](https://api.trustedservices.intel.com/documents/Intel_SGX_PCK_Certificate_CRL_Spec-1.5.pdf), certificates have the following extensions marked as "critical":

*   **PCK Leaf Certificate**: `Key Usage` (`Digital Signature`, `Non Repudiation`), `Basic Constraints` (`CA:FALSE`).
*   **PCK Issuer CA Certificate**: `Key Usage` (`Certificate Sign`, `CRL Sign`), `Basic Constraints` (`CA:TRUE`, `pathlen:0`).
*   **Intel SGX Root CA Certificate**: `Key Usage` (`Certificate Sign`, `CRL Sign`), `Basic Constraints` (`CA:TRUE`, `pathlen:1`).
*   **TCB Singing Certificate**: `Key Usage` (`Digital Signature`, `Non Repudiation`), `Basic Constraints` (`CA:FALSE`).

Failing to enforce these validations may allow certificates with inappropriate key usage or incorrect CA constraints, weakening the trustworthiness of the certificate chain.

**Exploit Scenario:**

 An attacker obtains or generates a rogue certificate incorrectly marked with `CA:TRUE` or with inappropriate `Key Usage`. If the validation logic fails to explicitly check these critical attributes, the system might incorrectly accept this certificate, potentially allowing it to sign or validate unauthorized certificates or CRLs, undermining the entire trust model.

**Recommendation:** Verify the presence and correctness of critical `Key Usage` and `Basic Constraints` extensions in all certificates

1.   `pck.rs::validate_pck_cert()`: `pck_leaf_cert`, `pck_issuer_cert`, and `intel_sgx_root_cert`.
2.   `tcb_info.rs::validate_tcb_signing_certificate()`: `tcb_signing_cert`.

Here is a sample code:

```
fn validate_cert_extensions(cert: &X509Certificate, expected_ca: bool, expected_pathlen: Option<u8>, expected_ku: &[KeyUsage]) -> Result<()> {
    let mut ku_validated = false;
    let mut bc_validated = false;

    for ext in cert.extensions() {
        if ext.critical {
            match ext.parsed_extension() {
                ParsedExtension::KeyUsage(ku) => {
                    for usage in expected_ku {
                        if !ku.has(*usage) {
                            bail!("Certificate Key Usage mismatch: {:?}", usage);
                        }
                    }
                    ku_validated = true;
                }
                ParsedExtension::BasicConstraints(bc) => {
                    if bc.ca != expected_ca || bc.path_len_constraint != expected_pathlen {
                        bail!("Certificate Basic Constraints mismatch: ca={}, pathlen={:?}", expected_ca, expected_pathlen);
                    }
                    bc_validated = true;
                }
                _ => bail!("Unknown critical extension: {}", ext.oid),
            }
        }
    }

    if !ku_validated {
        bail!("Missing critical Key Usage extension");
    }
    if !bc_validated {
        bail!("Missing critical Basic Constraints extension");
    }
    Ok(())
}
```

```
pub fn validate_pck_cert<'a>(
    pck_leaf_cert: &X509Certificate<'a>,
    pck_issuer_cert: &X509Certificate<'a>,
    intel_sgx_root_cert: &X509Certificate<'_>,
    intel_crls: &IntelSgxCrls,
) -> Result<ValidityIntersection> {
    // ... existing code block ...

    // validate leaf cert extensions
    validate_cert_extensions(
        pck_leaf_cert,
        false,
        None,
        &[KeyUsage::DigitalSignature, KeyUsage::NonRepudiation],
    )
    .context("PCK Leaf cert extension validation failed")?;

    // validate issuer cert extensions
    validate_cert_extensions(
        pck_issuer_cert,
        true,
        Some(0),
        &[KeyUsage::KeyCertSign, KeyUsage::CRLSign],
    )
    .context("PCK Issuer cert extension validation failed")?;

    // validate root cert extensions
    validate_cert_extensions(
        intel_sgx_root_cert,
        true,
        Some(1),
        &[KeyUsage::KeyCertSign, KeyUsage::CRLSign],
    )
    .context("Intel SGX Root cert extension validation failed")?;

    // ... existing code block ...
}
```

```
pub fn validate_tcb_signing_certificate(
    tcb_signing_cert: &X509Certificate,
    intel_sgx_root_cert: &X509Certificate,
    intel_crls: &IntelSgxCrls,
) -> Result<ValidityIntersection> {

    // ... existing code block ...

    // Explicitly validate critical X509 extensions according to Intel SGX specification
    validate_cert_extensions(
        tcb_signing_cert,
        false,                   // CA must be false
        None,                    // pathlen must be absent
        &[KeyUsage::DigitalSignature, KeyUsage::NonRepudiation], // Key usage exactly as specified
    )
    .context("TCB Signing cert extension validation failed")?;

    // ... existing code block ...
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Datachain LCP-zkDCAP |
| Report Date | N/A |
| Finders | Gereon Mendler, Mustafa Hasan, Andy Lin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/datachain-lcp-zk-dcap/15bac7cd-3b90-47c7-a25e-b0c3214c6630/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/datachain-lcp-zk-dcap/15bac7cd-3b90-47c7-a25e-b0c3214c6630/index.html

### Keywords for Search

`vulnerability`

