Title: Jira - LDAP filter and domain groups configuration
Date: 2023-01-24
Category: Jira
Tags: atlassian, jira
Slug: jira-ldap-groups

**Note**
I'm reffereing to Jira but those configuratoins can be used with Confluence or Bitbucket.

**Note 2**
This concept is relying on users being managed via Active Directory or LDAP

Jira administration has many aspects and points which can be tuned. One of those is how jira is connected to domain/ldap. One of best practicies is to not to multiplicate elements when not needed. In that context Jira should be connected to Domain/LDAP and trough that connection user permissions managed. By doing so Jira Administrator will not recreate LDAP group or create other than Domain groups for local Jira usage.

Such setup will remove user & group management from Jira System administrator and place it on: Project and LDAP administration.

**Project administration** it's nothing more than placing Domain groups under expected permission roles.

**Domain groups**
This should be also setup carefully as Jira administration and users don't want to see all domain groups being synchronized with Jira.

To achieve that goal domain group can be tagged with extenssionAttribute(n) or any other not used parameter. In my case I'll stay with ```extenssionAttribute1=Jira```. This way each group tagged with it will be "selected" to be used in Jira.

Now User Directory need to be updated under "Group Object Filter" to be like:
```(&(objectCategory=Group)(extenssionAttribute1=*Jira*))```

```extenssionAttribute1=*Jira*``` - (*) in that filter is because we can go one step further and want to use same group among few applications eg: Jira and Confluence. Then Domain attribute can look like: ```extenssionAttribute1=Jira,Confluence,Bitbucket```. Filter will do the job and select only those groups which are matching specified application.

Idea of using group attribute has also another advantage. User Directory can have "Base DN" pointing to top of our AD, like: ```o=example,c=com```, but filter will match and synchronize only those elements which are needed. Maintainers (Active Directory and  Operations) will not need to think "Where group need to be created to make it visible in Jira?" or "Can we move group to different OU?". Grups can be anywhere within AD tree structure and will remain usable for Jira.

Supported by Jira LDAP directories: [Atlassian KB](https://confluence.atlassian.com/adminjiraserver/connecting-to-an-ldap-directory-938847052.html) 