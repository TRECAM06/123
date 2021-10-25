from Lexer import *
from Lexemes import *
from Token import Token
from typing import List
import copy


class Parser_Syntax_Error(BaseException):
    """Exception raised because the Parser found a Syntax Error

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        self.message = message


def Balance_Closures(tokens:List[Token]) -> None:
    tokens = copy.deepcopy(tokens)

    

    closure_types = [
        Token_Enum.Closures.Paren_Close,
        Token_Enum.Closures.Paren_Open,
        Token_Enum.Closures.Curly_Open,
        Token_Enum.Closures.Curly_Close,
    ]
    #NOs' (() , (;
    closure_stack = []

    while tokens:
        next_token = tokens.pop(0)

        token_type = next_token.get_type()
        # Check if the token is relevant, if not continue 
        if next_token.get_type() not in closure_types+[Token_Enum.Line_End.Line_End]:
            continue
        # Error Conditions
        if closure_stack: # Stack is not empty
            stack_type = closure_stack[-1]

            if stack_type == Token_Enum.Closures.Paren_Open and token_type == Token_Enum.Closures.Curly_Close:
                raise(Parser_Syntax_Error("SyntaxError: ( cannot match with } "))
            if stack_type == Token_Enum.Closures.Curly_Open and token_type == Token_Enum.Closures.Paren_Close:
                raise(Parser_Syntax_Error("SyntaxError: { cannot match with ) "))
            if stack_type == Token_Enum.Closures.Paren_Open:
                if token_type == Token_Enum.Line_End.Line_End :
                    raise(Parser_Syntax_Error("SyntaxError: Line end before matching ) "))
                if token_type == Token_Enum.Closures.Curly_Open :
                    raise(Parser_Syntax_Error("SyntaxError: Found { following unclosed (\n\t statements cannot be included inside expressions "))

        #Matching Closure Conditions
            if token_type == Token_Enum.Closures.Paren_Close or token_type == Token_Enum.Closures.Curly_Close:
                closure_stack.pop()
            else:
                if token_type != Token_Enum.Line_End.Line_End:
                    closure_stack.append(token_type)
        else: # The Stack is empty
            if token_type in [Token_Enum.Closures.Paren_Close, Token_Enum.Closures.Curly_Close]:
                raise (Parser_Syntax_Error("SyntaxError: Found {} with no matching open token".format(token_type)))
            elif token_type in [Token_Enum.Closures.Paren_Open, Token_Enum.Closures.Curly_Open]:
                closure_stack.append(token_type)
            
    if closure_stack:
        raise (Parser_Syntax_Error("SyntaxError: Found the following unmatched {} ".format(closure_stack)))