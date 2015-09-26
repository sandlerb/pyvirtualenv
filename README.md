PyVirtualenv
======

**Note** [virtualenv-api][api_link] exists so you should probably use that
mature library, but I'd like to finish this anyhow

A python wrapper around [virtualenv][virtualenv_link] for programmatic use.
Useful for building a release in a fresh virtualenv.

[api_link]: https://github.com/sjkingo/virtualenv-api
[virtualenv_link]: https://virtualenv.pypa.io/en/latest/index.html

## Usage

Create a `Virtualenv` object and use it to run your commands:

```
ve = Virtualenv(virtualenv='great_venv')
ve.run('source script/bootstrap.sh')
ve.run('source script/release.sh')
ve.destroy()
```

If the virtualenv does not exist, it will be created.

If you don't specify a virtualenv in the constructor, the virtualenv will be
created in a temporary directory.  Be sure to `destroy()` it after use.

You can also supply your own runner if you're using `invoke` or some other
task runner, `ve = Virtualenv(runner=invoke.run)`.  If a runner is not
specified `os.system()` will be used.

Use it as a context manger:

```
TODO
```

## How it works

This just prepends each command with a virtualenv's activate script, but it
wraps it up all nice and tidy like.

Tested on:
- OS X Yosemite

## TODO

- [ ] Use an existing virtualenv
- [ ] Use as a context manager
- [ ] Test windows support (CMD, not powershell)

## Authors

* Brett Sandler

## License

MIT
