# zoom-eopkg

[Solus](https://getsol.us) packaging of Zoom video conferencing app

Accomplished by re-packaging the Ubuntu `.deb` release

## Building yourself

### Requirements

You've set up a Solus packaging directory according to this document:
https://getsol.us/articles/packaging/building-a-package/en/

Assuming `$SOLUS_PKG_DIR` points to your packaging directory with `common`
already cloned:

```
$ git clone https://github.com/yacn/zoom-eopkg.git "$SOLUS_PKG_DIR/zoom"
$ cd "$SOLUS_PKG_DIR"
$ echo "include ../Makefile.common" > Makefile
$ make
$ ls *.eopkg
```
