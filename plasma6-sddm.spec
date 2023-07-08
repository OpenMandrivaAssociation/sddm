%define date 20230708

Name: plasma6-sddm
Summary: Lightweight display manager
Version: 0.19.1
%if %{date}
Release: 0.%{date}.1
# Packaged from git for the time being -- no download URL available
# git archive --format=tar --prefix sddm-0.18.1-$(date +%Y%m%d)/ HEAD | xz -vf > sddm-0.18.1-$(date +%Y%m%d).tar.xz
Source0: https://github.com/sddm/sddm/archive/develop/%{name}-%{version}-%{date}.tar.gz
%else
Release: 17
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
# Based on
# https://github.com/sddm/sddm/pull/1603
# (difference: backported to current stable tree)
Patch8: 1603.patch

BuildRequires: cmake(ECM)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Quick)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6LinguistTools)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pam-devel
BuildRequires: systemd-rpm-macros

# For /etc/X11/Xsession
Requires: xinitrc
Requires(pre): systemd
%systemd_requires
Provides: dm
Conflicts: sddm

%description
Lightweight display manager (login screen).

%prep
%if %{date}
%autosetup -n sddm-develop -p1
%else
%autosetup -p1
%endif

sed -i -e 's,system-login,system-auth,g' services/*.pam

%cmake_kde5 \
    -DBUILD_WITH_QT6:BOOL=ON \
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
%{_bindir}/sddm
%{_bindir}/sddm-greeter
%{_datadir}/sddm
%dir %{_sysconfdir}/sddm.conf.d
%config(noreplace) %{_sysconfdir}/sddm.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%{_sysconfdir}/pam.d/sddm
%{_sysconfdir}/pam.d/sddm-greeter
%{_sysconfdir}/pam.d/sddm-autologin
%{_sysusersdir}/sddm.conf
%{_tmpfilesdir}/sddm.conf
%{_libexecdir}/sddm-helper
%{_libexecdir}/sddm-helper-start-x11user
%{_libexecdir}/sddm-helper-start-wayland
%{_unitdir}/sddm.service
%{_libdir}/qt6/qml/SddmComponents
%{_datadir}/X11/dm.d/11sddm.conf
