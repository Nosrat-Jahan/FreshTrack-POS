# Security Policy | OS Scheduler Engine Pro

This document defines the security reporting protocols and maintenance standards for the **OS Scheduler Engine Pro**. As a BSc in CSE academic project, we prioritize system integrity and secure resource simulation.

## Supported Versions
Only the latest stable release is actively monitored for security patches.

| Version | Supported          |
| ------- | ------------------ |
| v6.6.6  | :white_check_mark: |
| < v6.0  | :x:                |

## Reporting a Vulnerability
If you identify any security flaw or logic-gate vulnerability within this simulator:
1. **Private Reporting**: Please do not open a public issue. Direct contact via GitHub profile or academic email is preferred.
2. **Investigation**: I will investigate the report within 48-72 hours.
3. **Resolution**: A security patch will be pushed to the `main` branch, followed by a public advisory.

## Security Architecture
- **Environment Isolation**: Recommended use of virtual environments (`venv`) to prevent dependency conflicts.
- **Input Sanitization**: Client-side and server-side validation of burst times and time quantum to prevent execution errors.

---
**Status:** Active Monitoring | **Dev:** Nosrat Jahan | **BSc in CSE Portfolio Project**
