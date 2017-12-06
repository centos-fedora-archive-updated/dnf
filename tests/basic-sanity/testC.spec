Summary: testC Package
Name: testC
Version: 1
Release: 0
Group: System Environment/Base
License: GPL
BuildArch: noarch
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Provides: testC-provides
Requires: testA

%description

This is a testC test package

%build

%install
mkdir -p %{buildroot}/usr/bin/
touch %{buildroot}/usr/bin/testC

%files
/usr/bin/testC
