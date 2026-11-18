# 发布工作台

分支推送和拉取请求会运行 Workbench CI and CD。GitHub 的 Linux 机器构建前后端镜像，在 API 镜像里运行工作台及故障诊断的 pytest，再通过 Nginx 请求 `/studio`、该页面使用的 JavaScript 和 `/api/health`。这些检查使用教学数据，无需模型密钥。

## 首次连接已有的云端工作台

云端需要一套已经手动跑通的离线发布版，包含 `compose.yaml`、镜像名 `ai-workbench-web` 和 `ai-workbench-api`，以及 Web 的本机端口。脚本读取现有端口、沿用现有数据卷和公网入口。云端登录用户需要能写该发布目录，并能执行以下检查。

```bash
sudo -n docker compose version
sudo -n docker ps
command -v python3 flock
```

在 GitHub 仓库的 **Settings → Environments** 创建 `production`，将部署分支限制为 `main`。配置以下环境变量和机密。

| 类型 | 名称 | 值 |
|---|---|---|
| Variable | `WORKBENCH_HOST` | 能从 GitHub 托管运行器通过 SSH 连接的服务器主机名或 IP |
| Variable | `WORKBENCH_USER` | 已验证可以执行上面命令的 SSH 用户 |
| Variable | `WORKBENCH_RELEASE_DIR` | 该用户主目录下已有的发布文件夹名称 |
| Secret | `WORKBENCH_SSH_KEY` | 专为部署生成的 SSH 私钥全文，对应公钥加入云端用户的 `~/.ssh/authorized_keys` |
| Secret | `WORKBENCH_KNOWN_HOSTS` | 含主机地址、密钥类型及完整公钥的 OpenSSH 主机记录 |

在可信的云控制台终端运行 `cat /etc/ssh/ssh_host_ed25519_key.pub` 获取服务器公钥，以 `主机地址 ssh-ed25519 AAAA…` 格式填写主机记录。私钥通过 GitHub 的环境 Secret 表单或 `gh secret set --env production` 的标准输入设置。此部署密钥可操作云端 Docker，只授予受信任的发布人员修改工作流和部署环境的权限。

## 运行一次发布

1. 将审核通过的工作流与应用合并到默认分支 `main`。
2. 打开 **Actions → Workbench CI and CD → Run workflow**。选择 `main` 并勾选部署。只做 CI 时保持该选项关闭。
3. 检查通过后，工作流把同一次运行的两份镜像标记为 `git-<完整提交 SHA>`，压缩并交给部署任务。部署任务校验文件、通过 SSH 导入镜像，然后在已有目录更新 Compose 并检查页面、JS 和两个后端模块。
4. 如果切换后检查失败，部署脚本恢复上一版 Compose 和镜像并重新检查。云端保留 `compose.previous.yaml`。回退针对应用镜像和 Compose 配置，涉及持久化数据的格式变更需要另行安排兼容迁移。

首次手动发布成功后，如果希望每次相关改动进入 `main` 都自动发布，在仓库的 **Settings → Secrets and variables → Actions → Variables** 设置仓库变量 `WORKBENCH_AUTO_DEPLOY=true`。将它改回 `false` 可恢复手动触发发布。入口工作流运行在 GitHub 托管机器上，云主机继续只运行项目容器。
