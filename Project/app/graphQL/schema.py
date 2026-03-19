import graphene

from app.graphQL.query import Query
from app.graphQL.mutations import Mutation


schema = graphene.Schema(query=Query, mutation=Mutation)
