%define debug_package %{nil}

Name:           ollama
Version:        0.5.11
Release:        1%{?dist}
Summary:        Tool for running AI models on-premise
License:        MIT
URL:            https://ollama.com
Source:         %{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.gz
Source2:        %{name}.service
Source3:        %{name}-user.conf
Patch0:         ollama-disable-avx.patch
Patch1:         remove-redundant-backends.patch
Patch2:         fix-linking-stdcppfs.patch
Patch3:         optimize-gpu-compiler.patch
Patch4:         ollama-0.5.11-sm35.patch
Patch5:         enable-lto.patch
Patch6:         golang-version.patch
BuildRequires:  cmake >= 3.24
BuildRequires:  zstd
BuildRequires:  golang >= 1.23.1
BuildRequires:  gcc-c++
BuildRequires:  libstdc++
BuildRequires:  systemd-rpm-macros
BuildRequires:  cuda-toolkit-11-8
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

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
export CFLAGS='-ffunction-sections -fdata-sections -flto -Wl,--gc-sections -Wl,--strip-all'
export CXXFLAGS=$CFLAGS
export LDFLAGS='-flto -Wl,--gc-sections -Wl,--strip-all -lstdc++fs'
export PATH=/usr/local/cuda-11/bin:$PATH
export GIN_MODE=release
export GOFLAGS="-mod=vendor -ldflags=-s -ldflags=-w -buildvcs=false"
export GOAMD64=v2
export CGO_ENABLED=1

cmake --preset="CUDA 11"
cmake --build build --config Release
go build -v .

%install
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/%{name}.conf
install -D -m 0755 %{name} %{buildroot}/%{_bindir}/%{name}
install -d %{buildroot}%{_localstatedir}/lib/%{name}

install -d %{buildroot}/usr/lib/systemd/system
install -p -m 0644 %{SOURCE2} %{buildroot}/usr/lib/systemd/system/%{name}.service

install -d %{buildroot}%{_prefix}/lib/ollama
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
* Wed Feb 19 2025 <nthien86@gmail.com> - 0.5.11-1
- Initial release with 0.5.11 patched to disable AVX requirements

