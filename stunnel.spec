Summary:	Universal SSL tunnel
Summary(pl):	Uniwersalne narzedzie do bezpiecznego tunelowania
Name:		stunnel
Version:	3.4a
Release:	1
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Copyright:	GPL
Source0:	http://mike.daewoo.com.pl/computer/stunnel/%{name}-%{version}.tar.gz
Patch0:		stunnel-Makefile.patch
URL:		http://mike.daewoo.com.pl/computer/stunnel/
BuildRequires:	openssl-devel
BuildRoot:	/tmp/%{name}-%{version}-root

%define		certsdir	/var/state/openssl/certs

%description
The stunnel program is designed to work  as  SSL  encryption
wrapper between remote client and local (inetd-startable) or
remote server. The concept is that having non-SSL aware dae-
mons  running  on  your  system you can easily setup them to
communicate with clients over secure SSL channel.

stunnel can be used to add  SSL  functionality  to  commonly
used  inetd  daemons  like  POP-2,  POP-3  and  IMAP servers
without any changes in the programs' code.

%description -l pl
Stunnel umo¿liwia stawianie silnie kodowanych tuneli pomiêdzy 
serwerem a komputerem klienta. Przy jego u¿yciu mo¿na ³atwo 
zrealizowaæ us³ugi pop3s lub https.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
LDFLAGS="-s" ; export LDFLAGS
%configure 
	
make \
	SSLLIBS="-lssl -lsslcrypto" \
	SSLINCDIR="%{_includedir}/openssl" 

%install
rm -rf $RPM_BUILD_ROOT

make install \
	DESTDIR="$RPM_BUILD_ROOT%{_prefix}" \
	CERTDIR="$RPM_BUILD_ROOT%{certsdir}"
	
gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	FAQ HISTORY README BUGS 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {FAQ,HISTORY,README,BUGS}.gz 
%doc %lang(pl) doc.polish/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
%attr(600,root,root) %{certsdir}/stunnel.pem
