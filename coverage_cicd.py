import os

import requests

GIST_COVERAGE_TOKEN = os.getenv("GIST_COVERAGE_TOKEN")
GIST_COVERAGE_ID = os.getenv("GIST_COVERAGE_ID")
COVERAGE_THRESHOLD = float(os.getenv("COVERAGE_THRESHOLD", 70))


class ThresholdException(Exception):
    pass


def get_coverage_from_xml(xml_path="coverage.xml"):
    import xml.etree.ElementTree as ET

    tree = ET.parse(xml_path)
    root = tree.getroot()
    line_rate = float(root.attrib.get("line-rate", 0))
    return round(line_rate * 100, 2)


def build_svg(result: float) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="196" height="20">
    <title>Coverage - {result}%</title>
    <defs>
        <linearGradient id="workflow-fill" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop stop-color="#444D56" offset="0%"></stop>
            <stop stop-color="#24292E" offset="100%"></stop>
        </linearGradient>
        <linearGradient id="state-fill" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop stop-color="#34D058" offset="0%"></stop>
            <stop stop-color="#28A745" offset="100%"></stop>
        </linearGradient>
    </defs>
    <g fill="none" fill-rule="evenodd">
        <g font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
            <path d="M0,3 C0,1.3431 1.3552,0 3.027,0 L146,0 L146,20 L3.027,20 C1.3552,20 0,18.6569 0,17 Z"
                  fill="url(#workflow-fill)"></path>
            <text fill="#010101" fill-opacity=".3">
                <tspan x="22" y="15" aria-hidden="true">Coverage</tspan>
            </text>
            <text fill="#FFFFFF"><tspan x="22" y="14">Coverage</tspan></text>
        </g>
        <g transform="translate(146)" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
            <path d="M0 0h46.939C48.629 0 50 1.343 50 3v14c0 1.657-1.37 3-3.061 3H0V0z"
                  fill="url(#state-fill)"></path>
            <text fill="#010101" fill-opacity=".3" aria-hidden="true">
                <tspan x="4" y="15">{result}%</tspan>
            </text>
            <text fill="#FFFFFF"><tspan x="4" y="14">{result}%</tspan></text>
        </g>
    </g>
</svg>"""


def update_gist(svg: str):
    payload = {
        "description": "Coverage badge",
        "files": {"coverage.svg": {"content": svg}},
    }
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GIST_COVERAGE_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url = f"https://api.github.com/gists/{GIST_COVERAGE_ID}"
    response = requests.patch(url, headers=headers, json=payload, timeout=10)
    response.raise_for_status()


if __name__ == "__main__":
    result = get_coverage_from_xml("coverage.xml")
    print(f"Coverage: {result}%")

    if result < COVERAGE_THRESHOLD:
        raise ThresholdException(
            f"Coverage {result}% is below threshold {COVERAGE_THRESHOLD}%"
        )

    svg = build_svg(result)
    update_gist(svg)
    print("Badge updated successfully")
