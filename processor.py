import re


class SecurityException(Exception):
    pass


class InputPreprocessor:
    def __init__(self, sensitive_words_file="sensitive_words.txt"):
        # 加载敏感词库（可从文件或数据库读取）
        self.sensitive_words = self._load_sensitive_words(sensitive_words_file)
        # 指令注入防护规则
        self.injection_rules = [
            r"^(system:|assistant:|user:)",  # 防止角色伪造
            r"eval\(|exec\(|import\s",  # 防止代码注入
            r"file:|cd\s|rm\s|mkdir\s"  # 防止系统命令注入
        ]

    def _load_sensitive_words(self, file_path):
        """加载敏感词库"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("敏感词库文件不存在，使用默认词库")
            return ["敏感词1", "敏感词2", "..."]  # 可替换为默认词库

    def filter_sensitive_words(self, text):
        """敏感词过滤（支持正则替换）"""
        for word in self.sensitive_words:
            text = re.sub(word, "**" * len(word), text)
        return text

    def prevent_injection_attacks(self, text):
        """指令注入防护检测"""
        for pattern in self.injection_rules:
            if re.search(pattern, text, re.IGNORECASE):
                raise SecurityException("检测到潜在指令注入攻击")
        return text

    def preprocess_input(self, input_data):
        """完整输入预处理流程"""
        try:
            # 1. 敏感词过滤
            if "prompt" in input_data:
                input_data["prompt"] = self.filter_sensitive_words(input_data["prompt"])

            # 2. 指令注入检测
            if "prompt" in input_data:
                self.prevent_injection_attacks(input_data["prompt"])

            # 3. 格式标准化（如统一大小写、去除多余空格）
            if "prompt" in input_data:
                input_data["prompt"] = re.sub(r"\s+", " ", input_data["prompt"]).strip()

            return input_data
        except SecurityException as se:
            raise se
        except Exception as e:
            raise Exception(f"输入预处理失败: {str(e)}")