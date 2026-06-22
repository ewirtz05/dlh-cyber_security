# Network Protocols

This directory contains scripts related to network protocol inspection and basic Linux security checks.

## Files

### `0-iptables.sh`

Displays all current `iptables` firewall rules in a readable format, including line numbers.

The script uses:

- `iptables -L` to list rules
- `-v` for verbose output
- `-n` to avoid DNS/name resolution
- `--line-numbers` to show rule numbers

## Usage

```bash
chmod +x 0-iptables.sh
sudo ./0-iptables.sh
