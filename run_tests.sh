#!/bin/bash
# Скрипт для тестирования всех параметров командной строки
echo "=== Тестирование эмулятора ==="

# Создаем тестовые VFS директории
mkdir -p test_vfs1 test_vfs2

echo "1. Тест с VFS и скриптом:"
python main.py --vfs test_vfs1 --script test_success.sh

echo ""
echo "2. Тест с ошибкой в скрипте:"
python main.py --vfs test_vfs2 --script test_error.sh

echo ""
echo "3. Тест только с VFS (интерактивный режим):"
echo "Запустите: python main.py --vfs test_vfs1"
echo "И введите команды вручную"

# Очистка
rm -rf test_vfs1 test_vfs2 