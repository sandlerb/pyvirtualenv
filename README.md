PyVirtualenv
======

**Note** [virtualenv-api][api_link] exists so you should probably use that
more mature library, but I'd like to finish this anyhow

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

Use it as a context manger:

```
with Virtualenv() as ve:
    ve.run('python release.py')
```

If the virtualenv does not exist, it will be created.

If you don't specify a virtualenv in the constructor, the virtualenv will be
created in a temporary directory.  Be sure to `destroy()` it after use.

You can also supply your own runner if you're using `invoke` or some other
task runner, `ve = Virtualenv(runner=invoke.run)`.  If a runner is not
specified `os.system()` will be used.

## Limitations

Since the `run` method works by prepending the `command` parameter with a string
to activate the virtualenv, `command` must be a string as well.

## How it works

This just prepends each command with a virtualenv's activate script, but it
wraps it up all nice and tidy like.

Tested on:
- OS X Yosemite

## TODO

- [ ] Test windows support (CMD, not powershell)

## Authors

* Brett Sandler

## License

MIT
