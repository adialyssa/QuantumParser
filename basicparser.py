""""Digits/valid numbs"""
DIGITS = '0123456789'

"""Errors"""
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f' File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, details, pos_start, pos_end):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, details, pos_start, pos_end):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)


"""Position"""
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


"""Tokens"""
TT_INT = 'TT_INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_EQUALS = 'EQUALS'
TT_EXP = 'EXP'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_GT = 'GT'
TT_LT = 'LT'




class quantum_token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self): # EDITED
        return f'{self.type}:{self.value}' if self.value else f'{self.type}'


class quantum_lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(quantum_token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(quantum_token(TT_MINUS)) 
                self.advance()
            elif self.current_char == '*':
                tokens.append(quantum_token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(quantum_token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(quantum_token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(quantum_token(TT_RPAREN))
                self.advance()
            elif self.current_char == '=':
                tokens.append(quantum_token(TT_EQUALS))
                self.advance()
            elif self.current_char == '^':
                tokens.append(quantum_token(TT_EXP))
                self.advance()
            elif self.current_char == '>':
                tokens.append(quantum_token(TT_GT))
                self.advance()
            elif self.current_char == '<':
                tokens.append(quantum_token(TT_LT))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(f" '{char}' ", pos_start, self.pos)
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        while self.current_char is not None and self.current_char in f'{DIGITS}.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return quantum_token(TT_INT, int(num_str))
        else:
            return quantum_token(TT_FLOAT, float(num_str))


"""Parser and Interpreter"""
class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.token_idx += 1
        self.current_token = self.tokens[self.token_idx] if self.token_idx < len(self.tokens) else None

    def parse(self):
        result = self.expr()
        if self.current_token is not None:
            raise InvalidSyntaxError(
                "Unexpected token", self.current_token.pos_start, self.current_token.pos_end
            )
        return result

    def expr(self):
        left = self.term()
        while self.current_token is not None and self.current_token.type in (TT_PLUS, TT_MINUS):
            token = self.current_token
            self.advance()
            if token.type == TT_PLUS:
                left += self.term()
            elif token.type == TT_MINUS:
                left -= self.term()
        if self.current_token is not None and self.current_token.type == TT_EQUALS:
            self.advance()
            right = self.expr()
            return left == right
        if self.current_token is not None and self.current_token.type in (TT_GT, TT_LT):
            return self.compare(left)
        return left

    def term(self):
        result = self.power()
        while self.current_token is not None and self.current_token.type in (TT_MUL, TT_DIV):
            token = self.current_token
            self.advance()
            if token.type == TT_MUL:
                result *= self.power()
            elif token.type == TT_DIV:
                result /= self.power()
        return result

    def power(self):
        result = self.factor()
        while self.current_token is not None and self.current_token.type == TT_EXP:
            token = self.current_token
            self.advance()
            result **= self.factor()
        return result

    def factor(self):
        token = self.current_token
        self.advance()
        if token.type in (TT_INT, TT_FLOAT):
            return token.value
        elif token.type == TT_LPAREN:
            result = self.expr()
            if self.current_token.type != TT_RPAREN:
                raise InvalidSyntaxError("Expected ')'", token.pos_start, token.pos_end)
            self.advance()
            return result
        else:
            raise InvalidSyntaxError("Expected number or '('", token.pos_start, token.pos_end)

    def compare(self, left):
        token = self.current_token
        self.advance()
        right = self.term()
        if token.type == TT_GT:
            return left > right
        elif token.type == TT_LT:
            return left < right


"""Run"""
def run(fn, text):
    lexer = quantum_lexer(fn, text)
    tokens, error = lexer.make_tokens()

    # Check for lexing errors
    if error: 
        return None, error
    
    # Check if tokens were generated 
    if not tokens:
        return None, Error(
            Position(0, 0, 0, fn, text),
            Position(len(text), 0, len(text), fn, text),
            'Empty Input',
            'No tokens were generated from the input'
        )
    
    try:
        # Initialize interpreter and parse tokens
        interpreter = Interpreter(tokens)
        result = interpreter.parse()
        if isinstance(result, bool):
            result = "True" if result else "False"
        return result, None

    except SyntaxError as e:
        return None, e

    except ZeroDivisionError:
        return None, Error(
            Position(0, 0 ,0, fn, text),
            Position(len(text), 0, len(text), fn, text),
            'Runtime Error',
            'Division by zero'
        )

    except Exception as e:
        return None, Error(
            Position(0, 0, 0, fn, text),
            Position(len(text), 0, len(text), fn, text),
            'Runtime Error',
            str(e)
        ) 
