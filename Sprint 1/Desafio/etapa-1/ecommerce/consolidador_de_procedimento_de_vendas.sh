#!/bin/bash
cat $(find ~/ecommerce/vendas/backup -type f -name 'relatorio*' -exec printf "%s " {} +) > relatoriofina.txt

