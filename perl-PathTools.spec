%{?scl:%scl_package perl-PathTools}

%global base_version 3.62
Name:           %{?scl_prefix}perl-PathTools
Version:        3.63
Release:        367%{?dist}
Summary:        PathTools Perl module (Cwd, File::Spec)
License:        (GPL+ or Artistic) and BSD
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/PathTools/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/PathTools-%{base_version}.tar.gz
# Disable VMS test (bug #973713)
Patch0:         PathTools-3.47-Disable-VMS-tests.patch
# Unbundled from perl 5.24.0
Patch1:         PathTools-3.62-Upgrade-to-3.63.patch
# Avoid loading optional modules from default . (CVE-2016-1238)
Patch2:         PathTools-3.63-CVE-2016-1238-avoid-loading-optional-modules-from.patch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  %{?scl_prefix}perl
BuildRequires:  %{?scl_prefix}perl-devel
BuildRequires:  %{?scl_prefix}perl-generators
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker)
BuildRequires:  sed
# Run-time:
BuildRequires:  %{?scl_prefix}perl(Carp)
BuildRequires:  %{?scl_prefix}perl(constant)
BuildRequires:  %{?scl_prefix}perl(Exporter)
# File::Basename not needed because of removed File::Spec::VMS
BuildRequires:  %{?scl_prefix}perl(Scalar::Util)
BuildRequires:  %{?scl_prefix}perl(strict)
BuildRequires:  %{?scl_prefix}perl(vars)
# Tests:
BuildRequires:  %{?scl_prefix}perl(Carp::Heavy)
BuildRequires:  %{?scl_prefix}perl(Config)
BuildRequires:  %{?scl_prefix}perl(File::Path)
BuildRequires:  %{?scl_prefix}perl(File::Temp)
BuildRequires:  %{?scl_prefix}perl(lib)
BuildRequires:  %{?scl_prefix}perl(Test::More) >= 0.88
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))
Requires:       %{?scl_prefix}perl(Carp)
Requires:       %{?scl_prefix}perl(Scalar::Util)

%{?perl_default_filter}

%description
This is the combined distribution for the File::Spec and Cwd modules.

%prep
%setup -q -n PathTools-%{base_version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# Do not distribute File::Spec::VMS as it works on VMS only (bug #973713)
rm lib/File/Spec/VMS.pm
sed -i -e '/^lib\/File\/Spec\/VMS.pm/d' MANIFEST

# Remove bundled modules
rm -rf t/lib
sed -i -e '/t\/lib\//d' MANIFEST

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" && make %{?_smp_mflags}%{?scl:'}

%install
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=$RPM_BUILD_ROOT%{?scl:'}
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}

%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Cwd.pm
%{perl_vendorarch}/File/
%{_mandir}/man3/*

%changelog
* Wed Aug 03 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.63-367
- Avoid loading optional modules from default . (CVE-2016-1238)

* Mon Jul 11 2016 Petr Pisar <ppisar@redhat.com> - 3.63-366
- SCL

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.63-365
- Increase release to favour standalone package

* Wed May 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.63-1
- 3.63 bump in order to dual-live with perl 5.24

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Petr Pisar <ppisar@redhat.com> - 3.62-1
- 3.62 bump

* Mon Jan 11 2016 Petr Pisar <ppisar@redhat.com> - 3.60-2
- Fix CVE-2015-8607 (File::Spec::canonpath() loses tain) (bug #1297455)

* Thu Nov 19 2015 Petr Pisar <ppisar@redhat.com> - 3.60-1
- 3.60 bump

* Mon Nov 16 2015 Petr Pisar <ppisar@redhat.com> - 3.59-1
- 3.59 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.56-346
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.56-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.56-2
- Perl 5.22 rebuild

* Mon Apr 27 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.56-1
- 3.56 bump in order to dual-live with Perl 5.22

* Tue Jan 13 2015 Petr Pisar <ppisar@redhat.com> - 3.47-311
- Require constant module

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.47-310
- Increase release to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.47-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.47-1
- 3.47 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.40-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 3.40-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 3.40-4
- Link minimal build-root packages against libperl.so explicitly

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 3.40-3
- Disable VMS test (bug #973713)

* Fri Jun 14 2013 Petr Pisar <ppisar@redhat.com> - 3.40-2
- Do not distribute File::Spec::VMS (bug #973713)

* Mon Feb 04 2013 Petr Pisar <ppisar@redhat.com> - 3.40-1
- 3.40 bump

* Tue Sep 18 2012 Petr Pisar <ppisar@redhat.com> - 3.39.01-1
- 3.39_01 bump

* Wed Aug 15 2012 Petr Pisar <ppisar@redhat.com> - 3.33-8
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.33-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 3.33-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Petr Pisar <ppisar@redhat.com> - 3.33-4
- RPM 4.9 dependency filtering added

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.33-3
- Perl mass rebuild

* Sun May 29 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.33-2
- Own the %%{perl_vendorarch}/File dir.

* Mon Feb 28 2011 Marcela Mašláňová <mmaslano@redhat.com> 3.33-1
- Specfile autogenerated by cpanspec 1.79.
