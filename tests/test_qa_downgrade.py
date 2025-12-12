from __future__ import annotations

import click


def test_no_downgrade_flag_is_silent(runner, monkeypatch):
    monkeypatch.delenv("CLICK_QA_DOWNGRADE_TO", raising=False)
    monkeypatch.delenv("CLICK_QA_DOWNGRADE_STRICT", raising=False)

    @click.command()
    def cli():
        click.echo("ok")

    result = runner.invoke(cli, prog_name="cli")

    assert result.exit_code == 0
    assert result.stdout == "ok\n"
    assert result.stderr == ""


def test_warns_with_requested_downgrade(runner, monkeypatch):
    monkeypatch.setattr(click.core, "_installed_click_version", lambda: "8.2.0")

    @click.command()
    def cli():
        click.echo("ok")

    result = runner.invoke(
        cli, env={"CLICK_QA_DOWNGRADE_TO": "7.0"}, prog_name="cli"
    )

    assert result.exit_code == 0
    assert result.stdout == "ok\n"
    assert (
        "Warning: QA requested downgrade to Click 7.0"
        " (command cli; running Click 8.2.0)\n"
        == result.stderr
    )


def test_warns_on_blank_requested_version(runner, monkeypatch):
    @click.command()
    def cli():
        click.echo("ok")

    result = runner.invoke(
        cli, env={"CLICK_QA_DOWNGRADE_TO": "   "}, prog_name="cli"
    )

    assert result.exit_code == 0
    assert result.stdout == "ok\n"
    assert (
        "Warning: QA downgrade requested via CLICK_QA_DOWNGRADE_TO but no target was"
        " provided.\n"
        == result.stderr
    )


def test_warns_on_non_numeric_target(runner, monkeypatch):
    monkeypatch.setattr(click.core, "_installed_click_version", lambda: "8.2.0")

    @click.command()
    def cli():
        click.echo("ok")

    result = runner.invoke(
        cli, env={"CLICK_QA_DOWNGRADE_TO": "next-release"}, prog_name="cli"
    )

    assert result.exit_code == 0
    assert result.stdout == "ok\n"
    assert "requested version is not numeric" in result.stderr
    assert "running Click 8.2.0" in result.stderr


def test_strict_mode_errors_and_stops_execution(runner, monkeypatch):
    monkeypatch.setattr(click.core, "_installed_click_version", lambda: "8.2.0")

    @click.command()
    def cli():
        click.echo("should not run")

    result = runner.invoke(
        cli,
        env={
            "CLICK_QA_DOWNGRADE_TO": "9.0",
            "CLICK_QA_DOWNGRADE_STRICT": "1",
        },
        prog_name="cli",
    )

    assert result.exit_code == 1
    assert "requested version is not lower than the installed version" in result.stderr
    assert result.stdout == ""
