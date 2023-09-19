#!/bin/bash

# 输入文件目录，输出文件目录
INPUT_DIR="./json"
#OUTPUT_PY_DIR="./out/python"
OUTPUT_PY_DIR="../app/schemas/gen"
#OUTPUT_TS_DIR="./out/typescript"
OUTPUT_TS_DIR="../../good-kids/assets/scripts/app/schemas"

# 检查输入目录是否存在
if [ ! -d "$INPUT_DIR" ]; then
  echo "Input directory not found: $INPUT_DIR"
  exit 1
fi

# 清空输出目录
rm -rf "$OUTPUT_PY_DIR"/*
rm -rf "$OUTPUT_TS_DIR"/*

# 创建输出目录，如果它们不存在
mkdir -p "$OUTPUT_PY_DIR"
mkdir -p "$OUTPUT_TS_DIR"

# 检查是否安装了datamodel-codegen，如果没有则安装
if ! command -v datamodel-codegen &> /dev/null; then
    read -p "datamodel-codegen could not be found, do you want to install it? (y/n) " RESP
    if [ "$RESP" != "y" ]; then
        echo "Exiting script."
        exit 1
    fi
    pip install datamodel-code-generator
fi

# 检查是否安装了json2ts，如果没有则安装
if ! command -v json2ts &> /dev/null; then
    read -p "json2ts could not be found, do you want to install it? (y/n) " RESP
    if [ "$RESP" != "y" ]; then
        echo "Exiting script."
        exit 1
    fi
    npm install -g json-schema-to-typescript
fi

# 遍历输入目录中的所有 JSON 文件
for INPUT_FILE in "$INPUT_DIR"/*.json; do

  echo processing: $INPUT_FILE

  # 获取文件名（不带扩展名）
  FILENAME=$(basename -- "$INPUT_FILE")
  FILENAME="${FILENAME%.*}"

  # 生成 Python 代码
  datamodel-codegen --input-file-type jsonschema --input "$INPUT_FILE" --output "$OUTPUT_PY_DIR/$FILENAME.py" --disable-timestamp
  # 添加 import 语句到 __init__.py 文件
  echo "from .$FILENAME import *" >> "$OUTPUT_PY_DIR/__init__.py"

  # 生成 TypeScript 代码
  json2ts "$INPUT_FILE" > "$OUTPUT_TS_DIR/$FILENAME.ts"
done

read -p "press any key to continue..."
