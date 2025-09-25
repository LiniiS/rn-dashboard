# 📱 Dashboard de Análise de Ideias de Aplicativos

Um dashboard interativo desenvolvido em Streamlit para analisar as ideias de aplicativos que alunos gostariam de desenvolver, com foco em recursos técnicos necessários, complexidade de desenvolvimento e implicações éticas/legais.

## 🎯 Objetivo

Este dashboard foi criado para visualizar e analisar dados de uma pesquisa sobre:
- Tipos de aplicativos que alunos desejam desenvolver
- Recursos React Native necessários para cada projeto
- Nível de complexidade de desenvolvimento
- Aplicativos semelhantes existentes no mercado
- Alertas éticos e legais importantes

## 🌟 Características

### ✨ Funcionalidades Principais
- **Visualizações Interativas**: Gráficos dinâmicos com Plotly
- **Filtros Avançados**: Filtragem por complexidade, recursos técnicos e alertas éticos
- **Análise por Categorias**: Classificação automática das ideias por tipo de aplicativo
- **Análise Técnica**: Correlação entre complexidade e recursos necessários
- **Análise Ética**: Identificação e detalhamento de implicações legais

### ♿ Acessibilidade
- **WCAG 2.2 AAA**: Cores e contrastes seguem padrões de acessibilidade
- **Navegação por Teclado**: Interface totalmente navegável por teclado
- **Texto Alternativo**: Descrições adequadas para leitores de tela
- **Foco Visível**: Indicadores claros de foco nos elementos interativos

## 🏗️ Estrutura do Projeto

```
rn-dashboard/
├── streamlit_app.py              # Dashboard principal
├── requirements.txt              # Dependências do projeto
├── ideias_apps_viabilidade.csv  # Dados completos da pesquisa (96 projetos)
├── utils/
│   ├── data_processor.py     # Processamento de dados
│   └── colors.py            # Paleta de cores acessível
└── components/
    ├── visualizations.py     # Módulo de visualizações
    └── filters.py           # Sistema de filtros
```

## 🚀 Como Executar

### Localmente

1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd rn-dashboard
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o dashboard**:
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Acesse no navegador**: O dashboard será aberto automaticamente em `http://localhost:8501`

### No Streamlit Cloud

1. **Faça o deploy**: Conecte este repositório ao [Streamlit Cloud](https://streamlit.io/cloud)
2. **Configure**: O arquivo principal é `streamlit_app.py`
3. **Acesse**: O link será fornecido após o deploy

## 📊 Abas do Dashboard

### 📊 Visão Geral
- Métricas principais do dataset
- Distribuição de complexidade dos projetos
- Recursos React Native mais utilizados

### 🏷️ Categorias
- Treemap das categorias de aplicativos
- Detalhamento de projetos por categoria

### ⚙️ Análise Técnica
- Correlação entre complexidade e recursos necessários
- Aplicativos semelhantes mais mencionados
- Análise de viabilidade técnica

### ⚖️ Ética e Legal
- Alertas éticos e legais identificados
- Recomendações para conformidade
- Análise de riscos regulatórios

### 📋 Dados
- Tabela completa com dados filtrados
- Opção de download em CSV
- Visualização detalhada de todos os campos

## 🔍 Sistema de Filtros

### Filtros Básicos
- **Complexidade**: Filtre por nível de dificuldade
- **Recursos RN**: Selecione recursos React Native específicos
- **Alertas Éticos**: Foque em projetos com ou sem alertas
- **Busca por Texto**: Encontre projetos por palavra-chave

### Filtros Avançados
- **Número de Recursos**: Range de recursos técnicos necessários
- **Apps Semelhantes**: Projetos com ou sem concorrentes identificados

## 🎨 Design e Acessibilidade

### Paleta de Cores
- **Primária**: #1f4e79 (Azul escuro - Contraste AAA)
- **Secundária**: #2d5a87 (Azul médio - Contraste AAA)
- **Destaque**: #8b4513 (Marrom escuro - Contraste AAA)
- **Texto**: #212529 (Preto suave - Contraste AAA)

### Critérios WCAG 2.2 AAA
- ✅ Contraste de cor mínimo de 7:1
- ✅ Texto redimensionável até 200%
- ✅ Navegação por teclado
- ✅ Foco visível em elementos interativos
- ✅ Texto alternativo em elementos visuais

## 📈 Dados Analisados

O dashboard analisa **96 projetos** com os seguintes campos:
- **ID**: Identificador único do projeto
- **Ideia Resumo**: Descrição da ideia de aplicativo
- **Apps Semelhantes**: Aplicativos existentes no mercado (93% dos projetos têm referências)
- **Recursos RN**: Câmera (15%), Mapas (11%), Notificações (38%), Autenticação (93%), Pagamentos (17%)
- **Complexidade**: Baixa (3%), Média (54%), Média-Alta (31%), Alta (11%)
- **Alertas Éticos**: 35% dos projetos requerem atenção ética/legal (16 tipos diferentes)

## 🛠️ Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)**: Framework para dashboards em Python
- **[Plotly](https://plotly.com/python/)**: Biblioteca de visualização interativa
- **[Pandas](https://pandas.pydata.org/)**: Manipulação e análise de dados
- **Python 3.8+**: Linguagem de programação

## 🤝 Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas ou sugestões:
- Abra uma issue no GitHub
- Entre em contato através dos canais da instituição

---

**Desenvolvido com ❤️ para análise educacional de projetos de aplicativos**
