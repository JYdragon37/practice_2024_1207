{ pkgs }: {
  deps = [
    pkgs.zlib
    pkgs.tk
    pkgs.tcl
    pkgs.openjpeg
    pkgs.libxcrypt
    pkgs.libwebp
    pkgs.libtiff
    pkgs.libjpeg
    pkgs.libimagequant
    pkgs.lcms2
    pkgs.freetype
    pkgs.geckodriver
    pkgs.lsof
    pkgs.python39Full
    pkgs.nodejs
    pkgs.glibc
    pkgs.gobject-introspection
    pkgs.gtk3
    pkgs.nss
    pkgs.libdrm
    pkgs.python3
    pkgs.chromedriver
    pkgs.chromium
    pkgs.python39
  ];
  env = {
      PYTHONBIN = "${pkgs.python39}/bin/python3.9";
      DISPLAY = ":99";
      CHROME_BIN = "${pkgs.chromium}/bin/chromium";
      CHROMEDRIVER_PATH = "${pkgs.chromedriver}/bin/chromedriver";
  };
}
