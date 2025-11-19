# Perlin Noise 2D

Gera uma imagem em escala de cinza usando ruído de Perlin 2D implementado do zero em `main.py`. É um exemplo educativo simples: sem dependência de bibliotecas de ruído externas, apenas a lógica básica (fade, gradientes e interpolação).

## Características
- Implementação auto-contida (classe `Perlin2D`).
- Determinístico via parâmetro `seed`.
- Ajuste de tamanho (`width`, `height`) e frequência (`scale`).
- Saída em imagem PNG monocromática (`mode="L"`).
- Código curto e fácil de expandir (octaves, colorização, etc.).

## Requisitos
- Python 3.8+ (qualquer versão 3.x recente deve funcionar).
- Bibliotecas: `Pillow`, `numpy`.

Instalação das dependências:
```powershell
pip install pillow numpy
```
(Optional) Crie um `requirements.txt` futuro com:
```
Pillow
numpy
```

## Uso Rápido
Executando diretamente (gera `perlin_selfcontained.png`):
```powershell
python main.py
```

Uso programático em outro script:
```python
from main import generate_perlin_image

# parâmetros padrão (500x500, scale 0.01)
generate_perlin_image()

# textura mais detalhada
generate_perlin_image(scale=0.05, filename="perlin_detalhada.png")

# textura mais suave (padrões maiores)
generate_perlin_image(scale=0.005, filename="perlin_suave.png")

# seed diferente (padrão visual alterado)
generate_perlin_image(seed=123, filename="perlin_seed123.png")

# tamanho customizado
generate_perlin_image(width=1024, height=256, scale=0.02, filename="perlin_banner.png")
```

## Parâmetros
| Parâmetro | Default | Descrição |
|-----------|---------|-----------|
| `width` | 500 | Largura da imagem; aumenta custo O(width*height). |
| `height` | 500 | Altura; idem custo. |
| `scale` | 0.01 | Frequência do ruído. Valores menores: padrões grandes; maiores: detalhes finos. |
| `seed` | `None` | Define embaralhamento determinístico da permutação; controla padrão. |
| `filename` | `perlin.png` | Nome do arquivo de saída PNG. |

## Como o Algoritmo Funciona
1. **Tabela de Permutação**: Cria lista 0..255 embaralhada e duplica (`p + p`) para facilitar indexação circular.
2. **Coordenadas**: Para cada ponto `(x,y)` normalizado por `scale`, obtém parte inteira (`xi, yi`) e fracionária (`xf, yf`).
3. **Fade Function**: Aplica `fade(t) = 6t^5 - 15t^4 + 10t^3` em `xf` e `yf` gerando `u` e `v` para suavizar transições (continuidade C2).
4. **Gradientes**: Usa apenas 4 direções derivadas de `hash & 3` para obter contribuições locais (produto escalar simplificado).
5. **Interpolação**: Interpola linearmente duas vezes (`lerp`): primeiro horizontal (x1, x2), depois vertical para valor final (~[-1,1]).
6. **Mapeamento**: Converte para [0,1] com `(value + 1) * 0.5` e escala a 0–255.

> Simplificações: apenas 4 gradientes (em implementações clássicas podem ser 8 ou 12); não há múltiplas oitavas (fractal Perlin / fBm); não é tileable.

## Exemplos Visuais (sugestões)
- `scale=0.005`: manchas largas e suaves.
- `scale=0.02`: textura média.
- `scale=0.05`: textura mais "granulada".
- Seeds diferentes (`42`, `123`, `999`) mudam a distribuição dos padrões.

Para gerar várias imagens variando seed:
```python
for s in [1, 2, 3, 4, 5]:
    generate_perlin_image(seed=s, filename=f"perlin_seed_{s}.png")
```

## Performance e Limitações
- Complexidade O(width * height); para imagens muito grandes o tempo cresce linearmente.
- Sem suporte a octaves (não há detalhe fractal em múltiplas escalas).
- Não tileable (bordas não casam).
- Apenas grayscale simples.
- Uso de Python puro em loops; para grandes tamanhos poderia otimizar com vetorização parcial ou Numba.


## Contribuindo
Sinta-se livre para abrir issues e enviar pull requests com melhorias, refatorações ou novos exemplos.

Passos sugeridos:
1. Fork do repositório.
2. Criar branch de feature (`feature/octaves`).
3. Implementar e testar.
4. Abrir Pull Request descrevendo mudanças.


## Referências
- https://rtouti.github.io/graphics/perlin-noise-algorithm
- Documentação Pillow: https://pillow.readthedocs.io/
- Numpy: https://numpy.org/
