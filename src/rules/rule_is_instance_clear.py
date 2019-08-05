from src.rules.rule import Rule


class RuleIsInstanceClear(Rule):
    def _do_check(self, details):
        self._compliance = 'COMPLIANT' if details.computer_light.lower() == 'green' else 'NON_COMPLIANT'
        self._compliance_msg = 'Current status: {}'.format(details.computer_light)
