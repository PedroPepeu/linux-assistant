pkgname=gemini-linux-assistant
pkgver=1.0.0
pkgrel=1
pkgdesc="Native Gemini-powered voice assistant for Arch/Hyprland"
arch=('any')
depends=('python-google-genai' 'python-pyaudio' 'python-openwakeword' 'pipewire-audio')

source=('git+https://github.com/youruser/linux-assistant.git')
sha256sums=('SKIP')

build() {
  cd "$srcdir/linux-assistant"
  python -m build --wheel --no-isolation
}

package() {
  cd "$srcdir/linux-assistant"
  python -m installer --destdir="$pkgdir" dist/*.whl
  
  # Install the systemd service to the correct user location
  install -Dm644 linux-assistant.service "$pkgdir/usr/lib/systemd/user/gemini-assistant.service"
}