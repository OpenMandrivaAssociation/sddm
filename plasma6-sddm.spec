#define date 20231112

Name: plasma6-sddm
Summary: Lightweight display manager
Version: 0.21.0
%if 0%{?date:1}
Release: 0.%{date}.1
# Packaged from git for the time being -- no download URL available
# git archive --format=tar --prefix sddm-0.20.1-$(date +%Y%m%d)/ HEAD | xz -vf > sddm-0.20.1-$(date +%Y%m%d).tar.xz
Source0: https://github.com/sddm/sddm/archive/develop/sddm-%{version}-%{date}.tar.gz
%else
Release: 2
Source0: https://github.com/sddm/sddm/archive/refs/tags/v%{version}.tar.gz
%endif
URL: https://github.com/sddm
Group: Graphical desktop/KDE
License: GPLv2
Source1: sddm.conf
Source2: sddm.pam
Source3: sddm-autologin.pam
Source4: sddm-sysuser.conf
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

# For qml(QtQuick.VirtualKeyboard) -- provided by both lib64Qt6VirtualKeyboard
# and qt5-qtvirtualkeyboard (but obviously we need the qt6 version)
Requires: %mklibname Qt6VirtualKeyboard

# For /etc/X11/Xsession
Requires: xinitrc
%systemd_requires
Provides: dm
Conflicts: sddm

%patchlist
sddm-0.20.0-allow-setting-default-session.patch
sddm-0.20.0-default-rootless.patch
https://github.com/sddm/sddm/commit/fbffb577796c471e4fabf64f6422aa7bab4ea990.patch
https://github.com/sddm/sddm/commit/cda8d936c2c47a85fa95797431b51d1e39b5c022.patch
https://github.com/sddm/sddm/commit/a11f05fc1091fce6a91bcb92658708ae081bf643.patch
https://github.com/sddm/sddm/commit/abb9f9eea9ffb31506a89d5f5de1060bea076056.patch
https://github.com/sddm/sddm/commit/71b2171f0224805a9cbd4662c99eb13d0bcea95d.patch
https://github.com/sddm/sddm/commit/8d32f3261eaa1f63ab060a8f5e1b114ac9d79ac5.patch
https://github.com/sddm/sddm/commit/fa65020883d5de1bda576d702d185ed865176aa4.patch
https://github.com/sddm/sddm/commit/391baf22f53f8d2db6d87c2557eee2676cf1010f.patch
https://github.com/sddm/sddm/commit/82af2534211f39c158ecb75f467bc90a132c53bc.patch
https://github.com/sddm/sddm/commit/b5fd7ecedfa583985ce6faac3b434e2079d79430.patch
https://github.com/sddm/sddm/commit/cc03fabf2f3025842cee30b5f05d20f56b6a2270.patch
https://github.com/sddm/sddm/commit/b82f9be9cbd25e734958ad5eb3465579befcd0c0.patch
https://github.com/sddm/sddm/commit/d4afb9069ba9322b0f957dd8ec09702cbceee486.patch
https://github.com/sddm/sddm/commit/dadf4e0eaa2dcebbc83970af451309358dec25a0.patch
https://github.com/sddm/sddm/commit/5c7af4e5c02247962da528d2ff49c162706fcecb.patch
https://github.com/sddm/sddm/commit/b704e2ee358646ba14f8dc5c723676c5e80dc495.patch
https://github.com/sddm/sddm/commit/d89a1f2dbc507ea6a1b267cdb8f63aa48e821b4f.patch
https://github.com/sddm/sddm/commit/07fe2c290f4348fe11474c7be890e9e34a653636.patch
https://github.com/sddm/sddm/commit/b6b6c7c391c1a8fc584c4bd4f379d6748fc93100.patch
https://github.com/sddm/sddm/commit/942e173cc29bfcfec74ad24cff997f76aaaf8f53.patch
https://github.com/sddm/sddm/commit/b96d323f79cb50f4189db71c11d56754ee2c8471.patch
https://github.com/sddm/sddm/commit/352878a7f99d7c429b768f5bac4aba87211d94ee.patch
https://github.com/sddm/sddm/commit/7b3fd9c798c9ddd004babbfe0d1f2e5bfe42907d.patch
https://github.com/sddm/sddm/commit/50e41247997e95d41c2daebec85f09e19b01b992.patch
https://github.com/sddm/sddm/commit/7baf8420d26ee9e0ee8a91a32f4ef188dcb18afd.patch
https://github.com/sddm/sddm/commit/4a9aa2e00399cb185701e4bb2b177ef96983d93b.patch
https://github.com/sddm/sddm/commit/9e6a9c12074a7b5c4db31aa409ded2c7ef436892.patch
https://github.com/sddm/sddm/commit/76454b651d4694da756a814cb4bae11714ae3a6d.patch
https://github.com/sddm/sddm/commit/57f3258329ca704212243d0f9443e568e49aa3a7.patch
https://github.com/sddm/sddm/commit/2d27436bab48eb49e4607ab073ab7ad1a98b9350.patch
https://github.com/sddm/sddm/commit/5aa1df94894ab1561a1cee6c47d3c30b84c86a69.patch
https://github.com/sddm/sddm/commit/f41193f83b4fa30ef679cc05f0236e8f4bb91363.patch
https://github.com/sddm/sddm/commit/c2b97dd63f726fa3db7f699bb40b2be3e62b8df5.patch
https://github.com/sddm/sddm/commit/17a333dff5c96df0386bfddc419279a28fc8df0e.patch
https://github.com/sddm/sddm/commit/d348eb892bebccce3bdae4aba80a6d512788b03f.patch
https://github.com/sddm/sddm/commit/c220e92147880697977a2f66005bb9e106ef0134.patch
https://github.com/sddm/sddm/commit/228778c2b4b7e26db1e1d69fe484ed75c5791c3a.patch
https://github.com/sddm/sddm/commit/e505a38c241677c3b3c8f4bdaf65249d452f05e3.patch
https://github.com/sddm/sddm/commit/9e51fa00c9329f2e9dd6faf0bf8cd86e10f210d3.patch
https://github.com/sddm/sddm/commit/42e88b70c3e558495d07d29d346664301da6e974.patch

%description
Lightweight display manager (login screen).

%prep
%if 0%{?date:1}
%autosetup -n sddm-develop -p1
%else
%autosetup -p1 -n sddm-%{version}
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

install -Dpcm 644 %{S:1} %{buildroot}%{_sysconfdir}/sddm.conf
install -Dpcm 644 %{S:2} %{buildroot}%{_sysconfdir}/pam.d/sddm
install -Dpcm 644 %{S:3} %{buildroot}%{_sysconfdir}/pam.d/sddm-autologin
install -Dpcm 644 %{S:4} %{buildroot}%{_sysusersdir}/sddm.conf

mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/sddm.conf.d
# use omv-background.png as sddm background for all themes
sed -i -e 's,\(^background=\).*,\1%{_datadir}/mdk/backgrounds/OpenMandriva-splash.png,' %{buildroot}%{_datadir}/sddm/themes/elarun/theme.conf
sed -i -e 's,\(^background=\).*,\1%{_datadir}/mdk/backgrounds/OpenMandriva-splash.png,' %{buildroot}%{_datadir}/sddm/themes/maldives/theme.conf

mkdir -p %{buildroot}%{_localstatedir}/lib/sddm

%pre
%sysusers_create_package %{name} %{S:4}

%post
%systemd_post sddm.service

%preun
%systemd_preun sddm.service

%postun
%systemd_postun sddm.service

%files
%{_bindir}/sddm
%{_bindir}/sddm-greeter-qt6
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
