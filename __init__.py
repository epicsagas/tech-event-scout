"""tech-event-scout — Hermes plugin entry point.

Hermes loads this module from ~/.hermes/plugins/tech-event-scout/ and calls
register(ctx) once at startup. Bundled skills under skills/ are
registered here so the agent can load them via skill_view("tech-event-scout:<skill>").
"""
from pathlib import Path


def register(ctx):
    """Register bundled skills with the Hermes plugin manager."""
    skills_dir = Path(__file__).parent / "skills"
    for child in sorted(skills_dir.iterdir()):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            ctx.register_skill(child.name, skill_md)
