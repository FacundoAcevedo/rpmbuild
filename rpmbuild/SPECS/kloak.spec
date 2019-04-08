%global _hardened_build 1



Name:           kloak
Version:        0.2
Release:        1%{?dist}
Summary:        Keystroke-level online anonymization kernel


License:       BSD
URL:           https://github.com/vmonaco/%{name}/
Source0:       https://github.com/vmonaco/%{name}/archive/v%{version}.tar.gz

BuildRequires: gcc
BuildRequires: make
BuildRequires: gzip
BuildRequires: rubygem-ronn

%if 0%{?rhel} && 0%{?rhel} < 8 || 0%{?fedora} <= 29
BuildRequires:  systemd
%else
BuildRequires:  systemd-rpm-macros
%{?systemd_requires}
%endif



%description
%{name} is a privacy tool that makes keystroke bio-metrics less effective.
This is accomplished by obfuscating the time intervals between key press and
release events, which are typically used for identification.
This project is experimental


%prep
%autosetup


%build
%set_build_flags
%make_build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/usr/lib/systemd/system/
mkdir -p %{buildroot}/%{_mandir}/man8/

install -Dpm 0755 %{name} %{buildroot}/%{_sbindir}/%{name}
install -Dpm 0755 eventcap %{buildroot}/%{_sbindir}/eventcap
install -Dpm 0644 lib/systemd/system/%{name}.service %{buildroot}/%{_unitdir}/%{name}.service

ronn --pipe  -r man/%{name}.8.ronn | gzip --best > %{buildroot}/%{_mandir}/man8/%{name}.8.gz
ronn --pipe  -r man/eventcap.8.ronn | gzip --best > %{buildroot}/%{_mandir}/man8/eventcap.8.gz

%post
%{_bindir}/systemctl daemon-reload

%postun
%{_bindir}/systemctl daemon-reload



%files
%{_sbindir}/%{name}
%{_sbindir}/eventcap
/%{_unitdir}/%{name}.service
%{_mandir}/man8/%{name}.8.gz
%{_mandir}/man8/eventcap.8.gz


%license LICENSE
%doc README.md changelog.upstream



%changelog
*  Wed Mar 27 2019 kaze <kaze@rlab.be> - 0.2-1
-   First release.
 
