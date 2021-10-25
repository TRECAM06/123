from Balance_Closures import *
from Lexer import *
from Lexer_Incomplete import *
import token
from typing import List
from AST_Nodes import *
import copy

def find_next_statment(tokens:List[Token]) -> AST_Node:
    
    tokens = copy.deepcopy(tokens)

    statement_tokens = []
    
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

        statement_tokens.append(next_token)

        if len(closure_stack) > 0 and next_token.get_type() == Token_Enum.Line_End.Line_End:
            break

        token_type = next_token.get_type()
        
        # Check if the token is relevant, if not continue 
        if next_token.get_type() not in closure_types+[Token_Enum.Line_End.Line_End]:
            continue
        # Error Conditions
        if closure_stack: # Stack is not empty
            stack_type = closure_stack[-1]

        #Matching Closure Conditions
            if token_type == Token_Enum.Closures.Paren_Close or token_type == Token_Enum.Closures.Curly_Close:
                closure_stack.pop()
            else:
                if token_type != Token_Enum.Line_End.Line_End:
                    closure_stack.append(token_type)
        else: # The Stack is empty
            if token_type in [Token_Enum.Closures.Paren_Open, Token_Enum.Closures.Curly_Open]:
                #raise (Parser_Syntax_Error("SyntaxError: Found {} with no matching open token".format(token_type)))
                closure_stack.append(token_type)


            

def Parse_Blocks(tokens:List[Token]) -> AST_Node:
    pass