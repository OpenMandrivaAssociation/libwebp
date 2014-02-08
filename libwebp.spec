%define major 4
%define libname %mklibname webp %{major}
%define devname %mklibname -d webp

Summary:	Library and tools for the WebP graphics format
Name:		libwebp
Version:	0.3.0
Release:	3
Group:		Development/C
# Additional IPR is licensed as well. See PATENTS file for details
License:	BSD
Url:		http://webmproject.org/
Source0:	http://webp.googlecode.com/files/%{name}-%{version}.tar.gz
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

#----------------------------------------------------------------------------

%package -n	%{devname}
Group:		Development/C
Summary:	Development files for libwebp, a library for the WebP format
Requires:	%{libname} = %{version}-%{release}
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
%setup -q
find . -perm 0640 | xargs chmod 0644

%build
%configure2_5x --disable-static 
%make

%install
%makeinstall_std

