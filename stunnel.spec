Summary:	Universal SSL tunnel
Summary(pl):	Uniwersalne narzedzie do bezpiecznego tunelowania
Name:		stunnel
Version:	3.8
Release:	4
License:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	http://mike.daewoo.com.pl/computer/stunnel/%{name}-%{version}.tar.gz
Patch1:		stunnel-DESTDIR.patch
Patch2:		stunnel-dirs.patch
Patch3:		stunnel-fixargs.patch
URL:		http://mike.daewoo.com.pl/computer/stunnel/
BuildRequires:	openssl-devel >= 0.9.4-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		certdir		/var/lib/openssl/certs

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
%patch1 -p1 
%patch2 -p1 
%patch3 -p0 

%build
autoconf
CFLAGS="$RPM_OPT_FLAGS -DHAVE_GETOPT"
LDFLAGS="-s"
export CFLAGS LDFLAGS
%configure 
	
%{__make} certdir=%{certdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	certdir=$RPM_BUILD_ROOT/%{certdir}
	
gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	FAQ HISTORY README BUGS 

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {FAQ,HISTORY,README,BUGS}.gz 
%doc %lang(pl) doc.polish/*
%doc stunnel.exe
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/*

%{_mandir}/man8/*
%config(noreplace) %verify(not size mtime md5) %attr(600,root,root) %{certdir}/stunnel.pem
