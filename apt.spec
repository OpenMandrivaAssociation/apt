%define	name		apt
%define version 0.5.15cnc6
%define release %mkrel 15
%define _lib_name	%{name}-pkg
%define lib_name_orig	lib%{_lib_name}
%define major		0
%define libname		%mklibname %_lib_name %major
%define libnamedevel	%mklibname %_lib_name %major -d

#TODO 
# check lua support ( switch )
# add something to ease downloading of source


Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Debian's Advanced Packaging Tool with RPM support 
Group:		System/Configuration/Packaging
Url:		https://moin.conectiva.com.br/AptRpm
License:	GPL
# downloaded on https://moin.conectiva.com.br/AptRpm?action=AttachFile&do=get&target=%{name}-%{version}.tar.bz2
# use wget -U some_user_agent, it prevent wget downloading
# wget -U plop "https://moin.conectiva.com.br/AptRpm?action=AttachFile&do=get&target=%{name}-%{version}.tar.bz2"
Source0:	https://moin.conectiva.com.br/files/AptRpm/attachments/%{name}-%{version}.tar.bz2
Source1:	%{name}-apt.conf.bz2
Source2:	%{name}-sources.list.bz2
Source3:	%{name}-vendors.list.bz2
Source4:	%{name}-rpmpriorities.bz2
Source5:	%{name}-mandriva.conf.bz2

# (misc) replace all mentions of Debian and Conectiva with Mandriva
Patch2:		%{name}-mandrake-everywhere.patch.bz2

# enhance the sorting by taking Obsoletes into account
Patch3:		%{name}-0.3.19cnc53-stelian-apt-pkg-algorithms-scores.patch.bz2
# mark some mdk package as essential
Patch4:		%{name}-0.5.4cnc7-rpmpriorities.patch.bz2
# add a configuration option ( APT::Install::Virtual )
Patch6:		%{name}-0.5.4cnc9-alt-install_virtual.patch.bz2
#Patch7:		%{name}-0.5.4cnc9-alt-install_virtual_version.patch.bz2

# TODO document this patch
Patch8:		%{name}-0.5.4cnc9-alt-packagemanager-CheckRConflicts.patch.bz2
# alternative scoring method ( PreDepends implies -1 instead of +50 )
Patch9:		%{name}-0.5.4cnc9-alt-pkgorderlist_score.patch.bz2
#Patch10:	%{name}-0.5.4cnc9-alt-rsync.patch.bz2

# add # to the list of the forbidden char in the name of cdrom
Patch11:	%{name}-0.5.4cnc9-alt-specialchars.patch.bz2

# add a missing ifdef
Patch12:	%{name}-0.5.5cnc1-alt-APT_DOMAIN.patch.bz2

# add APT::Ignore-dpkg option, to not take dpkg in account
# for score calculation
Patch13:	%{name}-0.5.5cnc1-alt-debsystem.patch.bz2

# s/de_DE/de/ and  /it_IT/it/ in po files
Patch14:	%{name}-invalid-lc-messages-dir.patch.bz2

# use the moo
Patch15:    %{name}-moo.patch.bz2

# enforce Epoch promotion
#Patch16:    %{name}.0.5.15cnc4-epoch.patch.bz2

# add WhatProvides command
Patch17:    %{name}-0.5.15cnc4-whatprovides.patch.bz2

# a quick bugfixe to make build-dep work
Patch18:    %{name}-build-dep.patch.bz2

# x86-64 and other build fixes for python
Patch19:        apt-0.5.15cnc6-python-build-fixes.patch.bz2

# rpm 4.4.4 fix
Patch20:	apt-0.5.15cnc6-rpm-4.4.4.patch.bz2

# (cjw) add support for rpm 4.4.x Suggests: tag
Patch21:	apt-0.5.15cnc6-rpm-suggests.patch.bz2

# rpm 4.4.6 fixes
Patch22:	apt-0.5.15cnc6-rpm-4.4.6.patch.bz2

# fix rpmlib(...) check for case when 1st internal dep matches
# from 0.5.15lorg3.2
Patch23:	apt-0.5.15cnc6-fix-rpm-internal-dep-check.patch.bz2

# use hdlist ( in gz ) instead of apt index ( in bz2 )
# it replace bz2 compression by gz, 
# it remove some check in acquire-item.cc
# it add default 0: Epoch to all package
Patch300:	%{name}-0.5.5cnc6-mdk.patch.bz2

Requires:	gnupg
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	docbook-utils
BuildRequires:	gettext-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-devel >= 4.2
BuildRequires:  python-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Epoch: 1

%description
A port of Debian's apt tools for RPM based distributions,
or at least for Mandriva Linux. Original RPM port done by and 
for Conectiva. It provides the apt-get utility that
provides a simpler, safer way to install and upgrade packages.
APT features complete installation ordering, multiple source
capability and several other unique features. 

Under development, use at your own risk!

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Provides:	%{lib_name_orig} = %{epoch}:%{version}-%{release}
Requires:   %name-common
Obsoletes:	libapt0.5
Provides:   libapt0.5

%description -n %{libname}
This package contains APT's libapt-pkg package manipulation library
modified for RPM.

%package -n %{libnamedevel}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	%{lib_name_orig}-devel
Obsoletes:	libapt0.5-devel
Provides:   libapt0.5-devel

%description -n %{libnamedevel}
This package contains the header files and static libraries for
developing with APT's libapt-pkg package manipulation library,
modified for RPM.

%package -n python-%{name}
Summary:	Python extension for %{name}
Group:		Development/Python

%description -n python-%{name}
This package contains a python modules to access to libapt-pkg. 
With it, you can use the apt configuration file, and access to 
the database of packages.

%package common
Summary:	Common file for %{name} frontend
Group:		System/Configuration/Packaging
Conflicts:  apt < 1:0.5.15cnc6-8mdk
%description common
This package contains the needed files for various apt-frontend, 
such as synaptic, aptitude.

%prep
%setup -q
# mdk everywhere patch
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
#%patch7 -p1
%patch8 -p1
%patch9 -p1
#%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
#%patch16 -p1
%patch17 -p1
%patch18 -p1 -b .build-dep-fix
%patch19 -p1 -b .fixes
%patch20 -p1 -b .rpm444
%patch21 -p1 -b .suggests
%patch22 -p1 -b .rpm446
%patch23 -p1 -b .internal-rpm-deps

%patch300 -p1 
#%patch301 -p1


bzcat %{SOURCE1} > apt.conf
bzcat %{SOURCE2} > sources.list
bzcat %{SOURCE3} > vendors.list
bzcat %{SOURCE4} > rpmpriorities
bzcat %{SOURCE5} > mandriva.conf

%build
# (misc) doesn't work without this on 24/12/2003, i do not have time to look further
cp -f /usr/share/gettext/po/Makefile.in.in po
export WANT_AUTOCONF_2_5=1
aclocal-1.7 -I buildlib
autoconf-2.5x
%configure2_5x --with-hashmap

# This next line is necessary because of the invalid-lc-messages-dir patch
(cd po; cp -f de_DE.po de.po; cp -f it_IT.po it.po)


# Parallel make is taken account in the configure script
%make NOISY=1

( cd python; %make )

%install
cat <<EOF >README.Mandriva
This version of apt includes various patch to integrate it with MandrivaLinux.

It uses the mandriva hdlist, which means you can use
any mandriva mirror in sources.list. You cannot use the synthesis
form of the hdlist at this time.

It adds an option APT::Install::Virtual, to control the installation
of pure virtual packages.

Christiaan Welvaart <cjw@daneel.dyndns.org> contributed  
a patch to add a whatprovides command to apt-cache, a patch
for apt-get build-dep and some other fixes.

And some others minor patch, please check the spec file 
on http://cvs.mandriva.com/contrib-SPECS/apt/

It was built without lua scripting support for the moment.
Python modules can be found in the python-apt package.
EOF

rm -rf $RPM_BUILD_ROOT
%makeinstall

install -d -m 755 $RPM_BUILD_ROOT/var/cache/%{name}/archives/partial
install -d -m 755 $RPM_BUILD_ROOT%{_localstatedir}/%{name}/lists/partial

install -d -m 755 $RPM_BUILD_ROOT%{_includedir}/apt-pkg
mv $RPM_BUILD_ROOT%{_includedir}/*.h $RPM_BUILD_ROOT%{_includedir}/apt-pkg

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/apt
install -m 644 apt.conf $RPM_BUILD_ROOT%{_sysconfdir}/apt
install -m 644 *.list $RPM_BUILD_ROOT%{_sysconfdir}/apt
install -m 644 rpmpriorities $RPM_BUILD_ROOT%{_sysconfdir}/apt

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/apt/apt.conf.d
install -m 644 mandriva.conf $RPM_BUILD_ROOT%{_sysconfdir}/apt/apt.conf.d

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/apt/translate.list.d

# (misc) remove this once the librpm package is fixed and do not
# contain reference to /home, no rpmlint warning.
perl -pi -e 's#-L/home/\w+##g' $RPM_BUILD_ROOT/%{_libdir}/*.la

%find_lang %{name}
%find_lang %{lib_name_orig}-pkg3.3
cat %{lib_name_orig}-pkg3.3.lang >> %{name}.lang
rm -f %{lib_name_orig}-pkg3.3.lang

# Python
install -d -m 755 $RPM_BUILD_ROOT/%py_sitedir/
install -m 644 python/_apt.so  $RPM_BUILD_ROOT/%py_sitedir/
install -m 644 python/apt.py $RPM_BUILD_ROOT/%py_sitedir/

%triggerun -- apt < 0.5.4
# Convert options from 0.3.X to 0.5.X
CONF=/etc/apt/apt.conf
if [ -f $CONF ]; then
   mv -f $CONF $CONF.rpmold
   sed -e 's/HoldPkgs/Hold/' \
       -e 's/AllowedDupPkgs/Allow-Duplicated/' \
       -e 's/IgnorePkgs/Ignore/' \
       -e 's/PostInstall/Post-Install/' \
       -e 's/.*Methods .*//' \
       $CONF.rpmold > $CONF
   if [ $? -ne 0 ]; then
      mv -f $CONF.rpmold $CONF
      echo "warning: couldn't convert old apt options"
   else
      echo "warning: original apt.conf saved as apt.conf.rpmold" 2>&1
   fi
fi

%triggerun -- apt > 0.5.4, apt < 0.5.4cnc4-1cl
# Fix bug in the trigger of first snapshot versions
CONF=/etc/apt/apt.conf
if [ -f $CONF ]; then
   mv $CONF $CONF.rpmtmp.$$
   sed -e 's/Holds/Hold/' \
       $CONF.rpmtmp.$$ > $CONF
   if [ $? -ne 0 ]; then
      mv -f $CONF.rpmtmp.$$ $CONF
   else
      rm -f $CONF.rpmtmp.$$
   fi
fi

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING* TODO doc/*.txt doc/examples AUTHORS* README.Mandriva
%{_bindir}/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files common
%{_libdir}/%{name}
/var/cache/%{name}
%{_localstatedir}/%{name}
%dir %{_sysconfdir}/apt
%config(noreplace) %{_sysconfdir}/apt/apt.conf 
%config(noreplace) %{_sysconfdir}/apt/sources.list
%config(noreplace) %{_sysconfdir}/apt/vendors.list
%config(noreplace) %{_sysconfdir}/apt/rpmpriorities
%dir %{_sysconfdir}/apt/apt.conf.d
%config(noreplace) %{_sysconfdir}/apt/apt.conf.d/mandriva.conf
%dir %{_sysconfdir}/apt/translate.list.d

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libnamedevel}
%defattr(-,root,root)
%{_includedir}/apt-pkg
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la

%files -n python-%{name}
%defattr(-,root,root)
%py_sitedir/*
