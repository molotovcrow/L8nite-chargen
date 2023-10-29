import random

from django.db import models

from l8nite.typedefs import DIE_TYPE_CHOICES


class Weapon(models.Model):
    WEAPON_CLASS_CHOICES = [
        ("SA", "Small Arms"),
        ("BA", "Big Arms"),
        ("ME", "Melee"),
        ("DE", "Demolitions"),
    ]

    WEAPON_RANGE_TYPE_CHOICES = [
        ("FT", "Feet"),
        ("ME", "Meters"),
    ]

    name = models.CharField()
    weapon_class = models.CharField(max_length=2, choices=WEAPON_CLASS_CHOICES)

    # I.e. MULTIPLIER * DIE_TYPE
    damage_die_multiplier = models.PositiveSmallIntegerField(default=1)
    damage_die_type = models.CharField(max_length=2, choices=DIE_TYPE_CHOICES)

    # I.e. RANGE by RANGE_TYPE
    weapon_range = models.PositiveIntegerField()
    weapon_range_type = models.CharField(max_length=2, choices=WEAPON_RANGE_TYPE_CHOICES, default="FT")

    cost = models.PositiveIntegerField()

    @property
    def damage_die_value(self) -> int:
        return int(self.damage_die_type[1:])

    def roll_damage(self, *, modifier: int = 0, disadvantage: bool = False, advantage: bool = False) -> int:
        """
        Rolls damage for this weapon: XDY + Z, applies advantage and/or disadvantage to the roll if specified.

        :param modifier: The player's damage modifier.
        :param disadvantage: ``True`` if rolling at disadvantage.
        :param advantage: ``True`` if rolling at advantage.
        """
        roll = (self.damage_die_multiplier * random.randint(1, self.damage_die_value)) + modifier
        if disadvantage:
            roll -= random.randint(1, 6)
        if advantage:
            roll += random.randint(1, 6)
        return roll


class RangedWeapon(Weapon):
    ammo = models.PositiveSmallIntegerField()
    attachments = models.PositiveSmallIntegerField()
    enchantments = models.PositiveSmallIntegerField()


class Armor(models.Model):
    ARMOR_TYPE_CHOICES = [
        ('HE', 'Head'),
        ('BO', 'Body'),
        ('SH', 'Shield'),
    ]

    name = models.CharField()
    armor_bonus = models.PositiveSmallIntegerField(default=0)
    hardiness_requirement = models.PositiveSmallIntegerField(default=0)
    cost = models.PositiveIntegerField()
    armor_type = models.CharField(choices=ARMOR_TYPE_CHOICES, default='SH')

    def clean(self, *args, **kwargs):
        if self.armor_type != 'SH' and getattr(self, 'armor_class', None) is None:
            raise TypeError("'%s' type armors must be initialized using 'ClassedArmor'")
        super().clean(*args, **kwargs)


class ClassedArmor(Armor):
    ARMOR_CLASS_CHOICES = [
        ('HA', 'Heavy Armor'),
        ('MA', 'Medium Armor'),
        ('LA', 'Light Armor'),
    ]

    armor_class = models.CharField(choices=ARMOR_CLASS_CHOICES)
    enchantments = models.PositiveSmallIntegerField(default=1)


class _BaseCrafting(models.Model):
    name = models.CharField()
    cost = models.PositiveIntegerField()
    description = models.CharField()


class Attachment(_BaseCrafting):
    pass


class Enchantment(_BaseCrafting):
    ENCHANTMENT_TYPE_CHOICES = [
        ('WE', 'Weapon'),
        ('AR', 'Armor'),
    ]

    CRAFTING_SKILL_TYPE_CHOICES = [
        ('TE', 'Technology'),
        ('MA', 'Magic'),
    ]

    enchantment_type = models.CharField(max_length=2, choices=ENCHANTMENT_TYPE_CHOICES)
    crafting_skill = models.CharField(max_length=2, choices=CRAFTING_SKILL_TYPE_CHOICES)
    skill_requirement = models.PositiveSmallIntegerField()
