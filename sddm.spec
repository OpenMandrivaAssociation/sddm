%define date 20191216

Name: sddm
Summary: Lightweight display manager
Version: 0.18.1
%if %{date}
Release: 5.%{date}.1
# Packaged from git for the time being -- no download URL available
# git archive --format=tar --prefix sddm-0.11.0-$(date +%Y%m%d)/ HEAD | xz -vf > sddm-0.11.0-$(date +%Y%m%d).tar.xz
Source0: %{name}-%{version}-%{date}.tar.xz
%else
Release: 1
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
## UH that is wrong wrong .. it means waits forever
## which again means we can deadlock on a displayscript.
## (rxu) wait until script exits
##Patch0: sddm-0.12.0-waitForFinished.patch
## do NOT enable that again - crazy -
Patch1: sddm-0.14.0-by-default-use-plasma-session.patch
Patch2: sddm-0.14.0-call-retain-splash-on-plymouth.patch
# (tpg) seems to be broken
#Patch4: sddm-0.14.0-Log-Xorg-server-output-to-the-journal.patch
# (tpg) based on this https://github.com/sddm/sddm/pull/525
#Patch3: sddm-0.14.0-add-support-to-QtAccountsService.patch
# (tpg) based on this https://github.com/sddm/sddm/pull/439
#Patch4: sddm-0.14.0-add-suport-to-plymouth-smooth-transition.patch
# (tpg) https://github.com/sddm/sddm/pull/817
Patch6: 0001-Execute-etc-X11-Xsession.patch
# This patch is IMPORTANT -- don't drop it just because it doesn't apply
# anymore!!!
# https://github.com/sddm/sddm/issues/733
Patch7: https://src.fedoraproject.org/cgit/rpms/sddm.git/plain/0001-Port-from-xauth-to-libXau.patch
Patch8: sddm-0.17.0-clang.patch
Patch9: https://src.fedoraproject.org/rpms/sddm/raw/master/f/sddm-0.18.0-environment_file.patch
BuildRequires: cmake(ECM)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
%if %{mdvver} <= 3000000
BuildRequires: pkgconfig(Qt5Declarative)
%endif
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
%autosetup -n %{name}-%{version}-%{date} -p1
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

# use omv-background.png as sddm background for all themes
sed -i -e 's,\(^background=\).*,\1%{_datadir}/mdk/backgrounds/OpenMandriva-splash.png,' %{buildroot}%{_datadir}/sddm/themes/elarun/theme.conf
sed -i -e 's,\(^background=\).*,\1%{_datadir}/mdk/backgrounds/OpenMandriva-splash.png,' %{buildroot}%{_datadir}/sddm/themes/maldives/theme.conf

%pre
%_pre_useradd sddm %{_var}/lib/sddm /bin/false

%postun
%_postun_userdel sddm

%files
%{_bindir}/%{name}
%{_bindir}/%{name}-greeter
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/sddm.conf
%config(noreplace) %{_sysconfdir}/sysconfig/sddm
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
