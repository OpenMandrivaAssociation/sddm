%define date 0

Name: sddm
Summary: Lightweight display manager
Version: 0.20.0
%if %{date}
Release: 0.%{date}.1
# Packaged from git for the time being -- no download URL available
# git archive --format=tar --prefix sddm-0.18.1-$(date +%Y%m%d)/ HEAD | xz -vf > sddm-0.18.1-$(date +%Y%m%d).tar.xz
Source0: https://github.com/sddm/sddm/archive/develop/%{name}-%{version}-%{date}.tar.gz
%else
Release: 6
Source0: https://github.com/sddm/sddm/archive/refs/tags/v%{version}.tar.gz
%endif
URL: https://github.com/sddm
Group: Graphical desktop/KDE
License: GPLv2
Source1: sddm.conf
# Allow specifying a default session (and default to plasma) for
# users that haven't logged in before
Patch0: sddm-0.20.0-allow-setting-default-session.patch
Patch1: sddm-0.20.0-default-rootless.patch
# (tpg) upstream patches
Patch100: https://github.com/sddm/sddm/commit/5b702ae986464fe6dbc8557d4b2da725ac1ed175.patch
Patch101: https://github.com/sddm/sddm/commit/e27b70957505dc7b986ab2fa68219af546c63344.patch
Patch102: https://github.com/sddm/sddm/commit/07631f2ef00a52d883d0fd47ff7d1e1a6bc6358f.patch
Patch103: https://github.com/sddm/sddm/commit/0823810ed1683e6dcb7d687795764e11ddb6ff8a.patch
Patch104: https://github.com/sddm/sddm/commit/9e7791d5fb375933d20f590daba9947195515b26.patch
BuildRequires: cmake(ECM)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(Qt5QuickTest)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pam-devel
BuildRequires: qt5-linguist-tools
BuildRequires: systemd-rpm-macros

# For /etc/X11/Xsession
Requires: xinitrc
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

install -Dpm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sddm.conf

mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/sddm.conf.d
# use omv-background.png as sddm background for all themes
sed -i -e 's,\(^background=\).*,\1%{_datadir}/mdk/backgrounds/OpenMandriva-splash.png,' %{buildroot}%{_datadir}/sddm/themes/elarun/theme.conf
sed -i -e 's,\(^background=\).*,\1%{_datadir}/mdk/backgrounds/OpenMandriva-splash.png,' %{buildroot}%{_datadir}/sddm/themes/maldives/theme.conf

cat >%{buildroot}%{_sysconfdir}/sddm.conf.d/00-rootless.conf <<EOF
[General]
DisplayServer=x11-user
EOF

%post
%systemd_post sddm.service

%preun
%systemd_preun sddm.service

%postun
%systemd_postun sddm.service

%files
%{_bindir}/%{name}
%{_bindir}/%{name}-greeter
%{_datadir}/%{name}
%dir %{_sysconfdir}/sddm.conf.d
%config(noreplace) %{_sysconfdir}/sddm.conf
%config(noreplace) %{_sysconfdir}/sddm.conf.d/00-rootless.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%{_sysconfdir}/pam.d/%{name}
%{_sysconfdir}/pam.d/%{name}-greeter
%{_sysconfdir}/pam.d/%{name}-autologin
%{_sysusersdir}/sddm.conf
%{_tmpfilesdir}/sddm.conf
%{_libexecdir}/sddm-helper
%{_libexecdir}/sddm-helper-start-wayland
%{_libexecdir}/sddm-helper-start-x11user
%{_unitdir}/%{name}.service
%{_libdir}/qt5/qml/SddmComponents
%attr(0755,sddm,sddm) %{_localstatedir}/lib/%{name}
