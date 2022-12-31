Title: Bitbucket enterprise way - permission model
Date: 2020-01-20
Category: Bitbucket
Tags: atlassian, bitbucket
Slug: bitbucket-permission-model

How to setup permission model?
As we have discussed connection setup and configuration another important topic to discuss is Permission model.

By Atlassian design Bitbucket has: Application access, Projects and Repositories. Branch permissions are most often too granular to be covered by IT/general setup.

![Global permissions]({static}/images/bb_global_permissions.png "Bitbucket screen"){: class="zooom"}

Does your company uses open model? 

* All developers can move between projects and repositories
* stash-users - can be enough as it will give permission to application + it can be configured on project level to grant read/write access

Do you have some projects to be hidden?

* Global permissions - stash-users will provide app access
* Project permission - selectively user access can be granted for those “to be limited”

Do you have most projects to be segregated? 

* They will provide user access only after user will be added to PROJKEY_Read/Write/Admin group.
* All projects will have group based access Read/Write/Admin
* User access can be agreed to not to be given
* Enabling public access can be removed via admin <BITBUCKET_HOME>/bitbucket.properties file (create the file if it does not exist)

```bash
feature.public.access=false
```