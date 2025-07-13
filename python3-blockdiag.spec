#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module	blockdiag
Summary:	Blockdiag generate block-diagram image file from spec-text file
Summary(pl.UTF-8):	Generowanie obrazków diagramów blokowych z opisu tekstowego
Name:		python3-%{module}
Version:	3.0.0
Release:	2
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/blockdiag/
Source0:	https://files.pythonhosted.org/packages/source/b/blockdiag/%{module}-%{version}.tar.gz
# Source0-md5:	e1bfc69b83254ad3565c572ff4b3ad97
# https://github.com/blockdiag/blockdiag/pull/175.patch
Patch0:		blockdiag-pytest.patch
# https://github.com/blockdiag/blockdiag/pull/179.patch
Patch1:		blockdiag-pillow10.patch
Patch2:		blockdiag-pillow10-setup.patch
URL:		http://blockdiag.com/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-docutils
BuildRequires:	python3-funcparserlib >= 1.0.0
BuildRequires:	python3-pillow >= 3.1.0
BuildRequires:	python3-pytest
BuildRequires:	python3-reportlab
BuildRequires:	python3-webcolors
%endif
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
blockdiag generates block-diagram image file from spec-text file.

Features:
- Generate block-diagram from dot like text (basic feature).
- Multilingualization for node-label (UTF-8 only).

%description -l pl.UTF-8
blockdiag generuje pliki obrazów diagramów blokowych z tekstowych
plików opisu.

Funkcje:
- generowanie diagramów z tekstu w stylu dot (podstawowa funkcja).
- obsługa wielu języków dla etykiet węzłów (tylko UTF-8).

%prep
%setup -q -n %{module}-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

# contains Pillow<10 dependency
%{__rm} -r src/blockdiag.egg-info

%build
# although project uses just setup.py, use PEP-517 build in order to get metadata for tests
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# disable tests requiring network:
#  test_command.py::TestBlockdiagApp::test_app_cleans_up_images
#  test_generate_diagram.py::test_generate_with_separate[.../diagrams/node_icon.diag-svg-options260]
PYTHONPATH=$(pwd)/build-3-test \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest src/blockdiag/tests -k 'not test_app_cleans_up_images and not test_generate_with_separate'
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/blockdiag/tests

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{blockdiag,blockdiag-3}
ln -s blockdiag-3 $RPM_BUILD_ROOT%{_bindir}/blockdiag
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p blockdiag.1 $RPM_BUILD_ROOT%{_mandir}/man1/blockdiag-3.1
echo '.so blockdiag-3.1' >$RPM_BUILD_ROOT%{_mandir}/man1/blockdiag.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%attr(755,root,root) %{_bindir}/blockdiag
%attr(755,root,root) %{_bindir}/blockdiag-3
%{py3_sitescriptdir}/blockdiag
%{py3_sitescriptdir}/blockdiag-%{version}.dist-info
%{_mandir}/man1/blockdiag.1*
%{_mandir}/man1/blockdiag-3.1*
