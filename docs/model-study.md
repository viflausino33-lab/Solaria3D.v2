# Solaria3D.v2 — Estudo das Tecnologias 2D → 3D

## Objetivo

Este documento registra o estudo das principais arquiteturas de reconstrução
3D a partir de imagens 2D antes da escolha da arquitetura definitiva do Solaria3D.v2.

Nenhum modelo listado neste documento é considerado obrigatório.

A função desta etapa é compreender:

- como cada sistema interpreta a imagem;
- como estima geometria;
- como trata partes não observadas;
- como utiliza múltiplas vistas;
- como representa a geometria;
- como produz a mesh;
- quais componentes podem ser combinados.

---

# 1. Problema central do Solaria

O problema que queremos resolver é:

```text
Uma imagem 2D
      ↓
Identificar o objeto
      ↓
Entender sua geometria
      ↓
Inferir partes não visíveis
      ↓
Construir uma representação 3D
      ↓
Gerar uma superfície
      ↓
Aplicar aparência
      ↓
Exportar modelo 3D