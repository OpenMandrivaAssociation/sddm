%define date 20140629

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
URL: https://github.com/sddm
Group: Graphical desktop/KDE
License: GPLv2
BuildRequires: cmake
BuildRequires: pkgconfig(Qt5Core) pkgconfig(Qt5Gui) pkgconfig(Qt5Declarative) pkgconfig(Qt5DBus) pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(systemd) pkgconfig(libsystemd-journal)
BuildRequires: pam-devel
BuildRequires: qt5-linguist-tools
BuildRequires: qmake5 ninja
# For /etc/X11/Xsession
Requires: xinitrc

%description
Lightweight display manager (login screen)

%prep
%setup -q -n %name-%date
%apply_patches
sed -i -e 's,system-login,system-auth,g' services/*.pam
%cmake \
	-DUSE_QT5:BOOL=ON \
	-DSESSION_COMMAND:FILEPATH=/etc/X11/Xsession \
	-G Ninja

%build
ninja -C build

%install
DESTDIR="%{buildroot}" ninja install -C build

%files
%_bindir/%name
%_bindir/%name-greeter
%_datadir/%name
%_sysconfdir/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%_sysconfdir/pam.d/%name
%_sysconfdir/pam.d/%name-greeter
%_sysconfdir/pam.d/%name-autologin
%_libexecdir/sddm-helper
%config(noreplace) %_sysconfdir/%name.conf
/lib/systemd/system/%name.service
%_libdir/qt5/qml/SddmComponents

%pre
%_pre_useradd sddm %_datadir/%name /bin/false

%postun
%_postun_userdel sddm
