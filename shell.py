"""
    name: shell
    once: false
    origin: tgpy://module/shell
    priority: 1677332636.668527
    save_locals: true
"""
import asyncio
import os

async def shell(code):
    proc = await asyncio.create_subprocess_exec(
        os.getenv("SHELL") or "/bin/sh", "-c", code,
        stdout=asyncio.subprocess.PIPE, 
        stderr=asyncio.subprocess.STDOUT
    )

    stdout, _ = await proc.communicate()

    return stdout.decode() + (f"\n\nReturn code: {proc.returncode}" if proc.returncode != 0 else "")


def sh_trans(cmd):
    if cmd.lower().startswith(".sh "):
        return f"await shell({repr(cmd[4:])})"
    return cmd


tgpy.add_code_transformer("shell", sh_trans)
