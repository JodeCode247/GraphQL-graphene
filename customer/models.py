from django.db import models
import uuid



class Client(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    trials = models.IntegerField(default=0)
    is_verify = models.BooleanField(default=True)


    def __str__(self):
        return self.name

# class Failed_Question(models.Model):
    



class ClientQuestions(models.Model):
    client = models.OneToOneField(Client,on_delete=models.CASCADE,blank=True,null=True,related_name='cq')
    question_id = models.CharField(max_length=100,blank=True,null=True,unique=True)


    def save(self,*args, **kwargs):
        if not self.pk:
            question_id = str(uuid.uuid4())
            while ClientQuestions.objects.filter(question_id=question_id).exists():
                question_id = str(uuid.uuid4())
            self.question_id = question_id
        
        super().save(*args, **kwargs)




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
    answer = models.CharField(max_length=300,null=True)

    def __str__(self):
        return self.answer
    

    
