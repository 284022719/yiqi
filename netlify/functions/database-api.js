const { spawn } = require('child_process');
const path = require('path');

exports.handler = async (event, context) => {
    // 设置CORS头
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // 处理预检请求
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers,
            body: ''
        };
    }

    try {
        const { action, ...params } = event.queryStringParameters || {};
        
        if (!action) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({
                    success: false,
                    error: '缺少action参数'
                })
            };
        }

        // 调用Python脚本处理数据库请求
        const result = await callPythonAPI(action, params);
        
        return {
            statusCode: 200,
            headers,
            body: JSON.stringify(result)
        };
        
    } catch (error) {
        console.error('数据库API错误:', error);
        
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({
                success: false,
                error: '服务器内部错误',
                details: error.message
            })
        };
    }
};

async function callPythonAPI(action, params) {
    return new Promise((resolve, reject) => {
        const pythonScript = path.join(__dirname, '../../src/database/api.py');
        
        // 构建参数
        const args = [pythonScript, action];
        
        // 添加其他参数
        Object.keys(params).forEach(key => {
            args.push(`--${key}`);
            args.push(params[key]);
        });
        
        const pythonProcess = spawn('python', args, {
            cwd: path.join(__dirname, '../..'),
            env: {
                ...process.env,
                PYTHONPATH: path.join(__dirname, '../..')
            }
        });
        
        let stdout = '';
        let stderr = '';
        
        pythonProcess.stdout.on('data', (data) => {
            stdout += data.toString();
        });
        
        pythonProcess.stderr.on('data', (data) => {
            stderr += data.toString();
        });
        
        pythonProcess.on('close', (code) => {
            if (code === 0) {
                try {
                    const result = JSON.parse(stdout);
                    resolve(result);
                } catch (error) {
                    reject(new Error(`解析Python输出失败: ${error.message}`));
                }
            } else {
                reject(new Error(`Python脚本执行失败 (代码: ${code}): ${stderr}`));
            }
        });
        
        pythonProcess.on('error', (error) => {
            reject(new Error(`启动Python进程失败: ${error.message}`));
        });
        
        // 设置超时
        setTimeout(() => {
            pythonProcess.kill();
            reject(new Error('Python脚本执行超时'));
        }, 30000); // 30秒超时
    });
} 