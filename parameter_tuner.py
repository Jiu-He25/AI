class ParameterTuner:
    def __init__(self, llm_service):
        self.llm_service = llm_service
        self.experiment_cases = [
            {"prompt": "设计一个环保主题的儿童绘本故事大纲", "params": {"temperature": 0.5, "top_p": 0.9}},
            {"prompt": "同上，要求故事包含会说话的动物角色", "params": {"temperature": 1.0, "top_p": 0.7}},
            {"prompt": "创作一段科幻风格的短篇对话，包含未来科技设定", "params": {"temperature": 1.2, "top_p": 0.5}}
        ]

    def run_tuning_experiment(self):
        """执行参数调优实验并生成对比报告"""
        results = []
        for case in self.experiment_cases:
            # 提取参数组合
            temp = case["params"]["temperature"]
            top_p = case["params"]["top_p"]
            prompt = case["prompt"]

            # 调用模型
            messages = [{"role": "user", "content": prompt}]
            response = self.llm_service.call_model(
                messages,
                temperature=temp,
                top_p=top_p,
                max_tokens=512
            )

            if response:
                results.append({
                    "prompt": prompt,
                    "parameters": {"temperature": temp, "top_p": top_p},
                    "output": response["choices"][0]["message"]["content"]
                })

        # 生成调优分析报告
        return self._generate_tuning_report(results)

    def recommend_parameters(self, prompt, params):
        """根据提示词和任务类型推荐参数"""
        # 简单示例：根据提示词长度和关键词判断任务类型
        if len(prompt) > 100 or "分析" in prompt or "解释" in prompt:
            # 逻辑类任务
            params["temperature"] = min(0.6, params.get("temperature", 0.7))
            params["top_p"] = max(0.9, params.get("top_p", 0.8))
        elif "创意" in prompt or "故事" in prompt or "设计" in prompt:
            # 创意类任务
            params["temperature"] = max(0.9, params.get("temperature", 0.7))
            params["top_p"] = min(0.8, params.get("top_p", 0.9))
        return params

    def _generate_tuning_report(self, results):
        """生成参数调优分析报告"""
        report = "### 参数调优实验报告\n\n"
        report += "#### 实验目的：分析temperature与top_p组合对输出的影响\n\n"

        for i, result in enumerate(results):
            report += f"#### 案例 {i + 1}\n"
            report += f"**提示词**：{result['prompt']}\n\n"
            report += f"**参数组合**：temperature={result['parameters']['temperature']}, top_p={result['parameters']['top_p']}\n\n"
            report += f"**输出结果**：\n```\n{result['output']}\n```\n\n"

        # 调优结论（以典型参数组合为例）
        report += "### 调优结论\n"
        report += "- **创意类任务**（如故事创作）：推荐temperature=1.0-1.2，top_p=0.6-0.8，平衡随机性与连贯性\n"
        report += "- **逻辑类任务**（如数据分析）：推荐temperature=0.3-0.6，top_p=0.9-1.0，提升结果确定性\n"
        report += "- **对话类任务**：推荐temperature=0.7-0.9，top_p=0.7-0.9，保持自然交互感\n"
        return report