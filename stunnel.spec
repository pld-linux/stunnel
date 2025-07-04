#
# Conditional build:
%bcond_without	systemd		# systemd socket activation support
%bcond_with	mimalloc	# use mimalloc

Summary:	Universal SSL tunnel
Summary(pl.UTF-8):	Uniwersalne narzędzie do bezpiecznego tunelowania
Name:		stunnel
Version:	5.75
Release:	2
License:	GPL v2+ with OpenSSL exception
Group:		Networking/Daemons
Source0:	https://www.stunnel.org/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	a10dc6f1925f4ce1945ff95dc327ed28
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.inet
Source4:	%{name}.tmpfiles
Patch0:		%{name}-config.patch
Patch1:		stunnel-libwrap_srv_name_log.patch
URL:		http://www.stunnel.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool >= 2:2.0
BuildRequires:	libwrap-devel
%{?with_mimalloc:BuildRequires:	mimalloc-devel}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	openssl-tools >= 0.9.7d
BuildRequires:	rpmbuild(macros) >= 1.268
%{?with_systemd:BuildRequires:	systemd-devel}
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

%package -n bash-completion-stunnel
Summary:	bash-completion for stunnel command
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów polecenia stunnel
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-stunnel
This package provides bash-completion for stunnel command.

%description -n bash-completion-stunnel -l pl.UTF-8
Pakiet ten dostarcza bashowe uzupełnianie parametrów polecenia
stunnel.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_mimalloc:ac_cv_header_mimalloc_h=no ac_cv_search_mi_malloc=no} \
	ac_cv_search_yp_get_default_domain=no \
	--disable-silent-rules \
	%{!?with_systemd:--disable-systemd} \
	--with-bashcompdir=%{bash_compdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig/rc-inetd},%{_mandir}/{pl,fr}/man8,%{_var}/run/stunnel} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_mandir}/man8/stunnel.pl.8 $RPM_BUILD_ROOT%{_mandir}/pl/man8/stunnel.8
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/stunnel/stunnel.conf-sample $RPM_BUILD_ROOT%{_sysconfdir}/stunnel/stunnel.conf

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/stunnel
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/stunnel
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/stunnel
install %{SOURCE4} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/stunnel
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/stunnel

%{__mv} $RPM_BUILD_ROOT%{bash_compdir}/stunnel.bash $RPM_BUILD_ROOT%{bash_compdir}/stunnel

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
%doc AUTHORS.md BUGS.md COPYING.md CREDITS.md NEWS.md PORTS.md README.md TODO.md doc/en/* doc/stunnel.html tools/{ca.*,importCA.*}
%doc %lang(pl) doc/pl/* doc/stunnel.pl.html
%attr(755,root,root) %{_bindir}/stunnel
%attr(755,root,root) %{_bindir}/stunnel3
%dir %{_sysconfdir}/stunnel
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/stunnel/stunnel.conf
%attr(750,stunnel,stunnel) %{_var}/run/stunnel
%{systemdtmpfilesdir}/%{name}.conf
%{_mandir}/man8/stunnel.8*
%lang(pl) %{_mandir}/pl/man8/stunnel.8*

%files standalone
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/stunnel
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/stunnel

%files inetd
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/stunnel

%files -n bash-completion-stunnel
%defattr(644,root,root,755)
%{bash_compdir}/stunnel
