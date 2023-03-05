Summary:	Pacman - simple library-based package manager (from Arch Linux)
Summary(pl.UTF-8):	Pacman - prosty, oparty na bibliotece zarządca pakietów (z Arch Linuksa)
Name:		alpm
Version:	6.0.2
Release:	0.1
License:	GPL v2+
Group:		Libraries
Source0:	https://sources.archlinux.org/other/pacman/pacman-%{version}.tar.xz
# Source0-md5:	f2c7e82cc5483a2c90f228a0393f5526
URL:		https://www.archlinux.org/pacman/
BuildRequires:	bash >= 4.4.0
BuildRequires:	bash-completion-devel >= 2.0
BuildRequires:	bsdtar
BuildRequires:	curl-devel >= 7.55.0
BuildRequires:	doxygen
BuildRequires:	file >= 5.38
BuildRequires:	gettext-devel >= 0.13.1
BuildRequires:	gpgme-devel >= 1.3.0
BuildRequires:	libarchive-devel >= 3.0.0
BuildRequires:	meson >= 0.51
BuildRequires:	ninja >= 1.5
# or nettle
BuildRequires:	openssl-devel
BuildRequires:	perl-base >= 1:5.10.1
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.2
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	bash >= 4.4.0
Requires:	file >= 5.38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pacman is a simple library-based package manager, designed for Arch
Linux.

%description -l pl.UTF-8
Pacman to prosty, oparty na bibliotece zarządca pakietów, powstały dla
Arch Linuksa.

%package -n bash-completion-alpm
Summary:	Bash completion for Arch Linux Package Manager (Pacman)
Summary(pl.UTF-8):	Bashowe dopełnianie parametrów dla zarządcy pakietów Arch Linuksa (Pacmana)
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-alpm
Bash completion for Arch Linux Package Manager (Pacman).

%description -n bash-completion-alpm -l pl.UTF-8
Bashowe dopełnianie parametrów dla zarządcy pakietów Arch Linuksa
(Pacmana).

%package -n zsh-completion-alpm
Summary:	ZSH completion for Arch Linux Package Manager (Pacman)
Summary(pl.UTF-8):	Dopełnianie parametrów zarządcy pakietów Arch Linuksa (Pacmana) dla powłoki ZSH
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-alpm
ZSH completion for Arch Linux Package Manager (Pacman).

%description -n zsh-completion-alpm -l pl.UTF-8
Dopełnianie parametrów zarządcy pakietów Arch Linuksa (Pacmana) dla
powłoki ZSH.

%package libs
Summary:	Arch Linux Package Management library
Summary(pl.UTF-8):	Biblioteka Arch Linux Package Management
Group:		Libraries
Requires:	curl-libs >= 7.55.0
Requires:	gpgme >= 1.3.0

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
Requires:	curl-devel >= 7.55.0
Requires:	gpgme-devel >= 1.3.0
Requires:	libarchive-devel >= 3.0.0
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
%meson build \
	-Ddoxygen=enabled

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# too generic names
%{__mv} $RPM_BUILD_ROOT%{_bindir}/{,pacman-}vercmp
%{__mv} $RPM_BUILD_ROOT%{_mandir}/man8/{,pacman-}vercmp.8

# "Spanish (Latin America)" - clone to individual countries or provide es_419 as common?
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/es_419
# less complete version of eu
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/eu_ES

# doxygen junk
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/_*.3*

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
%attr(755,root,root) %{_bindir}/makepkg
%attr(755,root,root) %{_bindir}/makepkg-template
%attr(755,root,root) %{_bindir}/pacman
%attr(755,root,root) %{_bindir}/pacman-conf
%attr(755,root,root) %{_bindir}/pacman-db-upgrade
%attr(755,root,root) %{_bindir}/pacman-key
%attr(755,root,root) %{_bindir}/pacman-vercmp
%attr(755,root,root) %{_bindir}/repo-add
%attr(755,root,root) %{_bindir}/repo-elephant
%attr(755,root,root) %{_bindir}/repo-remove
%attr(755,root,root) %{_bindir}/testpkg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/makepkg.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pacman.conf
%{_datadir}/makepkg
%{_datadir}/pacman
%{_npkgconfigdir}/libmakepkg.pc
%{_mandir}/man1/makepkg-template.1*
%{_mandir}/man5/BUILDINFO.5*
%{_mandir}/man5/PKGBUILD.5*
%{_mandir}/man5/alpm-hooks.5*
%{_mandir}/man5/makepkg.conf.5*
%{_mandir}/man5/pacman.conf.5*
%{_mandir}/man5/pacman-hooks.5*
%{_mandir}/man8/makepkg.8*
%{_mandir}/man8/pacman.8*
%{_mandir}/man8/pacman-conf.8*
%{_mandir}/man8/pacman-key.8*
%{_mandir}/man8/pacman-vercmp.8*
%{_mandir}/man8/repo-add.8*
%{_mandir}/man8/repo-remove.8*

%files -n bash-completion-alpm
%defattr(644,root,root,755)
%{bash_compdir}/makepkg
%{bash_compdir}/pacman
%{bash_compdir}/pacman-key

%files -n zsh-completion-alpm
%defattr(644,root,root,755)
%{_datadir}/zsh/site-functions/_pacman

%files libs -f libalpm.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_libdir}/libalpm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libalpm.so.13

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libalpm.so
%{_includedir}/alpm.h
%{_includedir}/alpm_list.h
%{_pkgconfigdir}/libalpm.pc
%{_mandir}/man3/libalpm.3*
%{_mandir}/man3/libalpm_*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libalpm.a
