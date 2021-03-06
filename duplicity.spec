%define		mainver 0.6
Summary:	Untrusted/encrypted backup using rsync algorithm
Summary(pl.UTF-8):	Wykonywanie szyfrowanych kopii zapasowych przy użyciu algorytmu rsync
Name:		duplicity
Version:	%{mainver}.19
Release:	1
License:	GPL v2
Group:		Applications/Archiving
Source0:	http://code.launchpad.net/duplicity/%{mainver}-series/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	c88122d0b651f84f3bfa42e55591c36b
Patch0:		%{name}-pexpect.patch
Patch1:		%{name}-backend-search.patch
URL:		http://www.nongnu.org/duplicity/
BuildRequires:	librsync-devel >= 0.9.6
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
Requires:	gnupg
Requires:	python >= 1:2.3
Requires:	python-gnupg >= 0.3.2
Requires:	python-modules
Requires:	python-pexpect >= 2.1
Suggests:	lftp
Suggests:	ncftp
Suggests:	python-boto >= 0.9d
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Duplicity incrementally backs up files and directory by encrypting
tar-format volumes with GnuPG and uploading them to a remote (or
local) file server. In theory many remote backends are possible; right
now only the local or ssh/scp backend is written. Because duplicity
uses librsync, the incremental archives are space efficient and only
record the parts of files that have changed since the last backup.
Currently duplicity supports deleted files, full Unix permissions,
directories, symbolic links, fifos, etc., but not hard links.

%description -l pl.UTF-8
Duplicity wykonuje przyrostowe kopie zapasowe plików i katalogów
poprzez szyfrowanie archiwów w formacie tar przy pomocy GnuPG i
przesyłanie ich na zdalny (lub lokalny) serwer plików. W teorii można
użyć wiele zdalnych backendów; aktualnie napisane są tylko backendy
lokalny oraz ssh/scp. Ponieważ duplicity używa librsync, przyrostowe
archiwa wydajnie wykorzystują miejsce dzięki zapisywaniu tylko tych
części plików, które zmieniły się od wykonywania poprzedniej kopii.
Aktualnie duplicity obsługuje pliki skasowane, pełny uniksowy system
uprawnień, katalogi, dowiązania symboliczne, nazwane potoki itp. - ale
nie twarde dowiązania.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

# Remove %{_datadir}/locale/io/LC_MESSAGES. It's not yet supported.
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/io

%py_postclean

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CHANGELOG README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*.1*
%dir %{py_sitedir}/duplicity
%dir %{py_sitedir}/duplicity/backends
%{py_sitedir}/duplicity/*.py[co]
%{py_sitedir}/duplicity/backends/*.py[co]
%attr(755,root,root) %{py_sitedir}/duplicity/*.so
%if "%{pld_release}" != "ac"
%{py_sitedir}/duplicity-*.egg-info
%endif
