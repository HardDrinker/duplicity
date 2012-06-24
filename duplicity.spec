
%include        /usr/lib/rpm/macros.python

Summary:	Untrusted/encrypted backup using rsync algorithm
Name:		duplicity
Version:	0.4.0
Release:	1
License:	GPL
Group:		Applications/Archiving
Source0:	http://savannah.nongnu.org/download/duplicity/%{name}-%{version}.tar.gz
URL:		http://www.nongnu.org/duplicity/
BuildRequires:	librsync-devel
BuildRequires:	python-devel >= 2.2.1
BuildRequires:	rpm-pythonprov
Requires:	gnupg
Requires:	python >= 2.2
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Duplicity incrementally backs up files and directory by encrypting
tar-format volumes with GnuPG and uploading them to a remote (or
local) file server. In theory many remote backends are possible; right
now only the local or ssh/scp backend is written. Because duplicity
uses librsync, the incremental archives are space efficient and only
record the parts of files that have changed since the last backup.
Currently duplicity supports deleted files, full unix permissions,
directories, symbolic links, fifos, etc., but not hard links.

%prep
%setup -q

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --optimize=2 --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*.1*
%dir %{py_sitedir}/duplicity
%{py_sitedir}/duplicity/*.py[co]
%{py_sitedir}/duplicity/*.so
