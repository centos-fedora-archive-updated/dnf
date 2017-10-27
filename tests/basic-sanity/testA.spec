Summary: testA Package
Name: testA
Version: 1
Release: 0
Group: System Environment/Base
License: GPL
BuildArch: noarch
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description

This is a testA test package

%build

%install
mkdir -p %{buildroot}/usr/bin/
touch %{buildroot}/usr/bin/testA

%files
/usr/bin/testA
