import re
from typing import List, Tuple

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, {self.line}, {self.column})"

class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def tokenize(self):
        while self.pos < len(self.source):
            ch = self.source[self.pos]

            # 跳过空白
            if ch.isspace():
                if ch == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1
                continue

            # 注释
            if ch == '#' and self.pos + 1 < len(self.source) and self.source[self.pos+1] == '#':
                self.pos += 2
                self.column += 2
                while self.pos < len(self.source) and self.source[self.pos] != '\n':
                    self.pos += 1
                    self.column += 1
                continue

            # 数字（支持整数）
            if ch.isdigit():
                start = self.pos
                while self.pos < len(self.source) and self.source[self.pos].isdigit():
                    self.pos += 1
                value = self.source[start:self.pos]
                self.tokens.append(Token('NUMBER', int(value), self.line, self.column))
                self.column += len(value)
                continue

            # 标识符（关键字或变量）
            if ch.isalpha() or ch == '_':
                start = self.pos
                while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                    self.pos += 1
                value = self.source[start:self.pos]
                token_type = self._keyword_type(value)
                self.tokens.append(Token(token_type, value, self.line, self.column))
                self.column += len(value)
                continue

            # 字符串 (双引号)
            if ch == '"':
                start = self.pos + 1
                self.pos += 1
                self.column += 1
                while self.pos < len(self.source) and self.source[self.pos] != '"':
                    self.pos += 1
                    self.column += 1
                if self.pos < len(self.source):
                    value = self.source[start:self.pos]
                    self.tokens.append(Token('STRING', value, self.line, self.column))
                    self.pos += 1
                    self.column += 1
                continue

            # 操作符
            if ch == ':':
                self.tokens.append(Token('COLON', ':', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue
            if ch == '=':
                self.tokens.append(Token('EQUALS', '=', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue
            if ch == ';':
                self.tokens.append(Token('SEMICOLON', ';', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue
            if ch == '{':
                self.tokens.append(Token('LBRACE', '{', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue
            if ch == '}':
                self.tokens.append(Token('RBRACE', '}', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue
            if ch == '(':
                self.tokens.append(Token('LPAREN', '(', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue
            if ch == ')':
                self.tokens.append(Token('RPAREN', ')', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue
            if ch == ',':
                self.tokens.append(Token('COMMA', ',', self.line, self.column))
                self.pos += 1
                self.column += 1
                continue

            # 未知字符
            raise SyntaxError(f"Unexpected character '{ch}' at line {self.line}, column {self.column}")

        self.tokens.append(Token('EOF', None, self.line, self.column))
        return self.tokens

    def _keyword_type(self, word):
        keywords = {
            'rule': 'RULE',
            'when': 'WHEN',
            'if': 'IF',
            'require': 'REQUIRE',
            'then': 'THEN',
            'ACCEPT': 'ACTION_ACCEPT',
            'REJECT': 'ACTION_REJECT',
            'REWRITE': 'ACTION_REWRITE',
            'exists': 'EXISTS',
            'and': 'AND',
            'or': 'OR',
            'not': 'NOT',
            'BEFORE': 'BEFORE',
            'AFTER': 'AFTER',
            'True': 'BOOLEAN',
            'False': 'BOOLEAN',
        }
        return keywords.get(word, 'IDENTIFIER')
