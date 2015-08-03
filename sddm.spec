%define date 20150705

Name: sddm
Summary: Lightweight display manager
Version: 0.11.0
%if %date
Release: 24.%{date}.3
# Packaged from git for the time being -- no download URL available
# git archive --format=tar --prefix sddm-0.11.0-$(date +%Y%m%d)/ HEAD | xz -vf > sddm-0.11.0-$(date +%Y%m%d).tar.xz
Source0: sddm-%{version}-%date.tar.xz
%else
Release: 24
Source0: https://github.com/sddm/sddm/archive/%{name}-%{version}.tar.gz
%endif
# Adds sddm to drakedm
Source1: 11sddm.conf
Source2: sddm.conf
Source3: sddm.pam
Source4: sddm-autologin.pam
Source5: tmpfiles-sddm.conf
Source6: omv-background.png
URL: https://github.com/sddm
Group: Graphical desktop/KDE
License: GPLv2
BuildRequires: cmake(ECM)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Declarative)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(libsystemd-journal)
BuildRequires: pam-devel
BuildRequires: qt5-linguist-tools
# For /etc/X11/Xsession
Requires: xinitrc
Requires(post,preun):	rpm-helper
# needed to get xcb plugin on Qt platform
Requires:	qt5-output-driver-default
# needed for QtQuick
Requires:	qt5-qtdeclarative

%description
Lightweight display manager (login screen).

%prep
%if %date
%setup -q -n %{name}-%{version}-%{date}
%else
%setup -q
%endif
%apply_patches

sed -i -e 's,system-login,system-auth,g' services/*.pam

%cmake_kde5 \
	-DUSE_QT5:BOOL=ON \
	-DSESSION_COMMAND:FILEPATH=/etc/X11/Xsession \
	-DENABLE_JOURNALD=ON \
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

mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}

# use omv-background.png as sddm background for all themes
install -Dpm 644 %{SOURCE6} %{buildroot}%{_datadir}/%{name}/themes/omv-background.png
sed -i -e 's,\(^background=\).*,\1%{_datadir}/%{name}/themes/omv-background.png,' %{buildroot}%{_datadir}/sddm/themes/*/theme.conf

%pre
%_pre_useradd sddm %{_var}/lib/sddm /bin/false

%postun
%_postun_userdel sddm

%files
%{_bindir}/%{name}
%{_bindir}/%{name}-greeter
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/sddm.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%{_sysconfdir}/pam.d/%{name}
%{_sysconfdir}/pam.d/%{name}-greeter
%{_sysconfdir}/pam.d/%{name}-autologin
%{_tmpfilesdir}/sddm.conf
%{_libexecdir}/sddm-helper
%{_unitdir}/%{name}.service
%{_libdir}/qt5/qml/SddmComponents
%{_datadir}/X11/dm.d/11sddm.conf
%attr(0755,sddm,sddm) %{_localstatedir}/lib/%{name}
