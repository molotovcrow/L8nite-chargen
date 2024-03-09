from typing import Literal

from django.db import models

from l8nite.abilities import CastedAbility
from l8nite.typedefs import RACE_CHOICES

# Create your models here.


class CharacterRace(models.Model):
    name = models.CharField(
        choices=RACE_CHOICES,
        max_length=50,
        required=True,
        unique=True,
    )

    speed = models.PositiveIntegerField(default=30)

    """
    These values will be set in a migration when the
    objects are saved to the database and then never changed
    programatically unless cam decides to change them.
    """
    base_har = models.PositiveIntegerField(default=0, editable=False)

    base_str = models.PositiveIntegerField(default=0, editable=False)

    base_dex = models.PositiveIntegerField(default=0, editable=False)

    base_arc = models.PositiveIntegerField(default=0, editable=False)

    base_log = models.PositiveIntegerField(default=0, editable=False)

    base_acu = models.PositiveIntegerField(default=0, editable=False)

    base_cha = models.PositiveIntegerField(default=0, editable=False)

    base_int = models.PositiveIntegerField(default=0, editable=False)

    def get_limit(
        self,
        att: Literal["har", "str", "dex", "arc", "log", "acu", "cha", "int"],
    ) -> int:
        return getattr(self, f"base_{att}", 0) + 10


class CharacterClass(models.Model):
    pass


class Character(models.Model):
    SECONDARY_SKILLS = (
        ("MA", "Mana"),
        ("CH", "Chi"),
        ("SY", "Synergy"),
    )

    first_name = models.Charfield(default="", blank=True, max_length=50)
    last_name = models.Charfield(default="", blank=True, max_length=50)
    alias = models.CharField(default="", blank=True, max_length=50)
    race = models.ForeignKey(
        CharacterRace,
        related_name="characters",
        null=True,
        on_delete=models.SET_NULL,
    )
    char_class = models.ForeignKey(
        CharacterClass,
        related_name="characters",
        null=True,
        on_delete=models.SET_NULL,
    )
    description = models.TextField(default="", blank=True)
    secondary_skill = models.CharField(
        max_length=2, choices=SECONDARY_SKILLS, default="MA"
    )

    max_health = models.PositiveIntegerField(defualt=0)
    max_secondary = models.PositiveIntegerField(defualt=0)

    hardiness = models.PositiveIntegerField(default=0)
    strength = models.PositiveIntegerField(default=0)
    dexterity = models.PositiveIntegerField(default=0)
    arcana = models.PositiveIntegerField(default=0)
    logic = models.PositiveIntegerField(default=0)
    acuity = models.PositiveIntegerField(default=0)
    charisma = models.PositiveIntegerField(default=0)
    intelligence = models.PositiveIntegerField(default=0)

    abilities = models.ManyToManyField(
        CastedAbility, on_delete=models.PROTECT, null=True
    )


class CharacterSkills(models.Model):
    character = models.ForeignKey(
        Character, related_name="skills", on_delete=models.CASCADE
    )

    # str
    small_arms = models.PositiveIntegerField(default=0)
    big_arms = models.PositiveIntegerField(default=0)
    melee = models.PositiveIntegerField(default=0)
    demolitions = models.PositiveIntegerField(default=0)

    # dex
    sneak = models.PositiveIntegerField(default=0)
    athletics = models.PositiveIntegerField(default=0)
    slight_of_hand = models.PositiveIntegerField(default=0)
    disguise = models.PositiveIntegerField(default=0)

    # arcana
    attack = models.PositiveIntegerField(default=0)
    support = models.PositiveIntegerField(default=0)
    healing = models.PositiveIntegerField(default=0)
    summoning = models.PositiveIntegerField(default=0)

    # logic
    piloting = models.PositiveIntegerField(default=0)
    hacking = models.PositiveIntegerField(default=0)
    security = models.PositiveIntegerField(default=0)
    kinetic = models.PositiveIntegerField(default=0)

    # acuity
    survival = models.PositiveIntegerField(default=0)
    perception = models.PositiveIntegerField(default=0)
    insight = models.PositiveIntegerField(default=0)
    investigation = models.PositiveIntegerField(default=0)

    # charisma
    deception = models.PositiveIntegerField(default=0)
    intimidation = models.PositiveIntegerField(default=0)
    persuasion = models.PositiveIntegerField(default=0)
    performance = models.PositiveIntegerField(default=0)

    # intelligence
    medicine = models.PositiveIntegerField(default=0)
    magic = models.PositiveIntegerField(default=0)
    history = models.PositiveIntegerField(default=0)
    technology = models.PositiveIntegerField(default=0)

    def get_modified_skill(self, skill: str) -> int:
        """
        Returns the modified skill value for the specified skill

        :param skill: The skill to be modified
        """
        # TODO
        return getattr(self, skill)
