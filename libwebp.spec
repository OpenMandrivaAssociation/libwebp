# libgphoto uses libwebp, wine uses libgphoto
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 8
%define libname %mklibname webp %{major}
%define devname %mklibname -d webp
%define lib32name %mklib32name webp %{major}
%define dev32name %mklib32name -d webp
%define _disable_lto %nil

Summary:	Library and tools for the WebP graphics format
Name:		libwebp
Version:	1.1.0
Release:	5
Group:		Development/C
# Additional IPR is licensed as well. See PATENTS file for details
License:	BSD
Url:		http://webmproject.org/
# https://chromium.googlesource.com/webm/libwebp/
# Take the last commit from the right branch --
# https://chromium.googlesource.com/webm/libwebp/+/%{version}
Source0:	https://chromium.googlesource.com/webm/libwebp/+archive/%{version}.tar.gz
Patch0:		libwebp-0.6.1-install-extras-lib.patch
Patch1:		libwebp-freeglut.patch
Patch2:		libwebp-1.1.0-vwebp-compile.patch
Patch3:		libwebp-1.1.0-no-useless-L-and-I.patch
Patch4:		libwebp-1.1.0-fix-disable-SIMD.patch
BuildRequires:	libtool
BuildRequires:	swig
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	giflib-devel
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	cmake ninja
%if %{with compat32}
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libGL)
BuildRequires:	devel(libglut)
BuildRequires:	devel(libjpeg)
BuildRequires:	devel(libgif)
BuildRequires:	devel(libtiff)
%endif

%description
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

#----------------------------------------------------------------------------

%package tools
Group:		Development/Other
Summary:	The WebP command line tools

%description tools
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%files tools
%{_bindir}/*
%{_mandir}/man1/*

#----------------------------------------------------------------------------

%package -n	%{libname}
Group:		Development/C
Summary:	Library for the WebP format

%description -n %{libname}
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*
%{_libdir}/%{name}.so.%{version}

%libpackage webpmux 3
%{_libdir}/libwebpmux.so.%{version}
%libpackage webpdemux 2
%{_libdir}/libwebpdemux.so.%{version}
%libpackage webpdecoder 4
%{_libdir}/libwebpdecoder.so.%{version}

#----------------------------------------------------------------------------

%package -n	%{devname}
Group:		Development/C
Summary:	Development files for libwebp, a library for the WebP format
Requires:	%{libname} = %{version}-%{release}
Requires:	%{mklibname webpmux 3} = %{EVRD}
Requires:	%{mklibname webpdemux 2} = %{EVRD}
Requires:	%{mklibname webpdecoder 4} = %{EVRD}
Provides:	webp-devel = %{version}-%{release}

%description -n %{devname}
This package includes the development files for %{name}.

%files -n %{devname}
%doc README PATENTS COPYING NEWS AUTHORS
%{_libdir}/%{name}*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/WebP

#----------------------------------------------------------------------------

%if %{with compat32}
%package -n	%{lib32name}
Group:		Development/C
Summary:	Library for the WebP format (32-bit)

%description -n %{lib32name}
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%files -n %{lib32name}
%{_prefix}/lib/%{name}.so.%{major}*
%{_prefix}/lib/%{name}.so.%{version}

%lib32package webpmux 3
%{_prefix}/lib/libwebpmux.so.%{version}
%lib32package webpdemux 2
%{_prefix}/lib/libwebpdemux.so.%{version}
%lib32package webpdecoder 4
%{_prefix}/lib/libwebpdecoder.so.%{version}

#----------------------------------------------------------------------------

%package -n	%{dev32name}
Group:		Development/C
Summary:	Development files for libwebp, a library for the WebP format (32-bit)
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}
Requires:	%mklib32name webpmux 3
Requires:	%mklib32name webpdemux 2
Requires:	%mklib32name webpdecoder 4

%description -n %{dev32name}
This package includes the development files for %{name}.

%files -n %{dev32name}
%{_prefix}/lib/%{name}*.so
%{_prefix}/lib/pkgconfig/*
%endif

%prep
%autosetup -p1 -c %{name}-%{version}

%ifarch aarch64
export CFLAGS="%{optflags} -frename-registers"
%endif

# WEBP_SIMD_FLAGS defaults to SSE41;SSE2;... - currently
# not supported by every CPU we target with i686 and
# generic x86_64 builds (but very much supported by
# znver1, so don't replace x86_64 with %{x86_64} below)
%if %{with compat32}
%cmake32 \
%ifarch x86_64 i686
	-DWEBP_SIMD_FLAGS="" \
	-DWEBP_ENABLE_SIMD:BOOL=OFF \
%else
	-DWEBP_ENABLE_SIMD:BOOL=ON \
%endif
	-DOpenGL_GL_Preference=GLVND \
	-G Ninja
cd ..
%endif

%if "%{_lib}" != "lib"
# Fix libdir= in *.pc files
sed -i -e 's,set(libdir.*,set(libdir "\\\${prefix\}/%{_lib}"),g' CMakeLists.txt
%endif

%cmake \
%ifarch x86_64 i686
	-DWEBP_SIMD_FLAGS="" \
	-DWEBP_ENABLE_SIMD:BOOL=OFF \
%else
	-DWEBP_ENABLE_SIMD:BOOL=ON \
%endif
	-DOpenGL_GL_Preference=GLVND \
	-G Ninja

%build
%if %{with compat32}
%ninja_build -C build32
%endif
%ninja_build -C build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%ninja_install -C build
