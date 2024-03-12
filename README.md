# Warp Cloner

原项目地址：https://github.com/totoroterror/warp-cloner

该Python脚本，可以克隆大量的 [Warp Plus](https://1.1.1.1/) 密钥。

使用此脚本，您将能够克隆更多的12-24 PB密钥。

还能生成 WireGuard 配置文件的信息。

## 安装和使用方法

1. 克隆此存储库

2. 安装 [Python 3.11](https://www.python.org/downloads/) 或更高版本的

3. 使用以下命令安装依赖项 `pip install -r requirements.txt`

4. 将 `.env.example` 文件，并改名为 `.env` ，选择性添加自己的12-24 PB密钥到BASE_KEYS=[""]中

5. 执行 `python -u src/main.py`命令，生成更多的12-24 PB密钥（在控制台中等待结果）

   或运行 `第1步：run.bat`文件，生成的结果默认输出到`output.txt`文件中

6. 运行 `第2步：Run_Build_WireGuard.bat` 文件（将`output.txt`中的秘钥和其他信息，构建 WireGuard 配置信息），生成的`cloudflare warp+ 的配置文件.md`文件就是你需要的配置文件信息。

# 环境变量(`.env.example`文件)

- `BASE_KEYS` (非必需)-要克隆的许可密钥，用逗号分隔，如果没有，则使用默认key(脚本可能无法使用默认key)
- `THREADS_COUNT` (默认: `1`) - 线程数量
- `DEVICE_MODELS` (非必需的) - 自定义设备型号名称，以逗号分隔
- `SAVE_WIREGUARD_VARIABLES` (默认: false) - 脚本可以获取生成 WireGuard 配置所需的变量吗 ?(peer ips, private / public key, endpoint)
- `PROXY_FILE` (非必需的) - 代理文件的路径，如果没有，则脚本将以无代理模式启动
- `DELAY` (默认: `25`) - 密钥克隆后多少秒休眠一下，默认即可
- `OUTPUT_FILE` (默认: `output.txt`) - 在output.txt文件后面追加，程序新生成的密钥和其它信息
- `OUTPUT_FORMAT` (默认: `{key} | {referral_count}`) - 输出格式 (如果 `SAVE_WIREGUARD_VARIABLES` 设置为 `true`, 其他可用的变量: `{private_key}`, `{peer_endpoint}`, `{peer_public_key}`, `{interface_addresses}`)
- `RETRY_COUNT` (默认: 3) - 应用程序将使用相同的密钥重试生成多少次。
