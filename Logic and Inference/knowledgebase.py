from read import *
from copy import *

class Fact(object):
    """
        Statement: The content of the fact itself
        FactSupports: List of facts it supports
        RuleSupports: List of rules it supports
    """
    def __init__(self, statement = None, supported_by = []):
        self.statement = statement
        self.fact_supports = []
        self.rule_supports = []
        self.supported_by = supported_by

    def add_fact(self, fact):
        self.fact_supports.append(fact)

    def add_rule(self, rule):
        self.rule_supports.append(rule)

class Rule(object):
    """
        LHS: A list of statements (tests)
        RHS: A single statement
        FactSupports: List of facts it supports
        RuleSupports: List of rules it supports
    """
    def __init__(self, lhs, rhs, supported_by = []):
        self.statement = lhs + rhs
        self.lhs = map(lambda x: Fact(x), lhs)
        self.rhs = Fact(rhs)
        self.fact_supports = []
        self.rule_supports = []
        self.supported_by = supported_by

    def add_fact(self, fact):
        self.fact_supports.append(fact)

    def add_rule(self, rule):
        self.rule_supports.append(rule)

class Kb(object):
    """
     Knowledge Base

        Facts: A list of facts
        Rules: A list of rules
    """
    def __init__(self, tokenized_facts, tokenized_rules):
        self.facts = []
        self.rules = []
        for f in tokenized_facts:
            self.assert_fact(Fact(f))
        for r in tokenized_rules:
            self.assert_rule(Rule(r[0], r[1]))

    def printing(self):
        print "facts:"
        for fact in self.facts:
            print fact.statement
        print
        print "rules:"
        for rule in self.rules:
            print rule.statement


    def assert_fact(self, fact):
        """
            Add a new fact to the KB. It also tests to see if any new facts or rules can be inferred.
        """
        list = map(lambda x: x.statement, self.facts)
        if fact.statement not in list:
            self.facts.append(fact)
            self.fact_infer(fact)

    def fact_infer(self, fact):
        """
            Add new facts and rules inferred from given fact
        """
        for rule in self.rules:
            bindings = match(rule.lhs[0], fact)
            if bindings != False:
                if len(rule.lhs) == 1:
                    new_statement = Fact(instantiate(r.rhs.statement, bindings), [fact, rule])
                    fact.add_fact(new_statement)
                    rule.add_rule(new_statement)
                    self.assert_fact(new_statement)
                else:
                    tests = map(lambda x: instantiate(x.statement, bindings), rule.lhs[1:])
                    rhs = instantiate(rule.rhs.statement, bindings)
                    new_rule = Rule(tests, rhs, [fact, rule])
                    fact.add_rule(new_rule)
                    rule.add_rule(new_rule)
                    self.assert_rule(new_rule)

    def assert_rule(self, rule):
        """
            Add a new rule to the KB. It also tests to see if any new facts or rules can be inferred.
        """
        list = map(lambda x: x.statement, self.rules)
        if rule.statement not in list:
            self.rules.append(rule)
            self.rule_infer(rule)

    def rule_infer(self, rule):
        """
            Add new facts and rules inferred from given rule
        """
        for fact in self.facts:
            bindings = match(rule.lhs[0], fact)
            if bindings != False:
                if len(rule.lhs) == 1:
                    new_statement = Fact(instantiate(rule.rhs.statement, bindings), [rule, fact])
                    fact.add_fact(new_statement)
                    rule.add_fact(new_statement)
                    self.assert_fact(new_statement)
                else:
                    lhs_list = map(lambda x: instantiate(x.statement, bindings), rule.lhs[1:])
                    rhs = instantiate(fact.statement, bindings)
                    new_rule = Rule(lhs_list, rhs, [rule, fact])
                    fact.add_rule(new_rule)
                    rule.add_rule(new_rule)
                    self.assert_rule(new_rule)

    def retract(self, fact):
        # used for retracting the facts it supports
        list = []
        for f in self.facts:
            if f.statement == Fact(fact).statement:
                list.append(f)
                self.facts.remove(f)
        for f in list:
            # retract supporting facts
            for support in f.fact_supports:
                self.retract(support)

    def ask(self, fact):
        """
            Takes a fact and returns the lists of bindings lists that hold if the fact is true in the KB.
        """
        bindings_list = []
        for f in self.facts:
            bindings = match(Fact(fact), f)
            if bindings != False and not(bindings in bindings_list):
                bindings_list.append(bindings)
        return bindings_list

    def ask_plus(self, statements):
        """
            Input: A list of statements
            Action: Test to see if the statements are in the Knowledge Base and are consistent with regard to the bindings
            Returns: A lists of bindings lists based on the matches found
        """
        bindings_lists = []
        for statement in statements:
            if bindings_lists !=[]:
                for pair in map(lambda x:instantiate(statement, x), bindings_lists):
                    for fact in self.facts:
                        bindings = match(Fact(pair[0]), fact)
                        if bindings != False:
                            for key in pair[1]:
                                bindings[key] = pair[1][key]
                            if bindings not in bindings_lists:
                                bindings_lists.append(bindings)
            else:
                for fact in self.facts:
                    bindings = match(Fact(statement), fact)
                    if bindings != False and bindings not in bindings_lists:
                        bindings_lists.append(bindings)
        return bindings_lists

    def why(self, statement):
        """
            Input: A statement
            Action:  Test to see if the statement is in the Knowledge Base
            For each fact that is true, print out the tree of fact/rule justifications for it
            Returns: A list of top level facts that matched
        """
        facts_visited = set()
        result = []
        item = []
        for fact in self.facts:
            if fact.statement == statement:
                facts_visited.add(fact)
                self.why_helper(facts_visited, fact, item, result)
        return result


    def why_helper(self, facts_visited, cur_fact_or_rule, item, result):
        """
            Use dfs as helper function of why
        """
        for fact_or_rule in cur_fact_or_rule.supported_by:
            if fact_or_rule not in facts_visited:
                facts_visited.add(fact_or_rule)
                item.append(fact_or_rule)
                self.why_helper(facts_visited, fact_or_rule, item, result)
                item.pop()
                facts_visited.remove(fact_or_rule)


        if len(item) > 0:
            result.append(deepcopy(item))


def varq(item):
    """
        Determine whether the given item is a variable
    """
    return item[0] == "?"

def match_element(e1, e2, bindings):
    """
        Match each element in statement
    """
    if e1 == e2:
        return bindings
    elif varq(e1):
        bind = bindings.get(e1, False)
        if bind:
            if e2 == bind:
                return bindings
            else:
                return False
        else:
            bindings[e1] = e2
            return bindings
    else:
        return False

def match_args(args1, args2):
    bindings = {}
    for e1, e2 in zip(args1, args2):
        bindings = match_element(e1, e2, bindings)
        if bindings == False:
            return False
    return bindings

def match(statement1, statement2):
    """
        Input: Two statements
        Action: Test to see if they can be interpreted as the same statement
        Returns: The bindings that need to hold is they are interpreted as the same
    """
    s1 = statement1.statement
    s2 = statement2.statement
    if s1[0] != s2[0]:
        return False
    return match_args(s1[1:], s2[1:])

def instantiate(statement, bindings):
    """
        Input: A statement and a list of bindings
        Action: Replace all of the variables with the constants they are bound to
    """
    new_statement = map(lambda x: bindings.get(x, x), statement[1:])
    new_statement.insert(0, statement[0])
    return new_statement

if __name__ == "__main__":
    tokenized_facts, tokenized_rules = read_tokenize("statements.txt")
    kb = Kb(tokenized_facts, tokenized_rules)
    kb.printing()
    print
    print "******************************** Test Ask ********************************"
    ask_statement = ['color','pyramid1','?x']
    bindings_list = kb.ask(ask_statement)
    print "Ask:", ask_statement
    print "Bindings list:", bindings_list

    print
    print "******************************** Test Ask+ ********************************"
    ask_plus_statements = [['inst', '?x', 'pyramid'],['color', '?x', 'green']]
    bindings_lists = kb.ask_plus(ask_plus_statements)
    print "Ask+:", ask_plus_statements
    print "Bindings lists:", bindings_lists

    print
    print "******************************** Test Retract ********************************"
    retract_statement = ['isa','cube','block']
    kb.retract(retract_statement)
    print "After retracting", retract_statement
    kb.printing()

    print
    print "******************************** Test Why ********************************"
    why_statement = ['flat', 'cube4']
    print "Why?", why_statement
    result = kb.why(why_statement)
    for facts in result:
        for fact in facts:
            print fact.statement
