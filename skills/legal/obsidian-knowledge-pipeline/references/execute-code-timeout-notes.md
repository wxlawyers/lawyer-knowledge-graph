# Execute Code Timeout Reference

## Observed Failure (2026-06-06)

**Scenario**: 6 `write_file` calls in one `execute_code` block
**Result**: Timeout at 304 seconds (limit: 300s)
**Error**: `⏰ Script timed out after 300s and was killed.`

## Root Cause

Each `write_file` call within `execute_code` involves:
- Network round-trip to the file system tool
- iCloud sync overhead (vault is in iCloud)
- Lint checks after write

With 6 calls, cumulative time exceeded 300s.

## Solution

1. **Primary**: Use parallel `write_file` tool calls directly (3 at a time)
2. **Fallback**: Keep `execute_code` batches to 3-4 `write_file` calls max
3. **Never**: Put 5+ `write_file` calls in a single `execute_code`

## Performance Notes

- Individual `write_file` calls complete in 3-8 seconds each
- 3 parallel calls complete in ~8 seconds total
- `execute_code` with 3 calls: ~25-30 seconds
- `execute_code` with 6 calls: timeout (>300s observed)
