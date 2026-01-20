from django.contrib import admin
from .models import Member, Team, Profile, Tournament, Match


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Admin interface for Team model.
    Demonstrates has_many relationship management.
    """
    list_display = ['id', 'name', 'member_count', 'created_date']
    search_fields = ['name', 'description']
    ordering = ['name']

    def member_count(self, obj):
        """Display number of members in the team."""
        return obj.members.count()
    member_count.short_description = 'Members'


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    """
    Admin interface for Tournament model.
    Demonstrates ManyToMany relationship management.

    Note: In Rails you'd define the relationship on BOTH sides.
    In Django, it's defined ONLY on Member model, but works from both sides!
    """
    list_display = ['id', 'name', 'location', 'start_date', 'end_date', 'participant_count']
    list_filter = ['start_date', 'location']
    search_fields = ['name', 'location']
    ordering = ['start_date', 'name']

    def participant_count(self, obj):
        """Display number of participants in the tournament."""
        return obj.members.count()
    participant_count.short_description = 'Participants'


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """
    Admin interface for Member model.
    Rails equivalent: ActiveAdmin.register Member

    Django's admin is built-in - no gems needed!
    """
    list_display = ['id', 'firstname', 'lastname', 'email', 'phone', 'team', 'joined_date']
    list_filter = ['joined_date', 'team']
    search_fields = ['firstname', 'lastname', 'email']
    ordering = ['lastname', 'firstname']
    readonly_fields = ['joined_date']
    filter_horizontal = ['tournaments']  # Nice UI for ManyToMany

    fieldsets = (
        ('Personal Information', {
            'fields': ('firstname', 'lastname')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Team Assignment', {
            'fields': ('team',)
        }),
        ('Tournaments', {
            'fields': ('tournaments',)
        }),
        ('Metadata', {
            'fields': ('joined_date',)
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for Profile model.
    Demonstrates has_one (OneToOne) relationship.
    """
    list_display = ['id', 'member', 'skill_level', 'favorite_surface']
    list_filter = ['skill_level', 'favorite_surface']
    search_fields = ['member__firstname', 'member__lastname', 'bio']

    fieldsets = (
        ('Member', {
            'fields': ('member',)
        }),
        ('Profile Information', {
            'fields': ('bio', 'skill_level', 'favorite_surface')
        }),
    )


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    """
    Admin interface for Match model.

    Demonstrates MULTIPLE FOREIGNKEYS TO THE SAME MODEL.
    Notice how player1, player2, and winner all point to Member,
    but each has a unique related_name to avoid conflicts.

    Rails would require defining all relationships on both sides.
    Django only requires unique related_name on the ForeignKey side.
    """
    list_display = ['id', 'date', 'player1', 'player2', 'winner', 'score_display', 'completed']
    list_filter = ['completed', 'date']
    search_fields = [
        'player1__firstname',
        'player1__lastname',
        'player2__firstname',
        'player2__lastname',
        'location'
    ]
    ordering = ['-date']
    date_hierarchy = 'date'

    fieldsets = (
        ('Match Details', {
            'fields': ('date', 'location')
        }),
        ('Players', {
            'fields': ('player1', 'player2'),
            'description': 'Select the two players for this match. They must be different members.'
        }),
        ('Results', {
            'fields': ('player1_score', 'player2_score', 'winner', 'completed'),
            'description': 'Enter scores and select winner once match is completed.'
        }),
    )

    def score_display(self, obj):
        """Display match score."""
        if obj.player1_score is not None and obj.player2_score is not None:
            return f"{obj.player1_score} - {obj.player2_score}"
        return "Not played yet"
    score_display.short_description = 'Score'


