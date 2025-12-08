// 如果安装依赖使用的包管理工具不是 pnpm，则在终端控制台中打印警告，然后退出本次执行的命令
if (!/pnpm/.test(process.env.npm_execpath || '')) {
    console.warn(
        `\u001b[33mThis repository must using pnpm as the package manager ` +
        ` for scripts to work properly.\u001b[39m\n`,
    )
    process.exit(1)
}
