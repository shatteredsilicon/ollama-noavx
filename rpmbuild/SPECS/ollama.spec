%define debug_package %{nil}

%bcond_without avx

Name:           ollama
Version:        0.12.10
Release:        1%{?dist}
Summary:        Tool for running AI models on-premise
License:        MIT
URL:            https://ollama.com
Source:         %{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.gz
Source2:        %{name}.service
Source3:        %{name}-user.conf
Patch0:         ollama-disable-avx512.patch
Patch1:         remove-redundant-backends.patch
Patch2:         fix-linking-stdcppfs.patch
Patch3:         optimize-gpu-compiler.patch
Patch4:         support-all-compute-models-for-cuda12.patch
Patch5:         enable-lto.patch
Patch6:         ollama-disable-avx.patch
BuildRequires:  cmake >= 3.24
BuildRequires:  zstd
BuildRequires:  golang >= 1.24.1
BuildRequires:  gcc-c++
BuildRequires:  libstdc++
BuildRequires:  systemd-rpm-macros
BuildRequires:  cuda-toolkit-12-9
%{?sysusers_requires_compat}

Requires: nvidia-driver-cuda-libs libcublas cuda-cudart

%description
Ollama is a tool for running AI models on one's own hardware.
It offers a command-line interface and a RESTful API.
New models can be created or existing ones modified in the
Ollama library using the Modelfile syntax.
Source model weights found on Hugging Face and similar sites
can be imported.

%prep
%setup
%setup -D -a 1

%patch1 -p1

%if %{with avx}
# default: AVX/AVX2 allowed -> only disable AVX512
%patch0 -p1
%else
# --without avx: no AVX at all
%patch6 -p1
%endif

%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
export CFLAGS='-ffunction-sections -fdata-sections -flto -Wl,--gc-sections -Wl,--strip-all'
export CXXFLAGS=$CFLAGS
export LDFLAGS='-flto -Wl,--gc-sections -Wl,--strip-all -lstdc++fs'
export PATH=/usr/local/cuda-12/bin:$PATH
export GIN_MODE=release
export GOFLAGS="-mod=vendor -ldflags=-s -ldflags=-w -buildvcs=false"
export CGO_ENABLED=1

%if !%{with avx}
export GOAMD64=v2
%endif

cmake --preset="CUDA 12"
cmake --build build --config Release %{?_smp_mflags}
go build -v .
strip %{name}

%install
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/%{name}.conf
%{__install} -D -m 0755 %{name} %{buildroot}/%{_bindir}/%{name}
%{__install} -d %{buildroot}%{_localstatedir}/lib/%{name}

%{__install} -d %{buildroot}/usr/lib/systemd/system
%{__install} -p -m 0644 %{SOURCE2} %{buildroot}/usr/lib/systemd/system/%{name}.service

%{__install} -d %{buildroot}%{_prefix}/lib/ollama
cp -r build/lib/ollama/* %{buildroot}%{_prefix}/lib/ollama

mkdir -p "%{buildroot}/%{_docdir}/%{name}"
cp -Ra docs/* "%{buildroot}/%{_docdir}/%{name}"

%pre
%sysusers_create_compat %{SOURCE3}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%doc README.md
%license LICENSE
%{_docdir}/%{name}
%{_bindir}/%{name}
%{_prefix}/lib/ollama
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.conf
%attr(-, ollama, ollama) %{_localstatedir}/lib/%{name}

%changelog
* Tue Nov 11 2025 Thien Nguyen <nthien86@gmail.com> - 0.12.10-1
- Update to version 0.12.10
- Add support for building with or without AVX

* Fri Sep 26 2025 <gordan@shatteredsilicon.net> - 0.12.2-1
- Update to 0.12.2

* Thu Sep 11 2025 <gordan@shatteredsilicon.net> - 0.11.10-1
- Update to 0.11.10

* Tue Aug 26 2025 <gordan@shatteredsilicon.net> - 0.11.7-1
- Update to 0.11.7

* Fri Aug 22 2025 <gordan@shatteredsilicon.net> - 0.11.6-1
- Update to 0.11.6

* Wed Aug 20 2025 <gordan@shatteredsilicon.net> - 0.11.5-1
- Update to 0.11.5

* Sun Aug 10 2025 <gordan@shatteredsilicon.net> - 0.11.4-1
- Update to 0.11.4

* Wed Aug 06 2025 <gordan@shatteredsilicon.net> - 0.11.3-1
- Update to 0.11.3

* Tue Aug 05 2025 <gordan@shatteredsilicon.net> - 0.11.0-1
- Update to 0.11.0

* Thu Jul 31 2025 <gordan@shatteredsilicon.net> - 0.10.1-1
- Update to 0.10.1

* Wed Jul 09 2025 <gordan@shatteredsilicon.net> - 0.9.6-1
- Update to 0.9.6

* Sun Jul 06 2025 <gordan@shatteredsilicon.net> - 0.9.5-1
- Update to 0.9.5

* Fri Jun 20 2025 <gordan@shatteredsilicon.net> - 0.9.2-1
- Update to 0.9.2

* Wed Jun 18 2025 <gordan@shatteredsilicon.net> - 0.9.1-1
- Update to 0.9.1

* Sat May 10 2025 <gordan@shatteredsilicon.net> - 0.6.8-1
- Update to 0.6.8

* Sun Apr 27 2025 <gordan@shatteredsilicon.net> - 0.6.6-1
- Update to 0.6.6

* Sat Apr 12 2025 <nthien86@gmail.com> - 0.6.5-1
- 0.6.5 patched to disable AVX requirements

* Thu Apr 03 2025 <nthien86@gmail.com> - 0.6.2-1
- 0.6.2 patched to disable AVX requirements

* Mon Mar 17 2025 <nthien86@gmail.com> - 0.6.1-1
- 0.6.1 patched to disable AVX requirements

* Sun Mar 16 2025 <nthien86@gmail.com> - 0.6.0-1
- 0.6.0 patched to disable AVX requirements

* Wed Feb 19 2025 <nthien86@gmail.com> - 0.5.11-1
- Initial release with 0.5.11 patched to disable AVX requirements
- CUDA 11 only, compute model 3.5 - 9.0

