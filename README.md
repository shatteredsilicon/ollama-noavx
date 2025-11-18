# ollama-noavx
Ollama Without AVX CPU Requirement

# Build without AVX

~~~~ {.bash}
$ rpmbuild -bb --without avx ollama-<version>.src.rpm
~~~~

# Install

If you see an install error like:

~~~~ {.bash}
Error: 
 Problem: conflicting requests
  - nothing provides cuda-cudart needed by ollama-0.12.10-1.el9.x86_64 from @commandline
  - nothing provides libcublas needed by ollama-0.12.10-1.el9.x86_64 from @commandline
~~~~

Build and install a small `virtual provides` shim RPM that maps these generic names to the
actual CUDA SONAMEs present on your system (`libcudart.so.12` and `libcublas.so.12`).
Then install the Ollama RPM.

**1) Build the shim RPM**

~~~~ {.bash}
$ rpmbuild -bb cuda-virtual-provides.spec
~~~~

**2) Install the shim and then Ollama**

~~~~ {.bash}
sudo dnf install -y ./cuda-virtual-provides-1-1.noarch.rpm
sudo dnf install -y ./ollama-<version>-1.el9.x86_64.rpm
~~~~

**Tip:** You should already have CUDA installed and `ldconfig` should see the libs:

~~~~ {.bash}
ldconfig -p | grep -E 'libcudart\.so\.12|libcublas\.so\.12'
~~~~
