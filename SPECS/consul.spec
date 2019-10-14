%define debug_package %{nil}

Name:		consul
Version:	1.6.1
Release:	1%{dist}
Summary:	A service mesh solution
License:	Mozilla Public License 2.0
URL:		https://www.consul.io
%ifarch x86_64 amd64
Source0:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
%else
Source0:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_386.zip
%endif
Source1:        %{name}.hcl
Source2:        %{name}.init
Source3:        %{name}.logrotate
Source4:        %{name}.sysconfig
Source5:        %{name}.service
Source6:        %{name}.tmpfiles
Source7:        %{name}.firewalld
%if 0%{?rhel} >= 7
Requires:         firewalld-filesystem
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
BuildRequires:    systemd-units
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Consul is a tool for service discovery and configuration.
Consul is distributed, highly available, and extremely scalable.

%prep
%setup -c
%build
%install
%{__install} -d -m 0755 %{buildroot}%{_sbindir} \
                        %{buildroot}%{_sysconfdir}/%{name} \
                        %{buildroot}%{_sysconfdir}/logrotate.d \
                        %{buildroot}%{_sysconfdir}/sysconfig \
                        %{buildroot}%{_localstatedir}/{lib,log}/%{name}
%if 0%{?rhel} < 7
%{__install} -d -m 0755 %{buildroot}%{_sysconfdir}/rc.d/init.d \
                        %{buildroot}%{_localstatedir}/run/%{name}
%else
%{__install} -d -m 0755 %{buildroot}%{_unitdir} \
                        %{buildroot}%{_rundir}/%{name} \
                        %{buildroot}%{_tmpfilesdir} \
                        %{buildroot}%{_prefix}/lib/firewalld/services
%endif
         
%{__install} -m 0755 %{name} %{buildroot}%{_sbindir}
%{__install} -m 0600 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}
%if 0%{?rhel} < 7
%{__install} -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
%else
%{__install} -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -m 0644 %{SOURCE6} %{buildroot}%{_tmpfilesdir}/%{name}.conf
%{__install} -m 0644 %{SOURCE7} %{buildroot}%{_prefix}/lib/firewalld/services/%{name}.xml
%endif
%{__install} -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
  useradd -r -g %{name} -s /sbin/nologin \
    -d %{_localstatedir}/lib/%{name} -c "Consul User" %{name}

%post
%if 0%{?systemd_post:1}
    %systemd_post %{name}.service
    %firewalld_reload
    /usr/bin/systemd-tmpfiles --create %{_tmpfilesdir}/%{name}.conf
%else
    /sbin/chkconfig --add %{name}
%endif

%preun
%if 0%{?systemd_preun:1}
    %systemd_preun %{name}.service
%else
    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}
%endif

%postun
%if 0%{?systemd_postun:1}
    %systemd_postun %{name}.service
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,consul,consul,-)
%attr(-,root,root) %{_sbindir}/%{name}
%attr(-,root,root) %{_sysconfdir}/logrotate.d/%{name}
%if 0%{?rhel} < 7
%attr(-,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%else
%attr(-,root,root) %{_unitdir}/%{name}.service
%attr(-,root,root) %{_tmpfilesdir}/%{name}.conf
%attr(-,root,root) %{_prefix}/lib/firewalld/services/%{name}.xml
%endif
%attr(-,root,root) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.*
%{_localstatedir}/lib/%{name}
%{_localstatedir}/log/%{name}
%if 0%{?rhel} >= 7
%ghost %attr(755,consul,consul) %{_rundir}/%{name}
%else
%{_localstatedir}/run/%{name}
%endif

%changelog
* Mon Oct 14 2019 Elia Pinto <pinto.elia@gmail.com> - 1.6.1-1
- Update to version 1.6.1

* Tue Apr 02 2019 Giuseppe Ragusa <giuseppe.ragusa@fastmail.fm> - 1.4.4-1
- Update to version 1.4.4
- Modified spec to properly support CentOS/RHEL 7
- Converted strategy from config file to config dir
- Converted sample config file to HCL
- Small uniformity mods

* Sun Mar 25 2018 Taylor Kimball <tkimball@linuxhq.org> - 1.0.6-1
- Update to version 1.0.6

* Mon Sep 26 2016 Taylor kimball <tkimball@linuxhq.org> - 0.7.0-1
- Update to version 0.7.0

* Tue May 03 2016 Taylor Kimball <tkimball@linuxhq.org> - 0.6.4-1
- Initial build.
