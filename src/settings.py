# settings.py
SCENARIO = 1

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
        "Tools.Argument",
        # "Tools.Factory"
    ],
    "projects": [
        "Cabine.Combinee",
        "Cabine.Enregistrement",
        "Cabine.Son",
        "Cabine.Touches"
    ]
}

EXCEPTIONS = [
    "AttributeError"
]
