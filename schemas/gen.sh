#!/bin/bash

# 输入文件目录，输出文件目录
INPUT_DIR="${1:-json}"
OUTPUT_PY_DIR="${2:-out/python}"
OUTPUT_TS_DIR="${3:-out/typescript}"

# 检查输入目录是否存在
if [ ! -d "$INPUT_DIR" ]; then
  echo "Input directory not found: $INPUT_DIR"
  exit 1
fi

# 创建输出目录，如果它们不存在
mkdir -p "$OUTPUT_PY_DIR"
mkdir -p "$OUTPUT_TS_DIR"

# 检查是否安装了datamodel-codegen，如果没有则安装
if ! command -v datamodel-codegen &> /dev/null
then
    echo "datamodel-codegen could not be found, installing..."
    pip install datamodel-code-generator
fi

# 检查是否安装了json2ts，如果没有则安装
if ! command -v json2ts &> /dev/null
then
    echo "json2ts could not be found, installing..."
    npm install -g json-schema-to-typescript
fi

# 遍历输入目录中的所有 JSON 文件
for INPUT_FILE in "$INPUT_DIR"/*.json; do
  # 获取文件名（不带扩展名）
  FILENAME=$(basename -- "$INPUT_FILE")
  FILENAME="${FILENAME%.*}"

  # 生成 Python 代码
  datamodel-codegen --input "$INPUT_FILE" --output "$OUTPUT_PY_DIR/$FILENAME.py"

  # 生成 TypeScript 代码
  json2ts "$INPUT_FILE" > "$OUTPUT_TS_DIR/$FILENAME.ts"
done