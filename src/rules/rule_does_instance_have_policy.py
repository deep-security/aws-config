from src.rules.rule import Rule


class RuleDoesInstanceHavePolicy(Rule):
    def _initialize(self):
        super()._initialize()

        self._policy = self._rule_parameters.get('dsPolicy')
        if not self._policy:
            raise ValueError('Missing parameter: dsPolicy')

    @property
    def policy(self):
        return self._policy

    def _do_check(self, details):
        self._compliance = 'COMPLIANT' if details.policy_name.lower() == self._policy.lower() else 'NON_COMPLIANT'
        self._compliance_msg = 'Current policy: {}'.format(details.policy_name)
