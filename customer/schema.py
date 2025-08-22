import graphene 
from graphene_django import DjangoObjectType ,DjangoListField 
from .models import Client,Questions,Options,Answer
from graphql import GraphQLError

class ClientType(DjangoObjectType):
    class Meta:
        model = Client
        fields = '__all__'


class QuestionType(DjangoObjectType):
     class Meta:
        model = Questions
        fields = '__all__'

class AnswerType(DjangoObjectType):
     class Meta:
        model = Answer
        fields = '__all__'

  
class OptionsType(DjangoObjectType):
     class Meta:
        model = Options
        fields = '__all__'




class Query(graphene.ObjectType):
    all_questions = graphene.List(QuestionType)
    all_options = graphene.List(OptionsType)
    question = graphene.Field(QuestionType, id=graphene.Int())
    options = graphene.Field(OptionsType,id=graphene.Int())
    # client = graphene.List(ClientType,args=graphene.Boolean())


    def resolve_all_questions(root, info):
        return Questions.objects.all()
    

    def resolve_question(root, info, id):
        try:
            return Questions.objects.get(id=id)
        
        except Questions.DoesNotExist:
            return None
        
    def resolve_options(root, info, id):
        try:
            return Options.objects.get(id=id)
        
        except Options.DoesNotExist:
            return None
    def resolve_all_options(root, info):
        try:
            return Options.objects.all()
        
        except Options.DoesNotExist:
            return None

    def resolve_clients(root, info,args):
        print(Client.objects.filter(paid=args))
        return Client.objects.filter(paid=args)


class CreateQuestionInput(graphene.InputObjectType):
    text = graphene.String(required=True)

# Define the mutation itself
class CreateQuestion(graphene.Mutation):
    class Arguments:
        input = CreateQuestionInput(required=True)

    # What the mutation returns
    Output = QuestionType

    # The logic to perform the mutation
    def mutate(root, info, input):
        question = Questions(text=input.text)
        question.save()
        return question

class UpdateQuestionInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    text = graphene.String(required=True)

class UpdateQuestion(graphene.Mutation):
    class Arguments:
        input = UpdateQuestionInput(required=True)

    # What the mutation returns
    Output = QuestionType

    def mutate(root, info, input):
        try:
            question = Questions.objects.get(id=input.id)
            question.text= input.text
            question.save()
            return question
        except:
            raise GraphQLError('INVALID ID')






class AnswerQuestionPayload(graphene.ObjectType):
    client = graphene.Field(ClientType)
    question = graphene.Field(QuestionType)
    correct = graphene.Boolean()
    message = graphene.String()

class AnswerQuestionInput(graphene.InputObjectType):
    examid = graphene.ID(required=True)
    answer = graphene.String(required=True)
    clientid = graphene.ID(required=True)
    
class AnswerQuestion(graphene.Mutation):
    class Arguments:
        input = AnswerQuestionInput(required=True)

    Output = AnswerQuestionPayload

    def mutate(root, info, input):
        try:
            client = Client.objects.get(id=input.clientid)
            question = Questions.objects.get(id=input.examid)
            correct_answer = Answer.objects.get(question=question).answer_alphabet

            if correct_answer == input.answer:
                client.score += 2
                client.save()
                return AnswerQuestionPayload(
                    client=client,
                    question=question,
                    correct=True,
                    message="You are correct!"
                )
            else:
                return AnswerQuestionPayload(
                    client=client,
                    question=question,
                    correct=False,
                    message=f'Correct answer is "{correct_answer}", you chose "{input.answer}"'
                )
        except Client.DoesNotExist:
            raise GraphQLError('INVALID CLIENT ID')
        except Questions.DoesNotExist:
            raise GraphQLError('INVALID QUESTION ID')
        except Answer.DoesNotExist:
            raise GraphQLError('NO ANSWER FOUND FOR QUESTION')
# Add the mutation to your main Mutation class
class Mutation(graphene.ObjectType):
    addquestion = CreateQuestion.Field()
    updateQuestion = UpdateQuestion.Field()
    answerQuestion = AnswerQuestion.Field()

# Update your schema to include the mutation
schema = graphene.Schema(query=Query, mutation=Mutation)