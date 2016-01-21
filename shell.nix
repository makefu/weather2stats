{ pkgs ? import <nixpkgs> {} }:

pkgs.stdenv.mkDerivation rec {
  name = "cacpanel-env";
  version = "1";
  buildInputs = with pkgs.python3Packages; [
    python
    requests2
    docopt
    beautifulsoup4
    pytz
  ];
}
