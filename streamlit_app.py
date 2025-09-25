"""
Dashboard Interativo para Análise de Ideias de Aplicativos
Desenvolvido para visualizar dados de pesquisa sobre aplicativos que alunos gostariam de desenvolver.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Importar módulos personalizados
from utils.data_processor import DataProcessor
from utils.colors import AccessibleColors
from components.visualizations import AppVisualizationManager
from components.filters import FilterManager


def configure_page():
    """Configura a página do Streamlit."""
    st.set_page_config(
        page_title="Dashboard de Análise de Apps",
        page_icon="📱",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': "Dashboard para análise de ideias de aplicativos dos alunos"
        }
    )


def load_custom_css():
    """Carrega CSS personalizado para acessibilidade."""
    colors = AccessibleColors()
    st.markdown(colors.get_streamlit_css(), unsafe_allow_html=True)


def display_header():
    """Exibe cabeçalho do dashboard."""
    st.title("📱 Dashboard de Análise de Ideias de Aplicativos")
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #1f4e79; margin-bottom: 2rem;">
        <p style="margin: 0; color: #495057;">
            <strong>Objetivo:</strong> Analisar as ideias de aplicativos que os alunos gostariam de desenvolver, 
            identificando recursos técnicos necessários, complexidade e implicações éticas/legais.
        </p>
    </div>
    """, unsafe_allow_html=True)


def display_overview_tab(data_processor, viz_manager, df_filtered):
    """Exibe aba de visão geral."""
    st.header("📊 Visão Geral dos Projetos")
    
    # Métricas principais
    viz_manager.display_metrics_cards(data_processor)
    
    # Cards de categorias (top 6)
    st.subheader("🏷️ Categorias sugeridas")
    viz_manager.display_category_summary_cards(data_processor)
    
    st.markdown("---")
    
    # Layout em colunas para gráficos principais
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de complexidade
        complexity_data = df_filtered['Complexidade'].value_counts()
        _display_complexity_chart(viz_manager, complexity_data)
    
    with col2:
        # Gráfico de recursos RN
        _display_features_chart(viz_manager, df_filtered)


def _display_complexity_chart(viz_manager, complexity_data):
    """Exibe gráfico de complexidade."""
    if not complexity_data.empty:
        fig_complexity = viz_manager.create_complexity_pie_chart(complexity_data)
        st.plotly_chart(fig_complexity, use_container_width=True)
    else:
        st.info("Nenhum dado de complexidade disponível com os filtros atuais.")


def _display_features_chart(viz_manager, df_filtered):
    """Exibe gráfico de recursos RN."""
    # Criar processador temporário com dados filtrados
    processor_filtered = DataProcessor("ideias_apps_viabilidade.csv")
    processor_filtered.df = df_filtered
    features_data = processor_filtered.get_rn_features_usage()
    
    palette = st.selectbox(
        "Paleta do gráfico de recursos:",
        options=["Viridis", "Cividis", "Plasma", "Inferno", "Turbo", "Greys"],
        index=0,
        help="Escolha uma paleta acessível para este gráfico"
    )

    if any(features_data.values()):
        fig_features = viz_manager.create_rn_features_bar_chart(features_data, palette=palette)
        st.plotly_chart(fig_features, use_container_width=True)
    else:
        st.info("Nenhum recurso React Native identificado com os filtros atuais.")


def display_categories_tab(data_processor, viz_manager, df_filtered):
    """Exibe aba de análise por categorias."""
    st.header("🏷️ Análise por Categorias")
    
    # Processar categorias com dados filtrados
    processor_filtered = DataProcessor("ideias_apps_viabilidade.csv")
    processor_filtered.df = df_filtered
    categories_data = processor_filtered.get_categories_analysis()
    
    # Treemap de categorias
    fig_treemap = viz_manager.create_categories_treemap(categories_data)
    st.plotly_chart(fig_treemap, use_container_width=True)
    
    st.markdown("---")
    
    # Detalhes por categoria
    st.subheader("📋 Detalhes por Categoria")
    
    for category, apps in categories_data.items():
        if apps:
            with st.expander(f"{category} ({len(apps)} projetos)"):
                for i, app in enumerate(apps, 1):
                    st.write(f"{i}. {app}")


def display_technical_tab(data_processor, viz_manager, df_filtered):
    """Exibe aba de análise técnica."""
    st.header("⚙️ Análise Técnica")
    
    # Criar processador com dados filtrados
    processor_filtered = DataProcessor("ideias_apps_viabilidade.csv")
    processor_filtered.df = df_filtered
    
    # Heatmap de recursos por categoria
    st.subheader("🔥 Recursos Necessários por Categoria")
    # Seletor de paleta acessível (todas são daltônico-friendly)
    palette = st.selectbox(
        "Paleta do mapa de calor:",
        options=["Viridis", "Cividis", "Plasma", "Inferno", "Turbo", "Greys"],
        index=0,
        help="Escolha uma paleta com alto contraste e acessível"
    )
    fig_heatmap = viz_manager.create_category_resources_heatmap(processor_filtered, palette=palette)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.markdown("---")
    
    # Gráfico de complexidade vs recursos
    st.subheader("📊 Complexidade por Número de Recursos")
    fig_complexity = viz_manager.create_complexity_vs_resources_chart(processor_filtered)
    st.plotly_chart(fig_complexity, use_container_width=True)
    
    st.markdown("---")
    
    # Resumo técnico
    st.subheader("📋 Resumo Técnico")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Recursos mais utilizados:**")
        features_data = processor_filtered.get_rn_features_usage()
        sorted_features = sorted(features_data.items(), key=lambda x: x[1], reverse=True)
        for feature, count in sorted_features[:3]:
            percentage = (count / len(df_filtered)) * 100 if len(df_filtered) > 0 else 0
            st.write(f"• {feature}: {count} projetos ({percentage:.1f}%)")
    
    with col2:
        st.markdown("**Distribuição de complexidade:**")
        complexity_dist = df_filtered['Complexidade'].value_counts()
        for complexity, count in complexity_dist.items():
            percentage = (count / len(df_filtered)) * 100 if len(df_filtered) > 0 else 0
            st.write(f"• {complexity}: {count} projetos ({percentage:.1f}%)")


def display_ethics_tab(data_processor, viz_manager, df_filtered):
    """Exibe aba de análise ética e legal."""
    st.header("⚖️ Análise Ética e Legal")
    
    # Processar alertas com dados filtrados
    processor_filtered = DataProcessor("ideias_apps_viabilidade.csv")
    processor_filtered.df = df_filtered
    alerts_data = processor_filtered.get_ethical_alerts_count()
    
    # Gráfico de alertas éticos com seletor de paleta
    palette_alerts = st.selectbox(
        "Paleta do gráfico de alertas:",
        options=["Viridis", "Cividis", "Plasma", "Inferno", "Turbo", "Greys"],
        index=0,
        help="Escolha uma paleta acessível para este gráfico"
    )
    fig_alerts = viz_manager.create_ethical_alerts_chart(alerts_data, palette=palette_alerts)
    st.plotly_chart(fig_alerts, use_container_width=True)
    
    st.markdown("---")
    
    # Detalhes dos alertas
    if alerts_data:
        st.subheader("⚠️ Detalhes dos Alertas Identificados")
        
        alert_descriptions = {
            'LGPD (dados pessoais/sensíveis)': {
                'description': 'Aplicativos que coletam e processam dados pessoais ou sensíveis dos usuários.',
                'recommendations': [
                    'Implementar política de privacidade clara',
                    'Obter consentimento explícito dos usuários',
                    'Implementar medidas de segurança para proteção de dados',
                    'Permitir que usuários acessem, corrijam e excluam seus dados'
                ]
            },
            'Moderação de conteúdo': {
                'description': 'Plataformas que permitem compartilhamento de conteúdo gerado pelos usuários.',
                'recommendations': [
                    'Implementar sistema de moderação automatizada e manual',
                    'Definir diretrizes claras de comunidade',
                    'Criar mecanismos de denúncia e bloqueio',
                    'Considerar impactos psicológicos do conteúdo'
                ]
            },
            'Coleta de localização': {
                'description': 'Aplicativos que acessam dados de localização dos usuários.',
                'recommendations': [
                    'Solicitar permissão explícita para acesso à localização',
                    'Explicar claramente como os dados serão utilizados',
                    'Implementar opções de localização aproximada quando possível',
                    'Permitir desativação do rastreamento'
                ]
            },
            'Regulação saúde/telemedicina': {
                'description': 'Aplicativos relacionados à saúde mental ou física dos usuários.',
                'recommendations': [
                    'Consultar regulamentações do CFM e ANVISA',
                    'Incluir disclaimers sobre não substituição de atendimento médico',
                    'Considerar certificações de segurança médica',
                    'Implementar mecanismos de emergência'
                ]
            }
        }
        
        for alert, count in alerts_data.items():
            _display_alert_details(alert, count, alert_descriptions)
    else:
        st.success("✅ Nenhum alerta ético ou legal identificado nos projetos filtrados.")


def _display_alert_details(alert, count, alert_descriptions):
    """Exibe detalhes de um alerta específico."""
    if alert not in alert_descriptions:
        return
        
    with st.expander(f"⚠️ {alert} ({count} projetos)"):
        info = alert_descriptions[alert]
        st.write(f"**Descrição:** {info['description']}")
        st.write("**Recomendações:**")
        for rec in info['recommendations']:
            st.write(f"• {rec}")


def display_data_table_tab(df_filtered):
    """Exibe aba com tabela de dados."""
    st.header("📋 Dados Detalhados")
    
    if df_filtered.empty:
        st.warning("Nenhum projeto encontrado com os filtros selecionados.")
        return
    
    # Preparar dados para exibição
    display_df = df_filtered.copy()
    
    # Renomear colunas para melhor legibilidade
    column_mapping = {
        'id': 'ID',
        'ideia_resumo': 'Ideia do Aplicativo',
        'apps_semelhantes': 'Apps Semelhantes',
        'RN_camera': 'Câmera',
        'RN_maps': 'Mapas',
        'RN_notificacoes': 'Notificações',
        'RN_autenticacao': 'Autenticação',
        'RN_pagamentos': 'Pagamentos',
        'Complexidade': 'Complexidade',
        'Alertas_etico_legais': 'Alertas Éticos/Legais'
    }
    
    display_df = display_df.rename(columns=column_mapping)
    
    # Selecionar colunas relevantes
    relevant_columns = [
        'ID', 'Ideia do Aplicativo', 'Apps Semelhantes', 
        'Câmera', 'Mapas', 'Notificações', 'Autenticação', 'Pagamentos',
        'Complexidade', 'Alertas Éticos/Legais'
    ]
    
    display_df = display_df[relevant_columns]
    
    # Exibir tabela
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )
    
    # Opção de download
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Baixar dados filtrados (CSV)",
        data=csv,
        file_name="ideias_apps_filtradas.csv",
        mime="text/csv"
    )


def main():
    """Função principal do dashboard."""
    configure_page()
    load_custom_css()
    display_header()
    
    # Carregar dados
    csv_path = "ideias_apps_viabilidade.csv"
    
    try:
        data_processor = DataProcessor(csv_path)
        
        if data_processor.df.empty:
            st.error("❌ Não foi possível carregar os dados. Verifique se o arquivo CSV está presente.")
            return
        
        # Inicializar componentes
        viz_manager = AppVisualizationManager()
        filter_manager = FilterManager(data_processor)
        
        # Criar filtros na barra lateral
        filters = filter_manager.create_sidebar_filters()
        advanced_filters = filter_manager.get_advanced_filters()
        
        # Aplicar filtros
        df_filtered = filter_manager.apply_filters(filters)
        df_filtered = filter_manager.apply_advanced_filters(df_filtered, advanced_filters)
        
        # Exibir resumo dos filtros
        filter_manager.display_filter_summary(data_processor.df, df_filtered)
        
        # Criar abas do dashboard
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Visão Geral", 
            "🏷️ Categorias", 
            "⚙️ Análise Técnica", 
            "⚖️ Ética e Legal", 
            "📋 Dados"
        ])
        
        with tab1:
            display_overview_tab(data_processor, viz_manager, df_filtered)
        
        with tab2:
            display_categories_tab(data_processor, viz_manager, df_filtered)
        
        with tab3:
            display_technical_tab(data_processor, viz_manager, df_filtered)
        
        with tab4:
            display_ethics_tab(data_processor, viz_manager, df_filtered)
        
        with tab5:
            display_data_table_tab(df_filtered)
        
        # Rodapé
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; color: #6c757d; font-size: 0.9em;">
                Dashboard desenvolvido com Cursor AI usando Streamlit + Python
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    except Exception as e:
        st.error(f"❌ Erro ao inicializar o dashboard: {e}")
        st.info("Verifique se o arquivo 'ideias_apps_viabilidade.csv' está presente no diretório.")


if __name__ == "__main__":
    main()
