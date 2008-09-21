Summary:	Universal SSL tunnel
Summary(pl.UTF-8):	Uniwersalne narzędzie do bezpiecznego tunelowania
Name:		stunnel
Version:	4.26
Release:	1
License:	GPL v2+
Group:		Networking/Daemons
Source0:	ftp://stunnel.mirt.net/stunnel/%{name}-%{version}.tar.gz
# Source0-md5:	0f6706540fbe000513940f4860698405
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.inet
Patch0:		%{name}-gethostbyname_is_in_libc_aka_no_libnsl.patch
Patch1:		%{name}-authpriv.patch
Patch2:		%{name}-ac_fixes.patch
Patch3:		%{name}-am.patch
Patch4:		%{name}-libwrap_srv_name_log.patch
Patch5:		%{name}-config.patch
URL:		http://www.stunnel.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	openssl-tools >= 0.9.7d
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(postun):	/sbin/ldconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(stunnel)
Provides:	user(stunnel)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The stunnel program is designed to work as SSL encryption wrapper
between remote client and local (inetd-startable) or remote server.
The concept is that having non-SSL aware daemons running on your
system you can easily setup them to communicate with clients over
secure SSL channel. stunnel can be used to add SSL functionality to
commonly used inetd daemons like POP-2, POP-3 and IMAP servers without
any changes in the programs' code.

%description -l pl.UTF-8
Stunnel umożliwia stawianie silnie kodowanych tuneli pomiędzy serwerem
a komputerem klienta. Przy jego użyciu można łatwo zrealizować usługi
pop3s lub HTTPS.

%package standalone
Summary:	stunnel acts as standalone server
Summary(pl.UTF-8):	stunnel działający jako samodzielny serwer
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts
Obsoletes:	stunnel-inetd

%description standalone
stunnel acts as standalone server.

%description standalone -l pl.UTF-8
stunnel działający jako samodzielny serwer.

%package inetd
Summary:	stunnel acts as inetd service
Summary(pl.UTF-8):	stunnel działający jako usługa inetd
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	rc-inetd
Obsoletes:	stunnel-standalone

%description inetd
stunnel acts as inetd service.

%description inetd -l pl.UTF-8
stunnel działający jako usługa inetd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig/rc-inetd},%{_mandir}/{pl,fr}/man8,%{_var}/run/stunnel}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_mandir}/man8/stunnel.fr.8 $RPM_BUILD_ROOT%{_mandir}/fr/man8/stunnel.8
mv -f $RPM_BUILD_ROOT%{_mandir}/man8/stunnel.pl.8 $RPM_BUILD_ROOT%{_mandir}/pl/man8/stunnel.8
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/stunnel/stunnel.conf-sample $RPM_BUILD_ROOT%{_sysconfdir}/stunnel/stunnel.conf

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/stunnel
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/stunnel
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/stunnel

rm -rf $RPM_BUILD_ROOT%{_libdir}/stunnel
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/stunnel/stunnel.pem
rm -rf $RPM_BUILD_ROOT%{_docdir}/stunnel

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 130 stunnel
%useradd -u 130 -d /var/run/stunnel -s /bin/false -c "stunnel User" -g stunnel stunnel

%post	-p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%userremove stunnel
	%groupremove stunnel
fi

%post standalone
/sbin/chkconfig --add stunnel
%service stunnel restart "stunnel daemon"

%preun standalone
if [ "$1" = "0" ]; then
	%service stunnel stop
	/sbin/chkconfig --del stunnel
fi

%post inetd
%service -q rc-inetd reload

%postun inetd
if [ "$1" = "0" ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
# note: this COPYING contains general information not GPL text
%doc AUTHORS BUGS COPYING CREDITS ChangeLog NEWS PORTS README TODO doc/en/* doc/stunnel.html
%doc src/stunnel.exe tools/{ca.*,importCA.*}
%doc %lang(fr) doc/stunnel.fr.html
%doc %lang(pl) doc/pl/* doc/stunnel.pl.html
%attr(750,stunnel,stunnel) %{_var}/run/stunnel
%dir %{_sysconfdir}/stunnel
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/stunnel/stunnel.conf
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man8/*
%lang(fr) %{_mandir}/fr/man8/*
%lang(pl) %{_mandir}/pl/man8/*

%files standalone
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/stunnel
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/stunnel

%files inetd
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/stunnel
