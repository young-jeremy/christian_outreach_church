#!/bin/bash

echo "🔍 Running autoflake to remove unused imports & variables..."
autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r coc/

echo "🎨 Running autopep8 for better formatting..."
autopep8 --in-place --aggressive --aggressive -r coc/

echo "🛠 Running black for code consistency..."
black coc/

echo "🗑 Running vulture to detect dead code..."
vulture coc/
