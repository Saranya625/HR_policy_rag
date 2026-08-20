"""Design system and theme configuration."""

# Color Palette
COLORS = {
    "background": "#FAFAFA",
    "surface": "#FFFFFF",
    "surface_hover": "#F8F9FA",
    "border": "#E5E7EB",
    "border_strong": "#D1D5DB",
    "text": "#111827",
    "text_secondary": "#6B7280",
    "text_muted": "#9CA3AF",
    "primary": "#2563EB",
    "primary_hover": "#1D4ED8",
    "primary_light": "#DBEAFE",
    "success": "#10B981",
    "success_light": "#D1FAE5",
    "warning": "#F59E0B",
    "warning_light": "#FEF3C7",
    "danger": "#EF4444",
    "danger_light": "#FEE2E2",
}

# Spacing (8px system)
SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px",
    "2xl": "48px",
    "3xl": "64px",
}

# Typography
TYPOGRAPHY = {
    "h1": {"size": "32px", "weight": "700", "line_height": "1.2"},
    "h2": {"size": "24px", "weight": "600", "line_height": "1.3"},
    "h3": {"size": "18px", "weight": "600", "line_height": "1.4"},
    "body": {"size": "15px", "weight": "400", "line_height": "1.6"},
    "caption": {"size": "13px", "weight": "400", "line_height": "1.5"},
    "small": {"size": "12px", "weight": "400", "line_height": "1.4"},
}

# Shadows
SHADOWS = {
    "sm": "0 1px 2px rgba(0, 0, 0, 0.05)",
    "md": "0 4px 6px rgba(0, 0, 0, 0.07)",
    "lg": "0 10px 15px rgba(0, 0, 0, 0.08)",
    "xl": "0 20px 25px rgba(0, 0, 0, 0.10)",
}

# Border Radius
RADIUS = {
    "sm": "6px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
    "full": "9999px",
}

# Layout
LAYOUT = {
    "max_width": "1200px",
    "nav_height": "64px",
    "sidebar_width": "240px",
}
