from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Ticket_Model(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    section = models.CharField(max_length=1, choices=(('A','Section A'),('B','Section B')))
    seat = models.IntegerField()
    price_paid = models.IntegerField(default=20)
    from_location = models.CharField(max_length=50,default='London')
    to_location = models.CharField(max_length=50,default='France')


    def __str__(self):
        return f"Ticket_Model #{self.pk} - {self.user} - Section : {self.section} - Seat : {self.seat}"

