# Supporting Multiple Versions

If you are a library maintainer, you may want to support multiple versions of
Click. See the Pallets [version policy] for information about our version
numbers and support policy.

[version policy]: https://palletsprojects.com/versions

Most features of Click are stable across releases, and don't require special
handling. However, feature releases may deprecate and change APIs. Occasionally,
a change will require special handling.

## QA Downgrade Requests

Quality assurance runs can request that a CLI be tested against an older Click
release without changing dependencies. Set the ``CLICK_QA_DOWNGRADE_TO``
environment variable to the target version to show a warning once per
invocation that includes the requested and running versions. Set
``CLICK_QA_DOWNGRADE_STRICT`` to a truthy value to turn the notice into an
error and abort early when the request can't be honored.

```console
$ CLICK_QA_DOWNGRADE_TO=7.0 my-cli --help
Warning: QA requested downgrade to Click 7.0 (command my-cli; running Click 8.3.1)
```

No notice is shown when the variables are unset, and non-numeric or blank
values are reported in the warning or error message.

## Use Feature Detection

Prefer using feature detection. Looking at the version can be tempting, but is
often more brittle or results in more complicated code. Try to use `if` or `try`
blocks to decide whether to use a new or old pattern.

If you do need to look at the version, use {func}`importlib.metadata.version`,
the standardized way to get versions for any installed Python package.

## Changes in 8.2

### `ParamType` methods require `ctx`

In 8.2, several methods of `ParamType` now have a `ctx: click.Context`
argument. Because this changes the signature of the methods from 8.1, it's not
obvious how to support both when subclassing or calling.

This example uses `ParamType.get_metavar`, and the same technique should be
applicable to other methods such as `get_missing_message`.

Update your methods overrides to take the new `ctx` argument. Use the
following decorator to wrap each method. In 8.1, it will get the context where
possible and pass it using the 8.2 signature.

```python
import functools
import typing as t
import click

F = t.TypeVar("F", bound=t.Callable[..., t.Any])

def add_ctx_arg(f: F) -> F:
    @functools.wraps(f)
    def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
        if "ctx" not in kwargs:
            kwargs["ctx"] = click.get_current_context(silent=True)

        return f(*args, **kwargs)

    return wrapper  # type: ignore[return-value]
```

Here's an example ``ParamType`` subclass which uses this:

```python
class CommaDelimitedString(click.ParamType):
    @add_ctx_arg
    def get_metavar(self, param: click.Parameter, ctx: click.Context | None) -> str:
        return "TEXT,TEXT,..."
```
