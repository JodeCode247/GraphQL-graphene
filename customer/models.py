from django.db import models



class Client(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)


def __str__(self):
    return self.name


class Questions(models.Model):
    text = models.CharField(max_length=300)

    def __str__(self):
        return self.text[:20]

class Options(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='options')
    option_alphabet = models.CharField(max_length=1)  # Stores 'a', 'b', 'c', etc.
    option_text = models.CharField(max_length=300) # Stores the full sentence of the option

    class Meta:
        unique_together = ('question', 'option_alphabet')

    def __str__(self):
        return f"{self.option_alphabet}. {self.option_text[:10]}"


class Answer(models.Model):
    question = models.OneToOneField(Questions, on_delete=models.CASCADE, related_name='correct_answer')
    answer_alphabet = models.CharField(max_length=1)

    def __str__(self):
        return self.answer_alphabet
    

    
