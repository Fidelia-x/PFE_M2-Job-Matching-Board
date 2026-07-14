import math


def radar_chart_svg(labels, current, target, max_value=100, size=280):
    n = len(labels)
    cx = cy = size / 2
    radius = size / 2 - 42

    def point(value, i):
        angle = -math.pi / 2 + i * (2 * math.pi / n)
        r = radius * min(value, max_value) / max_value
        return cx + r * math.cos(angle), cy + r * math.sin(angle)

    def polygon(values):
        pts = [point(v, i) for i, v in enumerate(values)]
        return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

    grid_rings = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{radius * f:.1f}" '
        f'style="fill:none;stroke:var(--ink-700);stroke-width:1" />'
        for f in (0.25, 0.5, 0.75, 1.0)
    )

    axis_lines = ""
    axis_labels = ""
    for i, label in enumerate(labels):
        x, y = point(max_value, i)
        axis_lines += (
            f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" '
            f'style="stroke:var(--ink-700);stroke-width:1" />'
        )
        lx, ly = point(max_value * 1.22, i)
        anchor = "middle"
        if lx < cx - 5:
            anchor = "end"
        elif lx > cx + 5:
            anchor = "start"
        axis_labels += (
            f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" '
            f'style="fill:var(--text-lo);font-family:Inter,sans-serif;font-size:11px" '
            f'dominant-baseline="middle">{label}</text>'
        )

    target_poly = polygon(target)
    current_poly = polygon(current)

    return f"""
    <div class="sg-radar-wrap">
        <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
            {grid_rings}
            {axis_lines}
            <polygon points="{target_poly}"
                style="fill:none;stroke:var(--text-discreet);stroke-width:1.5;stroke-dasharray:4,4" />
            <polygon points="{current_poly}"
                style="fill:var(--accent-dim);stroke:var(--accent);stroke-width:2" />
            {axis_labels}
        </svg>
        <div class="sg-radar-legend">
            <span><i style="background:var(--accent)"></i> Profil actuel</span>
            <span><i style="background:none;border:1.5px dashed var(--text-discreet)"></i> Profil cible</span>
        </div>
    </div>
    """


def gauge_svg(pct, size=150, label="Correspondance"):
    pct = max(0, min(100, pct))
    r = size / 2 - 14
    cx = cy = size / 2
    circumference = 2 * math.pi * r
    offset = circumference * (1 - pct / 100)

    return f"""
    <div class="sg-gauge-wrap">
        <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
            <circle cx="{cx}" cy="{cy}" r="{r}" style="fill:none;stroke:var(--ink-800);stroke-width:14" />
            <circle cx="{cx}" cy="{cy}" r="{r}" style="fill:none;stroke:var(--accent);stroke-width:14;
                stroke-linecap:round;stroke-dasharray:{circumference:.1f};stroke-dashoffset:{offset:.1f}"
                transform="rotate(-90 {cx} {cy})" />
            <text x="{cx}" y="{cy - 4}" text-anchor="middle"
                style="fill:var(--text-hi);font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:28px">{pct}%</text>
            <text x="{cx}" y="{cy + 18}" text-anchor="middle"
                style="fill:var(--text-discreet);font-family:'IBM Plex Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.05em">{label}</text>
        </svg>
    </div>
    """
