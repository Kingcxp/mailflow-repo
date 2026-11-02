"""Validator tests use subprocess fakes; they install nothing."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "validate_plugin", Path(__file__).resolve().parents[1] / "tools/validate_plugin.py"
)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.root_patch = patch.object(validator, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def plugin(self, category: str = "llm_backend", name: str = "mailflow-fake") -> Path:
        folder = self.root / category / name
        folder.mkdir(parents=True)
        (folder / "plugin.json").write_text(
            json.dumps(
                {
                    "id": name,
                    "package": name,
                    "version": "0.1.0",
                    "categories": [category],
                    "source": "local",
                    "readme": "local fake",
                }
            ),
            encoding="utf-8",
        )
        (folder / "pyproject.toml").write_text(
            f'[project]\nname = "{name}"\nversion = "0.1.0"\n'
            'dependencies = ["mailflow-core", "missing-library"]\n'
            f'[project.entry-points."mailflow.plugins"]\n{name} = "fake.plugin:plugin"\n',
            encoding="utf-8",
        )
        return folder

    def test_nested_source_and_deleted_file_changes_select_plugin(self) -> None:
        folder = self.plugin()
        output = f"llm_backend/{folder.name}/src/fake/plugin.py\n"
        with patch.object(
            validator.subprocess,
            "run",
            side_effect=[
                subprocess.CompletedProcess([], 0, output, ""),
                subprocess.CompletedProcess([], 0, "", ""),
                subprocess.CompletedProcess([], 0, "", ""),
            ],
        ):
            self.assertEqual(validator.changed_folders("origin/develop"), [folder])

    def test_url_dependency_requires_build_backend_support(self) -> None:
        folder = self.plugin()
        project = folder / "pyproject.toml"
        text = project.read_text(encoding="utf-8").replace(
            '"missing-library"', '"shared-backend @ git+https://example.invalid/backend.git"'
        )
        text += '\n[build-system]\nrequires = ["hatchling"]\nbuild-backend = "hatchling.build"\n'
        project.write_text(text, encoding="utf-8")
        errors = validator._failures(folder)
        self.assertEqual(len(errors), 1)
        self.assertIn("allow-direct-references", errors[0])
        project.write_text(
            text + "\n[tool.hatch.metadata]\nallow-direct-references = true\n", encoding="utf-8"
        )
        self.assertEqual(validator._failures(folder), [])

    def test_shared_validator_change_selects_all_plugins(self) -> None:
        folders = [self.plugin(), self.plugin("notifier", "mailflow-notifier")]
        with patch.object(
            validator.subprocess,
            "run",
            return_value=subprocess.CompletedProcess([], 0, "tools/plugin_smoke.py\n", ""),
        ):
            self.assertEqual(set(validator.changed_folders()), set(folders))

    def test_installation_uses_disposable_interpreter_and_dependencies(self) -> None:
        folder = self.plugin()
        core = self.root / "workspace/packages/mailflow-core"
        with (
            patch.object(validator.venv.EnvBuilder, "create") as create,
            patch.object(
                validator.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 0, "", ""),
            ) as run,
            patch.object(validator, "_run", return_value=[]) as smoke,
        ):
            self.assertEqual(validator._install_and_run(folder, core=core), [])
            environment = create.call_args.args[0]
            for call in run.call_args_list:
                command = call.args[0]
                self.assertNotEqual(command[0], sys.executable)
                self.assertTrue(Path(command[0]).is_relative_to(environment))
                self.assertNotIn("--no-deps", command)
            install = run.call_args_list[0].args[0]
            self.assertEqual(
                install[-3:], [str(core), str(core.parent / "mailflow-testkit"), str(folder)]
            )
            smoke.assert_called_once()
            self.assertFalse(environment.exists())

    def test_dependency_failure_stops_before_runtime_check(self) -> None:
        folder = self.plugin()
        with (
            patch.object(validator.venv.EnvBuilder, "create"),
            patch.object(
                validator.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 1, "", "missing-library"),
            ),
            patch.object(validator, "_run") as smoke,
        ):
            errors = validator._install_and_run(folder)
            self.assertIn("missing-library", errors[0])
            smoke.assert_not_called()

    def test_offline_mode_runs_sources_without_installing(self) -> None:
        folder = self.plugin()
        core = self.root / "workspace/packages/mailflow-core"
        with (
            patch.object(validator.venv.EnvBuilder, "create") as create,
            patch.object(
                validator.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 0, "", ""),
            ) as run,
        ):
            self.assertEqual(validator._install_and_run(folder, offline=True, core=core), [])
            create.assert_not_called()
            command = run.call_args.args[0]
            self.assertEqual(command[0], sys.executable)
            self.assertIn("--source", command)
            self.assertNotIn("pip", command)
            self.assertIn(str(folder / "src"), run.call_args.kwargs["env"]["PYTHONPATH"])
            paths = run.call_args.kwargs["env"]["PYTHONPATH"]
            self.assertIn(str(core / "src"), paths)
            self.assertIn(str(core.parent / "mailflow-testkit/src"), paths)

    def test_metadata_checks_version_and_entry_point(self) -> None:
        folder = self.plugin()
        self.assertEqual(validator._failures(folder), [])
        project = folder / "pyproject.toml"
        project.write_text(
            project.read_text()
            .replace('version = "0.1.0"', 'version = "9.0"')
            .replace('mailflow-fake = "fake.plugin:plugin"', 'wrong = "fake.plugin:plugin"')
        )
        errors = " ".join(validator._failures(folder))
        self.assertIn("version", errors)
        self.assertIn("entry point", errors)

    def test_installed_check_cannot_import_host_sources(self) -> None:
        folder = self.plugin()
        with (
            patch.dict(validator.os.environ, {"PYTHONPATH": "host-sources"}),
            patch.object(
                validator.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "", "")
            ) as run,
        ):
            self.assertEqual(
                validator._run(Path(sys.executable), folder, offline=False, core=None), []
            )
            self.assertNotIn("PYTHONPATH", run.call_args.kwargs["env"])


if __name__ == "__main__":
    unittest.main()
