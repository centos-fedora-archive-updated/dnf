Summary: testB Package
Name: testB
Version: 1
Release: 0
Group: System Environment/Base
License: GPL
BuildArch: noarch
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Provides: testB-provides
Requires: testC

%description

This is a testB test package

%build

%install
mkdir -p %{buildroot}/usr/bin/
touch %{buildroot}/usr/bin/testB

%files
/usr/bin/testB
