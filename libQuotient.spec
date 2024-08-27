#
# Conditional build:
%bcond_without	qt5		# Qt5 version
%bcond_without	qt6		# Qt6 version
%bcond_with	tests		# unit tests

%define		qt5_ver		5.15.2
%define		qt6_ver		6.0
Summary:	Qt5 library for Matrix clients
Summary(pl.UTF-8):	Biblioteka Qt5 dla klientów Matriksa
Name:		libQuotient
Version:	0.8.2
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://github.com/quotient-im/libQuotient/archive/refs/tags/%{version}.tar.gz
# Source0-md5:	5f5799bed02806d21680a8a5fae06f44
URL:		https://github.com/quotient-im/libQuotient
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= %{qt5_ver}
BuildRequires:	Qt5Gui-devel >= %{qt5_ver}
BuildRequires:	Qt5Keychain-devel
BuildRequires:	Qt5Multimedia-devel >= %{qt5_ver}
BuildRequires:	Qt5Network-devel >= %{qt5_ver}
BuildRequires:	Qt5Test-devel >= %{qt5_ver}
BuildRequires:	qt5-build >= %{qt5_ver}
%endif
%if %{with qt6}
BuildRequires:	Qt6Core-devel >= %{qt6_ver}
BuildRequires:	Qt6Gui-devel >= %{qt6_ver}
BuildRequires:	Qt6Keychain-devel
BuildRequires:	Qt6Network-devel >= %{qt6_ver}
BuildRequires:	Qt6Sql-devel >= %{qt6_ver}
BuildRequires:	Qt6Test-devel >= %{qt6_ver}
BuildRequires:	olm-devel >= 3.2.5
BuildRequires:	openssl-devel >= 1.1.0
BuildRequires:	qt6-build >= %{qt6_ver}
%endif
BuildRequires:	cmake >= 3.20
BuildRequires:	libstdc++-devel >= 6:11
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Quotient project aims to produce a Qt-based SDK to develop
applications for Matrix (<https://matrix.org/>). libQuotient is a
library that enables client applications. It is the backbone of
Quaternion (<https://github.com/quotient-im/Quaternion>), NeoChat
(<https://matrix.org/ecosystem/clients/neochat/>) and other projects.

%description -l pl.UTF-8
Celem projektu Quotient jest stworzenie opartego na Qt SDK do
tworzenia aplikacji dla Matriksa (<https://matrix.org/>). libQuotient
to biblioteka pozwalająca na tworzenie aplikacji klienckich. Jest to
podstawa projektów takich jak Quaternion
(<https://github.com/quotient-im/Quaternion>) czy NeoChat
(<https://matrix.org/ecosystem/clients/neochat/>).

%package devel
Summary:	Header files for Qt5 libQuotient development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających libQuotient z Qt5
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qt5_ver}
Requires:	Qt5Gui-devel >= %{qt5_ver}
Requires:	Qt5Keychain-devel
Requires:	Qt5Network-devel >= %{qt5_ver}
Requires:	libstdc++-devel >= 6:11

%description devel
Header files for Qt5 libQuotient development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających libQuotient z Qt5.

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
Requires:	libQuotient-qt6 = %{version}-%{release}
Requires:	Qt6Core-devel >= %{qt6_ver}
Requires:	Qt6Gui-devel >= %{qt6_ver}
Requires:	Qt6Keychain-devel
Requires:	Qt6Network-devel >= %{qt6_ver}
Requires:	Qt6Sql-devel >= %{qt6_ver}
Requires:	Qt6Test-devel >= %{qt6_ver}
Requires:	libstdc++-devel >= 6:11
Requires:	olm-devel >= 3.2.5

%description -n libQuotient-qt6-devel
Header files for Qt6 libQuotient development.

%description -n libQuotient-qt6-devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających libQuotient z Qt6.

%prep
%setup -q

%build
%if %{with qt5}
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif
%endif

%if %{with qt6}
%cmake \
	-B build6 \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DBUILD_WITH_QT6=ON \
	-DQuotient_ENABLE_E2EE=ON

%ninja_build -C build6

%if %{with tests}
ctest --test-dir build6
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with qt5}
%ninja_install -C build
%endif

%if %{with qt6}
%ninja_install -C build6
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n libQuotient-qt6 -p /sbin/ldconfig
%postun	-n libQuotient-qt6 -p /sbin/ldconfig

%if %{with qt5}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQuotient.so.*.*.*
%ghost %{_libdir}/libQuotient.so.0.8

%files devel
%defattr(644,root,root,755)
%{_libdir}/libQuotient.so
%{_includedir}/Quotient
%{_libdir}/cmake/Quotient
%{_pkgconfigdir}/Quotient.pc
%dir %{_datadir}/ndk-modules
%{_datadir}/ndk-modules/Android.mk
%endif

%if %{with qt6}
%files -n libQuotient-qt6
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQuotientQt6.so.*.*.*
%ghost %{_libdir}/libQuotientQt6.so.0.8

%files -n libQuotient-qt6-devel
%defattr(644,root,root,755)
%{_libdir}/libQuotientQt6.so
%{_includedir}/Quotient
%{_libdir}/cmake/QuotientQt6
%{_pkgconfigdir}/QuotientQt6.pc
%dir %{_datadir}/ndk-modules
%{_datadir}/ndk-modules/Android.mk
%endif
