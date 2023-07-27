_name="auc"
pkgname="auc"
pkgver=1.1.0
pkgrel=1
pkgdesc="A tool for checking for pacman based  distro updates. It's probably really bad."
arch=('x86_64')
url="https://github.com/lucyhancock3533/ArchUpdateChecker"
depends=('python-requests' 'python-yaml' 'python-ping' 'python-requests-unixsocket' 'python-urllib3')
makedepends=('python-poetry-core' 'python-build' 'python-installer' 'python-wheel')
source=("auc::git+https://github.com/lucyhancock3533/ArchUpdateChecker.git#tag=v1.1.0")
sha256sums=('SKIP')

build() {
  cd auc

  python -m build --wheel --no-isolation
}

package() {
  cd auc

  python -m installer --destdir="$pkgdir" dist/*.whl
}
