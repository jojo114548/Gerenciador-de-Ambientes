#!/bin/bash
# Script para executar testes com cobertura

echo "================================================"
echo "   SISTEMA NEXUS - TESTES DE COBERTURA"
echo "================================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verifica se pytest está instalado
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}❌ pytest não está instalado!${NC}"
    echo -e "${YELLOW}Execute: pip install -r requirements-test.txt${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Iniciando testes..."
echo ""

# Limpa cache anterior
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
rm -rf .pytest_cache htmlcov .coverage 2>/dev/null

echo -e "${YELLOW}📋 Executando todos os testes...${NC}"
echo ""

# Executa testes com cobertura
pytest tests/ \
    --cov=controller \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-report=xml \
    -v \
    --tb=short

# Captura código de saída
TEST_EXIT_CODE=$?

echo ""
echo "================================================"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ Todos os testes passaram!${NC}"
    echo ""
    echo -e "${YELLOW}📊 Relatório de cobertura gerado em:${NC}"
    echo "   - HTML: ./htmlcov/index.html"
    echo "   - XML:  ./coverage.xml"
    echo ""
    echo -e "${YELLOW}💡 Para visualizar o relatório HTML:${NC}"
    echo "   python -m http.server 8000 --directory htmlcov"
else
    echo -e "${RED}❌ Alguns testes falharam!${NC}"
    echo -e "${YELLOW}Verifique os erros acima.${NC}"
fi

echo "================================================"

exit $TEST_EXIT_CODE