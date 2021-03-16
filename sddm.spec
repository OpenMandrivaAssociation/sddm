%define date 0

Name: sddm
Summary: Lightweight display manager
Version: 0.19.0
%if %{date}
Release: 6.%{date}.3
# Packaged from git for the time being -- no download URL available
# git archive --format=tar --prefix sddm-0.18.1-$(date +%Y%m%d)/ HEAD | xz -vf > sddm-0.18.1-$(date +%Y%m%d).tar.xz
Source0: https://github.com/sddm/sddm/archive/develop/%{name}-%{version}-%{date}.tar.gz
%else
Release: 7
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
Source7: sddm.sysconfig
Patch1: sddm-0.14.0-by-default-use-plasma-session.patch
Patch2: sddm-0.18.1-add-suport-to-plymouth-smooth-transition.patch
# (tpg) https://github.com/sddm/sddm/pull/817
Patch6: 0001-Execute-etc-X11-Xsession.patch
# This patch is IMPORTANT -- don't drop it just because it doesn't apply
# anymore!!!
# https://github.com/sddm/sddm/issues/733
# https://github.com/sddm/sddm/pull/1230
#Patch7: https://github.com/sddm/sddm/pull/1230.patch

# (tpg) patches from upstream git
Patch101: 0000-Improve-font-config-deserialization.patch
Patch102: 0001-Use-PAM-s-username.patch
Patch103: 0004-Only-use-the-base-name-for-DESKTOP_SESSION.patch
Patch104: 0005-Fix-compilation-once-QTBUG-88431-gets-fixed.patch
Patch105: 0006-Merge-normal-and-testing-paths-in-XorgDisplayServer-.patch
Patch106: 0010-Retry-starting-the-display-server.patch
Patch107: 0011-Explicitly-stop-Xorg-when-starting-fails.patch
Patch108: 0012-Emit-XorgDisplayServer-started-only-when-the-auth-fi.patch
Patch110: 0014-Fix-sessions-being-started-as-the-wrong-type-on-auto.patch
Patch112: 0016-wayland-session-Ensure-SHELL-remains-correctly-set.patch
Patch114: 0018-Update-sv.ts-1342.patch
Patch115: 0019-Clear-VT-before-switching-to-it.patch
Patch116: 0020-Prevent-potential-crash-when-not-in-testing-mode.patch
Patch117: 0021-Allow-addition-env-vars-to-be-defined-in-session-fil.patch
Patch118: 0022-Add-fish-etc-profile-and-HOME-.profile-sourcing-1331.patch
Patch119: 0023-Error-in-elarun-theme-1336.patch
Patch120: 0024-Use-avatars-in-FacesDir-first-and-if-not-found-searc.patch
Patch121: 0025-Remove-suffix-for-Wayland-session-997.patch
Patch122: 0026-Fix-warning-from-SDDM-generateName.patch
Patch200: https://patch-diff.githubusercontent.com/raw/sddm/sddm/pull/1379.patch


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
BuildRequires: systemd-macros
# For /etc/X11/Xsession
Requires: xinitrc
Requires: weston
BuildRequires: rpm-helper
Requires(pre,postun): rpm-helper
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

%ifarch %{aarch64}
# As of sddm 0.18.0, clang 7.0.1, building sddm with clang
# on aarch64 results in the login screen not appearing because
# of a failing signal/slot connection
# QObject::connect: signal not found in QDBusPendingCallWatcher
export CC=gcc
export CXX=g++
%endif
%cmake_kde5 \
    -DUSE_QT5:BOOL=ON \
    -DSESSION_COMMAND:FILEPATH=/etc/X11/Xsession \
    -DENABLE_JOURNALD=ON \
    -DENABLE_PAM=ON \
    -DENABLE_PLYMOUTH=ON \
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
install -Dpm 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/sysconfig/sddm

mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/sddm.conf.d
# use omv-background.png as sddm background for all themes
sed -i -e 's,\(^background=\).*,\1%{_datadir}/mdk/backgrounds/OpenMandriva-splash.png,' %{buildroot}%{_datadir}/sddm/themes/elarun/theme.conf
sed -i -e 's,\(^background=\).*,\1%{_datadir}/mdk/backgrounds/OpenMandriva-splash.png,' %{buildroot}%{_datadir}/sddm/themes/maldives/theme.conf

%files
%{_bindir}/%{name}
%{_bindir}/%{name}-greeter
%{_datadir}/%{name}
%dir %{_sysconfdir}/sddm.conf.d
%config(noreplace) %{_sysconfdir}/sddm.conf
%config(noreplace) %{_sysconfdir}/sysconfig/sddm
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%{_sysconfdir}/pam.d/%{name}
%{_sysconfdir}/pam.d/%{name}-greeter
%{_sysconfdir}/pam.d/%{name}-autologin
%{_sysusersdir}/sddm.conf
%{_tmpfilesdir}/sddm.conf
%{_libexecdir}/sddm-helper*
%{_unitdir}/%{name}.service
%{_libdir}/qt5/qml/SddmComponents
%{_datadir}/X11/dm.d/11sddm.conf
%attr(0755,sddm,sddm) %{_localstatedir}/lib/%{name}
