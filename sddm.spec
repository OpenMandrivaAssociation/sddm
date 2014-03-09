%define date 20140309

Name: sddm
Summary: Lightweight display manager
Version: 0.1.1
%if %date
Release: 0.%date.1
# Packaged from git for the time being -- no download URL available
Source0: sddm-%date.tar.xz
%else
Release: 1
%endif
Patch0: sddm-config.patch
Patch1: sddm-20140309-systemd.patch
URL: https://github.com/sddm
Group: Graphical desktop/KDE
License: GPLv2
BuildRequires: cmake
BuildRequires: pkgconfig(Qt5Core) pkgconfig(Qt5Gui) pkgconfig(Qt5Declarative) pkgconfig(Qt5DBus) pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(systemd)
BuildRequires: qt5-linguist-tools
BuildRequires: qmake5 ninja

%description
Lightweight display manager (login screen)

%prep
%setup -q -n %name-%date
%apply_patches
sed -i -e 's,system-login,system-auth,g' services/*.pam
%cmake -DUSE_QT5:BOOL=ON -G Ninja

%build
ninja -C build

%install
DESTDIR="%{buildroot}" ninja install -C build

%files
%_bindir/%name
%_bindir/%name-greeter
%_datadir/apps/%name
%_sysconfdir/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%_sysconfdir/pam.d/%name
%config(noreplace) %_sysconfdir/%name.conf
/lib/systemd/system/%name.service
%_libdir/qt5/qml/SddmComponents
