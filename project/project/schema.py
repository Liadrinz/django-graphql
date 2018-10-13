import graphene
import data.schema

class Query(data.schema.Query, graphene.ObjectType):
    pass

class Mutations(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutations)
