Summary:	Universal SSL tunnel
Summary(pl):	Uniwersalne narzedzie do bezpiecznego tunelowania
Name:		stunnel
Version:	3.6
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	http://mike.daewoo.com.pl/computer/stunnel/%{name}-%{version}.tar.gz
Patch1:		stunnel-DESTDIR.patch
Patch2:		stunnel-dirs.patch
URL:		http://mike.daewoo.com.pl/computer/stunnel/
BuildRequires:	openssl-devel >= 0.9.4-2
BuildRoot:	/tmp/%{name}-%{version}-root

%define		certdir		/var/state/openssl/certs

%description
The stunnel program is designed to work as SSL encryption wrapper between
remote client and local (inetd-startable) or remote server. The concept is
that having non-SSL aware daemons running on your system you can easily
setup them to communicate with clients over secure SSL channel. stunnel can
be used to add SSL functionality to commonly used inetd daemons like POP-2,
POP-3 and IMAP servers without any changes in the programs' code.

%description -l pl
Stunnel umo�liwia stawianie silnie kodowanych tuneli pomi�dzy serwerem a
komputerem klienta. Przy jego u�yciu mo�na �atwo zrealizowa� us�ugi pop3s
lub https.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
autoconf
CFLAGS="$RPM_OPT_FLAGS -DHAVE_GETOPT"
LDFLAGS="-s"
export CFLAGS LDFLAGS
%configure 
	
make

%install
rm -rf $RPM_BUILD_ROOT

make install \
	DESTDIR=$RPM_BUILD_ROOT \
	certdir=$RPM_BUILD_ROOT/%{certdir}
	
gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	FAQ HISTORY README BUGS 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {FAQ,HISTORY,README,BUGS}.gz 
%doc %lang(pl) doc.polish/*
%doc stunnel.exe
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
%config(noreplace) %verify(not size mtime md5) %attr(600,root,root) %{certdir}/stunnel.pem
