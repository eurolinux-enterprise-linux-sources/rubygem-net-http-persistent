%if 0%{?fedora} < 17 && 0%{?rhel} < 7
%global	rubyabi		1.8
%else
%if 0%{?fedora} < 19
%global	rubyabi		1.9.1
%endif
%endif

%global	gem_name	net-http-persistent

Summary:	Persistent connections using Net::HTTP plus a speed fix
Name:		rubygem-%{gem_name}
Version:	2.8
Release:	4%{?dist}
Group:		Development/Languages
License:	MIT

URL:		http://seattlerb.rubyforge.org/net-http-persistent
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0:		rubygem-net-http-persistent-2.1-no-net-test.patch

%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
Requires:	ruby(release)
BuildRequires:	ruby(release)
%else
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby
BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby
%endif

BuildRequires:	rubygems-devel
BuildRequires:	rubygem(minitest)

Requires:	rubygems
BuildArch:	noarch

Provides:	rubygem(%{gem_name}) = %{version}

%description
Persistent connections using Net::HTTP plus a speed fix for 1.8.  It's
thread-safe too.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description    doc
This package contains documentation for %{name}.


%prep
%setup -q -c -T

TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

%patch0 -p1

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
%gem_install

#chmod 0644 ./%{gem_dir}/cache/%{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}/%{gem_dir}/
rm -f %{buildroot}%{gem_instdir}/{.autotest,.gemtest}

%check
pushd .%{gem_instdir}
testrb -Ilib test
popd

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Rakefile
%{gem_instdir}/lib/
%exclude	%{gem_cache}
%{gem_spec}

%files	doc
%exclude	%{gem_instdir}/Rakefile
%exclude	%{gem_instdir}/test/
%{gem_docdir}/

%changelog
* Thu Mar 21 2013 Vít Ondruch <vondruch@redhat.com> - 2.8-4
- Fix EL compatibility.
- Test are passing now.
- Cleanup.

* Thu Feb 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.8-3
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.8-1
- Update to 2.8

* Mon Nov 26 2012 Vít Ondruch <vondruch@redhat.com> - 2.1-6
- Add EL compatibility macros.
- Drop rubygem({hoe,rake}) build dependencies.

* Thu Aug  2 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.1-5
- Rescue test failure for now

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.1-3
- F-17: rebuild against ruby19

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct  9 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.1-1
- 2.1

* Sun Aug 28 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.0-1
- 2.0

* Sun Aug 14 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.8.1-1
- 1.8.1

* Mon Jul  4 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.8-1
- 1.8

* Sun Apr 24 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.7-1
- 1.7

* Thu Mar 10 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.6.1-1
- 1.6.1

* Thu Mar  3 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.6-1
- 1.6

* Sat Feb 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.2-1
- 1.5.2
- Patch0 merged

* Sat Feb 12 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.1-1
- 1.5.1

* Thu Feb 10 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5-3
- Rescue the case where socket is Nil, for mechanize testsuite

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5-1
- 1.5

* Sun Jan 16 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.1-1
- Initial package
