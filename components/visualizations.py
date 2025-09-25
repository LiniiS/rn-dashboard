"""
Módulo de visualizações interativas para o dashboard de análise de aplicativos.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Any
from utils.colors import AccessibleColors


class AppVisualizationManager:
    """Gerenciador de visualizações do dashboard."""
    
    def __init__(self):
        """Inicializa o gerenciador de visualizações."""
        self.colors = AccessibleColors()
        self.plotly_theme = self.colors.get_plotly_theme()
    
    def create_complexity_pie_chart(self, complexity_data: pd.Series) -> go.Figure:
        """
        Cria gráfico de pizza da distribuição de complexidade.
        
        Args:
            complexity_data: Série com dados de complexidade
            
        Returns:
            Figura Plotly
        """
        fig = px.pie(
            values=complexity_data.values,
            names=complexity_data.index,
            color=complexity_data.index,
            color_discrete_map=self.colors.COMPLEXITY_COLORS
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12,
            textfont_color='white'
        )
        
        layout_config = self.plotly_theme['layout'].copy()
        layout_config.update({
            'title': "Distribuição de Complexidade dos Projetos",
            'showlegend': True,
            'legend': dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            )
        })
        fig.update_layout(**layout_config)
        
        return fig
    
    def create_rn_features_bar_chart(self, features_data: Dict[str, int], palette: str = 'Viridis') -> go.Figure:
        """
        Cria gráfico de barras dos recursos React Native.
        
        Args:
            features_data: Dicionário com dados dos recursos
            
        Returns:
            Figura Plotly
        """
        df = pd.DataFrame(list(features_data.items()), columns=['Recurso', 'Quantidade'])
        
        fig = px.bar(
            df,
            x='Recurso',
            y='Quantidade',
            color='Quantidade',
            color_continuous_scale=palette
        )
        
        fig.update_traces(
            texttemplate='%{y}',
            textposition='outside',
            textfont_size=12,
            textfont_color=self.colors.TEXT_PRIMARY
        )
        
        layout_config = self.plotly_theme['layout'].copy()
        layout_config.update({
            'title': 'Recursos React Native Mais Utilizados',
            'xaxis_title': "Recursos React Native",
            'yaxis_title': "Número de Projetos",
            'showlegend': False
        })
        fig.update_layout(**layout_config)
        
        return fig
    
    def create_apps_comparison_chart(self, apps_data: Dict[str, int], palette: str = 'Viridis') -> go.Figure:
        """
        Cria gráfico de barras horizontais dos apps semelhantes.
        
        Args:
            apps_data: Dicionário com dados dos apps
            
        Returns:
            Figura Plotly
        """
        if not apps_data:
            fig = go.Figure()
            fig.add_annotation(
                text="Nenhum dado de apps semelhantes disponível",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=16, color=self.colors.TEXT_SECONDARY)
            )
            return fig
        
        df = pd.DataFrame(list(apps_data.items()), columns=['App', 'Menções'])
        df = df.sort_values('Menções', ascending=True)
        
        fig = px.bar(
            df,
            x='Menções',
            y='App',
            orientation='h',
            color='Menções',
            color_continuous_scale=palette
        )
        
        fig.update_traces(
            texttemplate='%{x}',
            textposition='outside',
            textfont_size=11,
            textfont_color=self.colors.TEXT_PRIMARY
        )
        
        layout_config = self.plotly_theme['layout'].copy()
        layout_config.update({
            'title': 'Apps Semelhantes Mais Mencionados',
            'xaxis_title': "Número de Menções",
            'yaxis_title': "Aplicativos",
            'height': max(400, len(apps_data) * 40),
            'showlegend': False
        })
        fig.update_layout(**layout_config)
        
        return fig
    
    def create_complexity_vs_features_scatter(self, data: pd.DataFrame) -> go.Figure:
        """
        Cria gráfico de dispersão complexidade vs recursos.
        
        Args:
            data: DataFrame com dados processados
            
        Returns:
            Figura Plotly
        """
        fig = px.scatter(
            data,
            x='recursos_necessarios',
            y='complexidade',
            hover_data=['ideia'],
            color='tem_alertas',
            color_discrete_map={
                True: self.colors.WARNING,
                False: self.colors.PRIMARY
            },
            labels={
                'recursos_necessarios': 'Número de Recursos RN',
                'complexidade': 'Complexidade',
                'tem_alertas': 'Tem Alertas Éticos'
            }
        )
        
        fig.update_traces(
            marker=dict(size=12, line=dict(width=2, color='white'))
        )
        
        layout_config = self.plotly_theme['layout'].copy()
        layout_config.update({
            'title': 'Relação entre Complexidade e Recursos Necessários',
            'xaxis': dict(
                title="Número de Recursos React Native Necessários",
                tickmode='linear',
                dtick=1
            ),
            'yaxis_title': "Nível de Complexidade"
        })
        fig.update_layout(**layout_config)
        
        return fig
    
    def create_categories_treemap(self, categories_data: Dict[str, List[str]]) -> go.Figure:
        """
        Cria treemap das categorias de aplicativos.
        
        Args:
            categories_data: Dicionário com categorias e apps
            
        Returns:
            Figura Plotly
        """
        # Preparar dados para o treemap
        labels = []
        parents = []
        values = []
        colors = []
        
        # Adicionar categorias principais
        for category, apps in categories_data.items():
            if apps:  # Só adicionar categorias com apps
                labels.append(category)
                parents.append("")
                values.append(len(apps))
                colors.append(self.colors.CHART_COLORS[len(labels) % len(self.colors.CHART_COLORS)])
        
        if not labels:
            fig = go.Figure()
            fig.add_annotation(
                text="Nenhuma categoria com dados disponível",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=16, color=self.colors.TEXT_SECONDARY)
            )
            return fig
        
        fig = go.Figure(go.Treemap(
            labels=labels,
            parents=parents,
            values=values,
            textinfo="label+value",
            textfont_size=12,
            marker_colors=colors[:len(labels)],
            hovertemplate='<b>%{label}</b><br>%{value} aplicativos<extra></extra>'
        ))
        
        layout_config = self.plotly_theme['layout'].copy()
        layout_config.update({
            'title': "Distribuição por Categorias de Aplicativos",
            'font_size': 12
        })
        fig.update_layout(**layout_config)
        
        return fig
    
    def create_ethical_alerts_chart(self, alerts_data: Dict[str, int], palette: str = 'Viridis') -> go.Figure:
        """
        Cria gráfico de alertas éticos e legais.
        
        Args:
            alerts_data: Dicionário com dados dos alertas
            
        Returns:
            Figura Plotly
        """
        if not alerts_data:
            fig = go.Figure()
            fig.add_annotation(
                text="Nenhum alerta ético/legal identificado",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=16, color=self.colors.SUCCESS)
            )
            fig.update_layout(**self.plotly_theme['layout'])
            return fig
        
        df = pd.DataFrame(list(alerts_data.items()), columns=['Alerta', 'Frequência'])
        df = df.sort_values('Frequência', ascending=True)
        
        fig = px.bar(
            df,
            x='Frequência',
            y='Alerta',
            orientation='h',
            color='Frequência',
            color_continuous_scale=palette
        )
        
        fig.update_traces(
            texttemplate='%{x}',
            textposition='outside',
            textfont_size=11,
            textfont_color=self.colors.TEXT_PRIMARY
        )
        
        layout_config = self.plotly_theme['layout'].copy()
        layout_config.update({
            'title': 'Alertas Éticos e Legais Identificados',
            'xaxis_title': "Frequência",
            'yaxis_title': "Tipo de Alerta",
            'height': max(300, len(alerts_data) * 50),
            'showlegend': False
        })
        fig.update_layout(**layout_config)
        
        return fig
    
    def display_metrics_cards(self, data_processor) -> None:
        """
        Exibe cards com métricas principais.
        
        Args:
            data_processor: Instância do processador de dados
        """
        df = data_processor.get_dataframe()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📱 Total de Ideias",
                value=len(df),
                help="Número total de ideias de aplicativos analisadas"
            )
        
        with col2:
            avg_features = df[['RN_camera', 'RN_maps', 'RN_notificacoes', 'RN_autenticacao', 'RN_pagamentos']].apply(
                lambda row: sum(1 for x in row if x == 'Sim'), axis=1
            ).mean()
            st.metric(
                label="⚙️ Recursos Médios",
                value=f"{avg_features:.1f}",
                help="Número médio de recursos React Native por projeto"
            )
        
        with col3:
            high_complexity = (df['Complexidade'].isin(['Alta', 'Média-Alta'])).sum()
            st.metric(
                label="🔴 Alta Complexidade",
                value=high_complexity,
                help="Projetos com complexidade Alta ou Média-Alta"
            )
        
        with col4:
            ethical_alerts = df['Alertas_etico_legais'].apply(lambda x: len(x) > 0 if x else False).sum()
            st.metric(
                label="⚠️ Com Alertas Éticos",
                value=ethical_alerts,
                help="Projetos que requerem atenção ética/legal"
            )

    def display_category_summary_cards(self, data_processor) -> None:
        """
        Exibe um conjunto de cards resumindo as categorias sugeridas.
        Mostra até 6 categorias mais numerosas com contagem de projetos.
        """
        df = data_processor.get_dataframe()
        categories = data_processor.get_categories_analysis()
        # Ordenar categorias por quantidade desc
        sorted_items = sorted(
            ((cat, len(items)) for cat, items in categories.items() if items),
            key=lambda x: x[1], reverse=True
        )
        if not sorted_items:
            st.info("Sem categorias identificadas nos dados atuais.")
            return
        top = sorted_items[:6]
        # Criar 3 colunas por linha
        rows = [top[i:i+3] for i in range(0, len(top), 3)]
        for row in rows:
            cols = st.columns(len(row))
            for col, (name, count) in zip(cols, row):
                with col:
                    st.metric(label=f"🏷️ {name}", value=count, help=f"Projetos na categoria {name}")

    def create_category_resources_heatmap(self, data_processor, palette: str = 'Viridis') -> go.Figure:
        """
        Cria heatmap mostrando recursos necessários por categoria de app.
        
        Args:
            data_processor: Instância do processador de dados
            
        Returns:
            Figura Plotly
        """
        df = data_processor.get_dataframe()
        categories = data_processor.get_categories_analysis()
        
        # Preparar dados para o heatmap
        category_names = []
        resource_names = ['Câmera', 'Mapas', 'Notificações', 'Autenticação', 'Pagamentos']
        resource_cols = ['RN_camera', 'RN_maps', 'RN_notificacoes', 'RN_autenticacao', 'RN_pagamentos']
        
        # Calcular percentual de uso de cada recurso por categoria
        heatmap_data = []
        
        for category, apps in categories.items():
            if not apps:
                continue
                
            category_names.append(category)
            category_row = []
            
            # Filtrar projetos desta categoria
            category_projects = df[df['ideia_resumo'].isin(apps)]
            
            for col in resource_cols:
                usage_pct = (category_projects[col] == 'Sim').mean() * 100
                category_row.append(usage_pct)
            
            heatmap_data.append(category_row)
        
        if not heatmap_data:
            fig = go.Figure()
            fig.add_annotation(
                text="Nenhuma categoria com dados disponível",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=16, color=self.colors.TEXT_SECONDARY)
            )
            return fig
        
        # Usar paletas perceptualmente uniformes e daltônico-friendly
        # Remover texto dentro das células para evitar problemas de contraste; manter no hover
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=resource_names,
            y=category_names,
            colorscale=palette,
            hoverongaps=False,
            hovertemplate='<b>%{y}</b><br>%{x}: %{z:.1f}%<extra></extra>'
        ))
        
        layout_config = self.plotly_theme['layout'].copy()
        layout_config.update({
            'title': 'Uso de Recursos React Native por Categoria',
            'xaxis_title': "Recursos Técnicos",
            'yaxis_title': "Categorias de Aplicativos",
            'height': max(420, len(category_names) * 48),
            'coloraxis_colorbar': {
                'title': 'Uso (%)',
                'tickformat': '.0f',
                'outlinewidth': 1,
                'thickness': 14
            }
        })
        fig.update_layout(**layout_config)
        
        return fig

    def create_complexity_vs_resources_chart(self, data_processor) -> go.Figure:
        """
        Cria gráfico mostrando relação entre número de recursos e complexidade.
        
        Args:
            data_processor: Instância do processador de dados
            
        Returns:
            Figura Plotly
        """
        df = data_processor.get_dataframe()
        
        # Calcular número de recursos por projeto
        resource_cols = ['RN_camera', 'RN_maps', 'RN_notificacoes', 'RN_autenticacao', 'RN_pagamentos']
        df['num_recursos'] = df[resource_cols].apply(lambda row: sum(1 for x in row if x == 'Sim'), axis=1)
        
        # Agrupar por número de recursos e complexidade
        complexity_order = ['Baixa', 'Média', 'Média-Alta', 'Alta']
        df['Complexidade'] = pd.Categorical(df['Complexidade'], categories=complexity_order, ordered=True)
        
        # Criar dados para o gráfico
        chart_data = []
        for recursos in sorted(df['num_recursos'].unique()):
            subset = df[df['num_recursos'] == recursos]
            for complexidade in complexity_order:
                count = (subset['Complexidade'] == complexidade).sum()
                if count > 0:
                    chart_data.append({
                        'Recursos': recursos,
                        'Complexidade': complexidade,
                        'Projetos': count
                    })
        
        if not chart_data:
            fig = go.Figure()
            fig.add_annotation(
                text="Nenhum dado disponível para análise",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=16, color=self.colors.TEXT_SECONDARY)
            )
            return fig
        
        chart_df = pd.DataFrame(chart_data)
        
        fig = px.bar(
            chart_df,
            x='Recursos',
            y='Projetos',
            color='Complexidade',
            color_discrete_map=self.colors.COMPLEXITY_COLORS,
            title='Distribuição de Complexidade por Número de Recursos',
            labels={'Recursos': 'Número de Recursos RN Necessários', 'Projetos': 'Quantidade de Projetos'}
        )
        
        layout_config = self.plotly_theme['layout'].copy()
        layout_config.update({
            'xaxis': dict(
                title="Número de Recursos React Native",
                tickmode='linear',
                dtick=1
            ),
            'yaxis_title': "Número de Projetos"
        })
        fig.update_layout(**layout_config)
        
        return fig
