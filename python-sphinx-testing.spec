%if 0%{?fedora} || 0%{?rhel} >= 8
%global with_python3 1
%endif

%global srcname sphinx-testing

Name:           python-%{srcname}
Version:        0.7.2
Release:        1%{?dist}
Summary:        Testing utility classes and functions for Sphinx extensions

License:        BSD
URL:            https://github.com/sphinx-doc/sphinx-testing
Source0:        https://files.pythonhosted.org/packages/source/s/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-mock
BuildRequires:  python2-nose
BuildRequires:  python2-nose-cov
BuildRequires:  python2-setuptools
BuildRequires:  python2-six
BuildRequires:  python-sphinx

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-nose
BuildRequires:  python3-nose-cov
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-sphinx
%endif

%global common_desc \
This package provides a few utility classes and functions to help\
authors of Sphinx extensions write tests for those extensions.

%description
%common_desc

%package -n python2-%{srcname}
Summary:        Testing utility classes and functions for Sphinx extensions
Requires:       python2-six
Requires:       python2-sphinx
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%common_desc

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Testing utility classes and functions for Sphinx extensions
Requires:       python3-six
Requires:       python3-sphinx
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%common_desc
%endif

%prep
%setup -q -c

# Remove useless shebang
pushd %{srcname}-%{version}/src/sphinx_testing/
sed -i '\@/usr/bin/env python@d' path.py
popd

# Prepare for python3 build
cp -a %{srcname}-%{version} python3-%{srcname}-%{version}

%build
# Python 2 build
pushd %{srcname}-%{version}
%py2_build
python2 %{_bindir}/rst2html --no-datestamp CHANGES.rst changes.html
python2 %{_bindir}/rst2html --no-datestamp README.rst readme.html
popd

%if 0%{?with_python3}
# Python 3 build
pushd python3-%{srcname}-%{version}
%py3_build
python3 %{_bindir}/rst2html --no-datestamp CHANGES.rst changes.html
python3 %{_bindir}/rst2html --no-datestamp README.rst readme.html
popd
%endif

%install
# Python 2 install
pushd %{srcname}-%{version}
%py2_install
popd

%if 0%{?with_python3}
# Python 3 install
pushd python3-%{srcname}-%{version}
%py3_install
popd
%endif

%check
# Test the python 2 build
pushd %{srcname}-%{version}
PYTHONPATH=$PWD nosetests-%{python2_version} -v
popd

%if 0%{?with_python3}
# Python 3 install
pushd python3-%{srcname}-%{version}
PYTHONPATH=$PWD nosetests-%{python3_version} -v
popd
%endif

%files -n python2-%{srcname}
%doc %{srcname}-%{version}/{AUTHORS,Sphinx-AUTHORS,*.html}
%license %{srcname}-%{version}/LICENSE
%{python2_sitelib}/sphinx_testing*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc python3-%{srcname}-%{version}/{AUTHORS,Sphinx-AUTHORS,*.html}
%license python3-%{srcname}-%{version}/LICENSE
%{python3_sitelib}/sphinx_testing*
%endif

%changelog
* Thu May  4 2017 Jerry James <loganjerry@gmail.com> - 0.7.2-1
- New upstream version (bz 1447818)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-3
- Rebuild for Python 3.6

* Tue Mar  1 2016 Jerry James <loganjerry@gmail.com> - 0.7.1-2
- Clarify the description
- Fix nosetests invocation
- Don't preserve timestamp of altered file

* Thu Feb 25 2016 Jerry James <loganjerry@gmail.com> - 0.7.1-1
- Initial RPM
