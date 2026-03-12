# Kalaba

## Python / NLTK

The project uses NLTK. Required data (e.g. `wordnet`) is downloaded automatically on first `import pfmg`. To install it manually or in CI:

```bash
python -m nltk.downloader wordnet
```

## CUE

To install CUE: download the binary from <https://github.com/cue-lang/cue/releases/download/v0.6.0/cue_v0.6.0_linux_amd64.tar.gz>

This `sudo` command will place the binary in the command-line executables path:

```bash
sudo cp <download_location>/cue_v0.6.0_linux_amd64/cue /usr/local/bin
```

Test by typing `cue`: if the command is found, you are good to go.

test bis
