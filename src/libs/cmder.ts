import util from 'util';
import { exec } from 'child_process';
import { log } from '@/libs/logger'

const execPromise = util.promisify(exec);

async function runCommandInRenderer(command:any) {
    try {
      // 在渲染进程中执行命令并返回结果
      const { stdout, stderr } = await execPromise(command);
      log(stdout, stderr);
  
      // 在页面上展示结果
      const resultElement = document.getElementById('result');
      if(resultElement)
      resultElement.innerHTML = `<pre>${stdout}</pre>`;
  
    } catch (error:any) {
      console.error(error);
  
      //在页面上展示错误信息
      const resultElement = document.getElementById('result');
      if(resultElement)
      resultElement.innerHTML = `<pre>${error.message}</pre>`;
    }
  }
  
  // 调用示例
  //runCommandInRenderer('cd ~/github/fs');//
  //runCommandInRenderer('git status');
  //runCommand("ls")

  export async function runCommand(command:any) {
    const res: { code: number; result: string } = { code: 0, result: '' }
    try {
    // 在渲染进程中执行命令并返回结果
    const { stdout, stderr } = await execPromise(command);
    log(stdout, stderr);
    res.code = 0;
    res.result = stdout

  } catch (error:any) {
    console.error(error);
    res.code = 1;
    res.result = error.message
  }
  return res
}