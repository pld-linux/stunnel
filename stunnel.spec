Summary:	Universal SSL tunnel
Summary(pl):	Uniwersalne narzêdzie do bezpiecznego tunelowania
Name:		stunnel
Version:	4.05
Release:	1.1
License:	GPL v2
Group:		Networking/Daemons
Source0:	ftp://stunnel.mirt.net/stunnel/%{name}-%{version}.tar.gz
# Source0-md5:	e28a03cf694a43a7f144ec3d5c064456
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.inet
Patch0:		%{name}-gethostbyname_is_in_libc_aka_no_libnsl.patch
Patch1:		%{name}-authpriv.patch
Patch2:		%{name}-ac_fixes.patch
Patch3:		%{name}-am.patch
Patch4:		%{name}-getgrnam.patch
Patch5:		%{name}-libwrap_srv_name_log.patch
Patch6:		%{name}-config.patch
URL:		http://www.stunnel.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	openssl-tools >= 0.9.7d
BuildRequires:	libwrap-devel
PreReq:		rc-scripts
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Requires(post,preun):	/sbin/chkconfig
Requires(post,postun):	/sbin/ldconfig
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

%package standalone
Summary:	stunnel acts as standalone server 
Summary(pl):	stunnel dzia³aj±cy jako samodzielny serwer
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{name}-inetd

%description standalone
stunnel acts as standalone server.

%description standalone -l pl
stunnel dzia³aj±cy jako samodzielny serwer.

%package inetd 
Summary:	stunnel acts as inetd service
Summary(pl):	stunnel dzia³aj±cy jako us³uga inetd
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{name}-standalone

%description inetd
stunnel acts as inetd service.

%description standalone -l pl
stunnel dzia³aj±cy jako us³uga inetd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

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
mv -f $RPM_BUILD_ROOT/etc/stunnel/stunnel.conf-sample $RPM_BUILD_ROOT/etc/stunnel/stunnel.conf

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/stunnel
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/stunnel
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/stunnel

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig

%pre
if [ -n "`getgid stunnel`" ]; then
	if [ "`getgid stunnel`" != "130" ]; then
		echo "Error: group stunnel doesn't have gid=130. Correct this before installing stunnel." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 130 -r -f stunnel
fi
if [ -n "`id -u stunnel 2>/dev/null`" ]; then
	if [ "`id -u stunnel`" != "130" ]; then
		echo "Error: user stunnel doesn't have uid=130. Correct this before installing stunnel." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 130 -r -d /var/run/stunnel -s /bin/false -c "stunnel User" -g stunnel stunnel 1>&2
fi

%postun 
/sbin/ldconfig
if [ "$1" = "0" ]; then
	/usr/sbin/userdel stunnel
	/usr/sbin/groupdel stunnel
fi

%post standalone
/sbin/chkconfig --add stunnel
if [ -f /var/lock/subsys/stunnel ]; then
	/etc/rc.d/init.d/stunnel restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/stunnel start\" to start stunnel daemon."
fi

%preun standalone
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/stunnel ]; then
		/etc/rc.d/init.d/stunnel stop 1>&2
	fi
	/sbin/chkconfig --del stunnel
fi

%post inetd
if [ -f /var/lock/subsys/rc-inetd ]; then
        /etc/rc.d/init.d/rc-inetd restart 1>&2
else
        echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun inetd
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
fi

%files
%defattr(644,root,root,755)
# note: this COPYING contains general information not GPL text
%doc AUTHORS BUGS COPYING CREDITS ChangeLog NEWS PORTS README TODO doc/en/* doc/stunnel.html
%doc src/stunnel.exe  tools/{ca.*,importCA.*}
%doc %lang(fr) doc/stunnel.fr.html
%doc %lang(pl) doc/pl/* doc/stunnel.pl.html
%attr(750,stunnel,stunnel) %{_var}/run/stunnel
%dir /etc/stunnel
%config(noreplace) %verify(not size mtime md5) /etc/stunnel/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/*
%{_mandir}/man8/*
%lang(fr) %{_mandir}/fr/man8/*
%lang(pl) %{_mandir}/pl/man8/*

%files standalone
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/stunnel
/etc/sysconfig/stunnel

%files inetd
%defattr(644,root,root,755)
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/stunnel
