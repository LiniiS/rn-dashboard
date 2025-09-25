"""
Módulo para processamento e limpeza dos dados da pesquisa de aplicativos.
"""

import pandas as pd
import streamlit as st
from typing import Dict, List, Tuple, Optional


class DataProcessor:
    """Classe responsável pelo processamento dos dados da pesquisa."""
    
    def __init__(self, csv_path: str):
        """
        Inicializa o processador de dados.
        
        Args:
            csv_path: Caminho para o arquivo CSV
        """
        self.csv_path = csv_path
        self.df = None
        self._load_data()
    
    def _load_data(self) -> None:
        """Carrega os dados do CSV."""
        try:
            if not self.csv_path:
                # Se o caminho estiver vazio, não tentar carregar
                self.df = pd.DataFrame()
                return
                
            self.df = pd.read_csv(self.csv_path)
            self._clean_data()
        except FileNotFoundError:
            st.error(f"❌ Arquivo não encontrado: {self.csv_path}")
            st.info("Verifique se o arquivo 'ideias_alunos_app.csv' está no diretório correto.")
            self.df = pd.DataFrame()
        except Exception as e:
            st.error(f"❌ Erro ao carregar dados: {e}")
            self.df = pd.DataFrame()
    
    def _clean_data(self) -> None:
        """Limpa e processa os dados."""
        if self.df.empty:
            return
        
        # Remove linhas com ideias indefinidas ou vazias
        self.df = self.df.dropna(subset=['ideia_resumo'])
        self.df = self.df[~self.df['ideia_resumo'].str.contains('Sem ideia|indefinido', na=False)]
        
        # Limpa valores vazios
        self.df = self.df.fillna('')
        
        # Processa apps semelhantes
        self.df['apps_semelhantes_lista'] = self.df['apps_semelhantes'].apply(
            lambda x: [app.strip() for app in x.split(';')] if x else []
        )
        
        # Processa alertas éticos e legais
        self.df['alertas_lista'] = self.df['Alertas_etico_legais'].apply(
            lambda x: [alert.strip() for alert in x.split(';')] if x else []
        )
    
    def get_complexity_distribution(self) -> pd.Series:
        """Retorna a distribuição de complexidade dos projetos."""
        return self.df['Complexidade'].value_counts()
    
    def get_rn_features_usage(self) -> Dict[str, int]:
        """Retorna o uso de recursos React Native."""
        features = ['RN_camera', 'RN_maps', 'RN_notificacoes', 'RN_autenticacao', 'RN_pagamentos']
        usage = {}
        
        for feature in features:
            feature_name = feature.replace('RN_', '').title()
            usage[feature_name] = (self.df[feature] == 'Sim').sum()
        
        return usage
    
    def get_apps_semelhantes_count(self) -> Dict[str, int]:
        """Conta apps semelhantes mencionados."""
        all_apps = []
        for apps_list in self.df['apps_semelhantes_lista']:
            all_apps.extend(apps_list)
        
        apps_count = pd.Series(all_apps).value_counts()
        return apps_count.head(10).to_dict()
    
    def get_ethical_alerts_count(self) -> Dict[str, int]:
        """Conta alertas éticos e legais."""
        all_alerts = []
        for alerts_list in self.df['alertas_lista']:
            all_alerts.extend(alerts_list)
        
        if not all_alerts:
            return {}
        
        alerts_count = pd.Series(all_alerts).value_counts()
        return alerts_count.to_dict()
    
    def get_complexity_vs_features(self) -> pd.DataFrame:
        """Retorna relação entre complexidade e recursos necessários."""
        features = ['RN_camera', 'RN_maps', 'RN_notificacoes', 'RN_autenticacao', 'RN_pagamentos']
        
        result = []
        for _, row in self.df.iterrows():
            feature_count = sum(1 for feature in features if row[feature] == 'Sim')
            result.append({
                'ideia': row['ideia_resumo'][:50] + '...' if len(row['ideia_resumo']) > 50 else row['ideia_resumo'],
                'complexidade': row['Complexidade'],
                'recursos_necessarios': feature_count,
                'tem_alertas': len(row['alertas_lista']) > 0
            })
        
        return pd.DataFrame(result)
    
    def get_categories_analysis(self) -> Dict[str, List[str]]:
        """Categoriza as ideias por tipo de aplicativo."""
        categories = {
            'Redes Sociais': [],
            'Educação': [],
            'Jogos': [],
            'E-commerce': [],
            'Saúde/Bem-estar': [],
            'Entretenimento': [],
            'Produtividade': [],
            'Transporte/Localização': [],
            'Finanças': [],
            'Utilitários': []
        }
        
        category_keywords = {
            'Redes Sociais': ['rede social', 'relacionamento', 'social', 'comunidade', 'encontros', 'tinder', 'cassino social'],
            'Educação': ['aprendizado', 'educação', 'edu', 'conhecimento', 'curso', 'estudo', 'ensinar', 'tutorial', 'aula', 'roadmap'],
            'Jogos': ['jogo', 'game', 'diversão', 'competitivo', 'ritmo', 'fases', 'prêmios', 'desafios'],
            'E-commerce': ['mercadoria', 'busca', 'lojista', 'marketplace', 'cupons', 'preços', 'fornecedores'],
            'Saúde/Bem-estar': ['saúde', 'mental', 'humor', 'estresse', 'rotina', 'água', 'medicamentos', 'consultas', 'treino', 'dieta', 'meditação', 'bem-estar', 'cuidado', 'respiração'],
            'Entretenimento': ['youtube', 'evento', 'leitura', 'séries', 'mangás', 'música', 'wallpapers'],
            'Produtividade': ['agenda', 'controle', 'gestão', 'tempo', 'tarefas', 'organização', 'produtividade', 'hábitos', 'rotina diária'],
            'Transporte/Localização': ['caronas', 'transporte', 'ônibus', 'uber', 'viagens', 'entregas', 'localização', 'eventos da cidade'],
            'Finanças': ['tributário', 'estoque', 'lucros', 'dados de bancos', 'fundos', 'educação financeira', 'doações', 'pix']
        }
        
        for _, row in self.df.iterrows():
            ideia = row['ideia_resumo'].lower()
            categorized = False
            
            for category, keywords in category_keywords.items():
                if any(word in ideia for word in keywords):
                    categories[category].append(row['ideia_resumo'])
                    categorized = True
                    break
            
            if not categorized:
                categories['Utilitários'].append(row['ideia_resumo'])
        
        return categories
    
    def get_dataframe(self) -> pd.DataFrame:
        """Retorna o DataFrame processado."""
        return self.df.copy()
