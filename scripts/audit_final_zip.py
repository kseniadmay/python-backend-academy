import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)

from verify_platinum import run_platinum_audit

if __name__ == '__main__':
    print("=== AUDITING CANONICAL FINAL REMNOTE ZIP (525 FILES) ===")
    run_platinum_audit()
    print("🎉 ALL PLATINUM CHECKS PASSED FOR CANONICAL REMNOTE ZIP!")
