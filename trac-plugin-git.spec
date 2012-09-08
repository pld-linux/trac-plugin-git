%define		trac_ver	0.12
%define		plugin		gitplugin
Summary:	GIT version control plugin for Trac
Name:		trac-plugin-git
Version:	%{trac_ver}.0.5
Release:	1
License:	GPL v2
Group:		Applications/WWW
#Source0:	http://trac-hacks.org/changeset/latest/gitplugin?old_path=/&format=zip#/%{plugin}-%{version}.zip
# TH site is down at this moment, so use fedora mirror
Source0:	http://pkgs.fedoraproject.org/repo/pkgs/trac-git-plugin/TracGit-%{version}dev.tar.gz/b5e624f7c0f3a85240e0f1484492dc15/TracGit-%{version}dev.tar.gz
# Source0-md5:	b5e624f7c0f3a85240e0f1484492dc15
Patch0:		trac-git-plugin-python2.4.patch
URL:		http://trac-hacks.org/wiki/GitPlugin
BuildRequires:	python-devel >= 1:2.4
BuildRequires:	python-distribute
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	unzip
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
%setup -qn TracGit-%{version}dev
%if "%{py_ver}" < "2.5"
%patch0 -p1
%endif

%build
%{__python} setup.py build
%{__python} setup.py egg_info

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
