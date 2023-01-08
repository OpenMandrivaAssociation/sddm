%define date 0

Name: sddm
Summary: Lightweight display manager
Version: 0.19.0
%if %{date}
Release: 0.%{date}.3
# Packaged from git for the time being -- no download URL available
# git archive --format=tar --prefix sddm-0.18.1-$(date +%Y%m%d)/ HEAD | xz -vf > sddm-0.18.1-$(date +%Y%m%d).tar.xz
Source0: https://github.com/sddm/sddm/archive/develop/%{name}-%{version}-%{date}.tar.gz
%else
Release: 16
Source0: https://github.com/sddm/sddm/releases/download/v%{version}/%{name}-%{version}.tar.xz
%endif
URL: https://github.com/sddm
Group: Graphical desktop/KDE
License: GPLv2
# Adds sddm to drakedm
Source1: 11sddm.conf
Source2: sddm.conf
Source3: sddm.pam
Source4: sddm-autologin.pam
Source5: tmpfiles-sddm.conf
Source6: sddm.sysusers
Patch1: sddm-0.14.0-by-default-use-plasma-session.patch
# (tpg) https://github.com/sddm/sddm/pull/817
Patch6: 0001-Execute-etc-X11-Xsession.patch
# This patch is IMPORTANT -- don't drop it just because it doesn't apply
# anymore!!!
# https://github.com/sddm/sddm/issues/733
# https://github.com/sddm/sddm/pull/1230
Patch7: https://github.com/sddm/sddm/pull/1230.patch
# Based on
# https://github.com/sddm/sddm/pull/1603
# (difference: backported to current stable tree)
Patch8: 1603.patch

# (tpg) patches from upstream git
Patch100: 0000-Improve-font-config-deserialization.patch
Patch101: 0001-Only-use-the-base-name-for-DESKTOP_SESSION.patch
Patch102: 0002-Merge-normal-and-testing-paths-in-XorgDisplayServer-.patch
Patch103: 0003-Retry-starting-the-display-server.patch
Patch104: 0004-Explicitly-stop-Xorg-when-starting-fails.patch
Patch105: 0005-Emit-XorgDisplayServer-started-only-when-the-auth-fi.patch
Patch106: 0006-Fix-sessions-being-started-as-the-wrong-type-on-auto.patch
Patch107: 0007-wayland-session-Ensure-SHELL-remains-correctly-set.patch
Patch108: 0008-Clear-VT-before-switching-to-it.patch
Patch109: 0009-Error-in-elarun-theme-1336.patch
Patch110: 0010-Use-avatars-in-FacesDir-first-and-if-not-found-searc.patch
Patch111: 0011-Fix-warning-from-SDDM-generateName.patch
Patch112: 0012-Allocate-VT-for-the-display.patch
Patch113: 0013-sddm-service-is-a-part-of-graphical-target.patch
Patch114: 0014-Fix-displaying-user-icons.patch

BuildRequires: cmake(ECM)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pam-devel
BuildRequires: qt5-linguist-tools
BuildRequires: systemd-rpm-macros

# For /etc/X11/Xsession
Requires: xinitrc
Requires(pre): systemd
%systemd_requires
# needed to get xcb plugin on Qt platform
Requires: %{_lib}qt5-output-driver-default
# needed for QtQuick
Requires: qt5-qtdeclarative
Requires: qt5-qtimageformats
%ifnarch %{armx} %{riscv}
Requires: distro-theme-OpenMandriva >= 1.4.37
%endif
Provides: dm
# (tpg) fix update from 2014.0
Provides: kdm = 2:4.11.22-1.1
Obsoletes: kdm < 2:4.11.22-1.1

%description
Lightweight display manager (login screen).

%prep
%if %{date}
%autosetup -n %{name}-develop -p1
%else
%autosetup -p1
%endif

sed -i -e 's,system-login,system-auth,g' services/*.pam

%cmake_kde5 \
    -DUSE_QT5:BOOL=ON \
    -DSESSION_COMMAND:FILEPATH=/etc/X11/Xsession \
    -DENABLE_JOURNALD=ON \
    -DENABLE_PAM=ON \
    -DUID_MIN="1000" \
    -DUID_MAX="60000"

%build
%ninja -C build

%install
%ninja_install -C build

install -Dpm 644 %{SOURCE1} %{buildroot}%{_datadir}/X11/dm.d/11sddm.conf
install -Dpm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sddm.conf
install -Dpm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/sddm
install -Dpm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/pam.d/sddm-autologin
install -Dpm 644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/sddm.conf
install -Dpm 644 %{SOURCE6} %{buildroot}%{_sysusersdir}/sddm.conf

mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/sddm.conf.d
# use omv-background.png as sddm background for all themes
sed -i -e 's,\(^background=\).*,\1%{_datadir}/mdk/backgrounds/OpenMandriva-splash.png,' %{buildroot}%{_datadir}/sddm/themes/elarun/theme.conf
sed -i -e 's,\(^background=\).*,\1%{_datadir}/mdk/backgrounds/OpenMandriva-splash.png,' %{buildroot}%{_datadir}/sddm/themes/maldives/theme.conf

%pre
%sysusers_create_package %{name} %{SOURCE6}

%files
%{_bindir}/%{name}
%{_bindir}/%{name}-greeter
%{_datadir}/%{name}
%dir %{_sysconfdir}/sddm.conf.d
%config(noreplace) %{_sysconfdir}/sddm.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%{_sysconfdir}/pam.d/%{name}
%{_sysconfdir}/pam.d/%{name}-greeter
%{_sysconfdir}/pam.d/%{name}-autologin
%{_sysusersdir}/sddm.conf
%{_tmpfilesdir}/sddm.conf
%{_libexecdir}/sddm-helper
%{_unitdir}/%{name}.service
%{_libdir}/qt5/qml/SddmComponents
%{_datadir}/X11/dm.d/11sddm.conf
%attr(0755,sddm,sddm) %{_localstatedir}/lib/%{name}
