Name:		gnumed-server
Version:	16.14
Release:	1
Summary:	The GNUmed back end server
Group:		System/Servers
License:	GPLv2+ or GPLv1
URL:		http://wiki.gnumed.de/
Source0:	http://www.gnumed.de/downloads/server/v16/%{name}.%{version}.tgz
Source1:	http://www.gnu.org/licenses/gpl-1.0.txt	
Patch0:		gnumed-server-correct-dir.patch
Patch1:		upgrade-path.diff

BuildArch:	noarch

Requires:	python
Requires:	python-psycopg2
Requires:	mailx
Requires:	bzip2
Requires:	openssl
Requires:	postgresql
Requires:	rsync
Requires:	postgresql-plpgsql 


%description
The GNUmed project builds an open source Electronic Medical Record. 
It is developed by a handful of medical doctors and programmers from 
all over the world. It can be useful to anyone documenting the health 
of patients, including but not limited to doctors, physical therapists, 
occupational therapists.

%prep
%setup -q -n gnumed-server.%{version}

#Patch GM_SERVER_DIR path
#-GM_SERVER_DIR="/var/lib/gnumed/server/bootstrap"
#+GM_SERVER_DIR="/usr/share/gnumed-server/bootstrap"
%patch0 -p1
%patch1 -p1

%build

%install
pushd server

#Copy to /usr/share/gnumed-server/
%__install -d %{buildroot}%{_datadir}/gnumed/server
cp -p -r bootstrap %{buildroot}%{_datadir}/gnumed/server
cp -p -r pycommon %{buildroot}%{_datadir}/gnumed/server
cp -p -r sql %{buildroot}%{_datadir}/gnumed/server
%__install -m 644 __init__.py %{buildroot}%{_datadir}/gnumed/server
echo "%{version}" > %{buildroot}%{_datadir}/gnumed/server/version.txt

# silcence bootstrap process by setting interactive to 'no' and set 'gm-dbo' as default password
for conffile in `find %{buildroot}/%{_datadir}/gnumed/server/bootstrap -maxdepth 1 -type f -name \*.conf` ; do \
   sed -i 's/^\(interactive[[:space:]]*=[[:space:]]*\)yes/\1no/' "$conffile" ; \
   sed -i 's/^\(password[[:space:]]*=[[:space:]]*\)/\1 gm-dbo/' "$conffile" ; \
done


#copy config files to /etc
%__install -d %{buildroot}%{_sysconfdir}/%{name}
rename .conf.example .conf etc/gnumed/*.conf.example
#for conf in etc/gnumed/*.conf.example 
#    do mv $conf `echo $conf|sed 's/.example$//'`
#done
%__install -m 644 etc/gnumed/*.conf %{buildroot}%{_sysconfdir}/%{name}

#create .xz files and copy them to mandir
%__install -d %{buildroot}%{_mandir}/man8/
%__install -d %{buildroot}%{_mandir}/man1/

for man in `ls doc/*.*`; \
    do xz $man; \
done
%__install -m 644 doc/*.8.xz %{buildroot}%{_mandir}/man8
%__install -m 644 doc/*.1.xz %{buildroot}%{_mandir}/man1


#remove .sh extensions
#copy all scripts to bin dir
%__install -d -m 755 %{buildroot}%{_bindir}
rename ".sh" "" gm-*.sh
rename ".py" "" gm-*.py
%__install -m 755 gm-* %{buildroot}%{_bindir}

popd  


%files
%doc server/doc/README server/doc/schema/* server/GnuPublicLicense.txt
%{_datadir}/gnumed/server/
%{_bindir}/gm-*
%{_mandir}/man?/gm-*
%config(noreplace) %{_sysconfdir}/%{name}/
