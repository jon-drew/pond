from graphql import GraphQLError
from graphql.validation import ValidationRule


class DisableIntrospection(ValidationRule):
    """Blocks introspection queries in production (graphql-core 2.x compatible)."""

    def enter_field(self, node, *args):
        if node.name.value.startswith('__'):
            self.report_error(
                GraphQLError('Introspection is disabled in production.')
            )
