%define rev	20110217svn3815

Name:           rawstudio 
Version:        1.2
Release:        8%{?dist}.%{rev}
Summary:        Read, manipulate and convert digital camera raw images

Group:          Applications/Multimedia 
License:        GPLv2+
URL:            http://rawstudio.org

#Source0:        http://rawstudio.org/files/release/%{name}-%{version}.tar.gz
# Packaging a snapshot created with 
# svn export -r 3521 https://rawstudio.org/svn/rawstudio/trunk/ rawstudio
Source0:        %{name}-%{rev}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel, libxml2-devel, GConf2-devel, dbus-devel
BuildRequires:  lcms-devel, libjpeg-devel, libtiff-devel, exiv2-devel
BuildRequires:  flickcurl-devel, lensfun-devel, fftw-devel, libcurl-devel
BuildRequires:  sqlite-devel, openssl-devel
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  libtool

BuildRequires:  libgphoto2-devel
# http://bugzilla.rawstudio.org/show_bug.cgi?id=417
#Patch0:         rawstudio-1.2-link_libX11.patch


%description
Rawstudio is a highly specialized application for processing RAW images
from digital cameras. It is not a fully featured image editing application.

The RAW format is often recommended to get the best quality out of digital 
camera images.  The format is specific to cameras and cannot be read by most 
image editing applications.

Rawstudio makes it possible to read and manipulate RAW images, experiment 
with the controls to see how they affect the image, and finally export into 
JPEG, PNG or TIF format images from most digital cameras.


%prep
%setup -q -n %{name}-%{rev}
#%patch0 -p0

%build
./autogen.sh
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/usr/lib64/librawstudio-1.1.a
%find_lang %{name}

# Remove useless files
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

# Fix desktop file warning
# Note: the Encoding tag seems to be deprecated in desktop entry specs v1.0
#       so this has probably to go away in the future
echo "Encoding=UTF-8" >> ${RPM_BUILD_ROOT}%{_datadir}/applications/rawstudio.desktop

desktop-file-install --vendor fedora                            \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications         \
        --remove-category Application                           \
        --delete-original                                       \
        ${RPM_BUILD_ROOT}%{_datadir}/applications/rawstudio.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database &> /dev/null ||:

%postun
update-desktop-database &> /dev/null ||:


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README NEWS COPYING AUTHORS
%{_bindir}/rawstudio
%{_datadir}/rawstudio
%{_datadir}/rawspeed
%{_datadir}/pixmaps/rawstudio
%{_datadir}/applications/fedora-rawstudio.desktop
%{_datadir}/icons/rawstudio.png

# TODO: split a "librawstudio" package
%{_libdir}/librawstudio-1.1.so.*

# TODO: split in a librawstudio-devel package
%{_includedir}/rawstudio-1.1
%{_libdir}/librawstudio-1.1.so
%{_libdir}/pkgconfig/rawstudio-1.1.pc

%changelog
* Thu Feb 17 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 1.2-8.20110217svn3815
- update to svn3815

* Sun Jan 02 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.2-7.20100907svn3521
- rebuild (exiv2)

* Tue Sep  8 2010 Gianluca Sforna <giallu gmail com>
- Fix BuildRequires
- Add updated patch for X11 link issue

* Tue Sep  7 2010 Gianluca Sforna <giallu gmail com>
- move to a snapshot
- drop upstreamed patches
- add find-lang
- remove .la files
- disable static library build

* Mon May 31 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.2-5 
- rebuild (exiv2)

* Sat Feb 13 2010 Gianluca Sforna <giallu gmail com> - 1.2-4
- Add explicit link to libX11 (#564638)

* Mon Jan 04 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.2-3 
- rebuild (exiv2)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 10 2009 Gianluca Sforna <giallu gmail com> - 1.2-1
- New upstream release

* Thu Feb 26 2009 Gianluca Sforna <giallu gmail com> - 1.1.1-4
- Fix build with newer glibc

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.1.1-2 
- respin (eviv2)

* Mon Oct 13 2008 Gianluca Sforna <giallu gmail com> - 1.1.1-1
- new upstream release

* Tue Sep 16 2008 Gianluca Sforna <giallu gmail com> - 1.1-1
- new upstream release

* Thu May  1 2008 Gianluca Sforna <giallu gmail com> - 1.0-1
- new upstream release
- drop upstreamed patch
- slightly improved summary

* Tue Feb 24 2008 Gianluca Sforna <giallu gmail com> - 0.7-2
- rebuild with gcc 4.3

* Thu Jan 24 2008 Gianluca Sforna <giallu gmail com> - 0.7-1
- New upstream release
- Improved package description
- Add fix for PPC build

* Sun Aug 19 2007 Gianluca Sforna <giallu gmail com> 0.6-1
- New upstream release
- Updated License field
- Include new pixmaps directory

* Wed Feb 21 2007 Gianluca Sforna <giallu gmail com> 0.5.1-1
- New upstream release
- Fix desktop-file-install warnings

* Tue Feb 06 2007 Gianluca Sforna <giallu gmail com> 0.5-1
- new upstream version
- add libtiff-devel BR
- drop upstreamed patch
- drop dcraw runtime Require

* Wed Sep 27 2006 Gianluca Sforna <giallu gmail com> 0.4.1-1
- new upstream version
- Add DESTDIR patch (and BR: automake)
- New .desktop file and icon

* Fri Jul 28 2006 Gianluca Sforna <giallu gmail com> 0.3-1
- Initial package. Adapted from fedora-rpmdevtools template.
