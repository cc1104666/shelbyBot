 #!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import time
import json

class CloudflareSolver:
    def __init__(self, api_key: str):

        self.api_key = api_key
        self.base_url = "https://api.capmonster.cloud"
        
    def solve_turnstile(self, website_url: str, website_key: str, action: str = "submit") -> str:

        print(f"正在创建 CapMonster 任务...")
        
        # 创建任务
        task_data = {
            "clientKey": self.api_key,
            "task": {
                "type": "TurnstileTaskProxyless",
                "websiteURL": website_url,
                "websiteKey": website_key,
                "action": action
            }
        }
        
        try:
            # 发送创建任务请求
            response = requests.post(f"{self.base_url}/createTask", json=task_data)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("errorId") != 0:
                raise Exception(f"创建任务失败: {result.get('errorDescription', '未知错误')}")
            
            task_id = result["taskId"]
            print(f"任务创建成功，ID: {task_id}")
            
            # 等待任务完成
            print(f"正在等待验证结果...")
            token = self._wait_for_result(task_id)
            
            print(f"验证成功！")
            return token
            
        except Exception as e:
            raise Exception(f"解决 Turnstile 挑战失败: {str(e)}")
    
    def _wait_for_result(self, task_id: int, max_wait_time: int = 120) -> str:
        """
        等待任务结果
        
        Args:
            task_id: 任务ID
            max_wait_time: 最大等待时间（秒）
            
        Returns:
            token: 验证令牌
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            # 获取任务结果
            result_data = {
                "clientKey": self.api_key,
                "taskId": task_id
            }
            
            try:
                response = requests.post(f"{self.base_url}/getTaskResult", json=result_data)
                response.raise_for_status()
                
                result = response.json()
                
                if result.get("errorId") != 0:
                    raise Exception(f"获取任务结果失败: {result.get('errorDescription', '未知错误')}")
                
                status = result.get("status")
                
                if status == "ready":
                    # 任务完成，返回令牌
                    solution = result.get("solution", {})
                    token = solution.get("token")
                    
                    if not token:
                        raise Exception("未找到验证令牌")
                    
                    return token
                    
                elif status == "processing":
                    # 任务仍在处理中，等待后重试
                    time.sleep(3)
                    continue
                    
                else:
                    raise Exception(f"任务状态异常: {status}")
                    
            except Exception as e:
                print(f"获取任务结果时出错: {str(e)}")
                time.sleep(3)
                continue
        
        raise Exception(f"等待任务结果超时（{max_wait_time}秒）")
