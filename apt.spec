#Mandriva version adapted from Caixa Magica's apt package

#Workaround for awkward jsoncpp packaging: the jsoncpp-devel package
#doesnt provide any copy of libjsoncpp.so
%define _requires_exceptions devel(libjsoncpp

%define	name		apt
%define version		0.5.15lorg3.94
%define versionadd	pt
%define release %mkrel	1
%define _lib_name	%{name}-pkg
%define lib_name_orig	lib%{_lib_name}
%define major		4
%define libname		%mklibname %_lib_name %major
%define libnamedevel	%mklibname %_lib_name %major -d


Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Debian's Advanced Packaging Tool with RPM support 
Group:		System/Configuration/Packaging
Url:		http://www.apt-rpm.org/
License:	GPLv2+
Source0: 	%{name}-%{version}%{versionadd}.tar.bz2	
Source1:	%{name}-apt.conf.bz2
Source2:	%{name}-sources.list
Source3:	%{name}-vendors.list
Source4:	%{name}-rpmpriorities.bz2
Source5:	%{name}-mandriva.conf
# not used
Source8:	apt-pbo

## from Caixa Magica's apt:
# URPM Lists support 
# DUDF MANCOOSI project support
# Rollback, URPM, DUDF and pbo features 
Patch1:		%{name}-git-cm15-05.patch.bz2

# enhance the sorting by taking Obsoletes into account
Patch3:		apt-0.3.19cnc53-stelian-apt-pkg-algorithms-scores.patch
# TODO document this patch
Patch8:		%{name}-0.5.4cnc9-alt-packagemanager-CheckRConflicts.patch
# alternative scoring method ( PreDepends implies -1 instead of +50 )
Patch9:		%{name}-0.5.4cnc9-alt-pkgorderlist_score.patch
# add # to the list of the forbidden char in the name of cdrom
Patch11:	apt-0.5.15lorg3.2-alt-specialchars.patch

# s/de_DE/de/ and  /it_IT/it/ in po files
Patch14:	%{name}-invalid-lc-messages-dir.patch

# use the moo
Patch15:	apt-moo.patch

# a quick bugfixe to make build-dep work
Patch18:	%{name}-build-dep.patch


Requires:	gnupg
Requires: 	gzip
Requires:	%{name}-common
BuildRequires:	gettext-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-devel >= 4.6
# BuildRequires:  python-devel
BuildRequires:  libpopt-devel 
BuildRequires:  libxml2-devel 
BuildRequires:  sqlite3-devel
BuildRequires:  lua-devel >= 5.1
BuildRequires:  perl
BuildRequires:  automake, autoconf
BuildRequires:  jsoncpp-devel >= 0.5.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Epoch: 1

%description
A port of Debian's apt tools for RPM based distributions. 
Original RPM port done by and for Conectiva. It provides 
the apt-get utility that provides a simple way to install 
and upgrade packages. APT features complete installation 
ordering, multiple source capability and several other 
unique features. 

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Provides:	%{lib_name_orig} = %{epoch}:%{version}-%{release}
Requires:   %name-common
#For uuidgen
Requires:	e2fsprogs
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
# only header files in this package...
Requires:	jsoncpp-devel

%description -n %{libnamedevel}
This package contains the header files and static libraries for
developing with APT's libapt-pkg package manipulation library,
modified for RPM.

%package pbo
Summary:	Alternate dependency solver for apt.
Group:		System/Configuration/Packaging
BuildArch:	noarch
Requires:	%{name}-common
Requires:	perl
Requires:	minisat+
Requires:	perl-libapt-pkg
%description pbo
Alternate dependency solver for the apt package manager.
Currently in testing.

%package common
Summary:	Common file for %{name} frontend
Group:		System/Configuration/Packaging
%description common
This package contains the needed files for various apt-frontend, 
such as synaptic, aptitude.

%prep
%setup -q -n %{name}-%{version}%{versionadd}
%patch1 -p1
%patch3 -p1 -b .scores
%patch8 -p1 -b .checkrconflicts
%patch9 -p1 -b .predepends-scores
%patch11 -p1 -b .specialchars
%patch14 -p1
%patch15 -p1 -b .moo
%patch18 -p1 -b .build-dep-fix

bzcat %{SOURCE1} > apt.conf
sed 's/%%ARCH%%/%{_target_cpu}/' %{SOURCE2} > sources.list
cat %{SOURCE3} > vendors.list
bzcat %{SOURCE4} > rpmpriorities
cat %{SOURCE5} > mandriva.conf

%build
rm -f configure
libtoolize --copy --force --install
aclocal -I m4
automake -a -c
autoconf
%configure2_5x 

# This next line is necessary because of the invalid-lc-messages-dir patch
(cd po; cp -f de_DE.po de.po; cp -f it_IT.po it.po)


# Parallel make is taken account in the configure script
%make NOISY=1

#( cd python; %make )

%install
cat <<EOF >README.Mandriva
This version uses the synthesis form of the hdlist which is specified as a urpm 
source. The "rpm" source represents a debian-style pkglist, so full hdlists 
cannot be used anymore.

EOF

rm -rf $RPM_BUILD_ROOT
%makeinstall
rm -rf $RPM_BUILD_ROOT%{_bindir}/apt-pbo

install -d -m 755 $RPM_BUILD_ROOT/var/cache/%{name}/archives/partial
install -d -m 755 $RPM_BUILD_ROOT/var/lib/%{name}/lists/partial

install -d -m 755 $RPM_BUILD_ROOT%{_includedir}/apt-pkg
mv $RPM_BUILD_ROOT%{_includedir}/*.h $RPM_BUILD_ROOT%{_includedir}/apt-pkg

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/apt
echo "APT::Install-Suggests \"true\";" > $RPM_BUILD_ROOT%{_sysconfdir}/apt/apt.conf.d/01-suggests.conf
install -m 644 apt.conf $RPM_BUILD_ROOT%{_sysconfdir}/apt
install -m 644 *.list $RPM_BUILD_ROOT%{_sysconfdir}/apt
install -m 644 rpmpriorities $RPM_BUILD_ROOT%{_sysconfdir}/apt

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/apt/apt.conf.d
install -m 644 mandriva.conf $RPM_BUILD_ROOT%{_sysconfdir}/apt/apt.conf.d

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/apt/translate.list.d

install -d -m 755 $RPM_BUILD_ROOT%{_var}/lib/apt/dudf

#install -d -m 755 $RPM_BUILD_ROOT%{_sbindir}
#install -m 755 %SOURCE8 $RPM_BUILD_ROOT%{_sbindir}

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
#AG: Script directory, this should really be created by "make install" itself
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/apt/scripts

%find_lang %{name}
%find_lang %{lib_name_orig}-pkg3.3
cat %{lib_name_orig}-pkg3.3.lang >> %{name}.lang
rm -f %{lib_name_orig}-pkg3.3.lang


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

%post -n %{name}-common

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING* doc/*.txt doc/examples AUTHORS* README.Mandriva
%{_bindir}/*
%{_mandir}/man5/*
%{_mandir}/man8/*

#files pbo
#{_sbindir}/apt-pbo

%files common
%{_libdir}/%{name}
/var/cache/%{name}
/var/lib/%{name}
%{_datadir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/apt/apt.conf 
%config(noreplace) %{_sysconfdir}/apt/sources.list
%config(noreplace) %{_sysconfdir}/apt/vendors.list
%config(noreplace) %{_sysconfdir}/apt/rpmpriorities
%dir %{_sysconfdir}/apt/apt.conf.d
%config(noreplace) %{_sysconfdir}/apt/apt.conf.d/mandriva.conf
%config(noreplace) %{_sysconfdir}/apt/apt.conf.d/multilib.conf
%config(noreplace) %{_sysconfdir}/apt/apt.conf.d/01-suggests.conf
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
%{_libdir}/pkgconfig/*.pc

