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
        "Tools.Deamon",
        "Tools.GPIO",
        "Tools.Pad",
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
