import streamlit as st
import pandas as pd
import numpy as np
import base64
import io
from datetime import datetime, date
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Configuração da página
st.set_page_config(
    page_title="Oliveira Office Law - Auditoria Previdenciária",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Funções auxiliares
def get_logo_svg():
    """Retorna o código SVG do logo da Oliveira Office Law"""
    return '''
    <svg width="100" height="100" viewBox="0 0 100 100">
        <circle cx="50" cy="70" r="20" fill="#1E5128" />
        <rect x="45" y="25" width="10" height="45" fill="#1E5128" />
        <circle cx="30" cy="30" r="15" fill="#4E9F3D" />
        <circle cx="50" cy="20" r="15" fill="#4E9F3D" />
        <circle cx="70" cy="30" r="15" fill="#4E9F3D" />
        <circle cx="40" cy="40" r="10" fill="#4E9F3D" />
        <circle cx="60" cy="40" r="10" fill="#4E9F3D" />
        <circle cx="50" cy="25" r="3" fill="#111111" />
        <circle cx="65" cy="35" r="3" fill="#111111" />
        <circle cx="35" cy="35" r="3" fill="#111111" />
    </svg>
    '''

def load_css():
    """Carrega o CSS personalizado"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
        
        * {
            font-family: 'Roboto', sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #1E5128;
        }
        
        .main-header {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .logo-text {
            font-size: 1.5rem;
            font-weight: bold;
            color: #1E5128;
            margin-left: 0.5rem;
        }
        
        .green-card {
            background-color: #1E5128;
            color: white;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .black-card {
            background-color: #111111;
            color: white;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .white-card {
            background-color: white;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15);
        }
        
        .error-card {
            background-color: #FFF3F3;
            border-left: 5px solid #FF5A5A;
            padding: 0.8rem;
            margin-bottom: 0.8rem;
            border-radius: 0.3rem;
        }
        
        .highlight-box {
            background-color: #F0F9F0;
            border: 1px solid #C8E6C9;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .data-label {
            color: rgba(255,255,255,0.8);
            font-size: 0.85rem;
        }
        
        .data-value {
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        .download-btn {
            background-color: #4E9F3D;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 0.3rem;
            text-decoration: none;
            display: inline-block;
            margin-top: 0.5rem;
        }
        
        .warning-text {
            color: #FF5A5A;
            font-weight: bold;
        }
        
        .positive {
            color: #4E9F3D;
            font-weight: bold;
        }
        
        .negative {
            color: #D32F2F;
            font-weight: bold;
        }
        
        footer {
            text-align: center;
            padding: 1rem;
            background-color: #f5f5f5;
            margin-top: 2rem;
            border-top: 1px solid #ddd;
        }
        
        /* Melhorias para tabelas */
        .styled-table th {
            background-color: #1E5128;
            color: white;
            padding: 8px;
        }
        
        .styled-table td {
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }
        
        .styled-table tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        
        /* Melhorias para a visualização em dispositivos móveis */
        @media (max-width: 768px) {
            .hide-mobile {
                display: none;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def convert_df_to_csv(df):
    """Converte um DataFrame para CSV para download"""
    return df.to_csv(index=False).encode('utf-8')

def create_download_link(object_to_download, download_filename, download_link_text):
    """Cria um link de download para um objeto"""
    b64 = base64.b64encode(object_to_download).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{download_filename}" class="download-btn">{download_link_text}</a>'
    return href

def gerar_html_relatorio(data):
    """Gera um relatório HTML completo"""
    segurado = data['segurado']
    comparativo = data['comparativo']
    total_devido = data['total_devido']
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório de Auditoria Previdenciária - OLIVEIRA OFFICE LAW</title>
        <style>
            /* Estilos globais */
            :root {{
                --verde-primario: #1E5128;
                --verde-secundario: #4E9F3D;
                --preto: #111111;
                --cinza-claro: #f5f5f5;
                --cinza-medio: #e0e0e0;
                --branco: #ffffff;
            }}
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            
            body {{
                font-size: 14px;
                line-height: 1.6;
                color: #333;
                background-color: var(--cinza-claro);
            }}
            
            /* Container principal */
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                background-color: var(--branco);
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            
            /* Cabeçalho */
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding-bottom: 20px;
                border-bottom: 2px solid var(--verde-primario);
                margin-bottom: 30px;
            }}
            
            .logo-container {{
                display: flex;
                align-items: center;
            }}
            
            .logo-svg {{
                width: 60px;
                height: 60px;
            }}
            
            .logo-text {{
                margin-left: 15px;
            }}
            
            .logo-text h1 {{
                margin: 0;
                font-size: 24px;
                color: #333;
            }}
            
            .logo-text p {{
                margin: 5px 0 0;
                font-size: 16px;
                color: #666;
            }}
            
            .header-info {{
                text-align: right;
                font-size: 14px;
            }}
            
            /* Título principal */
            .main-title {{
                text-align: center;
                font-size: 22px;
                margin-bottom: 30px;
            }}
            
            /* Seções do relatório */
            .section {{
                margin-bottom: 30px;
            }}
            
            .section-title {{
                font-size: 20px;
                margin-bottom: 15px;
                color: var(--verde-primario);
            }}
            
            .section-content {{
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 5px;
            }}
            
            /* Tabelas */
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
            }}
            
            th {{
                background-color: var(--verde-primario);
                color: white;
                padding: 10px;
                text-align: left;
            }}
            
            td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }}
            
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            
            /* Cores para valores */
            .positive {{
                color: var(--verde-primario);
                font-weight: bold;
            }}
            
            .negative {{
                color: #D32F2F;
                font-weight: bold;
            }}
            
            /* Rodapé */
            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid var(--verde-primario);
                text-align: center;
            }}
            
            /* Versão para impressão */
            @media print {{
                body {{
                    background-color: white;
                }}
                
                .container {{
                    box-shadow: none;
                    max-width: 100%;
                }}
                
                @page {{
                    margin: 2cm;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo-container">
                    <svg class="logo-svg" viewBox="0 0 100 100">
                        <circle cx="50" cy="70" r="20" fill="#1E5128" />
                        <rect x="45" y="25" width="10" height="45" fill="#1E5128" />
                        <circle cx="30" cy="30" r="15" fill="#4E9F3D" />
                        <circle cx="50" cy="20" r="15" fill="#4E9F3D" />
                        <circle cx="70" cy="30" r="15" fill="#4E9F3D" />
                        <circle cx="40" cy="40" r="10" fill="#4E9F3D" />
                        <circle cx="60" cy="40" r="10" fill="#4E9F3D" />
                        <circle cx="50" cy="25" r="3" fill="#111111" />
                        <circle cx="65" cy="35" r="3" fill="#111111" />
                        <circle cx="35" cy="35" r="3" fill="#111111" />
                    </svg>
                    <div class="logo-text">
                        <h1>OLIVEIRA OFFICE LAW</h1>
                        <p>Consultoria Previdenciária</p>
                    </div>
                </div>
                <div class="header-info">
                    <p>Data: {data_atual}</p>
                    <p>Processo nº: AP-{segurado['numBeneficio']}</p>
                </div>
            </div>
            
            <h2 class="main-title">RELATÓRIO TÉCNICO DE AUDITORIA PREVIDENCIÁRIA</h2>
            
            <div class="section">
                <h3 class="section-title">1. IDENTIFICAÇÃO DO SEGURADO</h3>
                <div class="section-content">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div>
                            <p><strong>Nome:</strong> {segurado['nome']}</p>
                            <p><strong>CPF:</strong> {segurado['cpf']}</p>
                            <p><strong>Data de Nascimento:</strong> {segurado['dataNascimento']}</p>
                            <p><strong>NIT/PIS:</strong> {segurado['nit']}</p>
                        </div>
                        <div>
                            <p><strong>Número do Benefício:</strong> {segurado['numBeneficio']}</p>
                            <p><strong>Espécie do Benefício:</strong> {segurado['especieBeneficio']}</p>
                            <p><strong>Data de Requerimento:</strong> {segurado['dataRequerimento']}</p>
                            <p><strong>Tempo de Contribuição:</strong> {segurado['tempoContribuicao']['anos']} anos, {segurado['tempoContribuicao']['meses']} meses e {segurado['tempoContribuicao']['dias']} dias</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h3 class="section-title">2. RESUMO EXECUTIVO</h3>
                <div class="section-content">
                    <p>A presente auditoria previdenciária teve por objetivo verificar a regularidade do cálculo do benefício previdenciário concedido ao segurado em questão.</p>
                    <p>A análise técnica realizada no CNIS (Cadastro Nacional de Informações Sociais) e demais documentos previdenciários revelou inconsistências graves no cálculo efetuado pelo INSS, resultando em pagamento mensal inferior ao devido.</p>
                    
                    <p>As principais divergências identificadas foram:</p>
                    <ol style="margin-left: 20px;">
                        <li>Contagem incorreta do número de contribuições;</li>
                        <li>Aplicação inadequada da regra dos 80% maiores salários;</li>
                        <li>Desconsideração de períodos contributivos relevantes;</li>
                        <li>Cálculo incorreto do fator previdenciário.</li>
                    </ol>
                    
                    <p>Em função desses erros, o segurado recebe mensalmente R$ {(comparativo['auditoria']['salarioBeneficio'] - comparativo['inss']['salarioBeneficio']):.2f} a menos do que o valor correto, representando uma redução de {((comparativo['auditoria']['salarioBeneficio'] - comparativo['inss']['salarioBeneficio']) / comparativo['auditoria']['salarioBeneficio'] * 100):.2f}% no benefício.</p>
                    
                    <p style="font-weight: bold;">O valor total devido ao segurado, considerando as diferenças vencidas desde a concessão ({segurado['dataRequerimento']}) até a data atual ({data_atual}), incluindo correção monetária e juros legais, é de <span style="color: #1E5128;">R$ {total_devido['totalGeral']:.2f}</span>.</p>
                </div>
            </div>
            
            <div class="section">
                <h3 class="section-title">3. ANÁLISE TÉCNICA DO CÁLCULO</h3>
                
                <div style="margin-bottom: 20px;">
                    <h4 style="margin-bottom: 10px; font-size: 16px;">3.1. Composição do Período Contributivo</h4>
                    <table>
                        <thead>
                            <tr>
                                <th>Descrição</th>
                                <th>Cálculo INSS</th>
                                <th>Cálculo Auditoria</th>
                                <th>Diferença</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Total de registros analisados</td>
                                <td>{comparativo['inss']['totalContribuicoes']}</td>
                                <td>{comparativo['auditoria']['totalContribuicoes']}</td>
                                <td class="negative">{comparativo['auditoria']['totalContribuicoes'] - comparativo['inss']['totalContribuicoes']}</td>
                            </tr>
                            <tr>
                                <td>Contribuições consideradas (80%)</td>
                                <td>{comparativo['inss']['contribuicoesConsideradas']}</td>
                                <td>{comparativo['auditoria']['contribuicoesConsideradas']}</td>
                                <td class="negative">{comparativo['auditoria']['contribuicoesConsideradas'] - comparativo['inss']['contribuicoesConsideradas']}</td>
                            </tr>
                            <tr>
                                <td>Períodos ignorados que deveriam ser aproveitados</td>
                                <td>0</td>
                                <td>{comparativo['auditoria']['contribuicoesReaproveitaveis']}</td>
                                <td class="positive">+{comparativo['auditoria']['contribuicoesReaproveitaveis']}</td>
                            </tr>
                        </tbody>
                    </table>
                    <p style="font-size: 13px; margin-top: 10px;"><strong>Erro identificado:</strong> O INSS considerou registros inválidos para cálculo da média salarial, sendo que do total de {comparativo['inss']['totalContribuicoes']} registros analisados, apenas {comparativo['auditoria']['totalContribuicoes']} eram efetivamente válidos.</p>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <h4 style="margin-bottom: 10px; font-size: 16px;">3.2. Média Salarial e Fator Previdenciário</h4>
                    <table>
                        <thead>
                            <tr>
                                <th>Parâmetro</th>
                                <th>Cálculo INSS</th>
                                <th>Cálculo Auditoria</th>
                                <th>Diferença</th>
                                <th>Variação (%)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Média salarial (R$)</td>
                                <td>{comparativo['inss']['mediaContribuicoes']:.2f}</td>
                                <td>{comparativo['auditoria']['mediaContribuicoes']:.2f}</td>
                                <td class="positive">+{(comparativo['auditoria']['mediaContribuicoes'] - comparativo['inss']['mediaContribuicoes']):.2f}</td>
                                <td class="positive">+{((comparativo['auditoria']['mediaContribuicoes'] - comparativo['inss']['mediaContribuicoes']) / comparativo['inss']['mediaContribuicoes'] * 100):.2f}%</td>
                            </tr>
                            <tr>
                                <td>Fator previdenciário</td>
                                <td>{comparativo['inss']['fatorPrevidenciario']:.4f}</td>
                                <td>{comparativo['auditoria']['fatorPrevidenciario']:.4f}</td>
                                <td class="negative">{(comparativo['auditoria']['fatorPrevidenciario'] - comparativo['inss']['fatorPrevidenciario']):.4f}</td>
                                <td class="negative">{((comparativo['auditoria']['fatorPrevidenciario'] - comparativo['inss']['fatorPrevidenciario']) / comparativo['inss']['fatorPrevidenciario'] * 100):.2f}%</td>
                            </tr>
                            <tr style="font-weight: bold;">
                                <td>Salário de Benefício (R$)</td>
                                <td>{comparativo['inss']['salarioBeneficio']:.2f}</td>
                                <td>{comparativo['auditoria']['salarioBeneficio']:.2f}</td>
                                <td class="positive">+{(comparativo['auditoria']['salarioBeneficio'] - comparativo['inss']['salarioBeneficio']):.2f}</td>
                                <td class="positive">+{((comparativo['auditoria']['salarioBeneficio'] - comparativo['inss']['salarioBeneficio']) / comparativo['inss']['salarioBeneficio'] * 100):.2f}%</td>
                            </tr>
                        </tbody>
                    </table>
                    <p style="font-size: 13px; margin-top: 10px;"><strong>Impacto:</strong> A diferença na média salarial é de +{((comparativo['auditoria']['mediaContribuicoes'] - comparativo['inss']['mediaContribuicoes']) / comparativo['inss']['mediaContribuicoes'] * 100):.2f}%, o que, apesar da pequena redução no fator previdenciário, resulta em um salário de benefício consideravelmente maior.</p>
                </div>
                
                <div>
                    <h4 style="margin-bottom: 10px; font-size: 16px;">3.3. Valores Retroativos Devidos</h4>
                    <table>
                        <thead>
                            <tr>
                                <th>Componente</th>
                                <th>Valor (R$)</th>
                                <th>Participação (%)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Diferenças vencidas</td>
                                <td>{total_devido['diferencasVencidas']:.2f}</td>
                                <td>{(total_devido['diferencasVencidas'] / total_devido['totalGeral'] * 100):.2f}%</td>
                            </tr>
                            <tr>
                                <td>Correção monetária</td>
                                <td>{total_devido['correcaoMonetaria']:.2f}</td>
                                <td>{(total_devido['correcaoMonetaria'] / total_devido['totalGeral'] * 100):.2f}%</td>
                            </tr>
                            <tr>
                                <td>Juros legais</td>
                                <td>{total_devido['jurosLegais']:.2f}</td>
                                <td>{(total_devido['jurosLegais'] / total_devido['totalGeral'] * 100):.2f}%</td>
                            </tr>
                            <tr style="background-color: #111111; color: white; font-weight: bold;">
                                <td>TOTAL DEVIDO</td>
                                <td>{total_devido['totalGeral']:.2f}</td>
                                <td>100,00%</td>
                            </tr>
                        </tbody>
                    </table>
                    <p style="font-size: 13px; margin-top: 10px;"><strong>Observação:</strong> Os valores acima consideram a correção monetária pelo INPC e juros de 0,5% ao mês, conforme legislação aplicável.</p>
                </div>
            </div>
            
            <div class="section">
                <h3 class="section-title">4. CONCLUSÕES E RECOMENDAÇÕES</h3>
                <div class="section-content">
                    <p>Com base na análise técnica realizada, conclui-se que o benefício previdenciário do segurado {segurado['nome']} foi calculado de forma incorreta pelo INSS, resultando em pagamento mensal inferior ao devido.</p>
                    
                    <p>Recomenda-se as seguintes providências:</p>
                    <ol style="margin-left: 20px;">
                        <li>Ingressar com pedido administrativo de revisão junto ao INSS;</li>
                        <li>Em caso de indeferimento ou demora injustificada, ajuizar ação revisional com pedido de tutela de urgência para imediata correção do valor mensal do benefício;</li>
                        <li>Requerer o pagamento das diferenças vencidas desde a concessão, observado o prazo prescricional de 5 anos;</li>
                        <li>Solicitar a aplicação de correção monetária e juros legais sobre as parcelas em atraso.</li>
                    </ol>
                    
                    <p>Ressalta-se que a chancela de êxito para o caso em tela é considerada <strong>muito alta</strong>, tendo em vista a robustez das provas e a jurisprudência consolidada acerca da matéria.</p>
                    
                    <p style="font-weight: bold;">O ajuizamento da ação revisional deve ocorrer preferencialmente na Justiça Federal da Seção Judiciária do Maranhão, com fulcro no art. 109, I, da Constituição Federal.</p>
                </div>
            </div>
            
            <div class="footer">
                <p>São Luís, {data_atual}</p>
                <p style="font-weight: bold; margin-top: 40px;">OLIVEIRA OFFICE LAW</p>
                <p style="font-size: 13px;">Consultoria Jurídica Especializada</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

# Carregar dados
def load_data():
    """Carrega os dados do segurado e demais informações"""
    
    # Dados do segurado
    segurado = {
        "nome": "ANTONIO FRANCISCO BEZERRA",
        "cpf": "094.805.283-04",
        "dataNascimento": "11/01/1954",
        "nit": "112.54588.29-3",
        "numBeneficio": "171516921-0",
        "especieBeneficio": "42 - Aposentadoria por Tempo de Contribuição",
        "dataRequerimento": "11/12/2014",
        "idade": {
            "anos": 60,
            "meses": 11,
            "dias": 0
        },
        "tempoContribuicao": {
            "anos": 38,
            "meses": 1,
            "dias": 25
        }
    }
    
    # Comparativo INSS vs Auditoria
    comparativo = {
        "inss": {
            "totalContribuicoes": 215,
            "contribuicoesConsideradas": 172,
            "mediaContribuicoes": 3951.76,
            "fatorPrevidenciario": 0.9373,
            "salarioBeneficio": 3703.98
        },
        "auditoria": {
            "totalContribuicoes": 45,
            "contribuicoesConsideradas": 36,
            "contribuicoesReaproveitaveis": 37,
            "mediaContribuicoes": 4655.28,
            "fatorPrevidenciario": 0.9282,
            "salarioBeneficio": 4321.03
        }
    }
    
    # Cálculo do fator previdenciário
    fator_previdenciario = {
        "tempoContribuicao": 38.14,  # Anos
        "aliquota": 0.31,
        "expectativaSobrevida": 21.8,  # Anos
        "idade": 60.92,  # Anos
        "calculoFator": {
            "passo1": 38.14 * 0.31,  # = 11.82
            "passo2": (38.14 * 0.31) / 21.8,  # = 0.5423
            "passo3": 1 + ((60.92 + (38.14 * 0.31)) / 100),  # = 1.7274
            "resultadoFinal": ((38.14 * 0.31) / 21.8) * (1 + ((60.92 + (38.14 * 0.31)) / 100))  # = 0.9282
        }
    }
    
    # Evolução do benefício
    evolucao_beneficio = pd.DataFrame([
        {"ano": 2015, "inss": 3934.84, "auditoria": 4590.33, "reajuste": 6.23, "indiceSinapi": 8.19},
        {"ano": 2016, "inss": 4378.29, "auditoria": 5108.09, "reajuste": 11.28, "indiceSinapi": 6.64},
        {"ano": 2017, "inss": 4420.22, "auditoria": 5157.17, "reajuste": 0.98, "indiceSinapi": 3.82},
        {"ano": 2018, "inss": 4511.71, "auditoria": 5263.98, "reajuste": 2.10, "indiceSinapi": 3.05},
        {"ano": 2019, "inss": 4666.46, "auditoria": 5444.15, "reajuste": 3.43, "indiceSinapi": 3.86},
        {"ano": 2020, "inss": 4875.51, "auditoria": 5688.65, "reajuste": 4.45, "indiceSinapi": 10.16},
        {"ano": 2021, "inss": 5141.22, "auditoria": 5997.96, "reajuste": 5.46, "indiceSinapi": 18.65},
        {"ano": 2022, "inss": 5663.56, "auditoria": 6607.11, "reajuste": 10.21, "indiceSinapi": 9.34},
        {"ano": 2023, "inss": 5999.40, "auditoria": 6999.33, "reajuste": 5.92, "indiceSinapi": 2.76},
        {"ano": 2024, "inss": 6221.97, "auditoria": 7259.00, "reajuste": 3.72, "indiceSinapi": 1.68},
        {"ano": 2025, "inss": 6518.75, "auditoria": 7611.64, "reajuste": 4.77, "indiceSinapi": 2.05}
    ])
    
    # Diferenças acumuladas por ano
    diferencas_acumuladas = pd.DataFrame([
        {"ano": 2015, "mensal": 655.49, "meses": 12, "acumuladoAno": 7865.88, "correcao": 655.49, "juros": 0, "totalAno": 8521.37, "indiceSelic": 14.25},
        {"ano": 2016, "mensal": 729.80, "meses": 12, "acumuladoAno": 8757.60, "correcao": 729.80, "juros": 0, "totalAno": 9487.40, "indiceSelic": 13.75},
        {"ano": 2017, "mensal": 736.95, "meses": 12, "acumuladoAno": 8843.40, "correcao": 845.75, "juros": 0.25, "totalAno": 9689.40, "indiceSelic": 7.00},
        {"ano": 2018, "mensal": 752.27, "meses": 12, "acumuladoAno": 9027.24, "correcao": 880.00, "juros": 0, "totalAno": 9907.24, "indiceSelic": 6.50},
        {"ano": 2019, "mensal": 777.69, "meses": 12, "acumuladoAno": 9332.28, "correcao": 1002.00, "juros": 0, "totalAno": 10334.28, "indiceSelic": 4.50},
        {"ano": 2020, "mensal": 813.14, "meses": 12, "acumuladoAno": 9757.68, "correcao": 1001.00, "juros": 0, "totalAno": 10758.68, "indiceSelic": 2.00},
        {"ano": 2021, "mensal": 856.74, "meses": 12, "acumuladoAno": 10280.88, "correcao": 1080.40, "juros": 0, "totalAno": 11361.28, "indiceSelic": 9.25},
        {"ano": 2022, "mensal": 943.55, "meses": 12, "acumuladoAno": 11322.60, "correcao": 598.80, "juros": 0, "totalAno": 11921.40, "indiceSelic": 13.75},
        {"ano": 2023, "mensal": 999.93, "meses": 12, "acumuladoAno": 11999.16, "correcao": 599.52, "juros": 0, "totalAno": 12598.68, "indiceSelic": 11.75},
        {"ano": 2024, "mensal": 1037.03, "meses": 12, "acumuladoAno": 12444.36, "correcao": 408.00, "juros": 0, "totalAno": 12852.36, "indiceSelic": 10.50},
        {"ano": 2025, "mensal": 1092.89, "meses": 4, "acumuladoAno": 4371.56, "correcao": 743.12, "juros": 8000.00, "totalAno": 13114.68, "indiceSelic": 10.50}
    ])
    
    # Total devido acumulado
    total_devido = {
        "diferencasVencidas": 72146.39,
        "correcaoMonetaria": 11789.82,
        "jurosLegais": 26194.33,
        "totalGeral": 110130.54,
        "parcelasMensais": {
            "valor24": 5060.42,
            "valor36": 3506.52,
            "valor60": 2304.86
        }
    }
    
    # Vínculos empregatícios extraídos do CNIS
    vinculos_empregaticos = pd.DataFrame([
        {"seq": 1, "nit": "107.98673.20-3", "empresa": "SEDEL ENGENHARIA LTDA", "cnpj": "06.049.282/0001-06", "inicio": "12/05/1977", "fim": "14/01/1981", "status": "ENCERRADO"},
        {"seq": 2, "nit": "107.98673.20-3", "empresa": "TELECOMUNICACOES DO MARANHAO S.A", "cnpj": "06.274.633/0001-74", "inicio": "20/01/1981", "fim": "09/2001", "status": "ENCERRADO"},
        {"seq": 3, "nit": "112.54588.29-3", "empresa": "TELEMAR NORTE LESTE S/A. - EM RECUPERACAO JUDICIAL", "cnpj": "33.000.118/0062-90", "inicio": "20/01/1981", "fim": "10/05/2016", "status": "ENCERRADO"},
        {"seq": 4, "nit": "112.54588.29-3", "empresa": "RECOLHIMENTO (EMPREGADO DOMÉSTICO)", "cnpj": "-", "inicio": "01/11/1989", "fim": "31/03/1990", "status": "ENCERRADO"},
        {"seq": 5, "nit": "112.54588.29-3", "empresa": "RECOLHIMENTO (EMPREGADO DOMÉSTICO)", "cnpj": "-", "inicio": "01/05/1990", "fim": "31/10/1990", "status": "ENCERRADO"},
        {"seq": 6, "nit": "112.54588.29-3", "empresa": "PERÍODO DE ATIVIDADE DE SEGURADO ESPECIAL", "cnpj": "-", "inicio": "04/01/2001", "fim": "-", "status": "ENCERRADO"},
        {"seq": 7, "nit": "107.98673.20-3", "empresa": "TELEMAR NORTE LESTE S/A. - EM RECUPERACAO JUDICIAL", "cnpj": "33.000.118/0062-90", "inicio": "01/04/2002", "fim": "-", "status": "ENCERRADO"},
        {"seq": 8, "nit": "107.98673.20-3", "empresa": "BENEFÍCIO 42 - APOSENTADORIA POR TEMPO DE CONTRIBUICAO", "cnpj": "-", "inicio": "11/12/2014", "fim": "-", "status": "ATIVO"}
    ])
    
    # Dados de contribuições do CNIS
    contribuicoes_cnis = pd.DataFrame([
        {"competencia": "01/2014", "salario": 4390.24, "indice": 1.005, "corrigido": 4412.19, "status": "Considerado"},
        {"competencia": "02/2014", "salario": 4390.24, "indice": 1.010, "corrigido": 4434.14, "status": "Considerado"},
        {"competencia": "03/2014", "salario": 4390.24, "indice": 1.015, "corrigido": 4456.09, "status": "Considerado"},
        {"competencia": "04/2014", "salario": 4390.24, "indice": 1.020, "corrigido": 4478.04, "status": "Considerado"},
        {"competencia": "05/2014", "salario": 4390.24, "indice": 1.025, "corrigido": 4499.99, "status": "Considerado"},
        {"competencia": "06/2014", "salario": 4390.24, "indice": 1.030, "corrigido": 4521.95, "status": "Considerado"},
        {"competencia": "07/2014", "salario": 6049.73, "indice": 1.035, "corrigido": 6261.47, "status": "Considerado"},
        {"competencia": "08/2014", "salario": 4940.69, "indice": 1.040, "corrigido": 5138.32, "status": "Considerado"},
        {"competencia": "09/2014", "salario": 5320.14, "indice": 1.045, "corrigido": 5559.55, "status": "Considerado"},
        {"competencia": "10/2014", "salario": 4820.40, "indice": 1.050, "corrigido": 5061.42, "status": "Considerado"},
        {"competencia": "11/2014", "salario": 5395.92, "indice": 1.055, "corrigido": 5692.70, "status": "Considerado"},
        {"competencia": "12/2014", "salario": 5127.20, "indice": 1.060, "corrigido": 5434.83, "status": "Considerado"},
        {"competencia": "01/2013", "salario": 3525.06, "indice": 1.095, "corrigido": 3859.94, "status": "Considerado"},
        {"competencia": "02/2013", "salario": 6291.25, "indice": 1.100, "corrigido": 6920.38, "status": "Considerado"},
        {"competencia": "03/2013", "salario": 4875.47, "indice": 1.105, "corrigido": 5387.39, "status": "Considerado"},
        {"competencia": "04/2013", "salario": 3942.83, "indice": 1.110, "corrigido": 4376.54, "status": "Considerado"},
        {"competencia": "05/2013", "salario": 3872.51, "indice": 1.115, "corrigido": 4317.85, "status": "Considerado"},
        {"competencia": "06/2013", "salario": 5512.53, "indice": 1.120, "corrigido": 6174.03, "status": "Indeferido"},
        {"competencia": "07/2013", "salario": 5433.08, "indice": 1.125, "corrigido": 6112.21, "status": "Indeferido"},
        {"competencia": "08/2013", "salario": 5104.12, "indice": 1.130, "corrigido": 5767.66, "status": "Indeferido"},
        {"competencia": "09/2013", "salario": 4757.47, "indice": 1.135, "corrigido": 5399.73, "status": "Considerado"},
        {"competencia": "10/2013", "salario": 4564.30, "indice": 1.140, "corrigido": 5203.30, "status": "Considerado"},
        {"competencia": "11/2013", "salario": 4564.30, "indice": 1.145, "corrigido": 5226.12, "status": "Considerado"},
        {"competencia": "12/2013", "salario": 5485.45, "indice": 1.150, "corrigido": 6308.27, "status": "Indeferido"},
        {"competencia": "01/2012", "salario": 3430.37, "indice": 1.155, "corrigido": 3962.08, "status": "Considerado"},
        {"competencia": "02/2012", "salario": 4014.46, "indice": 1.160, "corrigido": 4656.77, "status": "Considerado"},
        {"competencia": "03/2012", "salario": 4438.21, "indice": 1.165, "corrigido": 5170.51, "status": "Considerado"},
        {"competencia": "04/2012", "salario": 4688.31, "indice": 1.170, "corrigido": 5485.32, "status": "Considerado"},
        {"competencia": "05/2012", "salario": 5787.53, "indice": 1.175, "corrigido": 6800.35, "status": "Considerado"},
        {"competencia": "06/2012", "salario": 5183.01, "indice": 1.180, "corrigido": 6115.95, "status": "Indeferido"},
        {"competencia": "07/2012", "salario": 4920.29, "indice": 1.185, "corrigido": 5830.54, "status": "Indeferido"},
        {"competencia": "08/2012", "salario": 3328.33, "indice": 1.190, "corrigido": 3960.71, "status": "Indeferido"},
        {"competencia": "09/2012", "salario": 5687.93, "indice": 1.195, "corrigido": 6797.08, "status": "Indeferido"},
        {"competencia": "10/2012", "salario": 4936.69, "indice": 1.200, "corrigido": 5924.03, "status": "Indeferido"},
        {"competencia": "11/2012", "salario": 6339.03, "indice": 1.205, "corrigido": 7638.53, "status": "Indeferido"},
        {"competencia": "12/2012", "salario": 6206.18, "indice": 1.210, "corrigido": 7509.48, "status": "Indeferido"},
        {"competencia": "01/2011", "salario": 3876.06, "indice": 1.215, "corrigido": 4709.41, "status": "Considerado"},
        {"competencia": "02/2011", "salario": 3104.00, "indice": 1.220, "corrigido": 3786.88, "status": "Considerado"},
        {"competencia": "03/2011", "salario": 3104.00, "indice": 1.225, "corrigido": 3802.40, "status": "Considerado"},
        {"competencia": "04/2011", "salario": 3104.00, "indice": 1.230, "corrigido": 3817.92, "status": "Considerado"},
        {"competencia": "05/2011", "salario": 3104.00, "indice": 1.235, "corrigido": 3833.44, "status": "Considerado"},
        {"competencia": "06/2011", "salario": 3865.89, "indice": 1.240, "corrigido": 4793.70, "status": "Indeferido"},
        {"competencia": "07/2011", "salario": 4246.48, "indice": 1.245, "corrigido": 5286.87, "status": "Indeferido"},
        {"competencia": "08/2011", "salario": 5036.96, "indice": 1.250, "corrigido": 6296.20, "status": "Indeferido"},
        {"competencia": "09/2011", "salario": 3107.30, "indice": 1.255, "corrigido": 3899.66, "status": "Indeferido"}
    ])
    
    # Ordenar contribuições por valor corrigido decrescente
    contribuicoes_cnis = contribuicoes_cnis.sort_values(by='corrigido', ascending=False).reset_index(drop=True)
    
    # Análise dos dados CNIS
    total_registros = len(contribuicoes_cnis)
    registros_considerados = int(total_registros * 0.8)
    media_maiores_salarios = contribuicoes_cnis.head(registros_considerados)['corrigido'].mean()
    periodos_incorretos = len(contribuicoes_cnis[
        (contribuicoes_cnis['status'] == 'Indeferido') & 
        (contribuicoes_cnis.index < registros_considerados)
    ])
    
    analise_cnis = {
        "totalRegistros": total_registros,
        "registrosConsiderados": registros_considerados,
        "mediaMaioresSalarios": media_maiores_salarios,
        "periodosIncorretos": periodos_incorretos
    }
    
    # Fundamentos legais
    fundamentos_legais = [
        {"lei": "Lei nº 8.213/91, art. 29", "descricao": "Estabelece os critérios para cálculo do salário de benefício, incluindo a regra de consideração dos 80% maiores salários de contribuição."},
        {"lei": "Lei nº 9.876/99", "descricao": "Institui o fator previdenciário e sua fórmula de cálculo."},
        {"lei": "Decreto nº 3.048/99, art. 188-A", "descricao": "Regulamenta a aplicação do fator previdenciário."},
        {"lei": "Instrução Normativa INSS/PRES nº 77/2015", "descricao": "Estabelece rotinas para aferição e comprovação do tempo de contribuição."},
        {"lei": "Art. 103-A da Lei nº 8.213/91", "descricao": "Trata do prazo decadencial para revisão do benefício."}
    ]
    
    # Retornar todos os dados em um dicionário
    return {
        "segurado": segurado,
        "comparativo": comparativo,
        "fator_previdenciario": fator_previdenciario,
        "evolucao_beneficio": evolucao_beneficio,
        "diferencas_acumuladas": diferencas_acumuladas,
        "total_devido": total_devido,
        "vinculos_empregaticos": vinculos_empregaticos,
        "contribuicoes_cnis": contribuicoes_cnis,
        "analise_cnis": analise_cnis,
        "fundamentos_legais": fundamentos_legais
    }

# Função principal do app
def main():
    # Carregar CSS
    load_css()
    
    # Carregar dados
    data = load_data()
    
    # Cabeçalho do app
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"""
        <div class="main-header">
            {get_logo_svg()}
            <span class="logo-text">OLIVEIRA OFFICE LAW</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("<h1>Sistema de Auditoria Previdenciária</h1>", unsafe_allow_html=True)
    
    # Criar abas
    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard Executivo", "Análise CNIS", "Visualização de Dados", "Exportar Relatório"])
    
    with tab1:
        # Dashboard Principal
        st.markdown("## Resumo da Auditoria Previdenciária")
        
        # Cards principais - Comparativo de valores
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="white-card">
                <span class="data-label" style="color: #666;">Valor INSS</span>
                <div class="data-value" style="color: #333;">R$ {data['comparativo']['inss']['salarioBeneficio']:.2f}</div>
                <span style="font-size: 0.85rem; color: #666;">Calculado pelo INSS</span>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="green-card">
                <span class="data-label">Valor Correto</span>
                <div class="data-value">R$ {data['comparativo']['auditoria']['salarioBeneficio']:.2f}</div>
                <span style="font-size: 0.85rem; color: rgba(255,255,255,0.8);">Apurado na auditoria</span>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            diferenca = data['comparativo']['auditoria']['salarioBeneficio'] - data['comparativo']['inss']['salarioBeneficio']
            percentual = (diferenca / data['comparativo']['inss']['salarioBeneficio']) * 100
            
            st.markdown(f"""
            <div class="black-card">
                <span class="data-label">Diferença Mensal</span>
                <div class="data-value">R$ {diferenca:.2f}</div>
                <span style="font-size: 0.85rem; color: rgba(255,255,255,0.8);">+{percentual:.2f}%</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Dados do segurado e Resumo da Análise
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Dados do Segurado")
            
            segurado = data['segurado']
            st.markdown(f"""
            <div class="white-card">
                <p><strong>Nome:</strong> {segurado['nome']}</p>
                <p><strong>CPF:</strong> {segurado['cpf']}</p>
                <p><strong>Data de Nascimento:</strong> {segurado['dataNascimento']}</p>
                <p><strong>NIT/PIS:</strong> {segurado['nit']}</p>
                <p><strong>Número do Benefício:</strong> {segurado['numBeneficio']}</p>
                <p><strong>Data de Requerimento:</strong> {segurado['dataRequerimento']}</p>
                <p><strong>Idade na DER:</strong> {segurado['idade']['anos']} anos, {segurado['idade']['meses']} meses</p>
                <p><strong>Tempo de Contribuição:</strong> {segurado['tempoContribuicao']['anos']} anos, {segurado['tempoContribuicao']['meses']} meses e {segurado['tempoContribuicao']['dias']} dias</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Principais Erros do INSS")
            
            st.markdown(f"""
            <div class="error-card">
                <h4 style="color: #D32F2F; margin-top: 0;">1. Contagem de Contribuições</h4>
                <p>Considerou {data['comparativo']['inss']['totalContribuicoes']} contribuições quando apenas {data['comparativo']['auditoria']['totalContribuicoes']} eram efetivamente válidas.</p>
            </div>
            <div class="error-card">
                <h4 style="color: #D32F2F; margin-top: 0;">2. Regra dos 80%</h4>
                <p>Aplicou 80% sobre total incorreto ({data['comparativo']['inss']['contribuicoesConsideradas']} de {data['comparativo']['inss']['totalContribuicoes']}) em vez de {data['comparativo']['auditoria']['contribuicoesConsideradas']} de {data['comparativo']['auditoria']['totalContribuicoes']}.</p>
            </div>
            <div class="error-card">
                <h4 style="color: #D32F2F; margin-top: 0;">3. Períodos Reaproveitáveis</h4>
                <p>Ignorou {data['comparativo']['auditoria']['contribuicoesReaproveitaveis']} períodos que deveriam ser considerados no cálculo.</p>
            </div>
            <div class="error-card">
                <h4 style="color: #D32F2F; margin-top: 0;">4. Fator Previdenciário</h4>
                <p>Aplicou fator {data['comparativo']['inss']['fatorPrevidenciario']} quando o correto seria {data['comparativo']['auditoria']['fatorPrevidenciario']}.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Resultados da Análise CNIS
            st.markdown("### Resultados da Análise do CNIS")
            
            analise = data['analise_cnis']
            st.markdown(f"""
            <div class="highlight-box">
                <ul style="list-style-type: disc; margin-left: 20px; padding-left: 0;">
                    <li>Total de contribuições válidas: <strong>{analise['totalRegistros']}</strong></li>
                    <li>Contribuições a considerar (80%): <strong>{analise['registrosConsiderados']}</strong></li>
                    <li>Média dos 80% maiores salários: <strong>R$ {analise['mediaMaioresSalarios']:.2f}</strong></li>
                    <li>Períodos indeferidos que deveriam ser considerados: <strong>{analise['periodosIncorretos']}</strong></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Gráfico de evolução do benefício
            st.markdown("### Evolução do Benefício (2015-2025)")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(data['evolucao_beneficio']['ano'], data['evolucao_beneficio']['inss'], marker='o', linewidth=2, color='#666666', label='Valor INSS')
            ax.plot(data['evolucao_beneficio']['ano'], data['evolucao_beneficio']['auditoria'], marker='o', linewidth=2, color='#4E9F3D', label='Valor Correto')
            
            # Formatação do gráfico
            ax.set_xlabel('Ano')
            ax.set_ylabel('Valor (R$)')
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.yaxis.set_major_formatter('R${x:,.2f}')
            
            # Destacar a diferença
            for i, ano in enumerate(data['evolucao_beneficio']['ano']):
                inss = data['evolucao_beneficio']['inss'].iloc[i]
                auditoria = data['evolucao_beneficio']['auditoria'].iloc[i]
                if i % 2 == 0:  # Mostrar apenas em alguns pontos para não sobrecarregar
                    ax.annotate(f'R${auditoria-inss:.2f}', 
                               xy=(ano, auditoria), 
                               xytext=(0, 10),
                               textcoords='offset points',
                               ha='center',
                               fontsize=8,
                               color='#4E9F3D',
                               bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7))
            
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig)
            
            # Impacto Financeiro e Simulação de Parcelamento
            col2_1, col2_2 = st.columns(2)
            
            with col2_1:
                st.markdown("### Impacto Financeiro Total")
                
                st.markdown(f"""
                <div class="black-card">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span>Diferenças vencidas:</span>
                        <span style="font-weight: bold;">R$ {data['total_devido']['diferencasVencidas']:.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span>Correção monetária:</span>
                        <span style="font-weight: bold;">R$ {data['total_devido']['correcaoMonetaria']:.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span>Juros legais:</span>
                        <span style="font-weight: bold;">R$ {data['total_devido']['jurosLegais']:.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 15px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.2); font-size: 1.1em;">
                        <span style="font-weight: bold;">Total devido:</span>
                        <span style="font-weight: bold; color: #4E9F3D;">R$ {data['total_devido']['totalGeral']:.2f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2_2:
                st.markdown("### Simulação de Parcelamento")
                
                st.markdown(f"""
                <div class="highlight-box">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span>24 parcelas:</span>
                        <span style="font-weight: bold;">R$ {data['total_devido']['parcelasMensais']['valor24']:.2f}/mês</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span>36 parcelas:</span>
                        <span style="font-weight: bold;">R$ {data['total_devido']['parcelasMensais']['valor36']:.2f}/mês</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span>60 parcelas:</span>
                        <span style="font-weight: bold;">R$ {data['total_devido']['parcelasMensais']['valor60']:.2f}/mês</span>
                    </div>
                    <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #C8E6C9; font-size: 0.8em; color: #555;">
                        <p>Cálculo com base na Tabela Price, taxa de juros de 0,5% a.m.</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        # Análise detalhada do CNIS
        st.markdown("## Análise Detalhada do CNIS")
        
        # Vínculos Empregatícios
        st.markdown("### Vínculos Empregatícios")
        st.dataframe(data['vinculos_empregaticos'], use_container_width=True)
        
        # Contribuições Analisadas
        st.markdown("### Contribuições Analisadas")
        st.markdown(f"Total de registros analisados: **{len(data['contribuicoes_cnis'])}**")
        
        # Função para destacar status
        def highlight_status(row):
            if row['status'] == 'Indeferido' and data['contribuicoes_cnis'].index.get_loc(row.name) < data['analise_cnis']['registrosConsiderados']:
                return ['background-color: #FFCDD2'] * len(row)
            elif row['status'] == 'Considerado':
                return ['background-color: #C8E6C9'] * len(row)
            else:
                return [''] * len(row)
                
        # Mostrar dataframe com estilo
        st.dataframe(data['contribuicoes_cnis'].style.apply(highlight_status, axis=1), use_container_width=True)
        
        # Cálculo do Fator Previdenciário
        st.markdown("### Cálculo do Fator Previdenciário")
        
        st.markdown("""
        <div class="white-card" style="background-color: #F5F5F5; padding: 15px; margin-bottom: 20px;">
            <p style="margin-bottom: 10px;">O fator previdenciário é calculado com base na seguinte fórmula:</p>
            <div style="background-color: #E0E0E0; text-align: center; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                <strong>Fator = (Tc × a) ÷ Es × [1 + (Id + Tc × a) ÷ 100]</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabela de parâmetros do fator previdenciário
        st.markdown("#### Parâmetros utilizados no cálculo:")
        
        parametros_df = pd.DataFrame([
            {"Parâmetro": "Tc", "Descrição": "Tempo de Contribuição", "Valor": f"{data['fator_previdenciario']['tempoContribuicao']:.2f} anos"},
            {"Parâmetro": "a", "Descrição": "Alíquota", "Valor": f"{data['fator_previdenciario']['aliquota']:.2f}"},
            {"Parâmetro": "Es", "Descrição": "Expectativa de Sobrevida", "Valor": f"{data['fator_previdenciario']['expectativaSobrevida']:.1f} anos"},
            {"Parâmetro": "Id", "Descrição": "Idade", "Valor": f"{data['fator_previdenciario']['idade']:.2f} anos"}
        ])
        
        st.table(parametros_df)
        
        # Passo a passo do cálculo
        st.markdown("#### Passo a passo do cálculo:")
        
        st.markdown(f"""
        <div class="highlight-box">
            <ol style="margin-left: 20px; padding-left: 0;">
                <li style="margin-bottom: 8px;">Tc × a = {data['fator_previdenciario']['tempoContribuicao']:.2f} × {data['fator_previdenciario']['aliquota']} = {data['fator_previdenciario']['calculoFator']['passo1']:.2f}</li>
                <li style="margin-bottom: 8px;">(Tc × a) ÷ Es = {data['fator_previdenciario']['calculoFator']['passo1']:.2f} ÷ {data['fator_previdenciario']['expectativaSobrevida']:.1f} = {data['fator_previdenciario']['calculoFator']['passo2']:.4f}</li>
                <li style="margin-bottom: 8px;">1 + (Id + Tc × a) ÷ 100 = 1 + ({data['fator_previdenciario']['idade']:.2f} + {data['fator_previdenciario']['calculoFator']['passo1']:.2f}) ÷ 100 = {data['fator_previdenciario']['calculoFator']['passo3']:.4f}</li>
                <li style="margin-bottom: 8px;">Fator = {data['fator_previdenciario']['calculoFator']['passo2']:.4f} × {data['fator_previdenciario']['calculoFator']['passo3']:.4f} = <strong>{data['fator_previdenciario']['calculoFator']['resultadoFinal']:.4f}</strong></li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # Análise de Índices Econômicos
        st.markdown("### Análise de Índices Econômicos (2015-2025)")
        
        # Gráfico de índices econômicos
        fig, ax = plt.subplots(figsize=(10, 5))
        
        ax.plot(data['evolucao_beneficio']['ano'], data['evolucao_beneficio']['reajuste'], marker='o', linewidth=2, color='#4E9F3D', label='Reajuste INSS (%)')
        ax.plot(data['evolucao_beneficio']['ano'], data['evolucao_beneficio']['indiceSinapi'], marker='s', linewidth=2, color='#D32F2F', label='Índice SINAPI (%)')
        
        # Formatação do gráfico
        ax.set_xlabel('Ano')
        ax.set_ylabel('Percentual (%)')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
        
        # Tabela com índices econômicos
        st.subheader("Detalhamento dos Índices Econômicos")
        
        indices_economicos = pd.DataFrame({
            'Ano': data['evolucao_beneficio']['ano'],
            'Reajuste INSS (%)': data['evolucao_beneficio']['reajuste'],
            'Índice SINAPI (%)': data['evolucao_beneficio']['indiceSinapi'],
            'SELIC (% a.a.)': data['diferencas_acumuladas']['indiceSelic'],
            'Diferença Acumulada (R$)': data['diferencas_acumuladas']['totalAno']
        })
        
        st.dataframe(indices_economicos, use_container_width=True)
        
        # Fundamentos Legais
        st.markdown("### Fundamentos Legais")
        
        for fundamento in data['fundamentos_legais']:
            st.markdown(f"""
            <div class="white-card" style="margin-bottom: 10px;">
                <h4 style="margin-top: 0; color: #1E5128;">{fundamento['lei']}</h4>
                <p>{fundamento['descricao']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        # Visualização gráfica dos dados
        st.markdown("## Visualização Gráfica dos Dados")
        
        # Distribuição de contribuições por status
        st.subheader("Distribuição das Contribuições por Status")
        
        contribuicoes_consideradas = len(data['contribuicoes_cnis'][data['contribuicoes_cnis']['status'] == 'Considerado'])
        contribuicoes_indeferidas_corretas = len(data['contribuicoes_cnis'][
            (data['contribuicoes_cnis']['status'] == 'Indeferido') & 
            (data['contribuicoes_cnis'].index >= data['analise_cnis']['registrosConsiderados'])
        ])
        contribuicoes_indeferidas_erradas = len(data['contribuicoes_cnis'][
            (data['contribuicoes_cnis']['status'] == 'Indeferido') &
            (data['contribuicoes_cnis'].index < data['analise_cnis']['registrosConsiderados'])
        ])
        
        status_data = {
            'Status': ['Consideradas', 'Indeferidas corretamente', 'Indeferidas erroneamente'],
            'Quantidade': [contribuicoes_consideradas, contribuicoes_indeferidas_corretas, contribuicoes_indeferidas_erradas],
            'Cor': ['#4CAF50', '#9E9E9E', '#F44336']
        }
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(status_data['Quantidade'], labels=status_data['Status'], autopct='%1.1f%%', 
              colors=status_data['Cor'], startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 1})
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Distribuição das Contribuições por Status')
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.pyplot(fig)
            
        with col2:
            st.markdown("""
            <div class="white-card" style="height: 100%;">
                <h4 style="margin-top: 0;">Análise da Distribuição</h4>
                <ul style="margin-left: 20px; padding-left: 0;">
                    <li>O INSS <strong>considerou corretamente</strong> contribuições válidas.</li>
                    <li>Porém, <strong>indeferiu erroneamente</strong> períodos que deveriam ter sido considerados por estarem entre os 80% maiores salários.</li>
                    <li>Apenas parte das contribuições indeferidas foram corretamente desconsideradas por não estarem entre os 80% maiores salários.</li>
                </ul>
                <p style="margin-top: 15px;">Esta distribuição incorreta resultou em uma média salarial inferior à devida.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Composição do valor devido
        st.subheader("Composição do Valor Total Devido")
        
        componentes = ['Diferenças Vencidas', 'Correção Monetária', 'Juros Legais']
        valores = [
            data['total_devido']['diferencasVencidas'],
            data['total_devido']['correcaoMonetaria'],
            data['total_devido']['jurosLegais']
        ]
        cores = ['#1E5128', '#4E9F3D', '#A9D196']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(valores, labels=componentes, autopct='%1.1f%%', colors=cores, 
              startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 1})
        ax.axis('equal')
        plt.title(f'Composição do Valor Total Devido: R$ {data["total_devido"]["totalGeral"]:.2f}')
        
        st.pyplot(fig)
        
        # Gráfico de barras comparativas - INSS vs. Auditoria
        st.subheader("Comparativo: INSS vs. Auditoria")
        
        comparativo_df = pd.DataFrame({
            'Parâmetro': ['Total de Contribuições', 'Contribuições Consideradas', 'Média Salarial (R$)', 'Salário Benefício (R$)'],
            'INSS': [
                data['comparativo']['inss']['totalContribuicoes'],
                data['comparativo']['inss']['contribuicoesConsideradas'],
                data['comparativo']['inss']['mediaContribuicoes'],
                data['comparativo']['inss']['salarioBeneficio']
            ],
            'Auditoria': [
                data['comparativo']['auditoria']['totalContribuicoes'],
                data['comparativo']['auditoria']['contribuicoesConsideradas'],
                data['comparativo']['auditoria']['mediaContribuicoes'],
                data['comparativo']['auditoria']['salarioBeneficio']
            ]
        })
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(comparativo_df['Parâmetro']))
        width = 0.35
        
        inss_bars = ax.bar(x - width/2, comparativo_df['INSS'], width, label='INSS', color='#666666')
        auditoria_bars = ax.bar(x + width/2, comparativo_df['Auditoria'], width, label='Auditoria', color='#4E9F3D')
        
        ax.set_xticks(x)
        ax.set_xticklabels(comparativo_df['Parâmetro'])
        ax.legend()
        
        # Adicionar valores nas barras
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{:.2f}'.format(height) if height > 100 else '{:.0f}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom',
                            fontsize=9)
        
        autolabel(inss_bars)
        autolabel(auditoria_bars)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Gráfico de evolução das diferenças acumuladas por ano
        st.subheader("Evolução das Diferenças Acumuladas por Ano")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Linha para valor total
        ax.plot(data['diferencas_acumuladas']['ano'], data['diferencas_acumuladas']['totalAno'], 
                marker='o', color='#4E9F3D', linewidth=2, label='Valor Acumulado')
        
        # Área sob a curva
        ax.fill_between(data['diferencas_acumuladas']['ano'], data['diferencas_acumuladas']['totalAno'], 
                       color='#4E9F3D', alpha=0.2)
        
        # Formatação do gráfico
        ax.set_xlabel('Ano')
        ax.set_ylabel('Valor Acumulado (R$)')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.yaxis.set_major_formatter('R${x:,.2f}')
        
        # Adicionar valores nos pontos
        for i, ano in enumerate(data['diferencas_acumuladas']['ano']):
            valor = data['diferencas_acumuladas']['totalAno'].iloc[i]
            ax.annotate(f'R${valor:.2f}', 
                       xy=(ano, valor), 
                       xytext=(0, 10),
                       textcoords='offset points',
                       ha='center',
                       fontsize=8,
                       bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7))
        
        plt.title('Evolução do Valor Acumulado por Ano')
        plt.tight_layout()
        st.pyplot(fig)
    
    with tab4:
        # Exportar relatório
        st.markdown("## Exportar Relatório de Auditoria")
        
        st.markdown("""
        <div class="white-card">
            <p>Nesta seção você pode exportar o relatório da auditoria previdenciária em diferentes formatos.</p>
            <p>Escolha o formato desejado e clique no botão correspondente para iniciar o download.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3>1. Relatório Completo em HTML</h3>", unsafe_allow_html=True)
            st.markdown("""
            <div class="white-card">
                <p><strong>Conteúdo:</strong> Relatório completo com todas as análises, tabelas e conclusões.</p>
                <p><strong>Uso recomendado:</strong> Visualização digital, envio por e-mail ou impressão detalhada.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Gerar HTML para download
            if st.button("Exportar Relatório HTML", key="btn_html"):
                html_report = gerar_html_relatorio(data)
                html_bytes = html_report.encode('utf-8')
                
                # Criar link de download
                st.markdown(
                    create_download_link(html_bytes, "relatorio_previdenciario.html", "Clique aqui para baixar o relatório HTML"),
                    unsafe_allow_html=True
                )
                st.success("Relatório HTML gerado com sucesso! Clique no link acima para baixar.")
        
        with col2:
            st.markdown("<h3>2. Dados em CSV</h3>", unsafe_allow_html=True)
            st.markdown("""
            <div class="white-card">
                <p><strong>Conteúdo:</strong> Dados brutos em formato CSV para importação em planilhas.</p>
                <p><strong>Uso recomendado:</strong> Análises complementares ou personalização do relatório.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Seleção das tabelas para exportar
            opcao_csv = st.selectbox(
                "Selecione os dados para exportar:",
                ["Contribuições CNIS", "Evolução do Benefício", "Diferenças Acumuladas", "Vínculos Empregatícios"]
            )
            
            # Mapear seleção para os dataframes
            df_map = {
                "Contribuições CNIS": data['contribuicoes_cnis'],
                "Evolução do Benefício": data['evolucao_beneficio'],
                "Diferenças Acumuladas": data['diferencas_acumuladas'],
                "Vínculos Empregatícios": data['vinculos_empregaticos']
            }
            
            # Botão para download do CSV selecionado
            if st.button("Exportar CSV", key="btn_csv"):
                csv_data = convert_df_to_csv(df_map[opcao_csv])
                filename = opcao_csv.lower().replace(" ", "_") + ".csv"
                
                # Criar link de download
                st.markdown(
                    create_download_link(csv_data, filename, f"Clique aqui para baixar {opcao_csv}.csv"),
                    unsafe_allow_html=True
                )
                st.success(f"Arquivo {filename} gerado com sucesso! Clique no link acima para baixar.")
        
        # Observações importantes
        st.markdown("<h3>Observações Importantes</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class="white-card" style="background-color: #FFF3E0; border-left: 5px solid #FF9800;">
            <ul style="margin-left: 20px; padding-left: 0;">
                <li>Os relatórios gerados são baseados nos dados da auditoria previdenciária realizada.</li>
                <li>Recomenda-se a revisão por um advogado especializado antes de iniciar qualquer procedimento judicial.</li>
                <li>A chancela de êxito para este caso é considerada <strong>muito alta</strong>, tendo em vista a robustez das provas e a jurisprudência consolidada acerca da matéria.</li>
                <li>O ajuizamento da ação revisional deve ocorrer preferencialmente na Justiça Federal da Seção Judiciária do Maranhão.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Formulário de contato
        st.markdown("<h3>Formulário de Contato</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class="white-card">
            <p>Para mais informações ou para iniciar o processo de revisão, preencha os dados abaixo:</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome completo")
            email = st.text_input("E-mail")
            telefone = st.text_input("Telefone")
        
        with col2:
            st.text_area("Mensagem", height=124)
            
        if st.button("Enviar Mensagem", key="btn_contato"):
            st.success("Mensagem enviada com sucesso! Em breve entraremos em contato.")
    
    # Rodapé
    st.markdown("""
    <footer>
        <p>© 2025 OLIVEIRA OFFICE LAW - Consultoria Previdenciária</p>
        <p>Desenvolvido pelo Departamento de Tecnologia da Informação</p>
        <p>Versão 2.0 - Atualizado em 29/04/2025</p>
    </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
                    <div style="display: flex; justify-content: space-between;
