# labs/02_structured_output.py
# 对应第十章：结构化输出（API级JSON强约束演示）
# 目标：将“请输出 JSON”升级为“必须符合 JSON Schema”，构建机器可验闭环。

import json
from jsonschema import validate, ValidationError

def run_experiment():
    print("--- 提示工程：结构化输出的本地验证引擎 ---\n")
    
    # 1. 制定严格的数据契约 (JSON Schema)
    # 这相当于给数据的“大纲模板”，说明每个字段该长什么样
    schema = {
        "type": "object",
        "properties": {
            "person": {"type": "string"},
            "location": {"type": "string"},
            "time": {"type": "string"}
        },
        "required": ["person", "location", "time"], # 必须存在的字段
        "additionalProperties": False               # 不允许 AI 胡乱增加其它字段
    }

    print("契约 (Schema) 定义完毕。")

    # 2. 模拟大语言模型的输出 (正常情况)
    # 注意，在真实业务中应使用 openai 提供的 Structured Output 或 Function calling 功能
    ai_output_success = '{"person":"Sam Altman","location":"San Francisco","time":"2023-11-17"}'
    
    # 模拟大语言模型的输出 (产生幻觉或加入废话的情况)
    ai_output_failure = '{"person":"Sam Altman","location":"San Francisco","time":"2023-11-17","emotion":"Happy"}'
    
    # 3. 校验机制
    def verify_json(text):
        try:
            data = json.loads(text)
            validate(instance=data, schema=schema)
            print(f"✅ 校验通过：\n{json.dumps(data, indent=2, ensure_ascii=False)}")
            return True
        except json.JSONDecodeError:
            print("❌ 校验失败：输出不是合法的 JSON 格式。")
        except ValidationError as e:
            print(f"❌ 校验失败：与契约不符！({e.message})")
        return False
        
    print("\n--- 场景 A：AI 按照规矩输出 ---")
    verify_json(ai_output_success)
    
    print("\n--- 场景 B：AI '贴心'地加入了一个没要求的 emotion 字段 ---")
    verify_json(ai_output_failure)

if __name__ == "__main__":
    run_experiment()
