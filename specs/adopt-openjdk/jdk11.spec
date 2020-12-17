################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%define __jar_repack %{nil}

################################################################################

%define jdk_major   11.0.9.1
%define jdk_minor   1

%define install_dir %{_prefix}/java/%{name}-%{version}
%define jdk_bin_dir %{install_dir}/bin
%define jdk_man_dir %{install_dir}/man/man1

%define alt_priority 1156

################################################################################

Summary:            OpenJDK Runtime Environment (JDK 11)
Name:               jdk11
Epoch:              1
Version:            %{jdk_major}
Release:            %{jdk_minor}%{?dist}
Group:              Development/Languages
License:            ASL 1.1 and ASL 2.0 and BSD and BSD with advertising and GPL+ and GPLv2 and GPLv2 with exceptions and IJG and LGPLv2+ and MIT and MPLv2.0 and Public Domain and W3C and zlib
URL:                https://adoptopenjdk.net

Source0:            https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-%{jdk_major}+%{jdk_minor}/OpenJDK11U-jdk_x64_linux_hotspot_%{jdk_major}_%{jdk_minor}.tar.gz
Source1:            java.sh

Source100:          checksum.sha512

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Conflicts:          java-1.6.0-openjdk-headless
Conflicts:          java-1.7.0-openjdk-headless
Conflicts:          java-1.8.0-openjdk-headless
Conflicts:          java-11-openjdk-headless

AutoProv:           no
AutoReqProv:        no

Provides:           jdk = 1:11
Provides:           jdk-lts = 1:11
Provides:           java = 1:11
Provides:           jdk-%{jdk_major} = 1:%{version}-%{release}
Provides:           jdk-lts-%{jdk_major} = 1:%{version}-%{release}
Provides:           java-%{jdk_major} = 1:%{version}-%{release}

Provides:           %{name} = %{version}-%{release}

################################################################################

%description
Java™ is the world's leading programming language and platform. AdoptOpenJDK
uses infrastructure, build and test scripts to produce prebuilt binaries from
OpenJDK™ class libraries and a choice of either the OpenJDK HotSpot or Eclipse
OpenJ9 VM.

All AdoptOpenJDK binaries and scripts are open source licensed and available
for free.

################################################################################

%prep
%{crc_check}

%setup -qn jdk-%{jdk_major}+%{jdk_minor}

%build

%install
rm -rf %{buildroot}

rm -rf demo release

mkdir -p %{buildroot}%{install_dir}
cp -a * %{buildroot}%{install_dir}/

install -pm 644 %{SOURCE1} %{buildroot}%{install_dir}/

%clean
rm -rf %{buildroot}

%post
deps="%{_bindir}/java java %{jdk_bin_dir}/java %{alt_priority}"

for bin in $(ls -1 %{jdk_bin_dir}) ; do
  deps="$deps --slave %{_bindir}/$bin $bin %{jdk_bin_dir}/$bin"
done

for doc in $(ls -1 %{jdk_man_dir}) ; do
  deps="$deps --slave %{_mandir}/man1/$doc $doc %{jdk_man_dir}/$doc"
done

deps="$deps --slave %{_sysconfdir}/profile.d/java.sh java-profile %{install_dir}/java.sh"

%{_sbindir}/update-alternatives --install $deps

%preun
%{_sbindir}/update-alternatives --remove java %{jdk_bin_dir}/java

################################################################################

%files
%defattr(-, root, root, -)
%{install_dir}

################################################################################

%changelog
* Sat Dec 12 2020 Anton Novojilov <andy@essentialkaos.com> - 11.0.9.1-1
- Updated to the latest version

* Tue Nov 10 2020 Anton Novojilov <andy@essentialkaos.com> - 11.0.9-11
- Updated to the latest version

* Mon Aug 10 2020 Anton Novojilov <andy@essentialkaos.com> - 11.0.8.10-0
- Updated to the latest version

* Sun May 24 2020 Anton Novojilov <andy@essentialkaos.com> - 11.0.7.10-0
- Updated to the latest version

* Sat Feb 22 2020 Anton Novojilov <andy@essentialkaos.com> - 11.0.6.10-1
- Fixed bug with removing previous version from alternatives

* Fri Jan 17 2020 Anton Novojilov <andy@essentialkaos.com> - 11.0.6.10-0
- Updated to the latest version

* Sat Dec 14 2019 Anton Novojilov <andy@essentialkaos.com> - 11.0.5.10-0
- Updated to the latest version

* Thu Aug 08 2019 Anton Novojilov <andy@essentialkaos.com> - 11.0.4.11-0
- Updated to the latest version

* Sun Jul 14 2019 Anton Novojilov <andy@essentialkaos.com> - 11.0.3.7-0
- Initial build for kaos repository
