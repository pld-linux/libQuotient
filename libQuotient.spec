#
# Conditional build:
%bcond_without	qt6		# Qt6 version
%bcond_with	tests		# unit tests

%define		qt_ver		6.4
Summary:	Library for Matrix clients
Summary(pl.UTF-8):	Biblioteka dla klientów Matriksa
Name:		libQuotient
Version:	0.9.3
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://github.com/quotient-im/libQuotient/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	bac8fe3b7fb08220d7a3606a2b73dbe0
URL:		https://github.com/quotient-im/libQuotient
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	Qt6Keychain-devel >= 0.12
BuildRequires:	Qt6Network-devel >= %{qt_ver}
BuildRequires:	Qt6Sql-devel >= %{qt_ver}
BuildRequires:	Qt6Test-devel >= %{qt_ver}
BuildRequires:	olm-devel >= 3.2.5
BuildRequires:	openssl-devel >= 3.0
BuildRequires:	qt6-build >= %{qt_ver}
BuildRequires:	cmake >= 3.26
BuildRequires:	libstdc++-devel >= 6:13
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6Core >= %{qt_ver}
Requires:	Qt6Gui >= %{qt_ver}
Requires:	Qt6Keychain >= 0.12
Requires:	Qt6Network >= %{qt_ver}
Requires:	Qt6Sql >= %{qt_ver}
Requires:	olm-devel >= 3.2.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Quotient project aims to produce a Qt-based SDK to develop
applications for Matrix (<https://matrix.org/>). libQuotient is a
library that enables client applications. It is the backbone of
Quaternion (<https://github.com/quotient-im/Quaternion>), NeoChat
(<https://matrix.org/ecosystem/clients/neochat/>) and other projects.

%package -n libQuotient-qt6
Summary:	Qt6 library for Matrix clients
Summary(pl.UTF-8):	Biblioteka Qt6 dla klientów Matriksa
Group:		X11/Development/Libraries

%description -n libQuotient-qt6
The Quotient project aims to produce a Qt-based SDK to develop
applications for Matrix (<https://matrix.org/>). libQuotient is a
library that enables client applications. It is the backbone of
Quaternion (<https://github.com/quotient-im/Quaternion>), NeoChat
(<https://matrix.org/ecosystem/clients/neochat/>) and other projects.

%description -n libQuotient-qt6 -l pl.UTF-8
Celem projektu Quotient jest stworzenie opartego na Qt SDK do
tworzenia aplikacji dla Matriksa (<https://matrix.org/>). libQuotient
to biblioteka pozwalająca na tworzenie aplikacji klienckich. Jest to
podstawa projektów takich jak Quaternion
(<https://github.com/quotient-im/Quaternion>) czy NeoChat
(<https://matrix.org/ecosystem/clients/neochat/>).

%package -n libQuotient-qt6-devel
Summary:	Header files for Qt6 libQuotient development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających libQuotient z Qt6
Group:		X11/Development/Libraries
Requires:	Qt6Core-devel >= %{qt_ver}
Requires:	Qt6Gui-devel >= %{qt_ver}
Requires:	Qt6Keychain-devel >= 0.12
Requires:	Qt6Network-devel >= %{qt_ver}
Requires:	Qt6Sql-devel >= %{qt_ver}
Requires:	libQuotient-qt6 = %{version}-%{release}
Requires:	libstdc++-devel >= 6:13
Requires:	olm-devel >= 3.2.5
Requires:	openssl-devel >= 3.0

%description -n libQuotient-qt6-devel
Header files for Qt6 libQuotient development.

%description -n libQuotient-qt6-devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających libQuotient z Qt6.

%prep
%setup -q

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DBUILD_WITH_QT6=ON \
	-DQuotient_ENABLE_E2EE=ON

%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libQuotient-qt6 -p /sbin/ldconfig
%postun	-n libQuotient-qt6 -p /sbin/ldconfig

%files -n libQuotient-qt6
%defattr(644,root,root,755)
%ghost %{_libdir}/libQuotientQt6.so.0.9
%attr(755,root,root) %{_libdir}/libQuotientQt6.so.*.*.*

%files -n libQuotient-qt6-devel
%defattr(644,root,root,755)
%{_libdir}/libQuotientQt6.so
%{_includedir}/Quotient
%{_libdir}/cmake/QuotientQt6
%{_pkgconfigdir}/QuotientQt6.pc
%dir %{_datadir}/ndk-modules
%{_datadir}/ndk-modules/Android.mk
