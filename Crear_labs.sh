#!/bin/bash

# Script para crear carpetas de Laboratorio
# Estructura estándar para la materia
# Organización y Arquitectura de Computadoras

# Lista de laboratorios a crear
LABS=("00" "01" "02" "03" "04" "05" "06" "07" "08" "09")

BASE_DIR="2_Laboratorio"

for i in "${LABS[@]}"; do
  LAB_NAME="L${i}_Tema"
  mkdir -p ${BASE_DIR}/${LAB_NAME}/{docs,src,out,bin}
  touch ${BASE_DIR}/${LAB_NAME}/README.md
  echo "Estructura creada para ${LAB_NAME}"
done

echo "Laboratorios creados correctamente."
