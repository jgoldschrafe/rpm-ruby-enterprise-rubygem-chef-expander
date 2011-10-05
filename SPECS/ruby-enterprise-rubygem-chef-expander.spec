%define ruby_dist ruby-enterprise
%define ruby_dist_dash %{ruby_dist}-
%define _prefix /opt/ruby-enterprise
%define _gem %{_prefix}/bin/gem
%define _ruby %{_prefix}/bin/ruby

# Generated from chef-expander-0.10.0.rc.1.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(%{_ruby} -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(%{_ruby} -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname chef-expander
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: A systems integration framework, built to bring the benefits of configuration management to your entire infrastructure
Name: %{?ruby_dist_dash}rubygem-%{gemname}
Version: 0.10.4
Release: 1%{?buildstamp}%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://wiki.opscode.com/display/chef
Source0: http://rubygems.org/downloads/%{gemname}-%{version}.gem
Source1: chef-expander.init
Source2: chef-expander.sysconfig
Source3: chef-expander.logrotate
Source4: config.rb

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: %{?ruby_dist_dash}rubygems
Requires: %{?ruby_dist_dash}rubygem(mixlib-log) >= 1.2.0
Requires: %{?ruby_dist_dash}rubygem(amqp) = 0.6.7
Requires: %{?ruby_dist_dash}rubygem(eventmachine) >= 0.12.10
Requires: %{?ruby_dist_dash}rubygem(em-http-request) >= 0.2.11
Requires: %{?ruby_dist_dash}rubygem(yajl-ruby) >= 0.7.7
Requires: %{?ruby_dist_dash}rubygem(uuidtools) >= 2.1.1
Requires: %{?ruby_dist_dash}rubygem(bunny) >= 0.6.0
Requires: %{?ruby_dist_dash}rubygem(fast_xs) >= 0.7.3
Requires: %{?ruby_dist_dash}rubygem(highline) >= 1.6.1
BuildRequires: %{?ruby_dist_dash}rubygems
BuildArch: noarch
Provides: %{?ruby_dist_dash}rubygem(%{gemname}) = %{version}

Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts
Requires: rabbitmq-server

%description
A systems integration framework, built to bring the benefits of configuration
management to your entire infrastructure.


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}/var/log/chef
mkdir -p %{buildroot}%{_sysconfdir}/chef
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/
mkdir -p %{buildroot}/var/run/chef
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d

%{_gem} install --local --install-dir %{buildroot}%{gemdir} \
                --force --rdoc %{SOURCE0}
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

cp %{SOURCE1} %{buildroot}/etc/rc.d/init.d/chef-expander
chmod +x %{buildroot}/etc/rc.d/init.d/chef-expander
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/chef-expander
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/chef-expander
cp %{SOURCE4} %{buildroot}%{_sysconfdir}/chef/expander.rb

%clean
rm -rf %{buildroot}

%post
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add chef-expander

if [ -z "`/usr/bin/id chef 2> /dev/null`" ]; then
	%{_sbindir}/adduser chef >/dev/null 2>&1 
	chown -R chef %{_sysconfdir}/chef
fi

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service chef-expander stop >/dev/null 2>&1
    /sbin/chkconfig --del chef-expander
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service chef-expander restart >/dev/null 2>&1 || :
fi

%files
%defattr(-, root, root, -)
%{_bindir}/chef-expander
%{_bindir}/chef-expander-vnode
%{_bindir}/chef-expanderctl
%{gemdir}/gems/%{gemname}-%{version}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/LICENSE
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%config(noreplace) %{_sysconfdir}/sysconfig/chef-expander
%config(noreplace) %{_sysconfdir}/logrotate.d/chef-expander
%{_sysconfdir}/rc.d/init.d/chef-expander
%{_sysconfdir}/chef/

%changelog
* Mon Oct  3 2011 Jeff Goldschrafe <jeff@holyhandgrenade.org> - 0.10.4-1.hhg
- Rebuild for Ruby Enterprise Edition

* Wed Jul 27 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.4-1
- preparing for 0.10.4

* Mon Jul 25 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.2-3
- updated release version format

* Mon Jul 25 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.2-2
- add buildstamp to release

* Mon Jul 04 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.2-1
- upstream update

* Fri May 06 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0-3
- included default expander config

* Fri May 06 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0-2
- added /etc/chef to files section

* Tue May 03 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0-1
- upstream update

* Mon May 02 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.2-1
- upstream update
- do not try to configure rabbit in post

* Fri Apr 29 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.1-2
- add init script
- create default dirs
- add logrotate config
- create chef user

* Thu Apr 28 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.1-1
- Initial package
