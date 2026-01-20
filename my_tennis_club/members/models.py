from django.db import models


class Team(models.Model):
    """
    Team model representing a tennis team.
    Demonstrates has_many relationship (Team has many Members).

    Rails equivalent:
        class Team < ApplicationRecord
            has_many :members
        end

    IMPORTANT: In Django, you only define the relationship on ONE side.
    The reverse relationship (Team.members) is created automatically.
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


class Tournament(models.Model):
    """
    Tournament model representing a tennis tournament.
    Demonstrates ManyToMany relationship.

    Rails equivalent:
        class Tournament < ApplicationRecord
            has_many :tournament_registrations
            has_many :members, through: :tournament_registrations
        end

        class Member < ApplicationRecord
            has_many :tournament_registrations
            has_many :tournaments, through: :tournament_registrations
        end

    IMPORTANT: In Django, ManyToMany is defined on ONE side only.
    Both directions work automatically!
    """
    name = models.CharField(max_length=255, help_text="Tournament name")
    location = models.CharField(max_length=255, help_text="Tournament location")
    start_date = models.DateField(help_text="Tournament start date")
    end_date = models.DateField(help_text="Tournament end date")

    # ManyToMany can be defined on either side
    # We'll define it on Member model instead (see below)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['start_date', 'name']
        verbose_name = 'Tournament'
        verbose_name_plural = 'Tournaments'


class Member(models.Model):
    """
    Member model representing a tennis club member.

    Demonstrates relationships:
    - belongs_to (ForeignKey to Team)
    - has_one (reverse of Profile's OneToOneField)
    - has_many :through (ManyToManyField to Tournament)

    Rails equivalent: app/models/member.rb

    IMPORTANT DIFFERENCE FROM RAILS:
    In Rails, you define relationships on BOTH models:
        class Member
            has_one :profile
            belongs_to :team
        end
        class Profile
            belongs_to :member
        end

    In Django, you define on ONE side only - Django creates the reverse automatically!
    """
    firstname = models.CharField(max_length=255, help_text="Member's first name")
    lastname = models.CharField(max_length=255, help_text="Member's last name")
    email = models.EmailField(unique=True, help_text="Member's email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Member's phone number")
    joined_date = models.DateField(auto_now_add=True, help_text="Date member joined")

    # BELONGS_TO relationship (Many-to-One)
    # Rails: belongs_to :team (defined in Member model)
    # Django: ForeignKey (defined ONLY in Member model)
    # Reverse: team.members.all()
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,  # Delete members when team is deleted
        related_name='members',     # Allows: team.members.all()
        null=True,                  # Team is optional
        blank=True,
        help_text="Team this member belongs to"
    )

    # HAS_MANY :THROUGH relationship (Many-to-Many)
    # Rails: has_many :tournaments, through: :tournament_registrations
    # Django: ManyToManyField (defined ONLY on ONE side - we chose Member)
    # Reverse: tournament.members.all() works automatically!
    tournaments = models.ManyToManyField(
        Tournament,
        related_name='members',     # Allows: tournament.members.all()
        blank=True,
        help_text="Tournaments this member is participating in"
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
            has_one :profile      # ← Defined in Member
        end

        class Profile < ApplicationRecord
            belongs_to :member    # ← Defined in Profile
        end

    Django equivalent (DIFFERENT!):
        class Member(models.Model):
            # NO profile field defined here!
            pass

        class Profile(models.Model):
            member = models.OneToOneField(Member, ...)  # ← Defined ONLY here

    This ONE definition in Profile creates BOTH:
        - profile.member (forward)
        - member.profile (reverse)
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

