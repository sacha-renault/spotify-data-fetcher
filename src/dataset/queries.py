class MongoQuery:
    """
    Helper class for MongoDB query operators.
    
    Example Usage:
    
    >>> query = {"field": {MongoQuery.IN: [v1, v2, v3]}}
    >>> query = {"age": {MongoQuery.GT: 21}}
    >>> query = {MongoQuery.OR: [
            {"age": {MongoQuery.LT: 21}},
            {"status": "student"}
        ]}
    """
    
    # Comparison Operators
    EQ = "$eq"
    """Equal: Matches values that are equal to the specified value."""
    
    NE = "$ne"
    """Not Equal: Matches all values that are not equal to the specified value."""
    
    GT = "$gt"
    """Greater Than: Matches values that are greater than the specified value."""
    
    GTE = "$gte"
    """Greater Than or Equal: Matches values that are greater than or equal to the specified value."""
    
    LT = "$lt"
    """Less Than: Matches values that are less than the specified value."""
    
    LTE = "$lte"
    """Less Than or Equal: Matches values that are less than or equal to the specified value."""
    
    IN = "$in"
    """In: Matches any of the values specified in an array."""
    
    NIN = "$nin"
    """Not In: Matches none of the values specified in an array."""
    
    # Logical Operators
    AND = "$and"
    """Logical AND: Joins query clauses with a logical AND returns all documents that match the conditions of both clauses."""
    
    OR = "$or"
    """Logical OR: Joins query clauses with a logical OR returns all documents that match the conditions of either clause."""
    
    NOT = "$not"
    """Logical NOT: Inverts the effect of a query expression and returns documents that do not match the query expression."""
    
    NOR = "$nor"
    """Logical NOR: Joins query clauses with a logical NOR returns all documents that fail to match both clauses."""
    
    # Element Operators
    EXISTS = "$exists"
    """Exists: Matches documents that have the specified field."""
    
    TYPE = "$type"
    """Type: Selects documents if a field is of the specified type."""
    
    # Array Operators
    ALL = "$all"
    """All: Matches arrays that contain all elements specified in the query."""
    
    SIZE = "$size"
    """Size: Matches any array with the specified number of elements."""
    
    # Text Search Operators
    TEXT = "$text"
    """Text: Performs a text search on the content of the fields indexed with a text index."""
    
    # Modifiers
    REGEX = "$regex"
    """Regular Expression: Provides regular expression capabilities for pattern matching strings in queries."""
    
    OPTIONS = "$options"
    """Options: Specifies options for regular expression searches, such as case insensitivity."""