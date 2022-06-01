""""
    This dictionary will help us to avoid 
    the strings and set an identifier 
    depending on the token type. (For COCOR)
"""
NodeType = {
    "ID" : 0,
    "LEFT_PARENTHESIS" : "(",
    "RIGHT_PARENTHESIS" : ")",
    "LEFT_BRACKET" : "[",
    "RIGHT_BRACKET" : "]",
    "CONCATENATION" : ":",
    "OR" : "|",
    "LEFT_KLEENE" : "l*",
    "RIGHT_KLEENE" : "r*",
    "UNION" : 9,
    "SUBSTRACTION" : "-",
    "RANGE" : 11,
    "NUMERIC" : 12,
    "CHAR" : 13,
    "STRING" : 14
}
    