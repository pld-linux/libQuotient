#
# Conditional build:
%bcond_without	qt5		# build qt5 version
%bcond_without	qt6		# build qt6 version
%bcond_with	tests		# build with tests
%define		kdeappsver	23.08.0
%define		kframever	5.94.0
%define		qtver		5.15.2
Summary:	libQuotient
Name:		libQuotient
Version:	0.8.1.2
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://github.com/quotient-im/libQuotient/archive/refs/tags/%{version}.tar.gz
# Source0-md5:	008cced6e9e409f5025563d12e1a6be4
URL:		https://github.com/quotient-im/libQuotient
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Keychain-devel
BuildRequires:	qt5-build >= %{qtver}
%endif
%if %{with qt6}
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Keychain-devel
BuildRequires:	qt6-build >= %{qtver}
%endif
BuildRequires:	cmake >= 3.20
BuildRequires:	ninja
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

%package -n libQuotient-qt6
Summary:	libQuotient Qt6

%description -n libQuotient-qt6
The Quotient project aims to produce a Qt-based SDK to develop
applications for [Matrix](https://matrix.org). libQuotient is a
library that enables client applications. It is the backbone of
[Quaternion](https://github.com/quotient-im/Quaternion),
[NeoChat](https://matrix.org/docs/projects/client/neo-chat) and other
projects.

%package -n libQuotient-qt6-devel
Summary:	Header files for %{name} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających libQuotient-qt6
Group:		X11/Development/Libraries
Requires:	libQuotient-qt6 = %{version}-%{release}

%description -n libQuotient-qt6-devel
Header files for libQuotient-qt6 development.

%description -n libQuotient-qt6-devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających libQuotient-qt6.

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
	-DBUILD_WITH_QT6=ON
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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n libQuotient-qt6 -p /sbin/ldconfig
%postun -n libQuotient-qt6  -p /sbin/ldconfig

%if %{with qt5}
%files
%defattr(644,root,root,755)
%ghost %{_libdir}/libQuotient.so.0.8
%attr(755,root,root) %{_libdir}/libQuotient.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/Quotient
%{_libdir}/cmake/Quotient
%{_libdir}/libQuotient.so
%{_pkgconfigdir}/Quotient.pc
%dir %{_datadir}/ndk-modules
%{_datadir}/ndk-modules/Android.mk
%endif

%if %{with qt6}
%files -n libQuotient-qt6
%defattr(644,root,root,755)
%ghost %{_libdir}/libQuotientQt6.so.0.8
%attr(755,root,root) %{_libdir}/libQuotientQt6.so.*.*.*

%files -n libQuotient-qt6-devel
%defattr(644,root,root,755)
%{_libdir}/cmake/QuotientQt6
%{_libdir}/libQuotientQt6.so
%{_pkgconfigdir}/QuotientQt6.pc
%dir %{_datadir}/ndk-modules
%{_datadir}/ndk-modules/Android.mk
%endif

