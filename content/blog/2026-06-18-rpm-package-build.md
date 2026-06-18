Title: RPM package build
Date: 2026-06-18
Tags: rpm, rpm-build, rhel
Slug: rpm-build


⚠️ This will be brief topic introduction not Production manual.

# Intro

Recently I came across topic which was new to me and I've never worked on. Building RPM package. Usually application deployment involves VM, DB, Loadbalancer, Storage. Any automation (eg. Ansible, Terraform, Helm, etc.) can be used. But some deployments do use client workstation or even client infrastructure. One solution is to use Linux package deployed in remote infrastructure. As RHEL does cover 43.1% enterprise servers [1](https://commandlinux.com/statistics/most-popular-linux-distributions-market-share) it's natural choice. Here [RPM](https://en.wikipedia.org/wiki/RPM_Package_Manager) comes to the picture.

# Requirements

Idea was to build dummy 'app' which will be installed as RPM. Package should install app and service. App need to provide log messages like start, ongoing ping and stop.

For that idea we already require:
- RPM compatible build platform
	- docker image: `rockylinux:9` and `rockylinux:9-ubi-init`
- RPM dev tools
- app:
	- bash script printing messages from config
	- config
- service

# RPM package build

source: https://developers.redhat.com/articles/2021/05/21/build-your-own-rpm-package-sample-go-program

On RPM compatible OS install:
- `rpm-build rpmdevtools systemd-rpm-macros` - main dev tools
- `rpmdev-setuptree` - will build RPM directory `~/rpmbuild` containing: `BUILD`, `RPMS`, `SOURCES`, `SPECS`, `SRPMS`.

## SOURCES

Here you need to place your app and required extras like in my case service

```bash
├── SOURCES  
│   ├── hello-world-1  
│   │   ├── hello-world.conf  
│   │   ├── hello-world.service  
│   │   └── hello-world.sh  
│   └── hello-world-1.tar.gz  
```

Create archive from sources:
```bash
cd SOURCES
tar -czf hello-world-1.tar.gz hello-world-1
```

RPM package does deliver:
- sources (`*.tar.gz`)
- package signature
- delta update

RPM build does default to rely on archive which is being referred in spec `Source0: %{name}-%{version}.tar.gz` and required by `%setup -q` [Using the %setup macro](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/rpm_packaging_guide/advanced-topics#using-the-setup-macro_more-on-macros) 

The `%setup` macro:
- Ensures that we are working in the correct directory.
- Removes residues of previous builds.
- Unpacks the source tarball.
- Sets up some default privileges.

then I'm adding `-q` flag which limits the verbosity of the `%setup` macro. Only `tar -xof` is executed instead of `tar -xvvof`. 
This can be replaced by `%autosetup` [autosetup](https://rpm-software-management.github.io/rpm/manual/autosetup.html) which is combining `%setup` and `%patch`  into one.

**Version bump workflow**
In case we will be releasing new packages we will need to use Versioning. This is why we include the version number in the path `SOURCES/hello-world-1 `. 

Version 2:
```bash
cd SOURCES
cp hello-world-1 hello-world-2
<modifications>
<changelog update in hello-world.spec>
tar -czf hello-world-2.tar.gz hello-world-2
```

Source files:
[hello-world.conf](https://github.com/marcin93/rpm_build/blob/main/SOURCES/hello-world-1/hello-world.conf "hello-world.conf")
[hello-world.service](https://github.com/marcin93/rpm_build/blob/main/SOURCES/hello-world-1/hello-world.service "hello-world.service")
[hello-world.sh](https://github.com/marcin93/rpm_build/blob/main/SOURCES/hello-world-1/hello-world.sh "hello-world.sh")

## SPEC

RPM does use `*.spec` to define package details - content, actions, etc.

Example spec can be found in: [Creating_the_spec_file](https://developers.redhat.com/articles/2021/05/21/build-your-own-rpm-package-sample-go-program#creating_the_spec_file) or [Your First RPM Package](https://rpm-packaging-guide.github.io/#hello-world)

```bash
├── SPECS  
│   └── hello-world.spec
```

Spec file does define steps to get all installed ( `%{?systemd_requires}, %prep, %setup -q, %install, %post, %files`) and what need to happen when package is being removed (`%preun`).

Following: [spec / Dependencies / Requires](https://rpm.org/docs/6.1.x/manual/spec.html)
- `%post` 
> Denotes the dependency must be present right after the package is installed, and is used a strong ordering hint to break possible dependency loops. A post-dependnecy is free to be removed once the install-transaction completes.
- `%preun` 
> Denotes the dependency must be present in before the package is is removed, and is used a strong ordering hint to break possible dependency loops.

As I'm about to have systemd in use `%{?systemd_requires}` and related details to it handling proper service state. 
More on systemd scriptlets: [Fedora Project / systemd](https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_systemd)

- `%systemd_post %{name}.service` - is taking care to make sure service is being started once package installed.
- `%systemd_preun %{name}.service`  - is stopping service before removing package.

Worth to mention is one addition in `%files` 
- `%config(noreplace)` - indicates that the file in the package should be installed with extension .rpmnew if there is already a modified file with the same name on the installed machine. [config](https://rpm-software-management.github.io/rpm/manual/spec.html#config) and [Jon Warbrick: rpm config](https://www.cl.cam.ac.uk/~jw35/docs/rpm_config.html)

Spec file:
[hello-world.spec](https://github.com/marcin93/rpm_build/blob/main/SPECS/hello-world.spec "hello-world.spec")

## Extras

As I'm about to use container to create package I'm defining `Dockerfile` and build script: `build.sh`

Extra files:
[Dockerfile](https://github.com/marcin93/rpm_build/blob/main/Dockerfile "Dockerfile")
[build.sh](https://github.com/marcin93/rpm_build/blob/main/build.sh "build.sh")

# Build

Initiate build
```bash
./build.sh
```

once build completed RPM should land in `dist` and be ready to be installed on other systems
```bash
tree
└── dist  
   └── hello-world-1-2.el9.noarch.rpm
```

# Verify

## Container

### Install & verify service

Due to use of containers, we need to make sure it is running systemd as PID 1. Therefore we need to use modified `rockylinux:9` -> `rockylinux:9-ubi-init` designed to execute multi-service within container.

1. Run `rockylinux:9-ubi-init` with extra parameters to get all required privileges and mount directory with generated rpm
```bash
docker run -d \
--name hello-world \
--privileged \
--cgroupns=host \
-v /sys/fs/cgroup:/sys/fs/cgroup:rw \
-v $(pwd)/dist:/rpms \
rockylinux/rockylinux:9-ubi-init
```

2. Install package
```bash
docker exec hello-world bash -c "dnf install -y /rpms/hello-world-1-2.el9.noarch.rpm --allowerasing"
```

### Inspect logs

3. Check service
```bash
docker exec hello-world systemctl status hello-world
```

4. Check `journalctl`
```bash
docker exec hello-world journalctl -u hello-world --no-pager
```

The service status and logs are now visible via `systemctl` and `journalctl`. Start, ping and Stop.

### Lint the package

5. Verify RPM itself
```bash
# access container and install rpmlint
dnf install rpmlint

rpmlint rpms/hello-world-1-2.el9.noarch.rpm
# use rpmlint -i to get more details

rpm -V hello-world # package name

# list content of package
rpm -ql hello-world
```

#### What rpmlint actually checks?

> **rpmlint** is a tool for checking common errors in rpm packages. It can be used to test individual packages and spec files before uploading or to check an entire distribution.
https://linux.die.net/man/1/rpmlint

https://rpm-packaging-guide.github.io/#checking-rpms-for-sanity

It can be used to verify spec and rpm package itself.

6. Verification & Cleanup
```bash
docker stop hello-world && docker rm hello-world
```
