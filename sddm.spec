%define date 20130426

Name: sddm
Summary: Lightweight display manager
Version: 0.1
%if %date
Release: 0.%date.1
# Packaged from git for the time being -- no download URL available
Source0: sddm-%date.tar.xz
%else
Release: 1
%endif
URL: https://github.com/sddm
Group: Graphical desktop/KDE
License: GPLv2
BuildRequires: pkgconfig(QtCore) pkgconfig(QtGui) pkgconfig(QtDeclarative)

%description
Lightweight display manager (login screen)

%prep
%setup -q -n %name-%date
%cmake_kde4

%build
cd build
%make

%install
cd build
%makeinstall_std

%files
%_bindir/%name
%_bindir/%name-greeter
%_datadir/apps/%name
%_sysconfdir/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%_sysconfdir/pam.d/%name
%config(noreplace) %_sysconfdir/%name.conf
/lib/systemd/system/%name.service
%_prefix/lib/qt4/imports/SddmComponents
