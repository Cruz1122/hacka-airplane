"""Canonical builder per section (paths relative to the research notes folder; args after spaces).

Pipeline: builder -> coordination/coordinator_fixes.py -> coordination/validate_knowledge.py.
Snapshot sections: their old generators predate corrections made in the JSON and now refuse to run.
"""

SNAPSHOT = "coordination/build_from_snapshot.py"

BUILDERS = {
    "actions": [f"{SNAPSHOT} actions"],
    "health_safety": ["health_safety/build_health_safety.py"],
    "weather_volcano": ["weather_volcano/generate_weather_volcano.py"],
    "access": [f"{SNAPSHOT} access"],
    "booking_fees": ["booking_fees/build_section.py"],
    "hours_status": [f"{SNAPSHOT} hours_status"],
    "preparation": ["preparation/build_preparation.py"],
    "activities": [f"{SNAPSHOT} activities"],
    "rules": ["rules/generate_rules.py"],
    "services": [f"{SNAPSHOT} services"],
    "fauna": ["fauna/build_corrected_fauna.py"],
    "flora_ecosystems": ["flora_ecosystems/generate_flora_ecosystems.py"],
    "geography": [f"{SNAPSHOT} geography"],
    "history_culture": ["history_culture/emit_corrected.py"],
    "conversation": [f"{SNAPSHOT} conversation"],
}
