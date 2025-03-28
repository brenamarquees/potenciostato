# Potenciostato

Este repositório serve como base para aprimorar e desenvolver o projeto de um programa conectado a um potenciostato. O potenciostato aplicará diferentes frequências, que serão exibidas em um gráfico na tela do usuário. A interface do usuário permitirá a exportação do gráfico e dos dados exibidos nos formatos PDF e CSV.

## Objetivo do Projeto
O objetivo é criar um programa simples em Python que estabeleça a conexão entre hardware e software, garantindo a visualização dos dados e sua exportação. 

## Status do Projeto
Atualmente, o repositório contém o design inicial das telas e as simulações realizadas. Para finalizar o projeto, é necessário realizar testes em laboratório.

## Link para Simulação
A simulação do potenciostato pode ser acessada no Tinkercad:
[Simulação no Tinkercad](https://www.tinkercad.com/things/efnSAjU3Q67-potenciostato?sharecode=7aPz0qyP8EY6kJt2ApTPFDCzkzfdWFfuTcVT8EceYLo)

## Resumo do Projeto
O projeto tem como finalidade desenvolver uma ferramenta para conectar um potenciostato a um sistema computacional, permitindo o controle, a aquisição e a análise de dados em tempo real. O sistema será responsável por capturar as frequências fornecidas pelo potenciostato e exibi-las graficamente, além de permitir a exportação dos resultados para análise posterior.

**Anexo:** O repositório também inclui um resumo em forma de artigo detalhando o projeto.

## Tecnologias Utilizadas
- **Linguagem:** Python
- **Bibliotecas:** Matplotlib, Pandas, PySerial, ReportLab (para exportação de PDF), entre outras conforme necessidade.

## Como Usar
1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Conecte o potenciostato ao computador via porta serial.**
3. **Execute o programa:**
   ```bash
   python main.py
   ```
4. **Selecione a porta correta e a taxa de transmissão (baud rate).**
5. **Clique em "Connect" para estabelecer a conexão.**
6. **Inicie a medição clicando em "Start Measurement".**
7. **Acompanhe os dados em tempo real no gráfico.**
8. **Para salvar os dados, utilize as opções "Export CSV" ou "Export PDF".**

## Como Contribuir
1. Faça um fork deste repositório.
2. Crie uma nova branch: `git checkout -b minha-feature`
3. Faça suas alterações e commit: `git commit -m 'Adicionando nova funcionalidade'`
4. Envie para o repositório remoto: `git push origin minha-feature`
5. Abra um Pull Request para análise.
