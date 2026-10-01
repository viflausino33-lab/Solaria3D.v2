# Arquitetura do Solaria3D.v2

## Objetivo

Construir e estudar um pipeline modular de reconstrução de objetos 3D
a partir de uma imagem 2D.

A arquitetura permite substituir modelos de IA sem reescrever o sistema inteiro.

## Pipeline conceitual

```text
Imagem 2D
   |
   v
Segmentação
   |
   v
Objeto isolado
   |
   +----------> Depth
   |
   +----------> Normals
   |
   +----------> Multiview
                   |
                   v
             Reconstrução 3D
                   |
                   v
              Point Cloud
                   |
                   v
                  Mesh
                   |
                   v
                Textura
                   |
                   v
              Exportação 3D
```

## Princípio

Nenhum modelo específico foi escolhido definitivamente.

Modelos como Marigold, Depth Anything, Zero123++, Wonder3D,
TripoSR, InstantMesh e Hunyuan3D serão estudados e testados
antes da decisão da arquitetura final.

## Módulos

- `segmentation`: separação do objeto.
- `depth`: estimativa de profundidade.
- `normals`: orientação das superfícies.
- `multiview`: geração de vistas adicionais.
- `reconstruction`: reconstrução da geometria 3D.
- `pointcloud`: processamento de nuvens de pontos.
- `mesh`: processamento e exportação de malhas.
- `texture`: aparência e texturização.

## Regra de desenvolvimento

Cada módulo será implementado e testado isoladamente.

A integração acontecerá somente depois que cada componente tiver sido validado.
