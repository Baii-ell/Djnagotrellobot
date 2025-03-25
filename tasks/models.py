from django.db import models






class User(models.Model):
    tg_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=55)

    def __str__(self):
        return f"User {self.tg_id} - {self.name}"



class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name





class Task(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reach_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    done = models.BooleanField(default=False)

    @property
    def is_completed(self):
        return self.done

    def __str__(self):
        return self.name