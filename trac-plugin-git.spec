%define		trac_ver	0.11
%define		plugin		gitplugin
Summary:	GIT version control plugin for Trac %{trac_ver}
Name:		trac-plugin-git
Version:	%{trac_ver}.0.2
Release:	0.3
License:	GPL v2
Group:		Applications/WWW
# Source0Download:	http://trac-hacks.org/changeset/latest/gitplugin?old_path=/&filename=gitplugin&format=zip
Source0:	%{plugin}.zip
# Source0-md5:	b4d3ae110223606a46a1c7a413e8994d
Patch0:		http://trac-hacks.org/attachment/ticket/6402/trac-git-plugin-python2.4.patch?format=raw
URL:		http://trac-hacks.org/wiki/GitPlugin
BuildRequires:	python-devel >= 1:2.4
Requires:	trac >= %{trac_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%prep
%setup -q -n %{plugin}
%patch0 -p1

%build
cd %{trac_ver}
%{__python} setup.py build
%{__python} setup.py egg_info

%install
rm -rf $RPM_BUILD_ROOT
cd %{trac_ver}
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

# warning: install_data: setup script did not provide a directory for 'COPYING'
# warning: install_data: setup script did not provide a directory for 'README'
rm $RPM_BUILD_ROOT%{_prefix}/{COPYING,README}

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
%doc %{trac_ver}/README
%dir %{py_sitescriptdir}/tracext
%{py_sitescriptdir}/tracext/git
%{py_sitescriptdir}/TracGit-*.egg-info
%{py_sitescriptdir}/TracGit-*-nspkg.pth
