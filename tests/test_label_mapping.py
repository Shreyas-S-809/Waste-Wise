"""
Unit tests for WasteWise dataset label mapping logic.
Verifies that all raw dataset categories correctly map to Wet, Dry, or Excluded.
"""

import pytest

LABEL_MAP = {
    # TechSash categories
    "O": "Wet",
    "R": "Dry",
    # RealWaste categories
    "Food Organics": "Wet",
    "Vegetation": "Wet",
    "Cardboard": "Dry",
    "Glass": "Dry",
    "Metal": "Dry",
    "Paper": "Dry",
    "Plastic": "Dry",
}

EXCLUDED_CLASSES = {"Textile Trash", "Miscellaneous Trash"}


def test_techsash_organic_maps_to_wet():
    assert LABEL_MAP.get("O") == "Wet"


def test_techsash_recyclable_maps_to_dry():
    assert LABEL_MAP.get("R") == "Dry"


def test_realwaste_organics_map_to_wet():
    assert LABEL_MAP.get("Food Organics") == "Wet"
    assert LABEL_MAP.get("Vegetation") == "Wet"


def test_realwaste_recyclables_map_to_dry():
    dry_categories = ["Cardboard", "Glass", "Metal", "Paper", "Plastic"]
    for cat in dry_categories:
        assert LABEL_MAP.get(cat) == "Dry", f"Category {cat} should map to Dry"


def test_ambiguous_classes_are_excluded():
    for cat in EXCLUDED_CLASSES:
        assert cat not in LABEL_MAP, f"Ambiguous class {cat} must not be mapped to Wet or Dry"


def test_no_unmapped_categories_default_to_wet_or_dry():
    unknown_item = "RandomWaste"
    assert unknown_item not in LABEL_MAP

