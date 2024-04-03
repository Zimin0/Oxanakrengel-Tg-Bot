#!/bin/bash

DIRECTORY="products_json"
CURRENT_TIME=$(date "+%Y-%m-%d %H:%M:%S")

if [ -d "$DIRECTORY" ]; then
    rm -rf "$DIRECTORY"/*
    echo "Директория $DIRECTORY очищена в $CURRENT_TIME"
else 
    echo "Директория $DIRECTORY не найдена."
fi
