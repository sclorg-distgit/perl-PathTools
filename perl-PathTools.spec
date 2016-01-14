%{?scl:%scl_package perl-PathTools}
%{!?scl:%global pkg_name %{name}}

%global cpan_version 3.40
Name:           %{?scl_prefix}perl-PathTools
Version:        %(echo '%{cpan_version}' | tr _ .)
Release:        3.sc1%{?dist}
Summary:        PathTools Perl module (Cwd, File::Spec)
License:        (GPL+ or Artistic) and BSD
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/PathTools/
Source0:        http://www.cpan.org/authors/id/S/SM/SMUELLER/PathTools-%{cpan_version}.tar.gz
# Disable VMS test (bug #973713)
Patch0:         PathTools-3.40-Disable-VMS-tests.patch
BuildRequires:  %{?scl_prefix}perl
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  %{?scl_prefix}perl(Carp)
BuildRequires:  %{?scl_prefix}perl(Exporter)
# File::Basename not needed because of removed File::Spec::VMS
BuildRequires:  %{?scl_prefix}perl(Scalar::Util)
BuildRequires:  %{?scl_prefix}perl(strict)
BuildRequires:  %{?scl_prefix}perl(vars)
# Tests:
BuildRequires:  %{?scl_prefix}perl(Carp::Heavy)
BuildRequires:  %{?scl_prefix}perl(Config)
BuildRequires:  %{?scl_prefix}perl(File::Path)
BuildRequires:  %{?scl_prefix}perl(lib)
BuildRequires:  %{?scl_prefix}perl(Test::More)
%{?scl:%global perl_version %(scl enable %{scl} 'eval "`perl -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`perl -V:version`"; echo $version)}
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})
Requires:       %{?scl_prefix}perl(Carp)
Requires:       %{?scl_prefix}perl(Scalar::Util)

%{?perl_default_filter}

%description
This is the combined distribution for the File::Spec and Cwd modules.

%prep
%setup -q -n PathTools-%{cpan_version}
%patch0 -p1
# Remove bundled modules
rm -r t/lib
sed -i -e '/^t\/lib\//d' MANIFEST
# Do not distribute File::Spec::VMS as it works on VMS only (bug #973713)
rm lib/File/Spec/VMS.pm
sed -i -e '/^lib\/File\/Spec\/VMS.pm/d' MANIFEST

%build
%{?scl:scl enable %{scl} '}
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
%{?scl:'}
%{?scl:scl enable %{scl} "}
make %{?_smp_mflags}
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
make pure_install DESTDIR=$RPM_BUILD_ROOT
%{?scl:"}
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%{?scl:scl enable %{scl} "}
make test
%{?scl:"}

%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Cwd.pm
%{perl_vendorarch}/File/
%{_mandir}/man3/*

%changelog
* Thu Feb 13 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.40-3
- Removed useless filter of dependencies
- Resolves: rhbz#1064855

* Wed Nov 13 2013 Jitka Plesnikova <jplesnik@redhat.com> - 3.40-2
- Disable VMS test (bug #973713)

* Mon Feb 18 2013 Jitka Plesnikova <jplesnik@redhat.com> - 3.40-1
- SCL package - initial import
