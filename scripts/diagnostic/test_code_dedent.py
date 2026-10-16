import textwrap

def clean_code_block(code_lines):
    # Убираем общий внешний отступ, сохраняя внутреннюю структуру Python
    raw_block = '\n'.join(code_lines)
    dedented = textwrap.dedent(raw_block)
    return dedented.splitlines()

# Пример с паразитным отступом 8 пробелов:
sample_lines = [
    "        def foo():",
    "            if True:",
    "                return 42"
]
print("Dedented:")
for l in clean_code_block(sample_lines):
    print(repr(l))
