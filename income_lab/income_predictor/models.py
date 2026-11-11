from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()   # eg User(id=3, username="alice")

class Scoreboard(models.Model):
    # user cols
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,   # If the user gets deleted all their game rounds get deleted too
        related_name='game_rounds'
    )
    user_guess = models.CharField(max_length=10)
    user_correct = models.BooleanField()

    # AI cols
    ai_guess = models.CharField(max_length=10)
    ai_confidence = models.FloatField()
    ai_correct = models.BooleanField()

    # game cols
    played_at = models.DateTimeField(auto_now_add=True)
    round_num = models.IntegerField()

    # test subject cols
    the_answer = models.CharField(max_length=40)
    age = models.IntegerField()
    workclass = models.CharField(max_length=40)
    education = models.CharField(max_length=40)
    marital_status = models.CharField(max_length=40)
    occupation = models.CharField(max_length=40)
    relationship = models.CharField(max_length=40)
    race = models.CharField(max_length=10)
    sex = models.CharField(max_length=10)
    hours_per_week = models.IntegerField()
    native_country = models.CharField(max_length=40)
    capital_net = models.FloatField()


    # to control how each row is displayed in panels
    def __str__(self):
        return f'Username: {self.user.username}, Round: {self.round_num}, {self.played_at}'