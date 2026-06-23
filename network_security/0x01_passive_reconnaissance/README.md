# Passive Reconnaissance

This directory contains basic passive reconnaissance scripts used to collect public information without directly interacting with the target system aggressively.

## Files

### 0-whois.sh

Extracts selected WHOIS information for `holbertonschool.com` and formats the output as CSV.

The script collects:

- Registrant Information
- Admin Information
- Tech Information

Each line is formatted as:

```text
Field,Value
