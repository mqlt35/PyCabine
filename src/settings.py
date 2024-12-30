# settings.py

MODULES = {
    "scenarios": [
        "Cabine.Scenarios.Scenario1",
        "Cabine.Scenarios.Scenario2",
        "Cabine.Scenarios.Scenario3"
    ],
    "tools": [
        "Tools.Utils",
        "Tools.Check",
        "Tools.Mixer",
        # "Tools.Factory"
    ],
    "projects": [
        "Cabine.Combinee",
        "Cabine.Enregistrement",
        # "Cabine.Locals",
        "Cabine.Son",
        "Cabine.Touches"
    ]
}

EXCEPTIONS = [
    "AttributeError"
]