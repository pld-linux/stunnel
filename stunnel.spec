Summary:	Universal SSL tunnel
Summary(pl):	Uniwersalne narzêdzie do bezpiecznego tunelowania
Name:		stunnel
Version:	3.22
Release:	2
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://stunnel.mirt.net/stunnel/%{name}-%{version}.tar.gz
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-gethostbyname_is_in_libc_aka_no_libnsl.patch
Patch2:		%{name}-piddir.patch
Patch3:		%{name}-gen-cert.patch
Patch4:		%{name}-authpriv.patch
Patch5:		%{name}-ac_fixes.patch
Patch6:		%{name}-3.22-sigchld.patch
URL:		http://www.stunnel.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openssl-devel >= 0.9.6a
BuildRequires:	openssl-tools >= 0.9.6a
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_certdir	/var/lib/stunnel

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
%patch5 -p1
%patch6 -p1

%build
%{__autoconf}
%configure \
	--with-pem-dir=%{_certdir}
	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	certdir=$RPM_BUILD_ROOT/%{_certdir}
	
gzip -9nf BUGS CREDITS FAQ HISTORY README TODO doc/english/transproxy.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz doc/english/*.gz doc/english/*.html
%doc %lang(pl) doc/polish/*
%doc stunnel.exe
%config(noreplace) %verify(not size mtime md5) %attr(600,root,root) %{_certdir}/stunnel.pem
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/*
%dir /var/run/stunnel
%{_mandir}/man8/*
