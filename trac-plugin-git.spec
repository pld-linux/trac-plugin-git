%define		trac_ver	0.12
%define		plugin		gitplugin
Summary:	GIT version control plugin for Trac
Name:		trac-plugin-git
Version:	%{trac_ver}.0.5
Release:	2
License:	BSD
Group:		Applications/WWW
#Source0:	https://github.com/hvr/trac-git-plugin/tarball/v%{version}/%{name}-%{version}.tgz
Source0:	https://github.com/hvr/trac-git-plugin/tarball/master/%{name}-%{version}.tgz
# Source0-md5:	897291bbbbc8d9a830a2def7f63acf76
Patch0:		trac-git-plugin-python2.4.patch
URL:		http://trac-hacks.org/wiki/GitPlugin
BuildRequires:	python-devel >= 1:2.4
BuildRequires:	python-distribute
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	unzip
Requires:	git-core >= 1.5.6
Requires:	trac >= %{trac_ver}
# included in trac 0.13+ (trac 1.0)
Conflicts:	trac >= 0.13
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This Trac plugin provides support for the GIT SCM.

Features:
- Browsing source code in a Git repository via the TracBrowser
- Viewing the change history of a file or directory using
  TracRevisionLog
- Performing diffs between any two files or two directories
- Displaying submitted changes in the TracTimeline
- (Optionally) caching TracChangeset information in Trac's database
- Caching Git commit relation graph in memory
- Using the TracSearch page to search change descriptions
- Annotation support, also known as "blame" operation
- Interpretation of 40-character wide hex-strings as sha1 commit
  checksums

%prep
%setup -qc
mv *-trac-git-plugin-*/* .
%if "%{py_ver}" < "2.5"
%patch0 -p1
%endif

%build
%{__python} setup.py build
%{__python} setup.py egg_info
%py_lint tracext

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	%banner -e %{name} <<-'EOF'
	To enable the %{plugin} plugin, add to conf/trac.ini:

	[components]
	tracext.git.* = enabled
EOF
fi

%files
%defattr(644,root,root,755)
%doc README
%dir %{py_sitescriptdir}/tracext
%{py_sitescriptdir}/tracext/git
%{py_sitescriptdir}/TracGit-*.egg-info
%{py_sitescriptdir}/TracGit-*-nspkg.pth
