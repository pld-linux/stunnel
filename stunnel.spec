Summary:	-
Summary(de):	-
Summary(fr):	-
Summary(pl):	-
Summary(tr):	-
Name:		stunnel
Version:	3.2
Release:	1
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Copyright:	GPL
Source0:	http://mike.daewoo.com.pl/computer/stunnel/%{name}-%{version}.tar.gz
Patch0:		stunnel-Makefile.patch
Patch1:		-
Patch2:		-
URL:		http://mike.daewoo.com.pl/computer/stunnel/
BuildPrereq:	openssl
BuildRoot:   	/tmp/%{name}-%{version}-root

%description

%description -l de

%description -l fr

%description -l pl

%description -l tr

%prep
%setup  -q -n %{name}
%patch0 -p1
#%patch1 -p1
#%patch2 -p1

%build
#(autoheader/autoconf/automake)
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure \
	--prefix=/usr \
	--target=%{_target_platform} \
	--host=%{_host} \
	
make \
	SSLLIBS="-lssl -lsslcrypto" \
	SSLINCDIR="/usr/include/ssl" 

%install
rm -rf $RPM_BUILD_ROOT

make install \
	DESTDIR="$RPM_BUILD_ROOT/usr" \
	CERTDIR="$RPM_BUILD_ROOT/var/state/ssl/certs"
	
gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	FAQ HISTORY README BUGS

%pre

%preun

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {FAQ,HISTORY,README,BUGS}.gz
%attr(755,root,root) /usr/sbin/*
%{_mandir}/man8/*
/var/state/ssl/certs/stunnel.pem

%changelog
* Thu May 13 1999 Artur Frysiak <wiget@pld.org.pl>
  [3.2-1]
- initial release  
