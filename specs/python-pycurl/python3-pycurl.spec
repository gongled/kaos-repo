################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%if 0%{?rhel} >= 7
%global python_base python36
%global __python3   %{_bindir}/python3.6
%else
%global python_base python34
%global __python3   %{_bindir}/python3.4
%endif

%global pythonver %(%{__python3} -c "import sys; print sys.version[:3]" 2>/dev/null || echo 0.0)
%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" 2>/dev/null)}

################################################################################

%define package_name  pycurl

%define pypi_path     0f/52/2c6951c4cd8a4e9288f2561eb9da1dc15b5d0f4e610a7e2acf39bc703281

# Used cURL version fo build
# DO NOT FORGOT TO UPDATE IF NEWER VERSION IS USED!
%define curl_version  7.68.0

################################################################################

Summary:        A Python 3 interface to libcurl
Name:           %{python_base}-%{package_name}
Version:        7.43.0.4
Release:        0%{?dist}
License:        BSD
Group:          Development/Libraries
URL:            http://pycurl.io

Source0:        https://files.pythonhosted.org/packages/%{pypi_path}/%{package_name}-%{version}.tar.gz

Source100:      checksum.sha512

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires:  %{python_base}-devel %{python_base}-setuptools
BuildRequires:  %{python_base}-bottle %{python_base}-nose
BuildRequires:  gcc openssl-devel curl-devel >= %{curl_version}

Requires:       %{python_base} %{python_base}-libs libcurl >= %{curl_version}

Provides:       %{name} = %{verion}-%{release}

################################################################################

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

################################################################################

%prep
%{crc_check}

%setup -qn %{package_name}-%{version}

%build
%{__python3} setup.py build -- --with-nss

%install
rm -rf %{buildroot}

%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

rm -rf %{buildroot}%{_datadir}/doc/pycurl

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING-LGPL COPYING-MIT ChangeLog README.rst doc
%{python3_sitearch}/curl/
%{python3_sitearch}/%{package_name}.*.so
%{python3_sitearch}/%{package_name}-%{version}-*.egg-info

################################################################################

%changelog
* Wed Jan 22 2020 Anton Novojilov <andy@essentialkaos.com> - 7.43.0.4-0
- Updated to the latest version

* Sat Dec 14 2019 Anton Novojilov <andy@essentialkaos.com> - 7.43.0.3-0
- Updated to the latest version

* Sat Aug 17 2019 Anton Novojilov <andy@essentialkaos.com> - 7.43.0-1
- Rebuilt with the latest version of curl
- Added CRC check for all sources

* Fri Jul 12 2019 Anton Novojilov <andy@essentialkaos.com> - 7.43.0.-1
- Hardcoded minimal required libcurl version

* Thu Apr 11 2019 Anton Novojilov <andy@essentialkaos.com> - 7.43.0-0
- Initital build for kaos repository
