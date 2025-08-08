import graphene 
from graphene_django import DjangoObjectType ,DjangoListField
from .models import Client,Questions,Options,Answer

# class ClientType(DjangoObjectType):
#     class Meta:
#         model = Client
#         fields = '__all__'




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

    def resolve_clients(root, info,args):
        print(Client.objects.filter(paid=args))
        return Client.objects.filter(paid=args)




# Define the input for our mutation
class CreateQuestionInput(graphene.InputObjectType):
    text = graphene.String(required=True)
    # You'd likely add more fields for options here in a full app

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

# Add the mutation to your main Mutation class
class Mutation(graphene.ObjectType):
    create_question = CreateQuestion.Field()

# Update your schema to include the mutation
schema = graphene.Schema(query=Query, mutation=Mutation)