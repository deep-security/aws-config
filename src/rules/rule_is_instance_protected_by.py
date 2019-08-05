from src.rules import CONTROL_NAMES
from src.rules.rule import Rule


class RuleIsInstanceProtectedBy(Rule):
    def _initialize(self):
        super()._initialize()

        self._control = self._rule_parameters.get('dsControl')
        if not self._control:
            raise ValueError('Missing parameter: dsControl')

    @property
    def control(self):
        return self._control

    def _do_check(self, details):
        control_prop = 'overall_{}_status'.format(self._control)
        control_status = getattr(details, control_prop)
        self._check_control(control_status)
        self._compliance_msg = '{} status: {}'.format(CONTROL_NAMES[self._control], control_status)

    def _check_control(self, control_status):
        self._compliance = 'NON_COMPLIANT'
        if self._control in ['anti_malware', 'integrity_monitoring']:
            if 'On, Real Time'.lower() in control_status.lower() or \
                    'On, Security Update In Progress, Real Time'.lower() in control_status.lower():
                self._compliance = 'COMPLIANT'
        elif self._control in ['intrusion_prevention']:
            if 'On, Prevent'.lower() in control_status.lower():
                self._compliance = 'COMPLIANT'
        else:
            if 'On'.lower() in control_status.lower():
                self._compliance = 'COMPLIANT'
