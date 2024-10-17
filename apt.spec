#Mandriva version adapted from Caixa Magica's apt package

#Workaround for awkward jsoncpp packaging: the jsoncpp-devel package
#doesnt provide any copy of libjsoncpp.so
%define _requires_exceptions devel(libjsoncpp

%define	name		apt
%define version 0.5.15lorg3.95
%define release %mkrel	1
%define _lib_name	%{name}-pkg
%define lib_name_orig	lib%{_lib_name}
%define major		4
%define libname		%mklibname %_lib_name %major
%define libnamedevel	%mklibname %_lib_name -d


Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Debian's Advanced Packaging Tool with RPM support 
Group:		System/Configuration/Packaging
Url:		https://www.apt-rpm.org/
License:	GPLv2+
# created from http://gitorious.org/rpm5distro/apt-rpm/
Source0:	http://apt-rpm.org/releases/%{name}-%{version}.tar.xz
Source1:	%{name}-apt.conf
Source2:	%{name}-sources.list
Source3:	%{name}-vendors.list
Source4:	%{name}-rpmpriorities
Source5:	%{name}-mandriva.conf
# not used
Source8:	apt-pbo

# use hdlist ( in gz ) instead of apt index ( in bz2 )
# it replace bz2 compression by gz, 
# it remove some check in acquire-item.cc
# it add default 0: Epoch to all package
#Patch300:	apt-0.5.15lorg3.2-mdv.patch

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
%setup -q
# TODO: make customizable
#%%patch300 -p1 -b .hdlist

%build
%configure2_5x 

# Parallel make is taken account in the configure script
%make NOISY=1

%if 0
(cd python; %make)
%endif

%install
cat <<EOF >README.Mandriva
This version uses the synthesis form of the hdlist which is specified as a urpm 
source. The "rpm" source represents a debian-style pkglist, so full hdlists 
cannot be used anymore.

EOF

rm -rf $RPM_BUILD_ROOT
%makeinstall -k
rm -rf $RPM_BUILD_ROOT%{_bindir}/apt-pbo

install -d -m 755 $RPM_BUILD_ROOT/var/cache/%{name}/archives/partial
install -d -m 755 $RPM_BUILD_ROOT/var/lib/%{name}/lists/partial

install -d -m 755 $RPM_BUILD_ROOT%{_includedir}/apt-pkg
mv $RPM_BUILD_ROOT%{_includedir}/*.h $RPM_BUILD_ROOT%{_includedir}/apt-pkg

install -m644 %{SOURCE1} -D $RPM_BUILD_ROOT%{_sysconfdir}/apt/apt.conf
echo "APT::Install-Suggests \"true\";" > $RPM_BUILD_ROOT%{_sysconfdir}/apt/apt.conf.d/01-suggests.conf
install -m644 %{SOURCE2} -D $RPM_BUILD_ROOT%{_sysconfdir}/apt/sources.list
install -m644 %{SOURCE3} -D $RPM_BUILD_ROOT%{_sysconfdir}/apt/vendors.list
install -m644 %{SOURCE4} -D $RPM_BUILD_ROOT%{_sysconfdir}/apt/rpmpriorities

install -m644 %{SOURCE5} -D $RPM_BUILD_ROOT%{_sysconfdir}/apt/apt.conf.d/mandriva.conf

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

# Python
%if 0
install -d -m 755 $RPM_BUILD_ROOT/%py_sitedir/
install -m 644 python/_apt.so  $RPM_BUILD_ROOT/%py_sitedir/
install -m 644 python/apt.py $RPM_BUILD_ROOT/%py_sitedir/
%endif

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
%{_libdir}/pkgconfig/libapt-pkg.pc

%if 0
%files -n python-%{name}
%defattr(-,root,root)
%py_sitedir/*
%endif
