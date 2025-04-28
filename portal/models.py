from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class LostFoundItem(models.Model):
    ITEM_TYPES = (
        ('Lost', 'Lost'),
        ('Found', 'Found'),
    )

    name = models.CharField(max_length=100 , default='Unnamed Item')
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    item_type = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    date = models.DateField()
    image = models.ImageField(upload_to='item_images/')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item_type} - {self.title}"
class ClaimDetail(models.Model):
    item = models.OneToOneField(LostFoundItem, on_delete=models.CASCADE)
    claimant_name = models.CharField(max_length=100)
    year = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    usn = models.CharField(max_length=20)
    claimed_at = models.DateTimeField(auto_now_add=True)
    is_claimed = models.BooleanField(default=False)

    def __str__(self):
        return f"Claim for {self.item.title} by {self.claimant_name}"
