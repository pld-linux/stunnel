# TODO:
# - fix /var/run/stunnel ownership (nobody must NOT own any files!)
Summary:	Universal SSL tunnel
Summary(pl):	Uniwersalne narzêdzie do bezpiecznego tunelowania
Name:		stunnel
Version:	4.04
Release:	0.9
License:	GPL v2
Group:		Networking/Daemons
Source0:	ftp://stunnel.mirt.net/stunnel/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-gethostbyname_is_in_libc_aka_no_libnsl.patch
Patch1:		%{name}-authpriv.patch
Patch2:		%{name}-ac_fixes.patch
Patch3:		%{name}-am.patch
Patch4:		%{name}-getgrnam.patch
URL:		http://www.stunnel.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	openssl-tools >= 0.9.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The stunnel program is designed to work as SSL encryption wrapper
between remote client and local (inetd-startable) or remote server.
The concept is that having non-SSL aware daemons running on your
system you can easily setup them to communicate with clients over
secure SSL channel. stunnel can be used to add SSL functionality to
commonly used inetd daemons like POP-2, POP-3 and IMAP servers without
any changes in the programs' code.

%description -l pl
Stunnel umo¿liwia stawianie silnie kodowanych tuneli pomiêdzy serwerem
a komputerem klienta. Przy jego u¿yciu mo¿na ³atwo zrealizowaæ us³ugi
pop3s lub https.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	-d $RPM_BUILD_ROOT%{_mandir}/pl/man8 \
	-d $RPM_BUILD_ROOT%{_var}/run/stunnel

%{__make} install DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT/%{_mandir}/man8/stunnel.pl.8* $RPM_BUILD_ROOT/%{_mandir}/pl/man8/

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/stunnel
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/stunnel

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS COPYING CREDITS ChangeLog NEWS PORTS README TODO doc/en/* doc/stunnel.html
%doc src/stunnel.exe
%doc $RPM_BUILD_ROOT%{_datadir}/doc/stunnel/examples/{c*,i*,stunnel.init}
%doc %lang(pl) doc/pl/* doc/stunnel.pl.html
%dir /etc/stunnel
%attr(755,root,root) /etc/rc.d/init.d/stunnel
%attr(600,root,root) /etc/sysconfig/stunnel
%attr(700,nobody,nobody) %{_var}/run/stunnel
%config(noreplace) %verify(not size mtime md5) /etc/stunnel/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/*
%{_mandir}/man8/*
%lang(pl) %{_mandir}/pl/man8/*
