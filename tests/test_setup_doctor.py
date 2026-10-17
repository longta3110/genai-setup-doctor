from pathlib import Path

import setup_doctor


def create_required_project_files(project_root: Path) -> None:
    for file_name in setup_doctor.REQUIRED_FILES:
        (project_root / file_name).write_text("test\n", encoding="utf-8")

    (project_root / ".gitignore").write_text(".env\n.venv/\n", encoding="utf-8")
    (project_root / ".git").mkdir()


def test_is_configured_rejects_empty_and_placeholder_values() -> None:
    assert not setup_doctor.is_configured(None)
    assert not setup_doctor.is_configured("")
    assert not setup_doctor.is_configured("replace_with_your_real_key")


def test_is_configured_accepts_a_non_placeholder_value() -> None:
    assert setup_doctor.is_configured("configured-for-local-testing")


def test_gitignore_rule_must_be_active(tmp_path: Path) -> None:
    (tmp_path / ".gitignore").write_text("# .env\n.venv/\n", encoding="utf-8")

    assert not setup_doctor.gitignore_has_rule(tmp_path, ".env")
    assert setup_doctor.gitignore_has_rule(tmp_path, ".venv/")


def test_collect_checks_can_report_a_ready_environment(
    tmp_path: Path, monkeypatch
) -> None:
    create_required_project_files(tmp_path)
    monkeypatch.setattr(setup_doctor, "package_is_installed", lambda _: True)
    monkeypatch.setattr(setup_doctor.sys, "prefix", "virtual-environment")
    monkeypatch.setattr(setup_doctor.sys, "base_prefix", "base-python")
    monkeypatch.setenv("OPENAI_API_KEY", "configured-for-local-testing")
    monkeypatch.setenv("OPENAI_MODEL", "configured-model")

    checks = setup_doctor.collect_checks(tmp_path)

    assert checks
    assert all(passed for _, passed in checks)


def test_print_report_returns_false_when_a_check_fails(capsys) -> None:
    ready = setup_doctor.print_report(
        [("First check", True), ("Second check", False)]
    )

    output = capsys.readouterr().out
    assert not ready
    assert "[PASS] First check" in output
    assert "[FAIL] Second check" in output
    assert "NOT READY" in output
