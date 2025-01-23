# settings.py
SCENARIO = 1
NAME_SERVICE = "cabine"

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
        "Tools.Service",
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
