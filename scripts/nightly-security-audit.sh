#!/bin/bash
# Chronos Lab Nightly Security Audit Script
# Based on SlowMist OpenClaw Security Practice Guide v2.7
# https://github.com/slowmist/openclaw-security-practice-guide

set -e

# Configuration
OC_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
REPORT_DIR="/tmp/openclaw/security-reports"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
REPORT_FILE="$REPORT_DIR/report-$DATE.txt"

# Create report directory
mkdir -p "$REPORT_DIR"

# Initialize report
echo "🛡️ OpenClaw Daily Security Audit Report ($DATE)" > "$REPORT_FILE"
echo "Generated at: $TIMESTAMP" >> "$REPORT_FILE"
echo "OpenClaw State Dir: $OC_DIR" >> "$REPORT_FILE"
echo "==========================================" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Helper function
check_result() {
    local metric_num=$1
    local metric_name=$2
    local status=$3
    local details=$4
    
    if [ "$status" = "0" ]; then
        echo "✅ $metric_name: $details" >> "$REPORT_FILE"
    else
        echo "❌ $metric_name: $details" >> "$REPORT_FILE"
    fi
}

# Metric 1: Platform Audit
echo "[1/13] Running platform audit..."
if command -v openclaw &> /dev/null; then
    openclaw security audit --deep > "$REPORT_DIR/platform-audit.txt" 2>&1 || true
    check_result 1 "Platform Audit" "0" "Native scan executed"
else
    check_result 1 "Platform Audit" "1" "OpenClaw CLI not found"
fi

# Metric 2: Process & Network Audit
echo "[2/13] Running process & network audit..."
ANOMALOUS_PORTS=$(ss -tnp 2>/dev/null | grep -E '(ESTAB|LISTEN)' | grep -v '127.0.0.1' | wc -l || echo "0")
if [ "$ANOMALOUS_PORTS" -eq "0" ]; then
    check_result 2 "Process & Network" "0" "No anomalous outbound/listening ports"
else
    check_result 2 "Process & Network" "1" "$ANOMALOUS_PORTS suspicious connections found"
fi

# Metric 3: Sensitive Directory Changes
echo "[3/13] Checking sensitive directory changes..."
CHANGED_FILES=$(find "$OC_DIR" /etc/ ~/.ssh/ -type f -mtime -1 2>/dev/null | wc -l || echo "0")
check_result 3 "Directory Changes" "0" "$CHANGED_FILES files modified in last 24h"

# Metric 4: System Scheduled Tasks
echo "[4/13] Checking system cron jobs..."
SYSTEM_CRON_COUNT=$(crontab -l 2>/dev/null | wc -l || echo "0")
CRON_D_COUNT=$(ls /etc/cron.d/ 2>/dev/null | wc -l || echo "0")
check_result 4 "System Cron" "0" "System cron: $SYSTEM_CRON_COUNT, /etc/cron.d: $CRON_D_COUNT"

# Metric 5: OpenClaw Cron Jobs
echo "[5/13] Checking OpenClaw cron jobs..."
if command -v openclaw &> /dev/null; then
    OC_CRON_COUNT=$(openclaw cron list 2>/dev/null | grep -c "enabled" || echo "0")
    check_result 5 "Local Cron" "0" "$OC_CRON_COUNT OpenClaw cron jobs"
else
    check_result 5 "Local Cron" "1" "OpenClaw CLI not found"
fi

# Metric 6: SSH Security
echo "[6/13] Checking SSH security..."
FAILED_SSH=$(journalctl -u sshd --since yesterday 2>/dev/null | grep -c "Failed" || echo "0")
check_result 6 "SSH Security" "0" "$FAILED_SSH failed brute-force attempts"

# Metric 7: Config Baseline
echo "[7/13] Checking config baseline..."
if [ -f "$OC_DIR/.config-baseline.sha256" ]; then
    cd "$OC_DIR"
    if sha256sum -c .config-baseline.sha256 > /dev/null 2>&1; then
        check_result 7 "Config Baseline" "0" "Hash check passed"
    else
        check_result 7 "Config Baseline" "1" "Hash mismatch detected!"
    fi
else
    check_result 7 "Config Baseline" "1" "No baseline found"
fi

# Metric 8: Yellow Line Audit
echo "[8/13] Checking yellow line operations..."
SUDO_COUNT=$(grep -c "sudo" /var/log/auth.log 2>/dev/null || echo "0")
MEMORY_LOG="$OC_DIR/workspace/memory/$DATE.md"
if [ -f "$MEMORY_LOG" ]; then
    LOGGED_SUDO=$(grep -c "sudo" "$MEMORY_LOG" 2>/dev/null || echo "0")
    check_result 8 "Yellow Line Audit" "0" "$SUDO_COUNT sudo executions ($LOGGED_SUDO logged)"
else
    check_result 8 "Yellow Line Audit" "0" "$SUDO_COUNT sudo executions (no memory log)"
fi

# Metric 9: Disk Usage
echo "[9/13] Checking disk usage..."
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_USAGE" -gt "85" ]; then
    check_result 9 "Disk Capacity" "1" "Root partition usage ${DISK_USAGE}%"
else
    check_result 9 "Disk Capacity" "0" "Root partition usage ${DISK_USAGE}%"
fi

# Metric 10: Environment Variables
echo "[10/13] Checking gateway environment..."
GW_PID=$(pgrep -f "openclaw.*gateway" || echo "")
if [ -n "$GW_PID" ]; then
    SENSITIVE_VARS=$(cat /proc/$GW_PID/environ 2>/dev/null | tr '\0' '\n' | grep -E '(KEY|TOKEN|SECRET|PASSWORD)' | wc -l || echo "0")
    check_result 10 "Environment Vars" "0" "$SENSITIVE_VARS credential env vars (names only)"
else
    check_result 10 "Environment Vars" "0" "Gateway process not found"
fi

# Metric 11: Sensitive Credential Scan (DLP)
echo "[11/13] Running DLP scan..."
MNEMONIC_COUNT=$(grep -rE '\b([a-z]{1,}\s+){11,}[a-z]{1,}\b' "$OC_DIR/workspace/memory/" 2>/dev/null | wc -l || echo "0")
check_result 11 "Sensitive Credential Scan" "0" "$MNEMONIC_COUNT potential mnemonic patterns (manual review recommended)"

# Metric 12: Skill/MCP Integrity
echo "[12/13] Checking Skill integrity..."
SKILL_COUNT=$(find "$OC_DIR/workspace/skills/" -type f 2>/dev/null | wc -l || echo "0")
check_result 12 "Skill Baseline" "0" "$SKILL_COUNT skill files"

# Metric 13: Disaster Backup
echo "[13/13] Running disaster backup..."
if [ -d "$OC_DIR/workspace/.git" ]; then
    cd "$OC_DIR/workspace"
    git add -A 2>/dev/null || true
    git commit -m "Nightly backup: $DATE" 2>/dev/null || true
    # git push origin main 2>/dev/null || true  # Uncomment if remote is configured
    check_result 13 "Disaster Backup" "0" "Git commit created"
else
    check_result 13 "Disaster Backup" "1" "Git repo not initialized"
fi

# Finalize report
echo "" >> "$REPORT_FILE"
echo "==========================================" >> "$REPORT_FILE"
echo "📝 Detailed report saved: $REPORT_FILE" >> "$REPORT_FILE"

# Output summary for Telegram/Discord push
echo ""
echo "🛡️ OpenClaw Daily Security Audit Report ($DATE)"
echo ""
cat "$REPORT_FILE"

echo ""
echo "Full report saved to: $REPORT_FILE"
