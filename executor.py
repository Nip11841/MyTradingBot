# Trading212 manual execution helper
import scanner

alerts = scanner.scan_gaps()

def generate_t212_instructions():
    instructions = []
    for trade in alerts:
        instructions.append(
            f"TICKER: {trade['ticker']}\n"
            f"ACTION: {'BUY' if trade['gap_pct'] < 0 else 'SELL'}\n"
            f"PRICE: Open ±0.5%\n"
            f"STOP: {1.5 * abs(trade['gap_pct']):.1f}%"
        )
    return instructions

print(generate_t212_instructions())  # Copy-paste to T212 or AHK
