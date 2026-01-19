from django.db import models


class Team(models.Model):
    """
    Team model representing a tennis team.
    Demonstrates has_many relationship (Team has many Members).

    Rails equivalent:
        class Team < ApplicationRecord
            has_many :members
        end
    """
    name = models.CharField(max_length=255, help_text="Team name")
    description = models.TextField(blank=True, help_text="Team description")
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'


class Member(models.Model):
    """
    Member model representing a tennis club member.

    Demonstrates relationships:
    - belongs_to (ForeignKey to Team)
    - has_one (reverse of Profile's ForeignKey)

    Rails equivalent: app/models/member.rb
    """
    firstname = models.CharField(max_length=255, help_text="Member's first name")
    lastname = models.CharField(max_length=255, help_text="Member's last name")
    email = models.EmailField(unique=True, help_text="Member's email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Member's phone number")
    joined_date = models.DateField(auto_now_add=True, help_text="Date member joined")

    # BELONGS_TO relationship (Many-to-One)
    # Rails: belongs_to :team
    # Django: ForeignKey
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,  # Delete members when team is deleted
        related_name='members',     # Allows: team.members.all()
        null=True,                  # Team is optional
        blank=True,
        help_text="Team this member belongs to"
    )

    def __str__(self):
        """
        String representation of the member.
        Rails equivalent: def to_s
        """
        return f"{self.firstname} {self.lastname}"

    class Meta:
        ordering = ['lastname', 'firstname']
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
        db_table = 'members'


class Profile(models.Model):
    """
    Profile model representing a member's extended profile.

    Demonstrates HAS_ONE relationship (One-to-One).
    Each Member has ONE Profile, each Profile belongs to ONE Member.

    Rails equivalent:
        class Member < ApplicationRecord
            has_one :profile
        end

        class Profile < ApplicationRecord
            belongs_to :member
        end

    Django equivalent:
        Member has_one Profile (accessed via: member.profile)
        Profile belongs_to Member (via OneToOneField)
    """
    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,   # Delete profile when member is deleted
        related_name='profile',      # Allows: member.profile
        help_text="Member this profile belongs to"
    )
    bio = models.TextField(blank=True, help_text="Member biography")
    skill_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('professional', 'Professional'),
        ],
        default='beginner'
    )
    favorite_surface = models.CharField(
        max_length=20,
        choices=[
            ('clay', 'Clay'),
            ('grass', 'Grass'),
            ('hard', 'Hard Court'),
        ],
        blank=True
    )

    def __str__(self):
        return f"Profile for {self.member}"

    class Meta:
        verbose_name = 'Member Profile'
        verbose_name_plural = 'Member Profiles'

