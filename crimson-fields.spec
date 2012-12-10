%define	version	0.5.3
%define	release	%mkrel 3

%define	pname	crimson
%define	name	%{pname}-fields

Name:		%name
Version:	%{version}
Release:	%{release}
Summary:	Crimson Fields - Tactical war game with hexagonal grid
License:	GPL
Group:		Games/Strategy
URL:		http://crimson.seul.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source:		http://crimson.seul.org/files/%{pname}-%{version}.tar.bz2

BuildRequires:	imagemagick 
BuildRequires:  SDL_mixer-devel 
BuildRequires:  SDL_ttf-devel 
BuildRequires:  libxslt-proc
BuildRequires:  zlib-devel
BuildRequires:  desktop-file-utils
Obsoletes:	crimson-field
Provides:	crimson-field

%package	utils
Summary:	Utilities for Crimson Fields (a tactical war game)
Group:		Games/Strategy
Requires:	%{name} = %{version}

%description
Crimson Fields is a tactical war game in the tradition of Battle Isle. While
not being an exact clone, it tries to keep closer to the very first part of the
series than to the later ones, especially with regard to a rather simple rule
set and straight forward game play.

A simple editor can be used to create custom level files.

%description	utils
Crimson Fields is a tactical war game in the tradition of Battle Isle. While
not being an exact clone, it tries to keep closer to the very first part of the
series than to the later ones, especially with regard to a rather simple rule
set and straight forward game play.

This package includes utilities for Crimson Fields, including a simple map
editor for creating custom level files, map compiler and Battle Isle map
conversion tool.

%prep
%setup -q -n %{pname}-%{version}

%build
%configure2_5x \
	--bindir=%{_gamesbindir} \
	--enable-cfed \
	--enable-bi2cf \
	--enable-comet

# (Abel) cfed uses SDL which initializes directfb when trying to build
# level files, which means this package is unbuildable without console
# access (at least I don't know how to do it without console access).
# When updating package, please regenerate level files in your machine
# and bundle them into source1.
# Version check is for preventing brainless updating.
[ "%version" = "0.4.2" ] && tar --bzip2 -xf %{SOURCE1}
touch levels/*.lev

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std


desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-MoreApplications-Games-Strategy;Game;StrategyGame" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


install -d $RPM_BUILD_ROOT%{_iconsdir} \
           $RPM_BUILD_ROOT%{_miconsdir}
install -m644 gfx/crimson.png -D $RPM_BUILD_ROOT%{_liconsdir}/%{pname}.png
convert -geometry 32x32 gfx/crimson.png $RPM_BUILD_ROOT%{_iconsdir}/%{pname}.png
convert -geometry 16x16 gfx/crimson.png $RPM_BUILD_ROOT%{_miconsdir}/%{pname}.png

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%doc ChangeLog COPYING NEWS README 
%{_iconsdir}/%{pname}.png
%{_miconsdir}/%{pname}.png
%{_liconsdir}/%{pname}.png
%{_gamesbindir}/crimson
%{_datadir}/%{pname}
%{_datadir}/pixmaps/*
%{_mandir}/man6/crimson.*
%{_datadir}/applications/crimson.desktop

%files utils
%defattr(-,root,root)
%doc README.CoMET README.bi2cf
%{_gamesbindir}/comet
%{_gamesbindir}/cfed
%{_gamesbindir}/bi2cf
%{_mandir}/man6/comet.*
%{_mandir}/man6/cfed.*
%{_mandir}/man6/bi2cf.*


%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.3-3mdv2011.0
+ Revision: 617438
- the mass rebuild of 2010.0 packages

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 0.5.3-2mdv2010.0
+ Revision: 437154
- rebuild

* Fri Apr 03 2009 trem <trem@mandriva.org> 0.5.3-1mdv2009.1
+ Revision: 363933
- update to 0.5.3
- fix the bug 49508

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 0.5.1-3mdv2009.0
+ Revision: 243727
- rebuild
- drop old menu

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0.5.1-1mdv2008.1
+ Revision: 136347
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Thu Jan 25 2007 Lenny Cartier <lenny@mandriva.com> 0.5.1-1mdv2007.0
+ Revision: 113282
- Update to 0.5.1

* Tue Dec 12 2006 Lenny Cartier <lenny@mandriva.com> 0.5.0-1mdv2007.1
+ Revision: 95345
- Update to 0.5.0

* Fri Oct 27 2006 Nicolas LÃ©cureuil <neoclust@mandriva.org> 0.4.9-3mdv2007.1
+ Revision: 73078
- Fix file list
- Fix BuildRequires
- import crimson-fields-0.4.9-2mdv2007.0

* Fri Aug 04 2006 Lenny Cartier <lenny@mandriva.com> 0.4.9-2mdv2007.0
- xdg

* Thu Nov 03 2005 trem <trem@zarb.org> 0.4.9-1mdk
- 0.4.9

* Wed Feb 23 2005 Lenny Cartier <lenny@mandrakesoft.com> 0.4.7-1mdk
- 0.4.7

* Wed Jan 19 2005 Lenny Cartier <lenny@mandrakesoft.com> 0.4.6-1mdk
- 0.4.6

* Sat Jun 19 2004 Abel Cheung <deaddog@deaddog.org> 0.4.2-1mdk
- New version
- Build map editor and other utils as well

* Thu Mar 04 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.4.1-1mdk
- 0.4.1

* Wed Feb 25 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.4.0-1mdk
- 0.4.0
- buildrequires
- cosmetics
- drop unused icons from src.rpm

