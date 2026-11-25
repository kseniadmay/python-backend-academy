import re

with open("standards/standards.html", "r", encoding="utf-8") as f:
    content = f.read()

# Search for prohibited terms in HR section
hr_start = content.find("const STAR_SCENARIOS")
hr_end = content.find("function viewMockInterview", hr_start)
end_of_mock = content.find("\nfunction ", hr_end + 30)
hr_section = content[hr_start:end_of_mock]

coddy_matches = re.findall(r"coddy|кодди", hr_section, re.IGNORECASE)
d3_matches = re.findall(r"\b3d\b|3д", hr_section, re.IGNORECASE)

print("Prohibited terms check in HR section:")
print(f"  Coddy/Кодди matches: {len(coddy_matches)}")
print(f"  3D/3д matches: {len(d3_matches)}")
