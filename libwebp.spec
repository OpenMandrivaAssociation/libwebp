# libgphoto uses libwebp, wine uses libgphoto
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 7
%define oldlibname %mklibname webp 7
%define libname %mklibname webp
%define devname %mklibname -d webp
%define oldlib32name %mklib32name webp 7
%define lib32name %mklib32name webp
%define dev32name %mklib32name -d webp

Summary:	Library and tools for the WebP graphics format
Name:		libwebp
Version:	1.6.0
Release:	1
Group:		Development/C
# Additional IPR is licensed as well. See PATENTS file for details
License:	BSD
Url:		https://webmproject.org/
# https://chromium.googlesource.com/webm/libwebp/
# Take the last commit from the right branch --
# https://chromium.googlesource.com/webm/libwebp/+/%{version}
Source0:	http://storage.googleapis.com/downloads.webmproject.org/releases/webp/%{name}-%{version}.tar.gz
#Patch0:		webp-1.2.1-compile.patch
Patch1:		libwebp-1.2.4-qt6-qtimageformats-buildfix.patch

BuildRequires:	swig
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	giflib-devel
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	cmake
BuildRequires:	ninja
%if %{with compat32}
BuildRequires:	devel(libz)
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libGL)
BuildRequires:	devel(libglut)
BuildRequires:	devel(libjpeg)
BuildRequires:	devel(libgif)
BuildRequires:	devel(libtiff)
%endif
%if %{with compat32}
# Ugly, but lib32name == src.rpm name
%rename %{oldlib32name}
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
%doc %{_mandir}/man1/*

#----------------------------------------------------------------------------

%package -n %{libname}
Group:		Development/C
Summary:	Library for the WebP format
%rename %{oldlibname}

%description -n %{libname}
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*
%{_libdir}/libsharpyuv.so.0*

%libpackage webpmux 3
%libpackage webpdemux 2
%libpackage webpdecoder 3

#----------------------------------------------------------------------------

%package -n %{devname}
Group:		Development/C
Summary:	Development files for libwebp, a library for the WebP format
Requires:	%{libname} = %{version}-%{release}
Requires:	%{mklibname webpmux} = %{EVRD}
Requires:	%{mklibname webpdemux} = %{EVRD}
Requires:	%{mklibname webpdecoder} = %{EVRD}
Provides:	webp-devel = %{version}-%{release}

%description -n %{devname}
This package includes the development files for %{name}.

%files -n %{devname}
%doc README* PATENTS COPYING NEWS AUTHORS
%{_libdir}/%{name}*.so
%{_libdir}/libsharpyuv.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/WebP

#----------------------------------------------------------------------------

%if %{with compat32}
%files
%{_prefix}/lib/%{name}.so.%{major}*
%{_prefix}/lib/libsharpyuv.so.0*

%lib32package webpmux 3
%lib32package webpdemux 2
%lib32package webpdecoder 3

#----------------------------------------------------------------------------

%package -n %{dev32name}
Group:		Development/C
Summary:	Development files for libwebp, a library for the WebP format (32-bit)
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}
Requires:	%mklib32name webpmux
Requires:	%mklib32name webpdemux
Requires:	%mklib32name webpdecoder

%description -n %{dev32name}
This package includes the development files for %{name}.

%files -n %{dev32name}
%{_prefix}/lib/%{name}*.so
%{_prefix}/lib/libsharpyuv.so
%{_prefix}/lib/pkgconfig/*
%endif

%prep
%autosetup -p1

%ifarch aarch64
export CFLAGS="%{optflags} -frename-registers"
%endif

# libwebp likes to assume everything that has SSE2
# also has SSE4.1. This is true for znver1 (so don't
# replace x86_64 below with %{x86_64} below), but not
# for every old x86_64 CPU we target.
# We "fix" it by doing a SIMD enabled build, but
# pretending our compiler doesn't support SSE4.1
%ifarch x86_64 i686
sed -i -e 's,-msse4.1,-mno-sse4.1,g;s,SSE41,NOSSE41,g' cmake/cpu.cmake
sed -i -e 's,__SSE4_1__,NO_WE_DONT_WANT_SSE41,g' src/dsp/dsp.h
%endif

%if %{with compat32}
%cmake32 \
%ifarch %{x86_64} %{aarch64} %{arm}
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
%ifarch %{x86_64} %{aarch64} %{arm}
	-DWEBP_ENABLE_SIMD:BOOL=ON \
%endif
	-DOpenGL_GL_Preference=GLVND \
	-G Ninja

%build
%if %{with compat32}
%ninja_build -C build32
%endif
%ninja_build -C build -v

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%ninja_install -C build
