Summary:	Pacman - simple library-based package manager (from Arch Linux)
Summary(pl.UTF-8):	Pacman - prosty, oparty na bibliotece zarządca pakietów (z Arch Linuksa)
Name:		alpm
Version:	4.2.0
Release:	0.1
License:	GPL v2+
Group:		Libraries
Source0:	ftp://ftp.archlinux.org/other/pacman/pacman-%{version}.tar.gz
# Source0-md5:	184ce14f1f326fede72012cca51bba51
URL:		https://www.archlinux.org/pacman/
BuildRequires:	bash >= 4.1.0
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	curl-devel >= 7.19.4
BuildRequires:	gettext-devel >= 0.13.1
BuildRequires:	gpgme-devel >= 1.3.0
BuildRequires:	libarchive-devel >= 2.8.0
BuildRequires:	libtool >= 2:2
BuildRequires:	openssl-devel
BuildRequires:	perl-base >= 1:5.10.1
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.7
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pacman is a simple library-based package manager, designed for Arch
Linux.

%description -l pl.UTF-8
Pacman to prosty, oparty na bibliotece zarządca pakietów, powstały dla
Arch Linuksa.

%package libs
Summary:	Arch Linux Package Management library
Summary(pl.UTF-8):	Biblioteka Arch Linux Package Management
Group:		Libraries

%description libs
Arch Linux Package Management library.

%description libs -l pl.UTF-8
Biblioteka Arch Linux Package Management, służąca do zarządzania
pakietami Arch Linuksa.

%package devel
Summary:	Header files for ALPM library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ALPM
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	curl-devel >= 7.19.4
Requires:	gpgme-devel >= 1.3.0
Requires:	libarchive-devel >= 2.8.0
Requires:	openssl-devel

%description devel
Header files for ALPM library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ALPM.

%package static
Summary:	Static ALPM library
Summary(pl.UTF-8):	Statyczna biblioteka ALPM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ALPM library.

%description static -l pl.UTF-8
Statyczna biblioteka ALPM.

%prep
%setup -q -n pacman-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libalpm.la

# too generic names
%{__mv} $RPM_BUILD_ROOT%{_bindir}/{,pacman-}testdb
%{__mv} $RPM_BUILD_ROOT%{_bindir}/{,pacman-}vercmp
%{__mv} $RPM_BUILD_ROOT%{_mandir}/man8/{,pacman-}vercmp.8

# outdated version of ko
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ko_KR

%find_lang libalpm
%find_lang pacman
%find_lang pacman-scripts
cat pacman-scripts.lang >> pacman.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f pacman.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cleanupdelta
%attr(755,root,root) %{_bindir}/makepkg
%attr(755,root,root) %{_bindir}/makepkg-template
%attr(755,root,root) %{_bindir}/pacman
%attr(755,root,root) %{_bindir}/pacman-db-upgrade
%attr(755,root,root) %{_bindir}/pacman-key
%attr(755,root,root) %{_bindir}/pacman-optimize
%attr(755,root,root) %{_bindir}/pacman-testdb
%attr(755,root,root) %{_bindir}/pacman-vercmp
%attr(755,root,root) %{_bindir}/pacsort
%attr(755,root,root) %{_bindir}/pactree
%attr(755,root,root) %{_bindir}/pkgdelta
%attr(755,root,root) %{_bindir}/repo-add
%attr(755,root,root) %{_bindir}/repo-elephant
%attr(755,root,root) %{_bindir}/repo-remove
%attr(755,root,root) %{_bindir}/testpkg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/makepkg.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pacman.conf
%{_datadir}/pacman
%{_mandir}/man1/makepkg-template.1*
%{_mandir}/man5/PKGBUILD.5*
%{_mandir}/man5/makepkg.conf.5*
%{_mandir}/man5/pacman.conf.5*
%{_mandir}/man8/makepkg.8*
%{_mandir}/man8/pacman.8*
%{_mandir}/man8/pacman-key.8*
%{_mandir}/man8/pacman-vercmp.8*
%{_mandir}/man8/pactree.8*
%{_mandir}/man8/pkgdelta.8*
%{_mandir}/man8/repo-add.8*
%{_mandir}/man8/repo-remove.8*

%files libs -f libalpm.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_libdir}/libalpm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libalpm.so.9

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libalpm.so
%{_includedir}/alpm.h
%{_includedir}/alpm_list.h
%{_pkgconfigdir}/libalpm.pc
%{_mandir}/man3/libalpm.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libalpm.a
