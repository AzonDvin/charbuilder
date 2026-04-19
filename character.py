"""
Character model for Savage Worlds Star Wars.
"""

import re
from typing import Iterable

try:
    from data import ARMOR
except ImportError:
    ARMOR = {}


def _die_to_num(die: str) -> int:
    return {"d4": 4, "d6": 6, "d8": 8, "d10": 10, "d12": 12}.get(die, 4)


def _num_to_die(num: int) -> str:
    return {4: "d4", 6: "d6", 8: "d8", 10: "d10", 12: "d12"}.get(num, "d4")


def parse_species_granted_skill_dice(
    abilities: str | None, valid_skill_names: Iterable[str]
) -> dict[str, str]:
    """
    Find explicit racial skill dice in species text, e.g. 'Piloting d6', 'Common Knowledge d6'.

    Only matches names in valid_skill_names (longest first). Ignores attribute lines
    like 'd6 Strength' / 'd6 Smarts'.
    """
    if not abilities:
        return {}
    text = abilities.strip()
    text = re.sub(
        r"\b(d4|d6|d8|d10|d12)\s+(Agility|Smarts|Spirit|Strength|Vigor)\b",
        "",
        text,
        flags=re.IGNORECASE,
    )
    names = sorted(set(valid_skill_names), key=len, reverse=True)
    out: dict[str, str] = {}
    for name in names:
        pat = (
            r"(?<![A-Za-z])"
            + re.escape(name)
            + r"\s+d(4|6|8|10|12)\b"
        )
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            die = f"d{m.group(1)}"
            if name not in out or _die_to_num(die) > _die_to_num(out[name]):
                out[name] = die
    return out


def skill_purchase_cost(
    skill_name: str,
    die_value: str,
    attributes: dict,
    core_skills: set,
    skill_attributes: dict,
) -> int:
    """Savage Worlds-style skill point cost from default (core d4 / non-core Untrained) to die_value."""
    is_core = skill_name in core_skills
    if die_value == "Untrained":
        return 0
    if die_value == "d4":
        return 0 if is_core else 1
    if die_value not in {"d6", "d8", "d10", "d12"}:
        return 0
    linked = skill_attributes.get(skill_name, "Smarts")
    attr_val = _die_to_num(attributes.get(linked, "d4"))
    val = _die_to_num(die_value)
    total = 0 if is_core else 1
    for step in range(1, (val - 4) // 2 + 1):
        current_die = 4 + (step - 1) * 2
        total += 1 if current_die < attr_val else 2
    return total


def adjusted_skill_purchase_cost(
    skill_name: str,
    die_value: str,
    attributes: dict,
    core_skills: set,
    skill_attributes: dict,
    species_abilities: str | None,
) -> int:
    """Purchase cost with species 'Skill d6' grants treated as already paid up to that die."""
    raw = skill_purchase_cost(
        skill_name, die_value, attributes, core_skills, skill_attributes
    )
    grants = parse_species_granted_skill_dice(
        species_abilities, skill_attributes.keys()
    )
    grant_die = grants.get(skill_name)
    if not grant_die:
        return raw
    raw_grant = skill_purchase_cost(
        skill_name, grant_die, attributes, core_skills, skill_attributes
    )
    return max(0, raw - raw_grant)


def size_toughness_bonus_from_species_abilities(text: str | None) -> int:
    """+N Size in species abilities adds +N Toughness (Savage Worlds Deluxe Size/mass rule)."""
    if not text:
        return 0
    total = 0
    for m in re.finditer(r"\+(\d+)\s*Size", text, re.IGNORECASE):
        total += int(m.group(1))
    return total


def compute_display_toughness(
    attributes: dict,
    armor_name: str,
    species_abilities: str | None = None,
) -> int:
    """2 + half Vigor + armor Toughness bonus + species Size bonus."""
    attrs = attributes or {}
    vig = attrs.get("Vigor", "d4")
    mapping = {"d4": 4, "d6": 6, "d8": 8, "d10": 10, "d12": 12}
    vigor_val = mapping.get(vig, 4)
    base = 2 + (vigor_val // 2)
    armor_bonus = 0
    if armor_name and armor_name in ARMOR:
        t = ARMOR[armor_name].get("toughness", "0")
        if "+" in str(t):
            try:
                armor_bonus = int(str(t).replace("+", ""))
            except ValueError:
                pass
    size_bonus = size_toughness_bonus_from_species_abilities(species_abilities)
    return base + armor_bonus + size_bonus


class Character:
    """Represents a Savage Worlds Star Wars character."""

    def __init__(self):
        self.name = ""
        self.species = ""
        self.species_abilities = ""
        self.attributes = {
            "Agility": "d4",
            "Smarts": "d4",
            "Spirit": "d4",
            "Strength": "d4",
            "Vigor": "d4",
        }
        self.skills = {}
        self.hindrances = []
        self.edges = []
        self.weapons = []
        self.armor = "No Armor"
        self.gear = []
        self.credits = 500
        self.hindrance_points_remaining = 0
        self.skill_points_remaining = 15
        self.human_free_edges_used = []  # Edges taken with Human species bonus

    def get_toughness(self):
        """Calculate toughness (2 + half Vigor + armor + species Size bonus)."""
        return compute_display_toughness(
            self.attributes,
            self.armor,
            self.species_abilities,
        )

    def _die_to_num(self, die):
        """Convert d4/d6/d8/d10/d12 to numeric value."""
        mapping = {"d4": 4, "d6": 6, "d8": 8, "d10": 10, "d12": 12}
        return mapping.get(die, 4)

    def get_parry(self):
        """Calculate Parry (2 + half Fighting)."""
        fighting = self.skills.get("Fighting", "d4")
        val = self._die_to_num(fighting)
        return 2 + (val // 2)

    def to_dict(self):
        """Export character as dictionary."""
        return {
            "name": self.name,
            "species": self.species,
            "species_abilities": self.species_abilities,
            "attributes": self.attributes.copy(),
            "skills": self.skills.copy(),
            "hindrances": self.hindrances.copy(),
            "edges": self.edges.copy(),
            "weapons": self.weapons.copy(),
            "armor": self.armor,
            "gear": self.gear.copy(),
            "credits": self.credits,
            "toughness": self.get_toughness(),
            "parry": self.get_parry(),
            "human_free_edges_used": getattr(self, "human_free_edges_used", []),
        }
