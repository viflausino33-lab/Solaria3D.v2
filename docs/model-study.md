# Solaria3D.v2 — Estudo das Tecnologias 2D → 3D

## Objetivo

Este documento registra o estudo das principais arquiteturas de reconstrução
3D a partir de imagens 2D antes da escolha da arquitetura definitiva do Solaria3D.v2.

Nenhum modelo listado neste documento é considerado obrigatório.

A finalidade desta etapa é compreender:

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
Isolar o objeto
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
```

A dificuldade principal é que uma imagem única não observa diretamente toda
a geometria do objeto.

Por isso, o Solaria estudará diferentes fontes de informação:

- RGB;
- máscara;
- depth;
- surface normals;
- múltiplas vistas;
- consistência entre vistas;
- reconstrução geométrica.

---

# 2. Famílias de solução

## 2.1 Depth monocular

Entrada:

```text
imagem RGB
```

Saída:

```text
mapa de profundidade
```

Tecnologias iniciais:

- Marigold;
- Depth Anything V2.

Perguntas:

1. O depth preserva a silhueta?
2. O depth preserva superfícies curvas?
3. Como se comporta nas bordas?
4. O resultado pode ser combinado com uma máscara?
5. O depth é suficiente para gerar uma geometria inicial?

---

## 2.2 Surface normals

Entrada:

```text
imagem RGB
```

Saída:

```text
orientação das superfícies
```

Tecnologias iniciais:

- Marigold Normals;
- outros modelos de surface normals.

Perguntas:

1. As normais ajudam a recuperar detalhes?
2. Elas complementam depth?
3. Elas melhoram a reconstrução de superfícies curvas?
4. Podem ser utilizadas em reconstrução multivista?

---

## 2.3 Geração multivista

Entrada:

```text
uma imagem
```

Saída:

```text
várias imagens do mesmo objeto
```

Tecnologia inicial:

- Zero123++.

Ideia:

```text
Imagem frontal
      ↓
modelo generativo
      ↓
frontal + laterais + traseira + outras vistas
```

Perguntas:

1. As vistas são consistentes?
2. O objeto mantém proporções?
3. O lado traseiro é plausível?
4. Detalhes mudam de uma vista para outra?
5. As vistas podem alimentar um reconstruidor?

---

## 2.4 RGB + Normals multivista

Entrada:

```text
uma imagem
```

Saída:

```text
RGB multivista
+
normais multivista
```

Tecnologia inicial:

- Wonder3D.

Ideia:

```text
imagem
  ↓
geração multivista
  ↓
RGB + normals
  ↓
reconstrução
```

Pergunta principal:

> A combinação de RGB, normais e múltiplas vistas fornece uma descrição
> geométrica melhor do que usar somente RGB?

---

## 2.5 Reconstrução 3D direta

Entrada:

```text
imagem única
```

Saída:

```text
representação 3D / mesh
```

Tecnologias de estudo:

- TripoSR;
- InstantMesh;
- Hunyuan3D.

Pergunta principal:

> Quando uma reconstrução direta é mais adequada do que um pipeline
> composto por vários modelos especializados?

---

## 2.6 Geometria visual

Entrada:

```text
uma ou mais imagens
```

Possíveis saídas:

```text
depth
câmeras
point maps
estrutura 3D
relações geométricas
```

Tecnologia de estudo:

- VGGT.

Pergunta principal:

> Podemos usar um modelo de entendimento geométrico como uma camada
> intermediária do Solaria?

---

# 3. Marigold

## Função

Estimativa de características densas da imagem.

## Informações de interesse

- depth;
- surface normals;
- intrinsic decomposition.

## Ideia arquitetural

O Marigold adapta modelos de difusão para tarefas de análise densa de imagens.

Para o Solaria, interessa principalmente investigar:

```text
RGB
 ↓
depth
```

e:

```text
RGB
 ↓
surface normals
```

## Perguntas

1. Como o modelo se comporta no objeto isolado?
2. O fundo ainda influencia o resultado?
3. Como são tratadas as bordas?
4. O depth é suficientemente estável para gerar geometria?
5. As normais acrescentam informação relevante?

## Experimento

```text
imagem original
      ↓
segmentação
      ↓
objeto isolado
      ↓
Marigold Depth
      +
Marigold Normals
```

---

# 4. Depth Anything V2

## Função

Estimativa monocular de profundidade.

## Ideia arquitetural

Modelo especializado em depth monocular, com diferentes tamanhos e
capacidades.

## Perguntas

1. Quanto detalhe geométrico é preservado?
2. Como o modelo funciona com fundo removido?
3. Como trata objetos finos?
4. Como trata superfícies curvas?
5. Qual a diferença visual para o Marigold?

## Experimento

```text
mesma imagem
   ├──> Marigold
   └──> Depth Anything V2
             ↓
        comparação
```

---

# 5. Zero123++

## Função

Geração de múltiplas vistas de um objeto a partir de uma imagem.

## Ideia central

Transformar a ausência de observação da parte traseira em um problema
de geração de novas observações.

```text
imagem
  ↓
Zero123++
  ↓
vista frontal
vista lateral
vista traseira
outras vistas
```

## Perguntas

1. A identidade do objeto é preservada?
2. A geometria mantém proporções?
3. O verso permanece coerente?
4. Pequenos detalhes são preservados?
5. As vistas compartilham uma geometria implícita consistente?

---

# 6. Wonder3D

## Função

Geração multivista de RGB e surface normals para reconstrução.

## Ideia central

Gerar:

```text
RGB multivista
+
normals multivista
```

para fornecer informações complementares à reconstrução.

## Perguntas

1. As normais são consistentes entre vistas?
2. A qualidade da máscara influencia a mesh?
3. Como o sistema representa superfícies ocultas?
4. Como ele trata detalhes pequenos?
5. O uso de normais reduz ambiguidades geométricas?

---

# 7. InstantMesh

## Função

Reconstrução de mesh a partir de imagem ou vistas esparsas.

## Ideia arquitetural

Utiliza conceitos de Large Reconstruction Models para recuperar uma
representação 3D rapidamente.

## Experimentos

Primeiro:

```text
imagem
  ↓
InstantMesh
  ↓
mesh
```

Depois:

```text
imagem
  ↓
Zero123++
  ↓
vistas
  ↓
InstantMesh
  ↓
mesh
```

Pergunta:

> A qualidade da multivista altera significativamente a qualidade da mesh?

---

# 8. TripoSR

## Função

Reconstrução 3D feed-forward a partir de uma imagem.

## Ideia

```text
imagem
  ↓
modelo de reconstrução
  ↓
representação 3D
  ↓
mesh
```

Perguntas:

1. Como trata a parte traseira?
2. Que tipo de detalhes consegue recuperar?
3. Quais artefatos aparecem?
4. Quanto tempo e memória são necessários?
5. Que partes do pipeline são internas ao modelo?

---

# 9. Hunyuan3D

## Função

Geração de assets 3D, incluindo geometria e aparência.

## Aspectos de interesse

- geração de forma;
- geração de textura;
- materiais PBR;
- separação entre forma e aparência.

## Perguntas

1. A geometria pode ser utilizada independentemente?
2. Como a textura é relacionada à mesh?
3. Podemos aproveitar apenas parte da arquitetura?
4. O conceito de shape separado de appearance é útil para o Solaria?

---

# 10. VGGT

## Função

Entendimento geométrico visual.

## Informações de interesse

- geometria;
- depth;
- câmeras;
- point maps;
- relações espaciais.

## Possível função no Solaria

```text
imagem
  ↓
entendimento geométrico
  ↓
Depth / câmera / estrutura
  ↓
outros módulos
```

Essa integração ainda não foi decidida.

---

# 11. Comparação conceitual

| Tecnologia | Entrada principal | Informação principal | Reconstrução direta |
|---|---|---|---|
| Marigold | 1 imagem | depth / normals | não |
| Depth Anything V2 | 1 imagem | depth | não |
| Zero123++ | 1 imagem | novas vistas | não |
| Wonder3D | 1 imagem | RGB + normals multivista | parcialmente |
| InstantMesh | imagem / vistas | geometria 3D | sim |
| TripoSR | 1 imagem | representação 3D | sim |
| Hunyuan3D | imagem | asset 3D | sim |
| VGGT | imagens | geometria visual | não como asset final |

---

# 12. Arquiteturas candidatas

## Candidato A — Depth

```text
Imagem
  ↓
Segmentação
  ↓
Depth
  ↓
Point Cloud
  ↓
Mesh
```

### Benefícios para estudo

- simples;
- modular;
- permite visualizar cada etapa.

### Limitação

A imagem única não observa diretamente a parte traseira.

---

## Candidato B — Multiview

```text
Imagem
  ↓
Segmentação
  ↓
Zero123++
  ↓
Multiview
  ↓
Reconstrução
  ↓
Mesh
```

### Benefício

Cria novas observações do objeto.

### Limitação

Erros nas vistas podem ser propagados para a reconstrução.

---

## Candidato C — Normals + Multiview

```text
Imagem
  ↓
Segmentação
  ↓
RGB multivista
+
Normals multivista
  ↓
Reconstrução
  ↓
Mesh
```

### Hipótese

As normais podem complementar informações que não aparecem claramente
nas imagens RGB.

---

## Candidato D — Pipeline híbrido

```text
                  Imagem
                     ↓
                Segmentação
                     ↓
               Objeto isolado
                     ↓
          ┌──────────┼──────────┐
          ↓          ↓          ↓
        Depth      Normals    Multiview
          │          │          │
          └──────────┼──────────┘
                     ↓
              Consistência 3D
                     ↓
               Reconstrução
                     ↓
                   Mesh
                     ↓
                 Textura
```

Esse é apenas um candidato de pesquisa.

A arquitetura final dependerá dos experimentos.

---

# 13. Avaliação dos experimentos

Cada modelo deve ser estudado separadamente.

## Geometria

Avaliar:

- silhueta;
- proporção;
- superfícies planas;
- superfícies curvas;
- detalhes;
- profundidade;
- parte traseira.

## Consistência

Avaliar:

- coerência entre vistas;
- escala;
- câmera;
- detalhes;
- identidade do objeto.

## Artefatos

Registrar:

- deformações;
- duplicações;
- buracos;
- superfícies impossíveis;
- fundo incorporado;
- detalhes inventados.

## Recursos

Registrar:

- GPU;
- VRAM;
- RAM;
- tempo;
- tamanho do modelo;
- complexidade de instalação.

---

# 14. Regra de decisão

Nenhum modelo será escolhido somente pela aparência de uma demonstração.

A avaliação será baseada em:

```text
qualidade
+
consistência
+
recursos
+
modularidade
+
controle
+
facilidade de integração
```

---

# 15. Ordem dos experimentos

```text
01 — Marigold Depth
02 — Depth Anything V2
03 — Marigold Normals
04 — Zero123++
05 — Wonder3D
06 — TripoSR
07 — InstantMesh
08 — Hunyuan3D
09 — VGGT
10 — combinações
11 — arquitetura final do Solaria
```

---

# 16. Regra do projeto

O Solaria não precisa reproduzir internamente um único projeto existente.

O objetivo é identificar componentes e ideias que possam trabalhar juntos.

A arquitetura deverá ser resultado dos experimentos.

```text
estudar
   ↓
testar
   ↓
medir
   ↓
comparar
   ↓
combinar
   ↓
implementar
```

---

# 17. Estado atual

Neste momento:

- nenhuma IA foi incorporada;
- nenhuma arquitetura final foi escolhida;
- nenhum modelo pesado foi instalado;
- o pipeline ainda é estrutural.

A próxima grande decisão só deverá ocorrer depois de estudar
como as principais famílias de solução funcionam internamente.

---

# 18. Próxima etapa

O primeiro estudo técnico detalhado será o Marigold.

A análise deverá cobrir:

1. entrada;
2. pré-processamento;
3. arquitetura;
4. inferência;
5. representação do depth;
6. representação das normais;
7. limitações;
8. integração possível com o Solaria.

Nenhum código de integração será criado antes desse estudo.