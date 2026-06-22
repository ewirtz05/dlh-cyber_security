#!/bin/bash
[ -f /etc/postfix/main.cf ] && grep -E '^[[:space:]]*smtpd_tls_security_level[[:space:]]*=' /etc/postfix/main.cf || echo "STARTTLS not configured"
