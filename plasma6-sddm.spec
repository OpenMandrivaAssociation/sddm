%define date 20230814

Name: plasma6-sddm
Summary: Lightweight display manager
Version: 0.20.1
%if %{date}
Release: 0.%{date}.3
# Packaged from git for the time being -- no download URL available
# git archive --format=tar --prefix sddm-0.20.1-$(date +%Y%m%d)/ HEAD | xz -vf > sddm-0.20.1-$(date +%Y%m%d).tar.xz
Source0: https://github.com/sddm/sddm/archive/develop/%{name}-%{version}-%{date}.tar.gz
%else
Release: 1
Source0: https://github.com/sddm/sddm/releases/download/v%{version}/%{name}-%{version}.tar.xz
%endif
URL: https://github.com/sddm
Group: Graphical desktop/KDE
License: GPLv2
Source1: sddm.conf
Patch0: sddm-0.20.0-allow-setting-default-session.patch
Patch1: sddm-0.20.0-default-rootless.patch
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

install -Dpm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sddm.conf

mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/sddm.conf.d
# use omv-background.png as sddm background for all themes
sed -i -e 's,\(^background=\).*,\1%{_datadir}/mdk/backgrounds/OpenMandriva-splash.png,' %{buildroot}%{_datadir}/sddm/themes/elarun/theme.conf
sed -i -e 's,\(^background=\).*,\1%{_datadir}/mdk/backgrounds/OpenMandriva-splash.png,' %{buildroot}%{_datadir}/sddm/themes/maldives/theme.conf

mkdir -p %{buildroot}%{_localstatedir}/lib/sddm

%post
%systemd_post sddm.service

%preun
%systemd_preun sddm.service

%postun
%systemd_postun sddm.service

%files
%{_bindir}/sddm
%{_bindir}/sddm-greeter
%{_datadir}/sddm
%dir %{_sysconfdir}/sddm.conf.d
%config(noreplace) %{_sysconfdir}/sddm.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf
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
%attr(-,sddm,sddm) %{_localstatedir}/lib/sddm
