#
# Conditional build:
%bcond_without	tests	# unit tests

%define 	module	blockdiag
Summary:	Blockdiag generate block-diagram image file from spec-text file
Summary(pl.UTF-8):	Generowanie obrazków diagramów blokowych z opisu tekstowego
Name:		python3-%{module}
Version:	2.0.1
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/blockdiag/
Source0:	https://files.pythonhosted.org/packages/source/b/blockdiag/%{module}-%{version}.tar.gz
# Source0-md5:	89898a6c32636ba2139502bfdb8eff12
URL:		http://blockdiag.com/en/blockdiag/index.html
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-ReportLab
BuildRequires:	python3-docutils
BuildRequires:	python3-funcparserlib
BuildRequires:	python3-nose
BuildRequires:	python3-nose_exclude
BuildRequires:	python3-pillow >= 3.0
BuildRequires:	python3-webcolors
%endif
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
Requires:	python3-modules >= 1:3.5
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

%build
%py3_build

%if %{with tests}
# disable tests requiring network: test_command.TestBlockdiagApp.test_app_cleans_up_images, test_generate_diagram.test_generate, test_generate_diagram.ghostscript_not_found_test
# test_setup_inline_svg_is_true_with_multibytes fails on utf-8 vs latin-1 inconsistency
PYTHONPATH=$(pwd)/src \
nosetests-%{py3_ver} src/blockdiag/tests -e 'test_app_cleans_up_images|test_generate|ghostscript_not_found_test|test_setup_inline_svg_is_true_with_multibytes'
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

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
%{py3_sitescriptdir}/blockdiag_sphinxhelper.py
%{py3_sitescriptdir}/__pycache__/blockdiag_sphinxhelper.cpython-*.py[co]
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_mandir}/man1/blockdiag.1*
%{_mandir}/man1/blockdiag-3.1*
