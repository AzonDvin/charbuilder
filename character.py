"""
Character model for Savage Worlds Star Wars.
"""

try:
    from data import ARMOR
except ImportError:
    ARMOR = {}


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
        """Calculate toughness (2 + half Vigor + armor)."""
        vigor_val = self._die_to_num(self.attributes["Vigor"])
        base = 2 + (vigor_val // 2)
        armor_bonus = 0
        if self.armor and self.armor in ARMOR:
            t = ARMOR[self.armor].get("toughness", "0")
            if "+" in str(t):
                try:
                    armor_bonus = int(str(t).replace("+", ""))
                except ValueError:
                    pass
        return base + armor_bonus

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
