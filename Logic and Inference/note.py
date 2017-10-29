from read import *

class fact(object):
    """
        Fact

            Statement: The content of the fact itself
            Supported By: List of fact/rule pairs that support it
            Asserted: (T/F)
            FactSupports: List of facts it supports
            RuleSupports: List of rules it supports
    """
    def __init__(self, statement = None, supported_by = []):
        self.statement = statement
        self.supported_by = supported_by
        if not supported_by:
            self.asserted = True
        else:
            self.asserted = False
        self.fact_supports = []
        self.rule_supports = []

class rule(object):
    """
    Rule

        LHS: A list of statements (tests)
        RHS: A single statement
        Supported By: List of fact/rule pairs that support it
        Asserted: (T/F)
        FactSupports: List of facts it supports
        RuleSupports: List of rules it supports
    """
    def __init__(self, rule, supported_by = []):
        self.lhs = rule[0]
        self.rhs = rule[1]
        self.supported_by = supported_by
        if not supported_by:
            self.asserted = True
        else:
            self.asserted = False
        self.fact_supports = []
        self.rule_supports = []

class kb(object):
    """
     Knowledge Base

        Facts: A list of facts
        Rules: A list of rules
    """
    def __init__(self):
        self.facts = []
        self.rules = []

    def add_fact(self, fact):
        self.facts.append(fact)

    def remove_fact(self, fact):
        self.facts.remove(fact)

    def add_rule(self, rule):
        self.rules.append(rule)

    def remove_rule(self, rule):
        self.rules.remove(rule)

    def kb_assert(self, statement):
        # assume statement is a fact
        f = fact(statement)
        self.add_fact(f)

def add_binding(bindings, variable, constant):
    bindings.append([variable, constant])

# def binding_val(bindings, variable):
#     for b in bindings:
#         if b[0] == variable:
#             return b[1]
#     return None

def find_binding(bindings, variable, constant):
    for b in bindings:
        if b == [variable, constant]:
            return bindings
    for b in bindings:
        if b[0] == variable:
            add_binding(bindings, variable, constant)
            return bindings

def match(statement1, statement2):
    """
    Match

        Input: Two statements
        Action: Test to see if they can be interpreted as the same statement
        Returns: The bindings that need to hold is they are interpreted as the same
    """
    if len(statement1) != len(statement2):
        return False
    if statement1[0] != statement2[0]:
        return False
    bindings = []
    for index in range(len(statement1)):
        if statement1[index][0] == '?':
            if statement2[index] == binding_val(bindings, statement1[index]):
                return True
            else:
                add_binding(bindings, statement1[index], statement2[index])
    return False

facts, rules = read_tokenize("statements.txt")
print facts
print rules

# f1 = fact(['isa', 'cube', 'block'])
# # print f1.statement
# # print f1.supported_by
# # print f1.asserted
# # print f1.fact_supports
# # print f1.rule_supports
#
# kb1 = kb()
# kb1.kb_assert(['isa', 'cube', 'block'])
# print kb1.facts
# print kb1.rules
