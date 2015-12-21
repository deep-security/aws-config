# AWS Config Rules for Deep Security

A set of AWS Config Rules to help ensure that your AWS deployments are leveraging the protection of Deep Security. These rules help centralize your compliance information in one place, AWS Config.

## Rules

### ds-IsInstanceProtectedByAntiMalware

Checks to see if the current instance is protected by Deep Security's anti-malware controls. Anti-malware must be "on" and in "real-time" mode for rule to be considered compliant.

#### Rule Parameters:

<table>
<tr>
  <th>Rule Parameter</th>
  <th>Expected Value Type</th>
  <th>Description</th>
</tr>
<tr>
  <td>dsUsername</td>
  <td>string</td>
  <td>The username of the Deep Security account to use for querying anti-malware status</td>
</tr>
<tr>
  <td>dsPassword</td>
  <td>string</td>
  <td>The password for the Deep Security account to use for querying anti-malware status. This password is readable by any identity that can access the AWS Lambda function. Use only the bare minimum permissions within Deep Security (see note below)</td>
</tr>
<tr>
  <td>dsTenant</td>
  <td>string</td>
  <td><i>Optional as long as dsHostname is specified</i>. Indicates which tenant to sign into within Deep Security</td>
</tr>
<tr>
  <td>dsHostname</td>
  <td>string</td>
  <td><i>Optional as long as dsTenant is specified</i>. Defaults to Deep Security as a Service. Indicates which Deep Security manager the rule should sign into</td>
</tr>
</table>

During execution, this rule sign into the Deep Security API. You should setup a dedicated API access account to do this. Deep Security contains a robust role-based access control (RBAC) framework which you can use to ensure that this set of credentials has the least amount of privileges to success. 

This rule requires view access to one or more computers within Deep Security.


### ds-IsInstanceProtectedBy

Checks to see if the current instance is protected by any of Deep Security's controls. Controls must be "on" and set to their strongest setting (a/k/a "real-time" or "prevention") in order for the rule to be considered compliant.

This is the generic version of *ds-IsInstanceProtectedByAntiMalware*.

#### Rule Parameters:

<table>
<tr>
  <th>Rule Parameter</th>
  <th>Expected Value Type</th>
  <th>Description</th>
</tr>
<tr>
  <td>dsUsername</td>
  <td>string</td>
  <td>The username of the Deep Security account to use for querying anti-malware status</td>
</tr>
<tr>
  <td>dsPassword</td>
  <td>string</td>
  <td>The password for the Deep Security account to use for querying anti-malware status. This password is readable by any identity that can access the AWS Lambda function. Use only the bare minimum permissions within Deep Security (see note below)</td>
</tr>
<tr>
  <td>dsTenant</td>
  <td>string</td>
  <td><i>Optional as long as dsHostname is specified</i>. Indicates which tenant to sign into within Deep Security</td>
</tr>
<tr>
  <td>dsHostname</td>
  <td>string</td>
  <td><i>Optional as long as dsTenant is specified</i>. Defaults to Deep Security as a Service. Indicates which Deep Security manager the rule should sign into</td>
</tr>
<tr>
  <td>dsControl</td>
  <td>string</td>
  <td>The name of the control to verify. Must be one of [ anti_malware, web_reputation, firewall, intrusion_prevention, integrity_monitoring, log_inspection ]</td>
</tr>
</table>

During execution, this rule sign into the Deep Security API. You should setup a dedicated API access account to do this. Deep Security contains a robust role-based access control (RBAC) framework which you can use to ensure that this set of credentials has the least amount of privileges to success. 

This rule requires view access to one or more computers within Deep Security.