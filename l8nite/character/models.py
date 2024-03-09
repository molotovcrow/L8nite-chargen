from functools import cached_property, reduce
from typing import Literal

from django.db import models

from l8nite.abilities.models import CastedAbility
from l8nite.typedefs import RACE_CHOICES

# Create your models here.
SkillName = Literal[
    "small_arms",
    "big_arms",
    "melee",
    "demolitions",
    "sneak",
    "athletics",
    "slight_of_hand",
    "disguise",
    "attack",
    "support",
    "healing",
    "summoning",
    "piloting",
    "hacking",
    "security",
    "kinetic",
    "survival",
    "perception",
    "insight",
    "investigation",
    "deception",
    "intimidation",
    "persuasion",
    "performance",
    "magic",
    "history",
    "medicine",
    "technology",
]

ShortAttName = Literal["har", "str", "dex", "arc", "log", "acu", "cha", "int"]


class CharacterRace(models.Model):
    name = models.CharField(
        choices=RACE_CHOICES,
        max_length=50,
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

    def get_limit(self, att: ShortAttName) -> int:
        return getattr(self, f"base_{att}", 0) + 10


class RacialTrait(models.Model):
    race = models.ForeignKey(
        CharacterRace,
        related_name="traits",
        on_delete=models.CASCADE,
    )
    description = models.TextField(default="", blank=True)


class CharacterClass(models.Model):
    pass


class Character(models.Model):
    SECONDARY_SKILLS = (
        ("MA", "Mana"),
        ("CH", "Chi"),
        ("SY", "Synergy"),
    )

    first_name = models.CharField(default="", blank=True, max_length=50)
    last_name = models.CharField(default="", blank=True, max_length=50)
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

    max_health = models.PositiveIntegerField(default=0)
    max_secondary = models.PositiveIntegerField(default=0)

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

    # ai_body = Models.ForeignKey(AIBody, null=True, default=None)
    # background = Models.ForeignKey(
    #     CharacterBackground, null=True, default=None
    # )
    # talents = Models.ForeignKey(Talent, null=True, default=None)
    # qualities = Models.ForeignKey(Quality, null=True, default=None)

    # we may want a max and a current for these
    noteriety = models.PositiveIntegerField(default=0)
    attribute_points = models.PositiveIntegerField(default=0)

    ac = cached_property(
        lambda self: 10 + self.dexterity + self.equipment.ac_mod
    )


class CharacterSkills(models.Model):
    character = models.OneToOneField(
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

    def get_modified_skill(self, skill: SkillName) -> int:
        """
        Returns the modified skill value for the specified skill

        :param skill: The name of the skill to be modified
        """
        # TODO do the modification calculations
        return getattr(self, skill)


class CharacterEquipment(models.Model):
    character = models.OneToOneField(
        Character, related_name="equipment", on_delete=models.CASCADE
    )
    # owned_equipment = models.ManyToManyField(Equipment)
    # head = models.ForeignKey(HeadEquipment)
    # body = models.ForeignKey(BodyEquipment)

    # these could be weapon, shield, focus, etc.
    # left_hand = models.ForeignKey(HandEquipment)
    # right_hand = models.ForeignKey(HandEquipment)

    # this is supposed to be like amulets, rings, special boots,
    # or perhaps a fancy broach
    # misc_equipped = models.ManyToManyField(MiscEquipment)

    @cached_property
    def ac_mod(self) -> int:
        return (
            self.head.armor_bonus
            + self.body.armor_bonus
            + self.left_hand.armor_bonus
            + self.right_hand.armor_bonus
            + sum(
                self.misc_equipped.all().values_list("armor_bonus", flat=True),
            )
        )
