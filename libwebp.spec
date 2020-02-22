%define major 7
%define libname %mklibname webp %{major}
%define devname %mklibname -d webp

Summary:	Library and tools for the WebP graphics format
Name:		libwebp
Version:	1.1.0
Release:	1
Group:		Development/C
# Additional IPR is licensed as well. See PATENTS file for details
License:	BSD
Url:		http://webmproject.org/
Source0:	http://storage.googleapis.com/downloads.webmproject.org/releases/webp/%{name}-%{version}.tar.gz
Patch0:		libwebp-install-extras-lib.patch
BuildRequires:	libtool
BuildRequires:	swig
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libpng)

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

%libpackage webpmux 3
%libpackage webpdemux 2
%libpackage webpdecoder 3
%libpackage webpextras 0

#----------------------------------------------------------------------------

%package -n	%{devname}
Group:		Development/C
Summary:	Development files for libwebp, a library for the WebP format
Requires:	%{libname} = %{version}-%{release}
Requires:	%mklibname webpmux 3
Requires:	%mklibname webpdemux 2
Requires:	%mklibname webpdecoder 3
Requires:	%mklibname webpextras 0
Provides:	webp-devel = %{version}-%{release}

%description -n %{devname}
This package includes the development files for %{name}.

%files -n %{devname}
%doc README PATENTS COPYING NEWS AUTHORS
%{_libdir}/%{name}*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

#----------------------------------------------------------------------------

%prep
%setup -qc %{name}-%{version}
%autopatch -p0

%build
autoreconf -vfi
%ifarch aarch64
export CFLAGS="%{optflags} -frename-registers"
%endif
%configure --disable-static \
	--enable-libwebpmux \
	--enable-libwebpdemux \
	--enable-libwebpdecoder \
	--enable-libwebpextras
%make_build

%install
%make_install
