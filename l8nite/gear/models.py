import random
from functools import cached_property

from django.db import models

from l8nite.typedefs import DIE_TYPE_CHOICES, FEET_TO_METERS


class Weapon(models.Model):
    """
    Base weapon information, can be linked to
    additional info via :py:class:`ArmWeaponStats`.
    """

    WEAPON_CLASS_CHOICES = [
        ("SA", "Small Arms"),
        ("BA", "Big Arms"),
        ("ME", "Melee"),
        ("DE", "Demolitions"),
    ]

    WEAPON_RANGE_TYPE_CHOICES = [
        ("CO", "Cone"),
    ]

    name = models.CharField()
    weapon_class = models.CharField(max_length=2, choices=WEAPON_CLASS_CHOICES)

    # I.e. MULTIPLIER * DIE_TYPE
    damage_die_multiplier = models.PositiveSmallIntegerField(default=1)
    damage_die_type = models.CharField(max_length=3, choices=DIE_TYPE_CHOICES)

    # I.e. RANGE by RANGE_TYPE (Cone)
    weapon_range = models.PositiveIntegerField()
    weapon_range_type = models.CharField(
        max_length=2,
        null=True,
        choices=WEAPON_RANGE_TYPE_CHOICES,
        default=None,
    )

    cost = models.PositiveIntegerField()

    @cached_property
    def damage_die_value(self) -> int:
        return int(self.damage_die_type[1:])

    @cached_property
    def weapon_range_meters(self) -> int:
        return int(self.weapon_range / FEET_TO_METERS)

    def roll_damage(
        self,
        *,
        modifier: int = 0,
        disadvantage: bool = False,
        advantage: bool = False
    ) -> int:
        """
        Rolls damage for this weapon: XDY + Z, applies
        advantage and/or disadvantage to the roll if specified.

        :param modifier: The player's damage modifier.
        :param disadvantage: ``True`` if rolling at disadvantage.
        :param advantage: ``True`` if rolling at advantage.
        """
        # Calculate the base roll, i.e. MULTIPLIER * DIE_TYPE + MODIFIER
        roll = 0
        for _ in range(self.damage_die_multiplier):
            roll += random.randint(1, self.damage_die_value)
        roll += modifier

        # Apply advantage/disadvantage
        if disadvantage:
            roll -= random.randint(1, 6)
        if advantage:
            roll += random.randint(1, 6)
        return roll


class ArmWeaponStats(models.Model):
    """
    Weapon statistics for small and big arm type weapons.
    """

    weapon = models.OneToOneField(
        Weapon, on_delete=models.CASCADE, related_name="arms_info"
    )
    ammo = models.PositiveSmallIntegerField()
    attachments = models.PositiveSmallIntegerField(default=0)
    enchantments = models.PositiveSmallIntegerField(default=0)


class Armor(models.Model):
    """
    Base armor information.
    """

    ARMOR_TYPE_CHOICES = [
        ("HE", "Head"),
        ("BO", "Body"),
        ("SH", "Shield"),
    ]

    ARMOR_CLASS_CHOICES = [
        ("HA", "Heavy Armor"),
        ("MA", "Medium Armor"),
        ("LA", "Light Armor"),
        (None, "No Class"),
    ]

    name = models.CharField()
    hardiness_requirement = models.PositiveSmallIntegerField(default=0)
    cost = models.PositiveIntegerField()
    armor_type = models.CharField(choices=ARMOR_TYPE_CHOICES)
    armor_bonus = models.PositiveSmallIntegerField(default=0)
    armor_class = models.CharField(choices=ARMOR_CLASS_CHOICES, null=True)
    enchantments = models.PositiveSmallIntegerField(default=1)


class EquipmentModification(models.Model):
    """
    Base equipment modification information, can be
    linked to additional information via :py:class:`CraftableModification`.

    Note: this is the "Crafting" sheet on the l8nite db excel document.
    """

    CRAFTING_TYPE_CHOICES = [
        ("EN", "Enhancement"),
        ("EC", "Enchantment"),
        ("AT", "Attachment"),
    ]

    name = models.CharField()
    cost = models.PositiveIntegerField()
    description = models.CharField()
    crafting_type = models.CharField(choices=CRAFTING_TYPE_CHOICES)


class CraftableModification(models.Model):
    """
    Additional crafting information for equipment
    modifications that can be crafted by the player.
    """

    CRAFTING_SKILL_TYPE_CHOICES = [
        ("TE", "Technology"),
        ("MA", "Magic"),
    ]

    equipment_modification = models.OneToOneField(
        EquipmentModification,
        on_delete=models.CASCADE,
        related_name="equipment_modification",
    )
    crafting_skill = models.CharField(
        max_length=2, choices=CRAFTING_SKILL_TYPE_CHOICES
    )
    skill_requirement = models.PositiveSmallIntegerField()
