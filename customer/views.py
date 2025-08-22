from django.shortcuts import render
import uuid,json
from .models import ClientQuestions,Client,Questions,Options,Answer
from django.http import JsonResponse
import random

def get_client_question(request):
    question_id = request.session.get('question_id')

    if not question_id:
        question = ClientQuestions.objects.create()
        question_id= question.question_id
        request.session['question_id']= question_id

        return question
    try:
        question=ClientQuestions.objects.get(question_id=question_id)
        if question:
            return question

    except ClientQuestions.DoesNotExist:
        question = ClientQuestions.objects.create()
        question_id= question.question_id
        request.session['question_id']= question_id
        return question


def get_questions():
    list_of_question=Questions.objects.all()
    questions =[]

    for question in list_of_question:
        text = question.text
        id = question.id
        options = [option.option_text for option in question.options.all()]

        context = {'id':id,'text':text,'options': options,}
        questions.append(context)
    return questions


def index(request):
    clientquestion = get_client_question(request)

    if not clientquestion.client:
        client = Client.objects.create(name='anonymous',)
        clientquestion.client=client
        clientquestion.save()     
    client = clientquestion.client
    trial=client.trials
    score=client.score

    questions = get_questions()
    
    random.shuffle(questions)
    return render(request, "customer/question.html", {'trial':trial,'score':score,
        "questions": questions,"clientquestion":clientquestion.question_id[:8],
        "questions_json": json.dumps(questions) 
    })


def submit_quiz(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question_set = data.get("answers", [])
        score = 0
        correct =0

        if question_set:
            for p in question_set:
                question_id = p.get('question_id')
                client_answer= p.get('answer')
                try:
                    q = Questions.objects.get(id=int(question_id))
                    if Answer.objects.get(question=q).answer == client_answer:
                        score+=2
                        correct+=1
                except:
                    return JsonResponse({'error':'Error submitting quiz'},status=400)
            user = get_client_question(request).client
            print(user)
            user.score += score
            user.trials +=1
            user.save()
          
        return JsonResponse({'score':score,"correct":correct})
                

                
            
            

              





    



    
