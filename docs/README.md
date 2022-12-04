## Building the Documents Locally with LaTeX
### Requirements
#### Ubuntu
```shell
sudo apt install texlive-full
# it's also enough to install only a subset of texlive-full (smaller in size):
sudo apt install texlive texlive-publishers texlive-science cm-super
```
#### Mac
``` shell
brew install texlive
# or 
brew install mactex
```

### Building the Project Summary
``` shell
# Go to the docs/project-summary folder
cd docs/project-summary

# Build docs/build/proposal.pdf + clean build files
make 
```

- For building without cleaning up: `make project-summary.pdf`
- Delete build files: `make clean`

The original project proposal can be built the same way from the `docs/proposal
folder`.
