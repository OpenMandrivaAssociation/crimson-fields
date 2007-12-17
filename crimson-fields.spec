%define	version	0.5.1
%define	release	%mkrel 1

%define	pname	crimson
%define	name	%{pname}-fields

Name:		%name
Version:	%{version}
Release:	%{release}
Summary:	Crimson Fields - Tactical war game with hexagonal grid
License:	GPL
Group:		Games/Strategy
URL:		http://crimson.seul.org/

Source:		http://crimson.seul.org/files/%{pname}-%{version}.tar.bz2

BuildRequires:	ImageMagick 
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

mkdir -p $RPM_BUILD_ROOT/%{_menudir}
cat << EOF > $RPM_BUILD_ROOT/%{_menudir}/%{name}
?package(%{name}): \
 command="%{_gamesbindir}/%{pname}" \
 icon="%{pname}.png" \
 needs="x11" \
 section="More Applications/Games/Strategy" \
 title="Crimson Fields" \
 longtitle="Tactical war game with hexagonal grid" \
 xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-MoreApplications-Games-Strategy;Game;StrategyGame" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


install -d $RPM_BUILD_ROOT%{_iconsdir} \
           $RPM_BUILD_ROOT%{_miconsdir}
install -m644 gfx/crimson.png -D $RPM_BUILD_ROOT%{_liconsdir}/%{pname}.png
convert -geometry 32x32 gfx/crimson.png $RPM_BUILD_ROOT%{_iconsdir}/%{pname}.png
convert -geometry 16x16 gfx/crimson.png $RPM_BUILD_ROOT%{_miconsdir}/%{pname}.png

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%doc ChangeLog COPYING NEWS README 
%{_menudir}/%{name}
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



