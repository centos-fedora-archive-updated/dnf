Name:           dnf
Version:        0.0.1
Release:        1%{?dist}
Summary:        dnf

Group:          Web
License:        GPLV3
URL:            dnf.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  yum coreutils
Requires:       yum coreutils

%description
dnf


%build
CFLAGS=
export CFLAGS=


%install
CFLAGS=
export CFLAGS=
mkdir -p $RPM_BUILD_ROOT
cat > $RPM_BUILD_ROOT/usr/bin/dnf <<EOF
#!/bin/bash
/usr/bin/yum $@
EOF
chmod 777 $RPM_BUILD_ROOT/usr/bin/dnf

%post
chmod 777 /usr/bin/dnf

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
/usr/bin/dnf


%changelog

