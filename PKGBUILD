_name="auc"
pkgname="auc"
pkgver=1.6.0
pkgrel=0
pkgdesc="A tool for checking for pacman based distro updates. It's probably really bad."
arch=('x86_64')
url="https://github.com/lucyhancock3533/ArchUpdateChecker"
depends=('python-requests' 'python-yaml' 'python-requests-unixsocket' 'python-urllib3')
makedepends=('python-poetry-core' 'python-build' 'python-installer' 'python-wheel')

build() {
  cd ..
  python -m build --wheel --no-isolation
}

package() {
  cd ..
  python -m installer --destdir="$pkgdir" dist/*.whl
}
