import os

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
academy_path = os.path.join(root, 'academy.html')

with open(academy_path, 'r', encoding='utf-8') as f:
    content = f.read()

print('Original academy.html length:', len(content))

# 1. Update .btn-dominant-cta in main CSS to Zen Glassmorphism matching notes buttons
t1 = """  .btn-dominant-cta {
    position: relative;
    overflow: hidden;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-height: 50px;
    height: 50px;
    padding: 0 24px !important;
    border-radius: 14px !important;
    background: linear-gradient(180deg, #34d399 0%, #10b981 100%) !important;
    border: none !important;
    box-shadow: 0 4px 0 #059669, 0 8px 22px rgba(16, 185, 129, 0.45) !important;
    font-weight: 850 !important;
    font-size: 0.96rem !important;
    color: #022318 !important;
    letter-spacing: 0.01em;
    cursor: pointer;
    text-decoration: none;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    -webkit-tap-highlight-color: transparent;
    transition: transform 0.14s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.14s ease, filter 0.14s ease !important;
  }
  .btn-dominant-cta:focus-visible {
    outline: 2px solid #34d399 !important;
    outline-offset: 3px !important;
  }
  .btn-dominant-cta:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 0 #047857, 0 10px 24px rgba(16, 185, 129, 0.5) !important;
  }
  .btn-dominant-cta:active {
    transform: translateY(2px) scale(0.99) !important;
    box-shadow: 0 1px 0 #047857, 0 4px 10px rgba(16, 185, 129, 0.3) !important;
  }"""

r1 = """  .btn-dominant-cta {
    position: relative;
    overflow: hidden;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-height: 52px;
    height: 52px;
    padding: 0 22px !important;
    border-radius: 16px !important;
    background: linear-gradient(180deg, rgba(16, 185, 129, 0.22) 0%, rgba(5, 150, 105, 0.14) 100%) !important;
    border: 1.5px solid rgba(52, 211, 153, 0.48) !important;
    box-shadow: 0 6px 22px rgba(16, 185, 129, 0.20), inset 0 1px 0 rgba(255, 255, 255, 0.14) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    font-weight: 800 !important;
    font-size: 0.96rem !important;
    color: #ffffff !important;
    letter-spacing: 0.01em;
    cursor: pointer;
    text-decoration: none;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    -webkit-tap-highlight-color: transparent;
    transition: transform 0.14s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.16s ease, border-color 0.16s ease, background 0.16s ease !important;
  }
  .btn-dominant-cta:focus-visible {
    outline: 2px solid #34d399 !important;
    outline-offset: 3px !important;
  }
  .btn-dominant-cta:hover {
    transform: translateY(-1px) !important;
    background: linear-gradient(180deg, rgba(16, 185, 129, 0.32) 0%, rgba(5, 150, 105, 0.22) 100%) !important;
    border-color: rgba(52, 211, 153, 0.72) !important;
    box-shadow: 0 8px 28px rgba(16, 185, 129, 0.32), inset 0 1px 0 rgba(255, 255, 255, 0.22) !important;
  }
  .btn-dominant-cta:active {
    transform: translateY(1px) scale(0.985) !important;
    box-shadow: 0 3px 12px rgba(16, 185, 129, 0.24) !important;
    filter: brightness(0.95) !important;
  }
  :root[data-theme="light"] .btn-dominant-cta {
    background: linear-gradient(180deg, rgba(16, 185, 129, 0.18) 0%, rgba(5, 150, 105, 0.10) 100%) !important;
    border-color: rgba(16, 185, 129, 0.45) !important;
    box-shadow: 0 6px 18px rgba(16, 185, 129, 0.15) !important;
    color: #064e3b !important;
  }"""

assert t1 in content, 'Target 1 (.btn-dominant-cta base styles) not found'
content = content.replace(t1, r1, 1)
print('1. [PASS] .btn-dominant-cta Zen Glassmorphism styles applied')

# 2. Update .cocoon-focus-cta-label and arrow colors to crisp white and emerald
t2 = """  .cocoon-focus-cta-label {
    text-align: left;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
    min-width: 0;
    flex: 1 1 auto;
    font-weight: 850 !important;
    color: #022318 !important;
  }
  .cocoon-focus-cta .btn-cta-arrow {
    color: #022318 !important;
    font-weight: 900 !important;
  }"""

r2 = """  .cocoon-focus-cta-label {
    text-align: left;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
    min-width: 0;
    flex: 1 1 auto;
    font-weight: 800 !important;
    color: #ffffff !important;
    letter-spacing: 0.01em;
  }
  .cocoon-focus-cta .btn-cta-arrow {
    color: #34d399 !important;
    font-weight: 900 !important;
    font-size: 1.05rem !important;
    display: inline-block;
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
  }
  .cocoon-focus-cta:hover .btn-cta-arrow {
    transform: translateX(4px) !important;
  }
  :root[data-theme="light"] .cocoon-focus-cta-label {
    color: #064e3b !important;
  }
  :root[data-theme="light"] .cocoon-focus-cta .btn-cta-arrow {
    color: #059669 !important;
  }"""

assert t2 in content, 'Target 2 (.cocoon-focus-cta-label) not found'
content = content.replace(t2, r2, 1)
print('2. [PASS] .cocoon-focus-cta-label crisp white and arrow styling applied')

# 3. Update .btn-reward-badge to glowing translucent emerald pill
t3 = """  .btn-reward-badge {
    display: inline-flex;
    align-items: center;
    gap: 3px;
    padding: 3px 9px;
    border-radius: 8px;
    background: rgba(2, 35, 24, 0.16) !important;
    border: 1px solid rgba(2, 35, 24, 0.28) !important;
    color: #022318 !important;
    font-weight: 850 !important;
    font-size: 0.82rem;
    letter-spacing: 0.02em;
    box-shadow: none !important;
    margin: 0 6px;
  }"""

r3 = """  .btn-reward-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    border-radius: 9px;
    background: rgba(16, 185, 129, 0.22) !important;
    border: 1px solid rgba(52, 211, 153, 0.40) !important;
    color: #34d399 !important;
    font-weight: 800 !important;
    font-size: 0.82rem;
    letter-spacing: 0.02em;
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.12) !important;
    margin: 0 6px;
  }
  :root[data-theme="light"] .btn-reward-badge {
    background: rgba(16, 185, 129, 0.14) !important;
    border-color: rgba(16, 185, 129, 0.35) !important;
    color: #065f46 !important;
  }"""

assert t3 in content, 'Target 3 (.btn-reward-badge) not found'
content = content.replace(t3, r3, 1)
print('3. [PASS] .btn-reward-badge glowing glass pill styles applied')

# 4. Update ctaLabel in viewDashboard to "Начать дальше (2 мин)" / "Продолжить дальше (2 мин)"
t4 = "const ctaLabel = isStarted ? 'Продолжить (2 мин)' : 'Начать (2 мин)';"
r4 = "const ctaLabel = isStarted ? 'Продолжить дальше (2 мин)' : 'Начать дальше (2 мин)';"
assert t4 in content, 'Target 4 (ctaLabel) not found'
content = content.replace(t4, r4, 1)
print('4. [PASS] ctaLabel updated to "Начать дальше (2 мин)" / "Продолжить дальше (2 мин)"')

with open(academy_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully updated academy.html. New length:', len(content))
