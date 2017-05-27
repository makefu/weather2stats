{ pkgs ? import <nixpkgs> {} }:
with pkgs.python3Packages;
let
  inp = [
    python
    requests2
    docopt
    beautifulsoup4
    pytz
    docopt
    influxdb
  ];
in buildPythonPackage {
  name = "weather2stats";
  src = ./.;
  buildInputs = inp;
}
