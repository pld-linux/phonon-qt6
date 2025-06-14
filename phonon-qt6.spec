%define		qt_ver		6.6.1

Summary:	Phonon: multimedia API for Qt6/KDE6
Summary(pl.UTF-8):	Phonon - biblioteka multimedialna dla Qt6/KDE6
Name:		phonon-qt6
Version:	4.12.0
Release:	3
License:	LGPL v2.1 or LGPL v3
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/phonon/%{version}/phonon-%{version}.tar.xz
# Source0-md5:	e80e9c73967080016bdb3c0ee514ceab
Patch0:		phonon-qm-suffix.patch
URL:		https://userbase.kde.org/Phonon
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6Designer-devel >= %{qt_ver}
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	Qt6OpenGL-devel >= %{qt_ver}
BuildRequires:	Qt6Qt5Compat-devel >= %{qt_ver}
BuildRequires:	Qt6Widgets-devel >= %{qt_ver}
BuildRequires:	Qt6Xml-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.20.0
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	kf6-extra-cmake-modules >= 5.90
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel >= 0.9.21
BuildRequires:	qt6-build >= %{qt_ver}
BuildRequires:	qt6-linguist >= %{qt_ver}
BuildRequires:	qt6-qmake >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6Core >= %{qt_ver}
Requires:	Qt6Gui >= %{qt_ver}
Requires:	Qt6OpenGL >= %{qt_ver}
Requires:	Qt6Widgets >= %{qt_ver}
Conflicts:	phonon < 4.10.3-3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Phonon is the multimedia API for Qt6/KDE6.

Phonon was originally created to allow KDE to be independent of any
single multimedia framework such as GStreamer or Xine and to provide a
stable API for KDE's lifetime. It was done to fix problems of
frameworks becoming unmaintained, API instability, and to create a
simple multimedia API.

%description -l pl.UTF-8
Phonon to biblioteka multimedialna dla Qt6/KDE6.

Pierwotnie powstała, aby pozwolić na niezależność KDE od konkretnego
środowiska multimedialnego, takiego jak GStreamer czy Xine, oraz
zapewnić stabilne API na cały czas życia KDE5. Została stworzona w
celu wyeliminowania problemów z porzucaniem bibliotek i
niestabilnością ich API, a także w celu stworzenia prostego API
multimedialnego.

%package settings
Summary:	Phonon settings application
Summary(pl.UTF-8):	Aplikacja do ustawień Phonona
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Provides:	phonon-settings = %{version}-%{release}
Obsoletes:	phonon-qt5-settings < 4.13

%description settings
Phonon settings application.

%description settings -l pl.UTF-8
Aplikacja do ustawień Phonona.

%package devel
Summary:	Header files for Phonon library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Phonon
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Core-devel >= %{qt_ver}
Requires:	Qt6Widgets-devel >= %{qt_ver}

%description devel
Header files for Phonon library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Phonon.

%package -n Qt6Designer-plugin-phonon
Summary:	Phonon plugin for Qt6 QtDesigner
Summary(pl.UTF-8):	Wtyczka Phonon dla Qt6 QtDesignera
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Designer >= %{qt_ver}

%description -n Qt6Designer-plugin-phonon
Phonon plugin for Qt6 QtDesigner.

%description -n Qt6Designer-plugin-phonon -l pl.UTF-8
Wtyczka Phonon dla Qt6 QtDesignera.

%prep
%setup -q -n phonon-%{version}
%patch -P0 -p1

for f in poqm/*/libphonon_qt.po ; do
	%{__mv} "$f" "${f%.po}6.po"
done

%build
%cmake -B build \
	-G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DPHONON_BUILD_DESIGNER_PLUGIN=ON \
	-DPHONON_BUILD_QT5=OFF \
	-DPHONON_BUILD_QT6=ON

%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

install -d $RPM_BUILD_ROOT%{_libdir}/qt6/plugins/phonon4qt6_backend

%find_lang libphonon_qt6 --with-qm
%find_lang phononsettings_qt --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f libphonon_qt6.lang
%defattr(644,root,root,755)
%ghost %{_libdir}/libphonon4qt6.so.4
%attr(755,root,root) %{_libdir}/libphonon4qt6.so.*.*.*
%ghost %{_libdir}/libphonon4qt6experimental.so.4
%attr(755,root,root) %{_libdir}/libphonon4qt6experimental.so.*.*.*
%dir %{_libdir}/qt6/plugins/phonon4qt6_backend

%files settings -f phononsettings_qt.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/phononsettings

%files devel
%defattr(644,root,root,755)
%{_libdir}/libphonon4qt6.so
%{_libdir}/libphonon4qt6experimental.so
%{_includedir}/phonon4qt6
%{_pkgconfigdir}/phonon4qt6.pc
%{_libdir}/cmake/phonon4qt6

%files -n Qt6Designer-plugin-phonon
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt6/plugins/designer/phonon4qt6widgets.so
