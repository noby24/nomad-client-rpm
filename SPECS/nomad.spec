%if 0%{?_version:1}
%define         _verstr      %{_version}
%else
%define         _verstr      0.7.1
%endif

Name:           nomad
Version:        %{_verstr}
Release:        1%{?dist}
Summary:        Nomad is a single binary that schedules applications and services

Group:          System Environment/Daemons
License:        MPLv2.0
URL:            https://www.nomadproject.io/
Source0:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
Source1:        %{name}.sysconfig
Source2:        %{name}.service
Source3:        %{name}.init
Source4:        %{name}.logrotate
Source5:        client.hcl
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
BuildRequires:  systemd-units
Requires:       systemd
%else
Requires:       logrotate
%endif
Requires(pre): shadow-utils


%description
Nomad is a tool for managing a cluster of machines and running applications on them. Nomad abstracts away machines and the location of applications, and instead enables users to declare what they want to run and Nomad handles where they should run and how to run them.

The key features of Nomad are:
 - Docker Support - Nomad supports Docker as a first-class workload type. Jobs submitted to Nomad can use the docker driver to easily deploy containerized applications to a cluster.
 - Operationally Simple - Nomad ships as a single binary, both for clients and servers, and requires no external services for coordination or storage.
 - Multi-Datacenter and Multi-Region Aware - Nomad models infrastructure as groups of datacenters which form a larger region. Scheduling operates at the region level allowing for cross-datacenter scheduling.
 - Flexible Workloads - Nomad has extensible support for task drivers, allowing it to run containerized, virtualized, and standalone applications.
 - Built for Scale - Nomad was designed from the ground up to support global scale infrastructure. Nomad is distributed and highly available, using both leader election and state replication to provide availability in the face of failures.

%prep
%setup -q -c

%install
mkdir -p %{buildroot}/%{_bindir}
cp nomad %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
cp %{SOURCE5} %{buildroot}/%{_sysconfdir}/%{name}/client.hcl
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
mkdir -p %{buildroot}/%{_unitdir}
cp %{SOURCE2} %{buildroot}/%{_unitdir}/
%else
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d
cp %{SOURCE3} %{buildroot}/%{_initrddir}/nomad
cp %{SOURCE4} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}
%endif

%pre

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
%else
%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
%endif

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir %attr(750, root, root) %{_sysconfdir}/%{name}
%attr(640, root, root) %{_sysconfdir}/%{name}/client.hcl
%dir %attr(750, root, root) %{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%endif
%attr(755, root, root) %{_bindir}/nomad



%doc


%changelog
* Tue Apr 04 2018 noby24
- version to 0.7.1
