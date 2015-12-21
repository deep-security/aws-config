# AWS Config Rules for Deep Security

A set of AWS Config Rules to help ensure that your AWS deployments are leveraging the protection of Deep Security. These rules help centralize your compliance information in one place, AWS Config.

## Permissions In Deep Security

Deep Security has a strong role-based access control (RBAC) system built-in. In order for these AWS Lambda functions to query Deep Security, they require credentials to sign in.

Here's the recommend configuration in order to implement this with the least amount of privileges possible within Deep Security.

### User

1. Create a new User with a unique, meaningful name (Administration > User Manager > Users > New...)
1. Set a unique, complex password
1. Fill in other details as desired

### Role

1. Create a new Role with a unique, meaningful name  (Administration > User Manager > Roles > New...)
1. Under "Access Type", check "Allow Access to web services API"
1. Under "Access Type", **uncheck** "Allow Access to Deep Security Manager User Interface"
1. On the "Computer Rights" tab, select either "All Computers" or "Selected Computers:" ensuring that only the greyed out "View" right (under "Allow Users to:") is selected
1. On the "Policy Rights" tab, select "Selected Policies" and ensure that no policies are selected (this makes sure the role grants no rights to user for any policies)
1. On the "User Rights" tab, ensure that "Change own password and contact information only" is selected
1. On the "Other Rights" tab, ensure that the default options remain with only "View-Only" and "Hide" assigned as permissions

With the new User and new Role in place. Make sure you assign the Role to the user. This will ensure that your API access has the minimal permissions possible which reduces the risk if the credentials are exposed. 

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

### ds-DoesInstanceHavePolicy

Checks to see if the current instance is protected by a specific Deep Security policy.

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
  <td>dsPolicy</td>
  <td>string</td>
  <td>The name of the policy to verify</td>
</tr>
</table>

During execution, this rule sign into the Deep Security API. You should setup a dedicated API access account to do this. Deep Security contains a robust role-based access control (RBAC) framework which you can use to ensure that this set of credentials has the least amount of privileges to success. 

This rule requires view access to one or more computers within Deep Security.

### ds-IsInstanceClear

Checks to see if the current instance is has any warnings, alerts, or errors in Deep Security. An instance is compliant if it does **not** have any warnings, alerts, or errors (a/k/a compliant which means everything is working as expected with no active security alerts).

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

## Risk of Credentials in AWS Config

If you're curious about the wisdom of storing access credentials in a 3rd party service...good. You've got your security hat on. Let's take a look at the risks.

Right now, Deep Security uses it's role-based access control to provide access to it's APIs (yes, a more elegant system is on the way). This means we need to provide our AWS Lambda functions with some way of getting a set of credentials.

Because Deep Security sits outside of the AWS IAM structure (a/k/a it's not an AWS service), we have the following options;

1. hard code the credentials inside the AWS Lambda function
1. pass the credentials to the function (current method)
1. put the credentials somewhere else and provide access to that location to the function

Option #1 removes the credentials from AWS Config and moves them to AWS Lambda. This allows for the segregation of duties via IAM access to these services. In turn it creates a significance maintenance challenge in the event you change credentials.

Option #2 (current method) stores the credentials in AWS Config. Any [user or role with sufficient privileges](http://docs.aws.amazon.com/config/latest/developerguide/recommended-iam-permissions-using-aws-config-console-cli.html) can access AWS Config and the stored credentials. This is the same situation as option #1 but doesn't present the same maintenance issue.

Option #3 would put the credentials in an alternative location (like S3 encrypted by KMS) reduces the possibility of the credentials leaking out significantly. Using IAM, you can ensure that only the Lambda execution role used for the function has access to the encryption key and the S3 key (object in the bucket). This solution has a lot more moving parts and is more difficult to configure.

In a discussion of option #1 vs #2, option #2 is the better choice as the maintenance issues presented by hard coding credentials are significant. If segregation is required, option #3 is far superior as it directly addresses the security issues of broader access to the credentials.

The risk posed by exposing the credentials to AWS COnfig can be partially mitigated by reducing the permissions that the credentials hold in Deep Security (see above, "Permissions In Deep Security"). However option #3 (storing the credentials in S3 and encrypting with KMS) is a much better option.

We will release guidelines on how to implement this solution shortly for situations when option #2 (which will remain the default) is insufficient.