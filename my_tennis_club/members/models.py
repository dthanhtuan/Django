from django.db import models


class Member(models.Model):
    """
    Member model representing a tennis club member.
    Rails equivalent: app/models/member.rb
    """
    firstname = models.CharField(max_length=255, help_text="Member's first name")
    lastname = models.CharField(max_length=255, help_text="Member's last name")
    email = models.EmailField(unique=True, help_text="Member's email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Member's phone number")
    joined_date = models.DateField(auto_now_add=True, help_text="Date member joined")

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
