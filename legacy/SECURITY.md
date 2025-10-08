# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security bugs seriously. We appreciate your efforts to responsibly disclose your findings, and will make every effort to acknowledge your contributions.

### How to Report a Security Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **brieuc@bdelaf.com**

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information in your report:

* Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
* Full paths of source file(s) related to the manifestation of the issue
* The location of the affected source code (tag/branch/commit or direct URL)
* Any special configuration required to reproduce the issue
* Step-by-step instructions to reproduce the issue
* Proof-of-concept or exploit code (if possible)
* Impact of the issue, including how an attacker might exploit it

### What to Expect

After you submit a report, we will:

1. Confirm the receipt of your vulnerability report within 48 hours
2. Provide regular updates on our progress
3. Credit you in our security advisories (unless you prefer to remain anonymous)

### GIFT Framework Specific Considerations

When reporting security vulnerabilities in the GIFT framework, please consider:

* **Computational Security**: Issues related to numerical stability, precision errors, or computational exploits
* **Data Integrity**: Problems with validation results, prediction accuracy, or scientific reproducibility
* **Access Control**: Unauthorized access to research data or computational resources
* **Dependency Vulnerabilities**: Security issues in third-party libraries used by the framework

### Scope

This security policy applies to:

* The GIFT Core Framework (`final/GIFT_Core_Framework.ipynb`)
* Research Challenges modules (`GIFT_Research_Challenges/`)
* Validation and testing infrastructure
* Documentation and metadata files
* GitHub Actions workflows
* Dependencies listed in `requirements.txt`

### Out of Scope

The following are considered out of scope for security reporting:

* Issues in experimental or research code that is clearly marked as such
* Theoretical physics discussions or scientific disagreements
* Issues that require physical access to the system
* Social engineering attacks
* Denial of service attacks that don't compromise data integrity

## Security Best Practices

### For Contributors

* Keep dependencies up to date
* Use secure coding practices
* Validate all inputs, especially in computational modules
* Follow the principle of least privilege
* Document security considerations in code comments

### For Users

* Always use the latest stable version
* Verify checksums when downloading releases
* Run the framework in a secure environment
* Be cautious when sharing computational results
* Report any suspicious behavior immediately

## Acknowledgments

We would like to thank the following security researchers who have responsibly disclosed vulnerabilities:

* [List will be updated as reports are received]

## License

This security policy is provided under the same license as the GIFT framework (MIT License).
