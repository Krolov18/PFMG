# Kalaba

## Python / NLTK

Le projet utilise NLTK. Les données nécessaires (ex. `wordnet`) sont téléchargées automatiquement au premier `import pfmg`. Pour les installer à la main ou en CI :

```bash
python -m nltk.downloader wordnet
```

## CUE

Pour installer CUE : télécharger le binaire ici : <https://github.com/cue-lang/cue/releases/download/v0.6.0/cue_v0.6.0_linux_amd64.tar.gz>

Cette instruction `sudo` placera le binaire dans les programmes exécutables en ligne de commande :

```bash
sudo cp <localisation_téléchargement>/cue_v0.6.0_linux_amd64/cue /usr/local/bin
```

Teste en tapant simplement `cue` : si la commande apparaît, c’est bon.
