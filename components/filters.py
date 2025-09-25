"""
Módulo de filtros interativos para o dashboard.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Tuple, Optional


class FilterManager:
    """Gerenciador de filtros do dashboard."""
    
    def __init__(self, data_processor):
        """
        Inicializa o gerenciador de filtros.
        
        Args:
            data_processor: Instância do processador de dados
        """
        self.data_processor = data_processor
        self.df = data_processor.get_dataframe()
    
    def create_sidebar_filters(self) -> Dict:
        """
        Cria filtros na barra lateral.
        
        Returns:
            Dicionário com os filtros selecionados
        """
        st.sidebar.header("🔍 Filtros de Análise")
        
        filters = {}
        
        # Filtro de complexidade
        complexity_options = ['Todos'] + sorted(self.df['Complexidade'].unique().tolist())
        filters['complexidade'] = st.sidebar.selectbox(
            "Nível de Complexidade:",
            options=complexity_options,
            help="Filtre projetos por nível de complexidade de desenvolvimento"
        )
        
        # Filtro de recursos React Native
        st.sidebar.subheader("Recursos React Native:")
        rn_features = ['RN_camera', 'RN_maps', 'RN_notificacoes', 'RN_autenticacao', 'RN_pagamentos']
        feature_names = {
            'RN_camera': '📷 Câmera',
            'RN_maps': '🗺️ Mapas', 
            'RN_notificacoes': '🔔 Notificações',
            'RN_autenticacao': '🔐 Autenticação',
            'RN_pagamentos': '💳 Pagamentos'
        }
        
        filters['recursos'] = []
        for feature in rn_features:
            if st.sidebar.checkbox(
                feature_names[feature],
                help=f"Projetos que utilizam {feature_names[feature].lower()}"
            ):
                filters['recursos'].append(feature)
        
        # Filtro de alertas éticos
        filters['com_alertas'] = st.sidebar.selectbox(
            "Alertas Éticos/Legais:",
            options=['Todos', 'Apenas com alertas', 'Apenas sem alertas'],
            help="Filtre projetos baseado na presença de alertas éticos ou legais"
        )
        
        # Filtro de busca por texto
        filters['busca_texto'] = st.sidebar.text_input(
            "🔍 Buscar por palavra-chave:",
            placeholder="Digite uma palavra-chave...",
            help="Busque nas descrições das ideias de aplicativos"
        )
        
        return filters
    
    def apply_filters(self, filters: Dict) -> pd.DataFrame:
        """
        Aplica os filtros aos dados.
        
        Args:
            filters: Dicionário com filtros selecionados
            
        Returns:
            DataFrame filtrado
        """
        df_filtered = self.df.copy()
        
        # Filtro de complexidade
        if filters['complexidade'] != 'Todos':
            df_filtered = df_filtered[df_filtered['Complexidade'] == filters['complexidade']]
        
        # Filtro de recursos RN
        if filters['recursos']:
            for recurso in filters['recursos']:
                df_filtered = df_filtered[df_filtered[recurso] == 'Sim']
        
        # Filtro de alertas éticos
        if filters['com_alertas'] == 'Apenas com alertas':
            df_filtered = df_filtered[df_filtered['Alertas_etico_legais'].str.len() > 0]
        elif filters['com_alertas'] == 'Apenas sem alertas':
            df_filtered = df_filtered[df_filtered['Alertas_etico_legais'].str.len() == 0]
        
        # Filtro de busca por texto
        if filters['busca_texto']:
            mask = df_filtered['ideia_resumo'].str.contains(
                filters['busca_texto'], 
                case=False, 
                na=False
            )
            df_filtered = df_filtered[mask]
        
        return df_filtered
    
    def display_filter_summary(self, df_original: pd.DataFrame, df_filtered: pd.DataFrame) -> None:
        """
        Exibe resumo dos filtros aplicados.
        
        Args:
            df_original: DataFrame original
            df_filtered: DataFrame filtrado
        """
        total_original = len(df_original)
        total_filtered = len(df_filtered)
        
        if total_filtered < total_original:
            st.info(
                f"📊 Mostrando {total_filtered} de {total_original} projetos "
                f"({total_filtered/total_original*100:.1f}% do total)"
            )
        
        if total_filtered == 0:
            st.warning("⚠️ Nenhum projeto encontrado com os filtros selecionados. Tente ajustar os critérios.")
    
    def create_comparison_selector(self) -> Optional[str]:
        """
        Cria seletor para comparação de projetos.
        
        Returns:
            ID do projeto selecionado para comparação ou None
        """
        st.sidebar.subheader("🔄 Comparação de Projetos")
        
        if len(self.df) < 2:
            st.sidebar.info("Necessário pelo menos 2 projetos para comparação")
            return None
        
        project_options = ['Nenhum'] + [
            f"{row['id']}: {row['ideia_resumo'][:30]}..." 
            if len(row['ideia_resumo']) > 30 
            else f"{row['id']}: {row['ideia_resumo']}"
            for _, row in self.df.iterrows()
        ]
        
        selected = st.sidebar.selectbox(
            "Selecione um projeto para destacar:",
            options=project_options,
            help="Destaque um projeto específico nas visualizações"
        )
        
        if selected != 'Nenhum':
            return int(selected.split(':')[0])
        
        return None
    
    def get_advanced_filters(self) -> Dict:
        """
        Cria filtros avançados em um expander.
        
        Returns:
            Dicionário com filtros avançados
        """
        with st.sidebar.expander("🔧 Filtros Avançados"):
            advanced_filters = {}
            
            # Filtro por número de recursos
            min_features, max_features = st.slider(
                "Número de recursos RN:",
                min_value=0,
                max_value=5,
                value=(0, 5),
                help="Filtre por quantidade de recursos React Native necessários"
            )
            advanced_filters['min_features'] = min_features
            advanced_filters['max_features'] = max_features
            
            # Filtro por apps semelhantes
            has_similar_apps = st.selectbox(
                "Apps semelhantes:",
                options=['Todos', 'Com apps semelhantes', 'Sem apps semelhantes'],
                help="Filtre baseado na existência de apps semelhantes no mercado"
            )
            advanced_filters['has_similar_apps'] = has_similar_apps
            
            return advanced_filters
    
    def apply_advanced_filters(self, df: pd.DataFrame, advanced_filters: Dict) -> pd.DataFrame:
        """
        Aplica filtros avançados aos dados.
        
        Args:
            df: DataFrame a ser filtrado
            advanced_filters: Filtros avançados
            
        Returns:
            DataFrame filtrado
        """
        df_filtered = df.copy()
        
        # Filtro por número de recursos
        rn_features = ['RN_camera', 'RN_maps', 'RN_notificacoes', 'RN_autenticacao', 'RN_pagamentos']
        df_filtered['num_features'] = df_filtered[rn_features].apply(
            lambda row: sum(1 for x in row if x == 'Sim'), axis=1
        )
        
        df_filtered = df_filtered[
            (df_filtered['num_features'] >= advanced_filters['min_features']) &
            (df_filtered['num_features'] <= advanced_filters['max_features'])
        ]
        
        # Filtro por apps semelhantes
        if advanced_filters['has_similar_apps'] == 'Com apps semelhantes':
            df_filtered = df_filtered[df_filtered['apps_semelhantes'].str.len() > 0]
        elif advanced_filters['has_similar_apps'] == 'Sem apps semelhantes':
            df_filtered = df_filtered[df_filtered['apps_semelhantes'].str.len() == 0]
        
        return df_filtered.drop('num_features', axis=1)
