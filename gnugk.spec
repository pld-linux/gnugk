Summary:	H.323 gatekeeper
Summary(pl):	Zarz±dca bramki H.323
Name:		gnugk
Version:	2.0.8
Release:	0.5
License:	GPL v2
Group:		Applications/Communications
Source0:	http://dl.sourceforge.net/openh323gk/%{name}-%{version}.tgz
# Source0-md5:	770309df3d631d6c94dfb3a95a9be25e
Source1:	%{name}.init
Source2:	%{name}.sysconfig
#Patch0:		%{name}-mak_files.patch
Patch1:		%{name}-openh323_headers.patch
Patch2:		%{name}-mak_variable.patch
URL:		http://www.gnugk.org/
BuildRequires:	speex-devel
BuildRequires:	openh323-devel >= 1.12.0
%requires_eq	openh323
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A H.323 gatekeeper controls all H.323 clients (endpoints like MS
Netmeeting) in his zone. Its most important function is address
translation between symbolic alias addresses and IP addresses. This
way you can call "jan" instead of knowing which IP address he
currently works on.

%description -l pl
Zarz±dca bramki kontroluje wszystkich klientów H.323 (koñcówki podobne
do MS Netmeeting) w swojej strefie. Jego najwa¿niejsz± funkcj± jest
translacja adresów pomiêdzy symbolicznymi aliasami a adresami IP. W
ten sposób mo¿esz wo³aæ "jan" zamiast podawaæ adres IP stanowiska
gdzie pracuje.

%prep
%setup -qn openh323gk
#%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
NO_LDAP=1; export NO_LDAP
NO_MYSQL=1; export NO_MYSQL
PWLIBDIR=%{_prefix}; export PWLIBDIR
OPENH323DIR=%{_prefix}; export OPENH323DIR
%{__make} %{?debug:debugshared}%{!?debug:optshared} \
	OPTCCFLAGS="%{!?debug:$RPM_OPT_FLAGS}" \
	CC="%{__cc}" CPLUS="%{__cxx}" \
	OH323MAK=%{_prefix}/share/openh323/openh323u.mak \
	VERSION_FILE=%{_prefix}/include/openh323/version.h

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}{/rc.d/init.d,/sysconfig}}

install obj_*/%{name} $RPM_BUILD_ROOT%{_sbindir}

# this config was insecure, insert empty file instead
#install etc/gnugk.ini $RPM_BUILD_ROOT%{_sysconfdir}
echo ";; See example config files in %{_docdir}/%{name}-%{version}" >$RPM_BUILD_ROOT%{_sysconfdir}/gnugk.ini

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/gnugk
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/gnugk

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add gnugk
if [ -r /var/lock/subsys/gnugk ]; then
	/etc/rc.d/init.d/gnugk restart >&2
else
	echo "Run \"/etc/rc.d/init.d/gnugk start\" to start OpenH323 gatekeeper."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/gnugk ]; then
		/etc/rc.d/init.d/gnugk stop >&2
	fi
	/sbin/chkconfig --del gnugk
fi

%files
%defattr(644,root,root,755)
%doc *.txt docs etc
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/gnugk.ini
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/gnugk
%attr(754,root,root) /etc/rc.d/init.d/gnugk
