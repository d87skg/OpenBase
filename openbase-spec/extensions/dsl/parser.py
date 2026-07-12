from .lexer import Token

class ASTNode:
    pass

class RuleNode(ASTNode):
    def __init__(self, name, trigger, conditions, invariants, action):
        self.name = name
        self.trigger = trigger
        self.conditions = conditions
        self.invariants = invariants
        self.action = action

class ConditionNode(ASTNode):
    def __init__(self, type, value):
        self.type = type
        self.value = value

class InvariantNode(ASTNode):
    def __init__(self, type, args):
        self.type = type
        self.args = args

class ActionNode(ASTNode):
    def __init__(self, type, payload):
        self.type = type
        self.payload = payload

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def next_token(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, type):
        tok = self.next_token()
        if tok.type != type:
            raise SyntaxError(f"Expected {type}, got {tok.type}")
        return tok

    def parse(self):
        rules = []
        while self.peek().type != 'EOF':
            rules.append(self.parse_rule())
        return rules

    def parse_rule(self):
        self.expect('RULE')
        name = self.expect('IDENTIFIER').value
        self.expect('COLON')
        self.expect('WHEN')
        trigger = self.expect('IDENTIFIER').value
        conditions = []
        invariants = []
        action = None

        while self.peek().type != 'THEN':
            if self.peek().type == 'IF':
                self.next_token()
                conditions = self.parse_conditions()
            elif self.peek().type == 'REQUIRE':
                self.next_token()
                invariants = self.parse_invariants()
            else:
                raise SyntaxError(f"Unexpected token {self.peek().type} in rule body")

        self.expect('THEN')
        action = self.parse_action()
        return RuleNode(name, trigger, conditions, invariants, action)

    def parse_conditions(self):
        conds = []
        while True:
            if self.peek().type == 'EXISTS':
                self.next_token()
                conds.append(self.parse_exists())
            elif self.peek().type == 'TRUST_THRESHOLD':
                # 简化处理
                pass
            # 可扩展更多条件类型
            if self.peek().type in ('AND', 'OR'):
                self.next_token()
                continue
            break
        return conds

    def parse_exists(self):
        # exists Evidence BEFORE timestamp
        obj = self.expect('IDENTIFIER').value
        if self.peek().type == 'BEFORE':
            self.next_token()
            time = self.expect('IDENTIFIER').value
            return ConditionNode('EXISTS_EVIDENCE', {'object': obj, 'time': time})
        else:
            return ConditionNode('EXISTS_EVIDENCE', {'object': obj})

    
    def parse_invariants(self):
        invs = []
        while True:
            if self.peek().type == 'IDENTIFIER':
                name = self.next_token().value
                if name == 'TrustStable':
                    self.expect('LPAREN')
                    tok = self.next_token()
                    # 处理数字（可能是 NUMBER 或 IDENTIFIER）
                    if tok.type == 'NUMBER':
                        window = tok.value
                    elif tok.type == 'IDENTIFIER':
                        try:
                            window = int(tok.value)
                        except ValueError:
                            raise SyntaxError(f'Expected number, got {tok.value}')
                    else:
                        raise SyntaxError(f'Expected number, got {tok.type}')
                    self.expect('RPAREN')
                    invs.append(InvariantNode('STABILITY_WINDOW', {'window': window}))
                elif name == 'no':
                    self.next_token()
                    self.expect('IDENTIFIER')
                    invs.append(InvariantNode('NO_CONFLICT', {}))
            if self.peek().type in ('AND', 'OR'):
                self.next_token()
                continue
            break
        return invs
def parse_action(self):
        tok = self.next_token()
        if tok.type == 'ACTION_ACCEPT':
            return ActionNode('ACCEPT', {})
        elif tok.type == 'ACTION_REJECT':
            self.expect('LPAREN')
            reason = self.expect('STRING').value
            self.expect('RPAREN')
            return ActionNode('REJECT', {'reason': reason})
        elif tok.type == 'ACTION_REWRITE':
            self.expect('LPAREN')
            sugg = self.expect('STRING').value
            self.expect('RPAREN')
            return ActionNode('REWRITE', {'suggestion': sugg})
        else:
            raise SyntaxError(f"Unexpected action token {tok.type}")
