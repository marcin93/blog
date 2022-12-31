Title: Jira - Watched issues as reason for mail flood
Date: 2020-05-28
Category: Jira
Tags: atlassian, jira
Slug: watched-issues

Tired with Jira mail flood? Or maybe your Outlook rules are working seamlessly enough to not to disturb you with notifications?

As Jira administrator I can rant some while on Jira features as well as users forcing their ideas to spam others.

As jira by default makes you watcher of any:
- commented issue
- created issue

Knowing above user to "protect" himself can have saved special query in his favourite filters. Speciality of that JQL rely on it's result.

```sql
watcher = currentUser() and resolution = Unresolved
```

Above query will return list of all not "Closed" issues which can be moved, commented or changed in anyway which will create notification sent to your mailbox. Thus it seems to be good idea to go trough such JQL and verify is there anything what you can "Stop watching".

*Batching notifications*
In addition to above JQL it would be good to verify which Jira version is running in your company. Starting from Jira 8 Server version Jira does provide email improvement called "batch notifications". It's enabled by default in Jira or can be enabled by administrator when disabled. Administrator can reach that feature under "cog" > System > Batching email notifications [Atlassian KB](https://confluence.atlassian.com/adminjiraserver080/configuring-email-notifications-967897768.html)

![Batching notifications]({static}/images/jira_email_batch.png "Email_batching")
