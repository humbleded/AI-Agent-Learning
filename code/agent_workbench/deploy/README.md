# 发布工作台

工作台由两个可以分别发布的容器组成。`web` 运行 Nginx 并提供 Vue 页面，`api` 运行 FastAPI。GitHub Actions 根据文件改动选择要构建的镜像，测试使用教学数据。

## 首次连接已有的云端工作台

云端需要一套已经手动跑通的离线发布版，包含 `compose.yaml`、镜像名 `ai-workbench-web` 和 `ai-workbench-api`，以及 Web 的本机端口。脚本读取现有端口、沿用现有数据卷和公网入口。云端登录用户需要能写该发布目录，并能执行以下检查。

```bash
sudo -n docker compose version
sudo -n docker ps
command -v python3 flock curl sha256sum
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

## 如何判断本次发布范围

| 本次改动 | GitHub 构建、检查和上传的镜像 | 云端更新 |
|---|---|---|
| Vue 源码、public 下的静态文件、前端依赖或容器内的 Nginx 配置 | web | 只更新 web |
| FastAPI、镜像中的 RAG 或故障评审代码、后端依赖、教学样本或对应测试 | api | 只更新 api |
| 前后端都改了，或修改了项目的 compose.yaml | web 和 api | 更新两个服务 |
| 只改发布脚本、流水线或普通说明 | 跳过镜像构建和上传，仍检查发布脚本和范围判断 | 跳过更新 |

PR 按分支相对合并起点的全部改动判断。普通分支推送按本次推送包含的改动判断。正式发布选 auto 时，从运行中容器的镜像标签读出每个服务各自的 Git 提交，与待发布版本比较。上次发布失败或跳过后，待发布改动仍会计入。首次接入的离线镜像缺少 Git 标签，以启用此策略前的 main 提交 `9765d20` 为累计比较起点；需要对齐更早的版本时，可手动选择对应服务。

前端单独构建时，CI 检查 /studio 和页面真正引用的 JS。后端单独构建时，在 API 镜像里运行 pytest 和 /api/health。两侧都构建时，会通过 Nginx 检查页面、JS 和后端。发布后，无论范围大小，都会通过云端 Nginx 复查这三项。Compose 只重新创建所选服务。

## 运行一次发布

1. 把通过检查的 PR 合并到 main。打开 **Actions → Workbench CI and CD → Run workflow**，选择 main、勾选 deploy，范围选 auto。只验 CI 时，取消 deploy。
2. 在 **Select services** 查看范围。需要重发指定服务时，手动选 web、api 或 both。此选项会强制构建指定范围，即使源文件相同。
3. GitHub 给选中并通过检查的镜像打上 `git-<完整提交 SHA>` 标签。腾讯云用临时 HTTPS 地址下载同一次运行上传的包，中断时可从已下载的位置继续。云端校验包的大小和两层 SHA-256 后，从磁盘导入镜像，再通过现有 Compose 切换服务。
4. 云端检查失败时，脚本恢复本次选中服务的旧镜像，再检查工作台。数据卷和公网端口沿用已有配置。涉及持久化数据格式的变更，仍需单独设计兼容迁移。

要在合并后自动发布，将仓库变量 `WORKBENCH_AUTO_DEPLOY` 设为 true（**Settings → Secrets and variables → Actions → Variables**）。将它设为 false 可恢复手动发布。PR 和普通分支运行验证；生产机密只在受保护的 main 发布中使用。
