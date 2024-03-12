# 从TXT文件中，读取WARP+秘钥相关的参数
def read_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        return lines


# 划分国内或国外IP
def update_rule_info(template):
    """
    注意：流量分流使用到 https://github.com/lmc999/auto-add-routes 中的文件
    """
    update_parameters = r'''PreUp = "C:\Program Files\WireGuard\bat\routes-up.bat"
PostUp = "C:\Program Files\WireGuard\bat\dns-up.bat"
PreDown = "C:\Program Files\WireGuard\bat\routes-down.bat"
PostDown = "C:\Program Files\WireGuard\bat\dns-down.bat"
[Peer]'''
    update_result = template.replace('DNS = 1.1.1.1', 'DNS = 127.0.0.1').replace('[Peer]', f'{update_parameters}')
    return update_result


if __name__ == '__main__':
    parameters = read_file('output.txt')
    # 1、拦截未经隧道的流量(不可以访问局域网保留的私有IP)，包括 127.0.0.1:54321 和 192.168.1.1 之类的私有IP都走代理(不能访问私有IP)
    template1 = """[Interface]
PrivateKey = {}
Address = {}
DNS = 1.1.1.1
MTU = 1280
[Peer]
PublicKey = {}
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = {}"""
    # 2、不拦截未经隧道的流量(可以访问局域网保留的私有IP)：可以访问 127.0.0.1:54321 或 192.168.1.1 之类的私有IP
    template2 = template1.replace("0.0.0.0/0, ::/0", "0.0.0.0/1, 128.0.0.0/1, ::/1, 8000::/1")
    # 3、流量分流：划分国内走直连，国外走代理
    template3 = update_rule_info(template=template2)
    if len(parameters) > 0:
        with open('cloudflare warp+ 的配置文件.md', mode='w', encoding="utf-8") as wf:
            for index, parameter in enumerate(parameters):
                sub_parameter = parameter.split(" | ")
                if len(sub_parameter) == 6:
                    warp_plus_key, referral_count, private_key, interface_addresses, peer_public_key, peer_endpoint = sub_parameter
                    ''' 大标题：一个秘钥一个标题 '''
                    wf.write(f"#### {str(index + 1).zfill(2)}、WARP+秘钥：{warp_plus_key}\t容量：{referral_count}GB\n")
                    """下面写入三种不同的配置文件"""
                    sub_titles = ["- 拦截未经隧道的流量(kill switch)(不可以访问局域网保留的私有IP)\n",
                                  "- 不拦截未经隧道的流量(kill switch)(可以访问局域网保留的私有IP)\n",
                                  "- 流量分流：划分国内走直连，国外走代理\n"]
                    templates_li = [template1, template2, template3]
                    for sub_title, new_template in list(zip(sub_titles, templates_li)):
                        wf.write(sub_title)
                        code_conf = new_template.format(private_key, interface_addresses, peer_public_key,
                                                        str(peer_endpoint).strip())
                        wf.write(f"```conf\n{code_conf}\n```")
                        wf.write("\n")
                    wf.write("需要用到的流量分流工具：https://github.com/lmc999/auto-add-routes\n")
                else:
                    print("读取的数据，数据不全(可能缺失)！")
