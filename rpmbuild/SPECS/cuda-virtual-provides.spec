Name:           cuda-virtual-provides
Version:        1.0.0
Release:        1%{?dist}
Summary:        Virtual provides for CUDA libs required by Ollama
License:        MIT
BuildArch:      noarch

# Satisfy Ollama’s name-based deps:
Provides:       libcublas
Provides:       cuda-cudart

# Ensure the *actual* libraries exist (works with 12.9 or 13.0, any vendor pkg):
Requires:       libcublas.so.12()(64bit)
Requires:       libcudart.so.12()(64bit)

%description
Metapackage that maps Ollama's generic CUDA deps to the real shared objects.

%files
# no files

%changelog
* Thu Nov 13 2025 Thien Nguyen <nthien86@gmail.com> - 1.0.0-1
- Initial release
