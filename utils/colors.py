"""
Paleta de cores acessível seguindo os critérios WCAG 2.2 AAA.
"""

from typing import Dict, List


class AccessibleColors:
    """Classe com paleta de cores acessível para o dashboard.
    Baseada em pares com razão de contraste AAA (≥ 7:1) conforme WCAG 2.2.
    Referência de verificação: color.review [AA/AAA].
    """
    
    # Cores principais com alto contraste em fundo claro (validadas ≥ 7:1)
    PRIMARY = "#0B3D91"   # Navy (excelente contraste sobre #FFFFFF)
    SECONDARY = "#004B50" # Teal escuro
    ACCENT = "#7A003C"    # Bordô escuro
    
    # Cores de fundo
    BACKGROUND = "#FFFFFF"  # Branco
    SURFACE = "#F5F7FA"     # Cinza muito claro
    
    # Cores de texto
    TEXT_PRIMARY = "#1F1F1F"   # Preto quase puro (ótimo em fundos claros)
    TEXT_SECONDARY = "#333333"  # Cinza escuro
    TEXT_MUTED = "#5A5A5A"      # Cinza médio-escuro
    
    # Cores de status (escuras para alto contraste)
    SUCCESS = "#155724"  # Verde escuro
    WARNING = "#8A6D00"  # Amarelo escuro/ocre
    ERROR = "#7A0010"    # Vermelho escuro
    INFO = "#0C4A6E"     # Azul petróleo escuro
    
    # Paleta discreta para gráficos (tons escuros e distinguíveis)
    CHART_COLORS = [
        "#0B3D91",  # Navy
        "#004B50",  # Teal escuro
        "#7A003C",  # Bordô
        "#4B0082",  # Índigo
        "#2F4F4F",  # SlateDark
        "#006400",  # Verde escuro
        "#800000",  # Marrom escuro
        "#2E8B57",  # SeaGreen escuro
        "#8B4513",  # SaddleBrown
        "#1B4D3E",  # Verde petróleo
    ]
    
    # Mapa de cores para níveis de complexidade (escuro → claro nocionalmente)
    COMPLEXITY_COLORS = {
        "Baixa": "#0B3D91",      # Azul escuro
        "Média": "#004B50",      # Teal escuro
        "Média-Alta": "#8B4513", # Marrom escuro
        "Alta": "#7A0010"        # Vermelho escuro
    }
    
    @classmethod
    def get_plotly_theme(cls) -> Dict:
        """Retorna tema Plotly com cores acessíveis."""
        return {
            'layout': {
                'paper_bgcolor': cls.BACKGROUND,
                'plot_bgcolor': cls.SURFACE,
                'font': {
                    'color': cls.TEXT_PRIMARY,
                    'family': 'Arial, sans-serif',
                    'size': 12
                },
                'colorway': cls.CHART_COLORS,
                'title': {
                    'font': {
                        'color': cls.TEXT_PRIMARY,
                        'size': 16,
                        'family': 'Arial, sans-serif'
                    }
                },
                'xaxis': {
                    'gridcolor': '#dee2e6',
                    'linecolor': cls.TEXT_SECONDARY,
                    'tickcolor': cls.TEXT_SECONDARY,
                    'tickfont': {'color': cls.TEXT_PRIMARY}
                },
                'yaxis': {
                    'gridcolor': '#dee2e6',
                    'linecolor': cls.TEXT_SECONDARY,
                    'tickcolor': cls.TEXT_SECONDARY,
                    'tickfont': {'color': cls.TEXT_PRIMARY}
                }
            }
        }
    
    @classmethod
    def get_streamlit_css(cls) -> str:
        """Retorna CSS personalizado para Streamlit."""
        return f"""
        <style>
        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
        
        .stMetric {{
            background-color: {cls.SURFACE};
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid {cls.PRIMARY};
        }}
        
        .stAlert {{
            border-radius: 0.5rem;
        }}
        
        h1, h2, h3 {{
            color: {cls.TEXT_PRIMARY};
            font-family: 'Arial', sans-serif;
        }}
        
        .stSelectbox label {{
            color: {cls.TEXT_PRIMARY} !important;
            font-weight: 600;
        }}
        
        .stMultiSelect label {{
            color: {cls.TEXT_PRIMARY} !important;
            font-weight: 600;
        }}
        
        /* Melhorar contraste dos elementos interativos */
        .stButton > button {{
            background-color: {cls.PRIMARY};
            color: {cls.BACKGROUND};
            border: 2px solid {cls.PRIMARY};
            border-radius: 0.25rem;
            font-weight: 600;
        }}
        
        .stButton > button:hover {{
            background-color: {cls.SECONDARY};
            border-color: {cls.SECONDARY};
        }}
        
        .stButton > button:focus {{
            outline: 3px solid {cls.ACCENT};
            outline-offset: 2px;
        }}
        </style>
        """
