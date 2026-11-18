"""Verify release selection using real Git commits, including deleted paths."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CLASSIFIER = Path(__file__).with_name("changed-services.py").resolve()


class ChangedServicesTest(unittest.TestCase):
    def test_committed_paths_from_workbench_subdirectory(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            workbench = repo / "code/agent_workbench"
            workbench.mkdir(parents=True)

            def git(*args):
                subprocess.run([
                    "git", "-c", "user.name=CI test", "-c", "user.email=ci@localhost",
                    "-c", "commit.gpgsign=false", *args,
                ], cwd=repo, check=True, stdout=subprocess.DEVNULL)

            def write(path):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("sample\n", encoding="utf-8")

            def checkpoint(message, expected):
                git("add", "--all")
                git("commit", "--allow-empty", "-qm", message)
                result = subprocess.check_output(
                    [sys.executable, CLASSIFIER, "HEAD^", "HEAD"], cwd=workbench, text=True,
                )
                self.assertEqual(result.splitlines(), [expected], message)

            git("init", "-q")
            git("commit", "--allow-empty", "-qm", "base")
            checkpoint("empty diff", "none")

            write(repo / ".github/workflows/workbench-web.yml")
            write(workbench / "deploy/apply-release.sh")
            write(workbench / "web/README.md")
            checkpoint("only workflow, deploy and documentation", "none")

            asset = workbench / "web/public/nested/sample document.md"
            write(asset)
            checkpoint("public Markdown served by Nginx", "web")

            sample = repo / "code/stage6/engineering_docs_rag/sample_docs/quickstart.md"
            sample.parent.mkdir(parents=True)
            asset.rename(sample)
            checkpoint("rename from web asset to API sample", "both")

            sample.unlink()
            checkpoint("delete API sample", "api")
            write(repo / "code/stage8/incident_change_review_agent/test_incident_graph.py")
            checkpoint("API test", "api")

            write(workbench / "compose.yaml")
            checkpoint("shared runtime configuration", "both")
