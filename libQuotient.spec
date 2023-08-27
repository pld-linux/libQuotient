#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	23.08.0
%define		kframever	5.94.0
%define		qtver		5.15.2
Summary:	libQuotient
Name:		libQuotient
Version:	0.8.1.1
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://github.com/quotient-im/libQuotient/archive/refs/tags/%{version}.tar.gz
# Source0-md5:	268d0d11cbc7aa8d021f877e92146065
URL:		https://github.com/quotient-im/libQuotient
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Keychain-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Quotient project aims to produce a Qt-based SDK to develop
applications for [Matrix](https://matrix.org). libQuotient is a
library that enables client applications. It is the backbone of
[Quaternion](https://github.com/quotient-im/Quaternion),
[NeoChat](https://matrix.org/docs/projects/client/neo-chat) and other
projects.

%package devel
Summary:	Header files for %{name} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{name}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{name}.

%prep
%setup -q

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%ghost %{_libdir}/libQuotient.so.0.8
%attr(755,root,root) %{_libdir}/libQuotient.so.0.*.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/Quotient
%{_libdir}/cmake/Quotient
%{_libdir}/libQuotient.so
%{_pkgconfigdir}/Quotient.pc
%{_datadir}/ndk-modules/Android.mk
