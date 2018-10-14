import graphene
import data.schema

class Query(graphene.ObjectType):
    pass

class Mutations(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutations)
